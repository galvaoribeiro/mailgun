import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = 'cold_emails.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de contatos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    name TEXT,
                    company TEXT,
                    position TEXT,
                    source TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de campanhas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS campaigns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    body_template TEXT NOT NULL,
                    status TEXT DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de envios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    campaign_id INTEGER,
                    contact_id INTEGER,
                    email TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    sent_at TIMESTAMP,
                    opened_at TIMESTAMP,
                    clicked_at TIMESTAMP,
                    bounced_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (campaign_id) REFERENCES campaigns (id),
                    FOREIGN KEY (contact_id) REFERENCES contacts (id)
                )
            ''')
            
            conn.commit()
    
    def add_contact(self, email: str, name: str = None, company: str = None, 
                   position: str = None, source: str = None) -> int:
        """Adiciona um novo contato"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO contacts (email, name, company, position, source, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, name, company, position, source, datetime.now()))
            conn.commit()
            return cursor.lastrowid
    
    def add_contacts_bulk(self, contacts: List[Dict]) -> int:
        """Adiciona múltiplos contatos de uma vez"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            count = 0
            for contact in contacts:
                try:
                    cursor.execute('''
                        INSERT OR REPLACE INTO contacts (email, name, company, position, source, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        contact['email'], 
                        contact.get('name'), 
                        contact.get('company'), 
                        contact.get('position'), 
                        contact.get('source'), 
                        datetime.now()
                    ))
                    count += 1
                except Exception as e:
                    print(f"Erro ao adicionar contato {contact['email']}: {e}")
            conn.commit()
            return count
    
    def get_contacts(self, status: str = 'active', limit: int = None) -> List[Dict]:
        """Busca contatos por status"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM contacts WHERE status = ?"
            params = [status]
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def create_campaign(self, name: str, subject: str, body_template: str) -> int:
        """Cria uma nova campanha"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO campaigns (name, subject, body_template, updated_at)
                VALUES (?, ?, ?, ?)
            ''', (name, subject, body_template, datetime.now()))
            conn.commit()
            return cursor.lastrowid
    
    def get_campaign(self, campaign_id: int) -> Optional[Dict]:
        """Busca uma campanha específica"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM campaigns WHERE id = ?', (campaign_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_campaigns(self) -> List[Dict]:
        """Lista todas as campanhas"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM campaigns ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def log_email_sent(self, campaign_id: int, contact_id: int, email: str) -> int:
        """Registra um email enviado"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO email_logs (campaign_id, contact_id, email, status, sent_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (campaign_id, contact_id, email, 'sent', datetime.now()))
            conn.commit()
            return cursor.lastrowid
    
    def update_email_status(self, email: str, status: str, **kwargs):
        """Atualiza o status de um email"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Constrói a query dinamicamente baseada nos kwargs
            fields = []
            params = []
            
            for key, value in kwargs.items():
                if key in ['opened_at', 'clicked_at', 'bounced_at']:
                    fields.append(f"{key} = ?")
                    params.append(value)
            
            if fields:
                query = f"UPDATE email_logs SET status = ?, {', '.join(fields)} WHERE email = ?"
                params = [status] + params + [email]
                cursor.execute(query, params)
                conn.commit()
    
    def get_campaign_stats(self, campaign_id: int) -> Dict:
        """Retorna estatísticas de uma campanha"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total de emails enviados
            cursor.execute('''
                SELECT COUNT(*) FROM email_logs WHERE campaign_id = ?
            ''', (campaign_id,))
            total_sent = cursor.fetchone()[0]
            
            # Emails abertos
            cursor.execute('''
                SELECT COUNT(*) FROM email_logs 
                WHERE campaign_id = ? AND opened_at IS NOT NULL
            ''', (campaign_id,))
            total_opened = cursor.fetchone()[0]
            
            # Emails clicados
            cursor.execute('''
                SELECT COUNT(*) FROM email_logs 
                WHERE campaign_id = ? AND clicked_at IS NOT NULL
            ''', (campaign_id,))
            total_clicked = cursor.fetchone()[0]
            
            # Bounces
            cursor.execute('''
                SELECT COUNT(*) FROM email_logs 
                WHERE campaign_id = ? AND bounced_at IS NOT NULL
            ''', (campaign_id,))
            total_bounced = cursor.fetchone()[0]
            
            return {
                'total_sent': total_sent,
                'total_opened': total_opened,
                'total_clicked': total_clicked,
                'total_bounced': total_bounced,
                'open_rate': (total_opened / total_sent * 100) if total_sent > 0 else 0,
                'click_rate': (total_clicked / total_sent * 100) if total_sent > 0 else 0,
                'bounce_rate': (total_bounced / total_sent * 100) if total_sent > 0 else 0
            }
    
    def get_daily_stats(self) -> Dict:
        """Retorna estatísticas do dia atual"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Emails enviados hoje - usando fuso horário local (UTC-3)
            cursor.execute('''
                SELECT COUNT(*) FROM email_logs 
                WHERE strftime('%Y-%m-%d', sent_at, '-3 hours') = strftime('%Y-%m-%d', 'now', '-3 hours')
            ''')
            emails_sent_today = cursor.fetchone()[0]
            
            # Total de contatos
            cursor.execute('SELECT COUNT(*) FROM contacts WHERE status = "active"')
            total_contacts = cursor.fetchone()[0]
            
            # Total de campanhas
            cursor.execute('SELECT COUNT(*) FROM campaigns')
            total_campaigns = cursor.fetchone()[0]
            
            return {
                'emails_sent_today': emails_sent_today,
                'total_contacts': total_contacts,
                'total_campaigns': total_campaigns,
                'daily_limit': 10000  # Limite padrão
            }
