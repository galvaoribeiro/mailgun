# 🚀 Guia de Início Rápido

Este guia te ajudará a configurar e usar o sistema de cold emails em menos de 10 minutos.

## ⚡ Configuração Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar Variáveis de Ambiente
Crie um arquivo `.env` com suas configurações do Mailgun:

```bash
MAILGUN_API_KEY=sua_api_key_aqui
MAILGUN_DOMAIN=mg.auditor-simples.com
PORT=5000
DEBUG=True
BATCH_SIZE=100
DELAY_BETWEEN_BATCHES=60
MAX_EMAILS_PER_DAY=1000
```

### 3. Testar Configuração
```bash
python test_setup.py
```

**⚠️ Se encontrar erros de compatibilidade (numpy.dtype), execute:**
```bash
python fix_dependencies.py
```

### 4. Iniciar Servidor
```bash
python app.py
```

Acesse: http://localhost:5000

## 📧 Primeiro Envio

### Opção 1: Via Interface Web
1. Acesse http://localhost:5000
2. Use os endpoints da API para:
   - Importar contatos
   - Criar campanha
   - Enviar emails

### Opção 2: Via Python
```python
from email_service import EmailService

# Inicializar
email_service = EmailService()

# Adicionar contatos
email_service.db.add_contact(
    email="teste@empresa.com",
    name="João Silva",
    company="Empresa ABC",
    position="CEO"
)

# Criar campanha
campaign_id = email_service.create_campaign(
    name="Primeira Campanha",
    subject_template="Olá {name}, oferta para {company}",
    body_template="Olá {name}, temos uma oferta especial..."
)

# Enviar (modo teste)
result = email_service.send_campaign(
    campaign_id=campaign_id,
    test_mode=True
)
```

### Opção 3: Usar Exemplo Completo
```bash
python example_usage.py
```

## 📊 Monitoramento

### Verificar Estatísticas
```bash
# Via API
curl http://localhost:5000/stats/daily

# Via Python
stats = email_service.get_daily_stats()
print(stats)
```

### Verificar Campanhas
```bash
# Via API
curl http://localhost:5000/campaigns/1/stats

# Via Python
stats = email_service.get_campaign_stats(1)
print(stats)
```

## 🔧 Configurações Importantes

### Para Começar (Recomendado)
```bash
BATCH_SIZE=100          # Emails por lote
DELAY_BETWEEN_BATCHES=120  # 2 minutos entre lotes
MAX_EMAILS_PER_DAY=1000    # Limite diário
```

### Para Produção
```bash
BATCH_SIZE=1000         # Emails por lote
DELAY_BETWEEN_BATCHES=60   # 1 minuto entre lotes
MAX_EMAILS_PER_DAY=10000   # Limite diário
```

## 📁 Arquivos Importantes

- `app.py` - Servidor principal
- `email_service.py` - Lógica de negócio
- `database.py` - Banco de dados
- `mailgun_client.py` - Cliente Mailgun
- `example_usage.py` - Exemplos de uso
- `sample_contacts.csv` - Contatos de exemplo

## 🚨 Dicas Importantes

1. **Sempre teste primeiro** com `test_mode=True`
2. **Use templates personalizados** com `{name}`, `{company}`, `{position}`
3. **Monitore bounces** e remova emails inválidos
4. **Respeite limites** de envio do Mailgun
5. **Mantenha lista limpa** de contatos

## 🆘 Solução de Problemas

### Erro de API Key
- Verifique se `MAILGUN_API_KEY` está correta
- Confirme se o domínio está ativo no Mailgun

### Emails não sendo enviados
- Verifique limite diário: `curl http://localhost:5000/health`
- Confirme se há contatos ativos
- Verifique logs de erro

### Webhooks não funcionando
- Confirme se endpoint está acessível publicamente
- Verifique configuração no painel do Mailgun

## 📞 Próximos Passos

1. **Configure webhooks** no Mailgun para tracking
2. **Importe sua lista** de contatos via CSV
3. **Crie templates** personalizados
4. **Monitore resultados** e otimize campanhas
5. **Escale gradualmente** conforme resultados

---

**🎯 Objetivo:** Envie seu primeiro cold email em menos de 10 minutos!

**📚 Documentação Completa:** Veja o `README.md` para detalhes avançados.
