# 📧 Cold Email Service - Interface Amigável

Sistema completo para envio de cold emails usando Mailgun com interface web moderna e intuitiva.

## 🚀 Como Usar

### 1. Configuração Inicial

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```
   MAILGUN_API_KEY=sua_chave_api_aqui
   MAILGUN_DOMAIN=seu_dominio.mailgun.org
   MAX_EMAILS_PER_DAY=10000
   ```

3. **Execute a aplicação:**
   ```bash
   python app.py
   ```

4. **Acesse a interface:**
   Abra seu navegador e vá para: `http://localhost:5000`

## 📱 Interface Amigável

A nova interface web oferece 4 seções principais:

### 📁 Upload CSV
- Faça upload do seu arquivo CSV com contatos
- O arquivo deve conter colunas: `email`, `name`, `company`, `position`
- Defina a fonte dos contatos (ex: site_web, linkedin, etc)

### 📝 Campanhas
- Crie novas campanhas de email
- Personalize assunto e corpo do email
- Use variáveis como `{nome}`, `{email}`, `{empresa}` para personalização
- Visualize todas as campanhas criadas

### 🚀 Enviar
- Selecione uma campanha para enviar
- Configure limite de contatos (opcional)
- Ative modo teste para enviar apenas para você
- Use envio assíncrono para melhor performance

### 📊 Estatísticas
- Acompanhe emails enviados hoje
- Visualize limite diário
- Veja total de contatos e campanhas
- Atualize estatísticas em tempo real

## 📋 Formato do CSV

Seu arquivo CSV deve ter a seguinte estrutura:

```csv
email,name,company,position
joao@empresa.com,João Silva,Empresa ABC,Gerente
maria@startup.com,Maria Santos,Startup XYZ,CEO
```

## 🔧 Recursos Avançados

### Personalização de Emails
Use variáveis no assunto e corpo dos emails:
- `{nome}` - Nome do contato
- `{email}` - Email do contato
- `{empresa}` - Empresa do contato
- `{cargo}` - Cargo do contato

### Modo Teste
Ative o modo teste para enviar emails apenas para você, útil para testar campanhas antes do envio em massa.

### Envio Assíncrono
O envio assíncrono permite que a aplicação continue funcionando enquanto envia emails em segundo plano.

## 📊 Monitoramento

A aplicação registra automaticamente:
- Emails enviados
- Emails abertos
- Emails clicados
- Bounces e erros

## 🔒 Segurança

- Validação de emails antes do envio
- Limite diário configurável
- Controle de rate limiting
- Logs detalhados de todas as operações

## 🆘 Suporte

Se encontrar problemas:
1. Verifique as configurações no arquivo `.env`
2. Confirme que sua chave API do Mailgun está correta
3. Verifique se o domínio está configurado no Mailgun
4. Consulte os logs da aplicação para detalhes de erros

## 📈 Próximas Funcionalidades

- [ ] Dashboard com gráficos
- [ ] Templates de email pré-definidos
- [ ] Segmentação de contatos
- [ ] Automação de campanhas
- [ ] Integração com CRM
- [ ] Relatórios avançados
