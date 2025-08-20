# 🚀 Sistema de Cold Emails com Mailgun

Sistema completo e profissional para envio de cold emails usando a API do Mailgun. Inclui gerenciamento de contatos, campanhas, tracking e estatísticas detalhadas.

## ✨ Funcionalidades

- 📧 **Envio em lote** com throttling automático
- 👥 **Gerenciamento de contatos** com importação CSV
- 📋 **Criação de campanhas** com templates personalizáveis
- 📊 **Tracking completo** (aberturas, cliques, bounces)
- 🔄 **Webhooks** para atualização automática de status
- 📈 **Estatísticas detalhadas** por campanha e diárias
- 🛡️ **Validação de emails** usando API do Mailgun
- ⚡ **Modo assíncrono** para envios em background
- 🧪 **Modo teste** para validação antes do envio
- 📱 **API REST** completa para integração

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd MAILGUN
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` baseado no `env_example.txt`:

```bash
# Configurações do Mailgun
MAILGUN_API_KEY=sua_api_key_aqui
MAILGUN_DOMAIN=mg.auditor-simples.com

# Configurações da aplicação
PORT=5000
DEBUG=True

# Configurações de envio
BATCH_SIZE=1000
DELAY_BETWEEN_BATCHES=60
MAX_EMAILS_PER_DAY=10000
```

### 4. Configure o Mailgun

1. Acesse [mailgun.com](https://mailgun.com) e crie uma conta
2. Adicione seu domínio ou use um domínio sandbox
3. Obtenha sua API Key nas configurações
4. Configure webhooks para receber eventos (opcional)

## 🚀 Como Usar

### Iniciando o Servidor

```bash
python app.py
```

O servidor estará disponível em `http://localhost:5000`

### Uso via API REST

#### 1. Importar Contatos
```bash
curl -X POST http://localhost:5000/contacts/import \
  -F "file=@contatos.csv" \
  -F "source=linkedin"
```

#### 2. Criar Campanha
```bash
curl -X POST http://localhost:5000/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Oferta Especial",
    "subject": "Olá {name}, oferta exclusiva para {company}",
    "body": "Olá {name}, temos uma oferta especial..."
  }'
```

#### 3. Enviar Campanha
```bash
curl -X POST http://localhost:5000/campaigns/1/send \
  -H "Content-Type: application/json" \
  -d '{
    "test_mode": true,
    "contact_limit": 100
  }'
```

#### 4. Verificar Estatísticas
```bash
curl http://localhost:5000/campaigns/1/stats
```

### Uso via Python

```python
from email_service import EmailService

# Inicializar serviço
email_service = EmailService()

# Adicionar contatos
email_service.db.add_contact(
    email="exemplo@empresa.com",
    name="João Silva",
    company="Empresa ABC",
    position="CEO"
)

# Criar campanha
campaign_id = email_service.create_campaign(
    name="Oferta Especial",
    subject_template="Olá {name}, oferta para {company}",
    body_template="Olá {name}, temos uma oferta..."
)

# Enviar campanha
result = email_service.send_campaign(
    campaign_id=campaign_id,
    test_mode=True
)
```

## 📁 Estrutura do Projeto

```
MAILGUN/
├── app.py                 # Aplicação Flask principal
├── config.py             # Configurações centralizadas
├── database.py           # Sistema de banco de dados
├── mailgun_client.py     # Cliente para API do Mailgun
├── email_service.py      # Serviço principal de emails
├── example_usage.py      # Exemplos de uso
├── requirements.txt      # Dependências Python
├── env_example.txt       # Exemplo de variáveis de ambiente
└── README.md            # Esta documentação
```

## 📊 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Documentação da API |
| POST | `/contacts/import` | Importar contatos CSV |
| GET | `/contacts` | Listar contatos |
| POST | `/campaigns` | Criar campanha |
| POST | `/campaigns/{id}/send` | Enviar campanha |
| GET | `/campaigns/{id}/stats` | Estatísticas da campanha |
| GET | `/stats/daily` | Estatísticas diárias |
| POST | `/webhook/mailgun` | Webhook do Mailgun |
| GET | `/health` | Status da aplicação |

## 📧 Formato do CSV

Para importar contatos, use um arquivo CSV com as seguintes colunas:

```csv
email,name,company,position
joao@empresa.com,João Silva,Empresa ABC,CEO
maria@startup.com,Maria Santos,Startup XYZ,CTO
```

## 🔧 Configuração de Webhooks

Para receber eventos do Mailgun (aberturas, cliques, bounces):

1. Acesse o painel do Mailgun
2. Vá em "Webhooks"
3. Configure o endpoint: `https://seu-dominio.com/webhook/mailgun`
4. Selecione os eventos: `delivered`, `opened`, `clicked`, `bounced`

## 📈 Monitoramento

### Estatísticas Disponíveis

- **Por Campanha:**
  - Total de emails enviados
  - Taxa de abertura
  - Taxa de clique
  - Taxa de bounce
  - Emails entregues

- **Diárias:**
  - Emails enviados hoje
  - Emails abertos hoje
  - Emails clicados hoje
  - Quota restante

### Logs e Debug

O sistema registra todos os envios e eventos no banco de dados SQLite. Você pode consultar:

```python
# Verificar logs de envio
logs = email_service.db.get_email_logs(campaign_id=1)

# Verificar bounces
bounces = email_service.mailgun.get_bounces()
```

## 🛡️ Boas Práticas

### Para Cold Emails

1. **Personalização:** Use variáveis `{name}`, `{company}`, `{position}`
2. **Assunto atrativo:** Seja específico e relevante
3. **Call-to-action claro:** Defina o que você quer que o destinatário faça
4. **Teste primeiro:** Use `test_mode=True` antes de enviar em massa
5. **Respeite limites:** Configure `MAX_EMAILS_PER_DAY` adequadamente
6. **Monitore bounces:** Remova emails que deram bounce automaticamente

### Configurações Recomendadas

```bash
# Para começar
BATCH_SIZE=100
DELAY_BETWEEN_BATCHES=120
MAX_EMAILS_PER_DAY=1000

# Para produção
BATCH_SIZE=1000
DELAY_BETWEEN_BATCHES=60
MAX_EMAILS_PER_DAY=10000
```

## 🚨 Limitações e Considerações

- **Rate Limiting:** O Mailgun tem limites de envio por hora/dia
- **Domínio:** Use um domínio verificado para melhor deliverability
- **Lista de Contatos:** Mantenha sua lista limpa e atualizada
- **Compliance:** Respeite leis de proteção de dados (LGPD, GDPR)

## 🔍 Troubleshooting

### Problemas Comuns

1. **Erro de API Key:**
   - Verifique se `MAILGUN_API_KEY` está correta
   - Confirme se o domínio está ativo no Mailgun

2. **Emails não sendo enviados:**
   - Verifique o limite diário
   - Confirme se há contatos ativos
   - Verifique logs de erro

3. **Webhooks não funcionando:**
   - Confirme se o endpoint está acessível publicamente
   - Verifique se o domínio está configurado corretamente

### Logs de Debug

Ative o modo debug para ver logs detalhados:

```bash
DEBUG=True python app.py
```

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs da aplicação
2. Consulte a documentação do Mailgun
3. Teste com `test_mode=True` primeiro
4. Verifique as configurações no arquivo `.env`

## 📄 Licença

Este projeto é de código aberto. Sinta-se livre para usar e modificar conforme suas necessidades.

---

**⚠️ Importante:** Sempre teste suas campanhas antes de enviar em massa e respeite as leis de proteção de dados aplicáveis.
