// Funções de navegação
function showTab(tabName, clickedElement) {
    console.log('showTab chamado com:', tabName, clickedElement);
    
    // Remove active de todas as tabs
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Adiciona active na tab selecionada
    clickedElement.classList.add('active');
    document.getElementById(tabName).classList.add('active');
    
    // Carrega dados específicos da tab
    if (tabName === 'campaigns') {
        loadCampaigns();
    } else if (tabName === 'send') {
        loadCampaignsForSend();
    } else if (tabName === 'batches') {
        loadBatches();
    } else if (tabName === 'stats') {
        loadStats();
    }
    
    console.log('Tab ativada:', tabName);
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

// Carregar lotes de contatos
async function loadBatches() {
    try {
        const response = await fetch('/contacts/batches');
        const result = await response.json();

        const batchesList = document.getElementById('batches-list');
        const batchesLoading = document.getElementById('batches-loading');

        if (result.success) {
            batchesLoading.style.display = 'none';
            if (result.batches.length > 0) {
                batchesList.innerHTML = result.batches.map(batch => {
                    const isActive = batch.batch_status === 'active';
                    return `
                        <div class="campaign-item">
                            <div class="campaign-name">Lote ${batch.batch_id}</div>
                            <div class="campaign-details">
                                Contatos: ${batch.contact_count} | 
                                Primeira importação: ${new Date(batch.first_import).toLocaleDateString('pt-BR')} | 
                                Última importação: ${new Date(batch.last_import).toLocaleDateString('pt-BR')} |
                                Status: ${batch.batch_status}
                            </div>
                            <div class="campaign-actions">
                                <button class="btn btn-secondary" onclick="activateBatch('${batch.batch_id}')" ${isActive ? 'disabled' : ''}>
                                    ${isActive ? 'Ativo' : 'Ativar'}
                                </button>
                                <button class="btn btn-danger" onclick="deactivateBatch('${batch.batch_id}')" ${!isActive ? 'disabled' : ''}>
                                    ${!isActive ? 'Inativo' : 'Desativar'}
                                </button>
                                <button class="btn" onclick="viewContacts('${batch.batch_id}')">Ver Contatos</button>
                            </div>
                        </div>
                    `;
                }).join('');
            } else {
                batchesList.innerHTML = '<p>Nenhum lote de contatos encontrado.</p>';
            }
        } else {
            batchesLoading.style.display = 'none';
            batchesList.innerHTML = '<p>Erro ao carregar lotes: ' + result.error + '</p>';
        }
    } catch (error) {
        batchesLoading.style.display = 'none';
        batchesList.innerHTML = '<p>Erro de conexão ao carregar lotes: ' + error.message + '</p>';
    }
}

// Função para ativar lote
async function activateBatch(batchId) {
    if (!confirm('Tem certeza que deseja ativar este lote?')) {
        return;
    }
    document.getElementById('batches-loading').style.display = 'block';
    try {
        const response = await fetch(`/contacts/batches/${batchId}/activate`, { method: 'POST' });
        const result = await response.json();
        if (result.success) {
            showAlert('batches-alert', result.message, 'success');
            loadBatches();
        } else {
            showAlert('batches-alert', `Erro ao ativar lote: ${result.error}`, 'error');
        }
    } catch (error) {
        showAlert('batches-alert', `Erro de conexão ao ativar lote: ${error.message}`, 'error');
    } finally {
        document.getElementById('batches-loading').style.display = 'none';
    }
}

// Função para desativar lote
async function deactivateBatch(batchId) {
    if (!confirm('Tem certeza que deseja desativar este lote?')) {
        return;
    }
    document.getElementById('batches-loading').style.display = 'block';
    try {
        const response = await fetch(`/contacts/batches/${batchId}/deactivate`, { method: 'POST' });
        const result = await response.json();
        if (result.success) {
            showAlert('batches-alert', result.message, 'success');
            loadBatches();
        } else {
            showAlert('batches-alert', `Erro ao desativar lote: ${result.error}`, 'error');
        }
    } catch (error) {
        showAlert('batches-alert', `Erro de conexão ao desativar lote: ${error.message}`, 'error');
    } finally {
        document.getElementById('batches-loading').style.display = 'none';
    }
}

// Função para visualizar contatos de um lote
async function viewContacts(batchId) {
    document.getElementById('batches-loading').style.display = 'block';
    try {
        const response = await fetch(`/contacts/batches/${batchId}`);
        const result = await response.json();
        if (result.success) {
            const contacts = result.contacts;
            let html = '<h3>Contatos do Lote ' + batchId + '</h3>';
            if (contacts.length > 0) {
                html += '<table>';
                html += '<tr><th>ID</th><th>Nome</th><th>Email</th><th>Empresa</th><th>Status</th><th>Ações</th></tr>';
                contacts.forEach(contact => {
                    html += '<tr>';
                    html += '<td>' + contact.id + '</td>';
                    html += '<td>' + (contact.name || '-') + '</td>';
                    html += '<td>' + contact.email + '</td>';
                    html += '<td>' + (contact.company || '-') + '</td>';
                    html += '<td>' + contact.status + '</td>';
                    html += '<td>';
                    if (contact.status !== 'active') {
                        html += '<button class="btn btn-secondary" onclick="updateContactStatus(' + contact.id + ', \'active\')">Ativo</button> ';
                    }
                    if (contact.status !== 'inactive') {
                        html += '<button class="btn btn-warning" onclick="updateContactStatus(' + contact.id + ', \'inactive\')">Inativo</button> ';
                    }
                    html += '<button class="btn btn-danger" onclick="deleteContact(' + contact.id + ')">Excluir</button>';
                    html += '</td>';
                    html += '</tr>';
                });
                html += '</table>';
            } else {
                html += '<p>Nenhum contato encontrado neste lote.</p>';
            }
            
            // Cria um modal mais elegante
            const modal = document.createElement('div');
            modal.className = 'modal';
            
            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content';
            modalContent.innerHTML = html;
            
            const closeBtn = document.createElement('button');
            closeBtn.textContent = 'Fechar';
            closeBtn.className = 'btn btn-secondary';
            closeBtn.style.marginTop = '20px';
            closeBtn.onclick = () => document.body.removeChild(modal);
            
            modalContent.appendChild(closeBtn);
            modal.appendChild(modalContent);
            document.body.appendChild(modal);
            
        } else {
            showAlert('batches-alert', 'Erro ao carregar contatos: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('batches-alert', 'Erro de conexão ao carregar contatos: ' + error.message, 'error');
    } finally {
        document.getElementById('batches-loading').style.display = 'none';
    }
}

// Função para atualizar status de um contato
async function updateContactStatus(contactId, status) {
    if (!confirm('Tem certeza que deseja alterar o status do contato ' + contactId + ' para "' + status + '"?')) {
        return;
    }
    document.getElementById('batches-loading').style.display = 'block';
    try {
        const response = await fetch('/contacts/' + contactId + '/status', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: status })
        });
        const result = await response.json();
        if (result.success) {
            showAlert('batches-alert', result.message, 'success');
            // Fecha o modal atual e recarrega os lotes
            const modal = document.querySelector('.modal');
            if (modal) {
                document.body.removeChild(modal);
            }
            loadBatches();
        } else {
            showAlert('batches-alert', 'Erro ao atualizar status: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('batches-alert', 'Erro de conexão ao atualizar status: ' + error.message, 'error');
    } finally {
        document.getElementById('batches-loading').style.display = 'none';
    }
}

// Função para excluir um contato
async function deleteContact(contactId) {
    if (!confirm('Tem certeza que deseja excluir o contato ' + contactId + '?')) {
        return;
    }
    document.getElementById('batches-loading').style.display = 'block';
    try {
        const response = await fetch('/contacts/' + contactId, { method: 'DELETE' });
        const result = await response.json();
        if (result.success) {
            showAlert('batches-alert', result.message, 'success');
            // Fecha o modal atual e recarrega os lotes
            const modal = document.querySelector('.modal');
            if (modal) {
                document.body.removeChild(modal);
            }
            loadBatches();
        } else {
            showAlert('batches-alert', 'Erro ao excluir contato: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('batches-alert', 'Erro de conexão ao excluir contato: ' + error.message, 'error');
    } finally {
        document.getElementById('batches-loading').style.display = 'none';
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
    console.log('DOM carregado, inicializando aplicação...');
    loadStats();
    loadCampaigns(); // Carregar campanhas ao iniciar
    loadCampaignsForSend(); // Carregar campanhas para envio ao iniciar
    loadBatches(); // Carregar lotes ao iniciar
});
