import requests
import json
import time
from typing import List, Dict, Optional
from datetime import datetime
from config import Config

class MailgunClient:
    def __init__(self):
        self.api_key = Config.MAILGUN_API_KEY
        self.domain = Config.MAILGUN_DOMAIN
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        self.session.auth = ('api', self.api_key)
    
    def send_single_email(self, to_email: str, subject: str, body: str, 
                         from_email: str = None, reply_to: str = None,
                         tracking: bool = True, tag: str = None) -> Dict:
        """Envia um email individual"""
        data = {
            'from': from_email or Config.FROM_EMAIL,
            'to': to_email,
            'subject': subject,
            'text': body,
            'o:tracking': 'yes' if tracking else 'no'
        }
        
        if reply_to:
            data['h:Reply-To'] = reply_to
        
        if tag:
            data['o:tag'] = tag
        
        response = self.session.post(f'{self.base_url}/messages', data=data)
        
        if response.status_code == 200:
            return {
                'success': True,
                'message_id': response.json().get('id'),
                'message': response.json().get('message')
            }
        else:
            return {
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }
    
    def send_bulk_emails(self, recipients: List[str], subject: str, body_template: str,
                        recipient_vars: Dict = None, batch_size: int = None,
                        delay: int = None, campaign_tag: str = None) -> List[Dict]:
        """Envia emails em lote com throttling"""
        batch_size = batch_size or Config.BATCH_SIZE
        delay = delay or Config.DELAY_BETWEEN_BATCHES
        results = []
        
        # Divide os destinatários em lotes
        for i in range(0, len(recipients), batch_size):
            batch_recipients = recipients[i:i + batch_size]
            
            # Prepara os dados para o lote
            data = {
                'from': Config.FROM_EMAIL,
                'to': batch_recipients,
                'subject': subject,
                'text': body_template,
                'o:tracking': 'yes' if Config.TRACKING_ENABLED else 'no',
                'h:Reply-To': Config.REPLY_TO
            }
            
            if recipient_vars:
                data['recipient-variables'] = json.dumps(recipient_vars)
            
            if campaign_tag:
                data['o:tag'] = f"{Config.TAG_PREFIX}-{campaign_tag}"
            
            # Envia o lote
            response = self.session.post(f'{self.base_url}/messages', data=data)
            
            batch_result = {
                'batch_number': i // batch_size + 1,
                'recipients_count': len(batch_recipients),
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
            
            if response.status_code == 200:
                batch_result['message_id'] = response.json().get('id')
                batch_result['message'] = response.json().get('message')
            else:
                batch_result['error'] = response.text
            
            results.append(batch_result)
            
            # Aguarda antes do próximo lote (exceto no último)
            if i + batch_size < len(recipients):
                time.sleep(delay)
        
        return results
    
    def send_personalized_emails(self, contacts: List[Dict], subject_template: str, 
                               body_template: str, batch_size: int = None,
                               delay: int = None, campaign_tag: str = None) -> List[Dict]:
        """Envia emails personalizados para cada contato"""
        batch_size = batch_size or Config.BATCH_SIZE
        delay = delay or Config.DELAY_BETWEEN_BATCHES
        results = []
        
        # Prepara variáveis dos destinatários
        recipient_vars = {}
        for contact in contacts:
            email = contact['email']
            recipient_vars[email] = {
                'name': contact.get('name', 'Cliente'),
                'company': contact.get('company', ''),
                'position': contact.get('position', '')
            }
        
        # Divide em lotes
        for i in range(0, len(contacts), batch_size):
            batch_contacts = contacts[i:i + batch_size]
            batch_emails = [contact['email'] for contact in batch_contacts]
            
            # Personaliza o assunto e corpo para o primeiro contato do lote
            # (Mailgun usa o mesmo template para todos no lote)
            first_contact = batch_contacts[0]
            subject = subject_template.format(
                name=first_contact.get('name', 'Cliente'),
                company=first_contact.get('company', '')
            )
            
            body = body_template.format(
                name=first_contact.get('name', 'Cliente'),
                company=first_contact.get('company', ''),
                position=first_contact.get('position', '')
            )
            
            # Envia o lote
            batch_result = self.send_bulk_emails(
                recipients=batch_emails,
                subject=subject,
                body_template=body,
                recipient_vars=recipient_vars,
                batch_size=len(batch_emails),
                delay=0,  # Sem delay entre sub-lotes
                campaign_tag=campaign_tag
            )
            
            results.extend(batch_result)
            
            # Aguarda antes do próximo lote (exceto no último)
            if i + batch_size < len(contacts):
                time.sleep(delay)
        
        return results
    
    def get_events(self, event_type: str = None, limit: int = 100) -> List[Dict]:
        """Busca eventos do Mailgun (opens, clicks, bounces, etc.)"""
        params = {'limit': limit}
        if event_type:
            params['event'] = event_type
        
        response = self.session.get(f'{self.base_url}/events', params=params)
        
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            return []
    
    def get_bounces(self, limit: int = 100) -> List[Dict]:
        """Busca emails que deram bounce"""
        response = self.session.get(f'{self.base_url}/bounces', params={'limit': limit})
        
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            return []
    
    def get_unsubscribes(self, limit: int = 100) -> List[Dict]:
        """Busca emails que cancelaram inscrição"""
        response = self.session.get(f'{self.base_url}/unsubscribes', params={'limit': limit})
        
        if response.status_code == 200:
            return response.json().get('items', [])
        else:
            return []
    
    def validate_email(self, email: str) -> Dict:
        """Valida um endereço de email usando a API do Mailgun"""
        response = self.session.get(
            f'https://api.mailgun.net/v4/address/validate',
            params={'address': email}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'valid': False, 'error': response.text}
    
    def get_domain_stats(self, start_date: str = None, end_date: str = None) -> Dict:
        """Busca estatísticas do domínio"""
        params = {}
        if start_date:
            params['start'] = start_date
        if end_date:
            params['end'] = end_date
        
        response = self.session.get(f'{self.base_url}/stats/total', params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {}
