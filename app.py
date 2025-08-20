from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from email_service import EmailService
from config import Config

app = Flask(__name__)
CORS(app)

# Inicializa o serviço de email
email_service = EmailService()

# Valida configurações na inicialização
try:
    Config.validate()
except ValueError as e:
    print(f"Erro de configuração: {e}")
    exit(1)

@app.route('/')
def index():
    """Página inicial com documentação da API"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cold Email Service - Mailgun</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #0066cc; }
            .url { font-family: monospace; background: #e0e0e0; padding: 2px 5px; }
        </style>
    </head>
    <body>
        <h1>🚀 Cold Email Service - Mailgun</h1>
        <p>Sistema completo para envio de cold emails usando Mailgun</p>
        
        <h2>📋 Endpoints Disponíveis:</h2>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/contacts/import</div>
            <p>Importa contatos de um arquivo CSV</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/campaigns</div>
            <p>Cria uma nova campanha de email</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/campaigns/{id}/send</div>
            <p>Envia uma campanha</p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <div class="url">/campaigns/{id}/stats</div>
            <p>Estatísticas de uma campanha</p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <div class="url">/stats/daily</div>
            <p>Estatísticas do dia atual</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/webhook/mailgun</div>
            <p>Webhook para receber eventos do Mailgun</p>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/contacts/import', methods=['POST'])
def import_contacts():
    """Importa contatos de um arquivo CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Arquivo deve ser CSV'}), 400
        
        # Salva o arquivo temporariamente
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            source = request.form.get('source', 'csv_import')
            count = email_service.add_contacts_from_csv(tmp_path, source)
            
            return jsonify({
                'success': True,
                'contacts_imported': count,
                'message': f'{count} contatos importados com sucesso'
            })
        
        finally:
            # Remove arquivo temporário
            os.unlink(tmp_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contacts', methods=['GET'])
def get_contacts():
    """Lista contatos"""
    try:
        status = request.args.get('status', 'active')
        limit = request.args.get('limit', type=int)
        
        contacts = email_service.db.get_contacts(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'contacts': contacts,
            'count': len(contacts)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns', methods=['POST'])
def create_campaign():
    """Cria uma nova campanha"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados JSON necessários'}), 400
        
        required_fields = ['name', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        campaign_id = email_service.create_campaign(
            name=data['name'],
            subject_template=data['subject'],
            body_template=data['body']
        )
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'message': 'Campanha criada com sucesso'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns/<int:campaign_id>/send', methods=['POST'])
def send_campaign(campaign_id):
    """Envia uma campanha"""
    try:
        data = request.get_json() or {}
        
        contact_limit = data.get('contact_limit')
        test_mode = data.get('test_mode', False)
        async_mode = data.get('async_mode', False)
        
        if async_mode:
            # Envia de forma assíncrona
            thread = email_service.send_campaign_async(
                campaign_id=campaign_id,
                contact_limit=contact_limit,
                test_mode=test_mode
            )
            
            return jsonify({
                'success': True,
                'message': 'Campanha iniciada em modo assíncrono',
                'campaign_id': campaign_id
            })
        else:
            # Envia de forma síncrona
            result = email_service.send_campaign(
                campaign_id=campaign_id,
                contact_limit=contact_limit,
                test_mode=test_mode
            )
            
            if result['success']:
                return jsonify(result)
            else:
                return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/campaigns/<int:campaign_id>/stats', methods=['GET'])
def get_campaign_stats(campaign_id):
    """Retorna estatísticas de uma campanha"""
    try:
        stats = email_service.get_campaign_stats(campaign_id)
        
        return jsonify({
            'success': True,
            'campaign_id': campaign_id,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats/daily', methods=['GET'])
def get_daily_stats():
    """Retorna estatísticas do dia atual"""
    try:
        stats = email_service.get_daily_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/mailgun', methods=['POST'])
def mailgun_webhook():
    """Webhook para receber eventos do Mailgun"""
    try:
        # Verifica se é um evento válido do Mailgun
        signature = request.form.get('signature')
        timestamp = request.form.get('timestamp')
        token = request.form.get('token')
        
        # Aqui você pode adicionar validação da assinatura do Mailgun
        # Por simplicidade, vamos processar todos os eventos
        
        event_data = {
            'recipient': request.form.get('recipient'),
            'event': request.form.get('event'),
            'timestamp': timestamp,
            'message-id': request.form.get('message-id'),
            'domain': request.form.get('domain')
        }
        
        # Atualiza status no banco de dados
        email_service.update_email_status_from_webhook(event_data)
        
        return jsonify({'success': True, 'message': 'Evento processado'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde da aplicação"""
    try:
        # Verifica se pode enviar mais emails
        can_send = email_service.can_send_more_emails()
        
        return jsonify({
            'status': 'healthy',
            'can_send_emails': can_send,
            'daily_sent_count': email_service.daily_sent_count,
            'daily_limit': Config.MAX_EMAILS_PER_DAY
        })
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando Cold Email Service...")
    print(f"📧 Domínio: {Config.MAILGUN_DOMAIN}")
    print(f"📊 Limite diário: {Config.MAX_EMAILS_PER_DAY} emails")
    print(f"🌐 Servidor rodando em: http://localhost:{Config.PORT}")
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
