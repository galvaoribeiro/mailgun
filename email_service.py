import time
import threading
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from database import Database
from mailgun_client import MailgunClient
from config import Config

class EmailService:
    def __init__(self):
        self.db = Database()
        self.mailgun = MailgunClient()
        self.sending_lock = threading.Lock()
        self.daily_sent_count = 0
        self.last_reset_date = datetime.now().date()
    
    def reset_daily_counter(self):
        """Reseta o contador diário se necessário"""
        current_date = datetime.now().date()
        if current_date > self.last_reset_date:
            self.daily_sent_count = 0
            self.last_reset_date = current_date
    
    def can_send_more_emails(self) -> bool:
        """Verifica se ainda pode enviar mais emails hoje"""
        self.reset_daily_counter()
        return self.daily_sent_count < Config.MAX_EMAILS_PER_DAY
    
    def add_contacts_from_csv(self, csv_file_path: str, source: str = 'csv_import') -> int:
        """Importa contatos de um arquivo CSV"""
        import pandas as pd
        
        try:
            df = pd.read_csv(csv_file_path)
            contacts = []
            
            for _, row in df.iterrows():
                contact = {
                    'email': row.get('email', '').strip(),
                    'name': row.get('name', '').strip(),
                    'company': row.get('company', '').strip(),
                    'position': row.get('position', '').strip(),
                    'source': source
                }
                
                if contact['email']:  # Só adiciona se tiver email
                    contacts.append(contact)
            
            return self.db.add_contacts_bulk(contacts)
        
        except Exception as e:
            print(f"Erro ao importar CSV: {e}")
            return 0
    
    def create_campaign(self, name: str, subject_template: str, body_template: str) -> int:
        """Cria uma nova campanha"""
        return self.db.create_campaign(name, subject_template, body_template)
    
    def send_campaign(self, campaign_id: int, contact_limit: int = None, 
                     test_mode: bool = False) -> Dict:
        """Envia uma campanha completa"""
        with self.sending_lock:
            # Busca a campanha
            campaign = self.db.get_campaign(campaign_id)
            if not campaign:
                return {'success': False, 'error': 'Campanha não encontrada'}
            
            # Busca contatos ativos
            contacts = self.db.get_contacts(status='active', limit=contact_limit)
            if not contacts:
                return {'success': False, 'error': 'Nenhum contato ativo encontrado'}
            
            # Verifica limite diário
            if not self.can_send_more_emails():
                return {'success': False, 'error': 'Limite diário de emails atingido'}
            
            # Se for modo teste, envia apenas para os primeiros 5 contatos
            if test_mode:
                contacts = contacts[:5]
            
            # Prepara templates
            subject_template = campaign['subject']
            body_template = campaign['body_template']
            
            # Envia emails
            results = self.mailgun.send_personalized_emails(
                contacts=contacts,
                subject_template=subject_template,
                body_template=body_template,
                campaign_tag=f"campaign_{campaign_id}"
            )
            
            # Registra envios no banco
            successful_sends = 0
            for result in results:
                if result['success']:
                    successful_sends += result['recipients_count']
                    
                    # Registra cada email enviado
                    for contact in contacts:
                        self.db.log_email_sent(
                            campaign_id=campaign_id,
                            contact_id=contact['id'],
                            email=contact['email']
                        )
            
            # Atualiza contador diário
            self.daily_sent_count += successful_sends
            
            return {
                'success': True,
                'campaign_id': campaign_id,
                'total_contacts': len(contacts),
                'successful_sends': successful_sends,
                'results': results
            }
    
    def send_campaign_async(self, campaign_id: int, contact_limit: int = None, 
                          test_mode: bool = False):
        """Envia uma campanha de forma assíncrona"""
        def send_worker():
            try:
                result = self.send_campaign(campaign_id, contact_limit, test_mode)
                print(f"Campanha {campaign_id} concluída: {result}")
            except Exception as e:
                print(f"Erro ao enviar campanha {campaign_id}: {e}")
        
        thread = threading.Thread(target=send_worker)
        thread.start()
        return thread
    
    def get_campaign_stats(self, campaign_id: int) -> Dict:
        """Retorna estatísticas detalhadas de uma campanha"""
        stats = self.db.get_campaign_stats(campaign_id)
        campaign = self.db.get_campaign(campaign_id)
        
        if campaign:
            stats['campaign_name'] = campaign['name']
            stats['campaign_subject'] = campaign['subject']
        
        return stats
    
    def update_email_status_from_webhook(self, event_data: Dict):
        """Atualiza status de emails baseado em webhooks do Mailgun"""
        email = event_data.get('recipient')
        event = event_data.get('event')
        
        if not email or not event:
            return
        
        # Mapeia eventos do Mailgun para status internos
        status_mapping = {
            'delivered': 'delivered',
            'opened': 'opened',
            'clicked': 'clicked',
            'bounced': 'bounced',
            'complained': 'complained',
            'unsubscribed': 'unsubscribed'
        }
        
        if event in status_mapping:
            timestamp = event_data.get('timestamp')
            if timestamp:
                timestamp = datetime.fromtimestamp(timestamp)
            
            # Determina qual campo de timestamp atualizar
            timestamp_field = None
            if event == 'opened':
                timestamp_field = 'opened_at'
            elif event == 'clicked':
                timestamp_field = 'clicked_at'
            elif event == 'bounced':
                timestamp_field = 'bounced_at'
            
            self.db.update_email_status(
                email=email,
                status=status_mapping[event],
                **{timestamp_field: timestamp} if timestamp_field else {}
            )
    
    def cleanup_bounced_emails(self):
        """Remove ou desativa emails que deram bounce"""
        bounces = self.mailgun.get_bounces()
        
        for bounce in bounces:
            email = bounce.get('address')
            if email:
                # Marca o contato como inativo
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        'UPDATE contacts SET status = ? WHERE email = ?',
                        ('bounced', email)
                    )
                    conn.commit()
    
    def validate_contacts(self, contacts: List[Dict]) -> Dict:
        """Valida uma lista de contatos usando a API do Mailgun"""
        results = {
            'valid': [],
            'invalid': [],
            'disposable': [],
            'unknown': []
        }
        
        for contact in contacts:
            email = contact['email']
            validation = self.mailgun.validate_email(email)
            
            if validation.get('valid'):
                if validation.get('is_disposable_address'):
                    results['disposable'].append(contact)
                else:
                    results['valid'].append(contact)
            elif validation.get('error'):
                results['invalid'].append(contact)
            else:
                results['unknown'].append(contact)
        
        return results
    
    def get_daily_stats(self) -> Dict:
        """Retorna estatísticas do dia atual"""
        # Obtém estatísticas do banco de dados
        db_stats = self.db.get_daily_stats()
        
        # Adiciona informações do contador diário
        db_stats.update({
            'remaining_quota': max(0, Config.MAX_EMAILS_PER_DAY - self.daily_sent_count),
            'daily_sent_count': self.daily_sent_count
        })
        
        return db_stats
