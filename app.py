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
    """Página inicial com interface amigável"""
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cold Email Service - Interface Amigável</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .content {
                padding: 40px;
            }
            
            .tabs {
                display: flex;
                border-bottom: 2px solid #eee;
                margin-bottom: 30px;
            }
            
            .tab {
                padding: 15px 30px;
                cursor: pointer;
                border-bottom: 3px solid transparent;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            
            .tab.active {
                border-bottom-color: #4facfe;
                color: #4facfe;
            }
            
            .tab:hover {
                background: #f8f9fa;
            }
            
            .tab-content {
                display: none;
            }
            
            .tab-content.active {
                display: block;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
            }
            
            .form-control {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }
            
            .form-control:focus {
                outline: none;
                border-color: #4facfe;
                box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
            }
            
            .btn {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .btn-secondary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .btn-danger {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            }
            
            .alert {
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                border-left: 4px solid;
            }
            
            .alert-success {
                background: #d4edda;
                border-color: #28a745;
                color: #155724;
            }
            
            .alert-error {
                background: #f8d7da;
                border-color: #dc3545;
                color: #721c24;
            }
            
            .alert-info {
                background: #d1ecf1;
                border-color: #17a2b8;
                color: #0c5460;
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .stat-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                border: 1px solid #e9ecef;
            }
            
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #4facfe;
            }
            
            .stat-label {
                color: #6c757d;
                margin-top: 5px;
            }
            
            .file-upload {
                border: 2px dashed #4facfe;
                border-radius: 10px;
                padding: 40px;
                text-align: center;
                background: #f8f9fa;
                transition: all 0.3s ease;
            }
            
            .file-upload:hover {
                border-color: #00f2fe;
                background: #e3f2fd;
            }
            
            .file-upload input[type="file"] {
                display: none;
            }
            
            .file-upload-label {
                cursor: pointer;
                color: #4facfe;
                font-weight: 600;
            }
            
            .campaign-list {
                margin-top: 20px;
            }
            
            .campaign-item {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 15px;
                border: 1px solid #e9ecef;
            }
            
            .campaign-name {
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
            
            .campaign-details {
                color: #6c757d;
                font-size: 0.9em;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #4facfe;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @media (max-width: 768px) {
                .container {
                    margin: 10px;
                    border-radius: 10px;
                }
                
                .header {
                    padding: 20px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .content {
                    padding: 20px;
                }
                
                .tabs {
                    flex-direction: column;
                }
                
                .tab {
                    text-align: center;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📧 Cold Email Service</h1>
                <p>Interface amigável para envio de emails em massa</p>
            </div>
            
            <div class="content">
                <div class="tabs">
                    <div class="tab active" onclick="showTab('upload')">📁 Upload CSV</div>
                    <div class="tab" onclick="showTab('campaigns')">📝 Campanhas</div>
                    <div class="tab" onclick="showTab('send')">🚀 Enviar</div>
                    <div class="tab" onclick="showTab('stats')">📊 Estatísticas</div>
                </div>
                
                <!-- Tab Upload CSV -->
                <div id="upload" class="tab-content active">
                    <h2>Importar Contatos</h2>
                    <p>Faça upload do seu arquivo CSV com os contatos para importar.</p>
                    
                    <div id="upload-alert"></div>
                    
                    <form id="upload-form">
                        <div class="form-group">
                            <label>Arquivo CSV:</label>
                            <div class="file-upload" onclick="document.getElementById('csv-file').click()">
                                <input type="file" id="csv-file" accept=".csv" onchange="updateFileName()">
                                <div class="file-upload-label">
                                    <div>📁 Clique para selecionar arquivo CSV</div>
                                    <div id="file-name" style="margin-top: 10px; font-size: 0.9em; color: #666;"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="form-group">
                            <label>Fonte dos contatos:</label>
                            <input type="text" class="form-control" id="source" value="csv_import" placeholder="Ex: site_web, linkedin, etc">
                        </div>
                        
                        <button type="submit" class="btn">📥 Importar Contatos</button>
                    </form>
                    
                    <div class="loading" id="upload-loading">
                        <div class="spinner"></div>
                        <p>Importando contatos...</p>
                    </div>
                </div>
                
                <!-- Tab Campanhas -->
                <div id="campaigns" class="tab-content">
                    <h2>Criar Nova Campanha</h2>
                    <p>Crie uma nova campanha de email personalizada.</p>
                    
                    <div id="campaign-alert"></div>
                    
                    <form id="campaign-form">
                        <div class="form-group">
                            <label>Nome da Campanha:</label>
                            <input type="text" class="form-control" id="campaign-name" placeholder="Ex: Campanha de Boas-vindas" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Assunto do Email:</label>
                            <input type="text" class="form-control" id="campaign-subject" placeholder="Ex: Olá {nome}, temos uma proposta para você!" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Corpo do Email:</label>
                            <textarea class="form-control" id="campaign-body" rows="10" placeholder="Digite o conteúdo do email. Use {nome}, {email}, {empresa} para personalização." required></textarea>
                        </div>
                        
                        <button type="submit" class="btn">📝 Criar Campanha</button>
                    </form>
                    
                    <div class="loading" id="campaign-loading">
                        <div class="spinner"></div>
                        <p>Criando campanha...</p>
                    </div>
                    
                    <h3 style="margin-top: 40px;">Campanhas Existentes</h3>
                    <div id="campaigns-list" class="campaign-list">
                        <p>Carregando campanhas...</p>
                    </div>
                </div>
                
                <!-- Tab Enviar -->
                <div id="send" class="tab-content">
                    <h2>Enviar Campanha</h2>
                    <p>Selecione uma campanha e envie para seus contatos.</p>
                    
                    <div id="send-alert"></div>
                    
                    <form id="send-form">
                        <div class="form-group">
                            <label>Selecionar Campanha:</label>
                            <select class="form-control" id="send-campaign" required>
                                <option value="">Selecione uma campanha...</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Limite de Contatos (opcional):</label>
                            <input type="number" class="form-control" id="contact-limit" placeholder="Deixe vazio para enviar para todos">
                        </div>
                        
                        <div class="form-group">
                            <label>
                                <input type="checkbox" id="test-mode"> Modo Teste (envia apenas para você)
                            </label>
                        </div>
                        
                        <div class="form-group">
                            <label>
                                <input type="checkbox" id="async-mode" checked> Envio Assíncrono (recomendado)
                            </label>
                        </div>
                        
                        <button type="submit" class="btn">🚀 Enviar Campanha</button>
                    </form>
                    
                    <div class="loading" id="send-loading">
                        <div class="spinner"></div>
                        <p>Enviando campanha...</p>
                    </div>
                </div>
                
                <!-- Tab Estatísticas -->
                <div id="stats" class="tab-content">
                    <h2>Estatísticas</h2>
                    <p>Acompanhe o desempenho das suas campanhas.</p>
                    
                    <div id="stats-alert"></div>
                    
                    <div class="stats-grid" id="daily-stats">
                        <div class="stat-card">
                            <div class="stat-number" id="daily-sent">-</div>
                            <div class="stat-label">Emails Enviados Hoje</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="daily-limit">-</div>
                            <div class="stat-label">Limite Diário</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="total-contacts">-</div>
                            <div class="stat-label">Total de Contatos</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="total-campaigns">-</div>
                            <div class="stat-label">Total de Campanhas</div>
                        </div>
                    </div>
                    
                    <button class="btn" onclick="loadStats()">🔄 Atualizar Estatísticas</button>
                </div>
            </div>
        </div>
        
        <script>
            // Funções de navegação
            function showTab(tabName) {
                // Remove active de todas as tabs
                document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                
                // Adiciona active na tab selecionada
                event.target.classList.add('active');
                document.getElementById(tabName).classList.add('active');
                
                // Carrega dados específicos da tab
                if (tabName === 'campaigns') {
                    loadCampaigns();
                } else if (tabName === 'send') {
                    loadCampaignsForSend();
                } else if (tabName === 'stats') {
                    loadStats();
                }
            }
            
            // Função para atualizar nome do arquivo
            function updateFileName() {
                const file = document.getElementById('csv-file').files[0];
                const fileName = document.getElementById('file-name');
                if (file) {
                    fileName.textContent = `Arquivo selecionado: ${file.name}`;
                } else {
                    fileName.textContent = '';
                }
            }
            
            // Função para mostrar alertas
            function showAlert(containerId, message, type = 'info') {
                const container = document.getElementById(containerId);
                container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
                setTimeout(() => {
                    container.innerHTML = '';
                }, 5000);
            }
            
            // Upload de CSV
            document.getElementById('upload-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const file = document.getElementById('csv-file').files[0];
                const source = document.getElementById('source').value;
                
                if (!file) {
                    showAlert('upload-alert', 'Por favor, selecione um arquivo CSV.', 'error');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                formData.append('source', source);
                
                document.getElementById('upload-loading').style.display = 'block';
                
                try {
                    const response = await fetch('/contacts/import', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert('upload-alert', `${result.message}`, 'success');
                        document.getElementById('upload-form').reset();
                        document.getElementById('file-name').textContent = '';
                    } else {
                        showAlert('upload-alert', `Erro: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('upload-alert', `Erro de conexão: ${error.message}`, 'error');
                } finally {
                    document.getElementById('upload-loading').style.display = 'none';
                }
            });
            
            // Criar campanha
            document.getElementById('campaign-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const name = document.getElementById('campaign-name').value;
                const subject = document.getElementById('campaign-subject').value;
                const body = document.getElementById('campaign-body').value;
                
                document.getElementById('campaign-loading').style.display = 'block';
                
                try {
                    const response = await fetch('/campaigns', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ name, subject, body })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert('campaign-alert', `Campanha criada com sucesso! ID: ${result.campaign_id}`, 'success');
                        document.getElementById('campaign-form').reset();
                        loadCampaigns();
                    } else {
                        showAlert('campaign-alert', `Erro: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('campaign-alert', `Erro de conexão: ${error.message}`, 'error');
                } finally {
                    document.getElementById('campaign-loading').style.display = 'none';
                }
            });
            
            // Enviar campanha
            document.getElementById('send-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const campaignId = document.getElementById('send-campaign').value;
                const contactLimit = document.getElementById('contact-limit').value;
                const testMode = document.getElementById('test-mode').checked;
                const asyncMode = document.getElementById('async-mode').checked;
                
                if (!campaignId) {
                    showAlert('send-alert', 'Por favor, selecione uma campanha.', 'error');
                    return;
                }
                
                document.getElementById('send-loading').style.display = 'block';
                
                try {
                    const response = await fetch(`/campaigns/${campaignId}/send`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            contact_limit: contactLimit || null,
                            test_mode: testMode,
                            async_mode: asyncMode
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        showAlert('send-alert', result.message, 'success');
                        document.getElementById('send-form').reset();
                        document.getElementById('send-campaign').innerHTML = '<option value="">Selecione uma campanha...</option>';
                        loadCampaignsForSend();
                    } else {
                        showAlert('send-alert', `Erro: ${result.error}`, 'error');
                    }
                } catch (error) {
                    showAlert('send-alert', `Erro de conexão: ${error.message}`, 'error');
                } finally {
                    document.getElementById('send-loading').style.display = 'none';
                }
            });
            
            // Carregar campanhas
            async function loadCampaigns() {
                try {
                    const response = await fetch('/campaigns');
                    const result = await response.json();
                    
                    const campaignsList = document.getElementById('campaigns-list');
                    
                    if (result.success && result.campaigns.length > 0) {
                        campaignsList.innerHTML = result.campaigns.map(campaign => `
                            <div class="campaign-item">
                                <div class="campaign-name">${campaign.name}</div>
                                <div class="campaign-details">
                                    ID: ${campaign.id} | Criada em: ${new Date(campaign.created_at).toLocaleDateString('pt-BR')}
                                </div>
                            </div>
                        `).join('');
                    } else {
                        campaignsList.innerHTML = '<p>Nenhuma campanha encontrada.</p>';
                    }
                } catch (error) {
                    document.getElementById('campaigns-list').innerHTML = '<p>Erro ao carregar campanhas.</p>';
                }
            }
            
            // Carregar campanhas para envio
            async function loadCampaignsForSend() {
                try {
                    const response = await fetch('/campaigns');
                    const result = await response.json();
                    
                    const select = document.getElementById('send-campaign');
                    select.innerHTML = '<option value="">Selecione uma campanha...</option>';
                    
                    if (result.success && result.campaigns.length > 0) {
                        result.campaigns.forEach(campaign => {
                            const option = document.createElement('option');
                            option.value = campaign.id;
                            option.textContent = campaign.name;
                            select.appendChild(option);
                        });
                    }
                } catch (error) {
                    console.error('Erro ao carregar campanhas:', error);
                }
            }
            
            // Carregar estatísticas
            async function loadStats() {
                try {
                    const response = await fetch('/stats/daily');
                    const result = await response.json();
                    
                    if (result.success) {
                        document.getElementById('daily-sent').textContent = result.stats.emails_sent_today || 0;
                        document.getElementById('daily-limit').textContent = result.stats.daily_limit || 10000;
                        document.getElementById('total-contacts').textContent = result.stats.total_contacts || 0;
                        document.getElementById('total-campaigns').textContent = result.stats.total_campaigns || 0;
                    }
                } catch (error) {
                    showAlert('stats-alert', 'Erro ao carregar estatísticas.', 'error');
                }
            }
            
            // Carregar dados iniciais
            document.addEventListener('DOMContentLoaded', function() {
                loadStats();
            });
        </script>
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

@app.route('/campaigns', methods=['GET'])
def list_campaigns():
    """Lista todas as campanhas"""
    try:
        campaigns = email_service.db.get_campaigns()
        
        return jsonify({
            'success': True,
            'campaigns': campaigns,
            'count': len(campaigns)
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
