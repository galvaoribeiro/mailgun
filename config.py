import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Configurações do Mailgun
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', 'sandbox4edf729669064f5ebc1687a8d6e403dd.mailgun.org')
    BASE_URL = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}'
    
    # Configurações de envio
    BATCH_SIZE = int(os.environ.get('BATCH_SIZE', 1000))
    DELAY_BETWEEN_BATCHES = int(os.environ.get('DELAY_BETWEEN_BATCHES', 60))
    MAX_EMAILS_PER_DAY = int(os.environ.get('MAX_EMAILS_PER_DAY', 10000))
    
    # Configurações da aplicação
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Configurações de email
    FROM_EMAIL = f'Auditor Simples <no-reply@{MAILGUN_DOMAIN}>'
    REPLY_TO = 'contato@auditor-simples.com'
    
    # Configurações de tracking
    TRACKING_ENABLED = True
    TAG_PREFIX = 'cold-email'
    
    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        if not cls.MAILGUN_API_KEY:
            raise ValueError("MAILGUN_API_KEY é obrigatória")
        if not cls.MAILGUN_DOMAIN:
            raise ValueError("MAILGUN_DOMAIN é obrigatória")
        return True
