# 🚀 Guia Rápido - Interface Amigável

## ⚡ Início Rápido

1. **Execute a aplicação:**
   ```bash
   python app.py
   ```

2. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

3. **Configure suas credenciais do Mailgun no arquivo `.env`:**
   ```
   MAILGUN_API_KEY=sua_chave_api_aqui
   MAILGUN_DOMAIN=seu_dominio.mailgun.org
   ```

## 📱 Como Usar a Interface

### 1. 📁 Upload de Contatos
- Clique na aba "Upload CSV"
- Clique na área pontilhada para selecionar seu arquivo CSV
- Defina a fonte dos contatos (ex: "linkedin", "site_web")
- Clique em "Importar Contatos"

### 2. 📝 Criar Campanha
- Vá para a aba "Campanhas"
- Preencha:
  - **Nome da Campanha:** Ex: "Oferta Especial"
  - **Assunto:** Ex: "Olá {nome}, temos uma proposta para {empresa}"
  - **Corpo:** Digite o conteúdo do email
- Clique em "Criar Campanha"

### 3. 🚀 Enviar Emails
- Vá para a aba "Enviar"
- Selecione a campanha criada
- Configure opções:
  - **Limite de contatos:** Deixe vazio para enviar para todos
  - **Modo teste:** Ative para testar primeiro
  - **Envio assíncrono:** Recomendado para grandes volumes
- Clique em "Enviar Campanha"

### 4. 📊 Acompanhar Resultados
- Vá para a aba "Estatísticas"
- Veja emails enviados hoje
- Acompanhe limite diário
- Clique em "Atualizar Estatísticas"

## 📋 Formato do CSV

Seu arquivo deve ter estas colunas:
```csv
email,name,company,position
joao@empresa.com,João Silva,Empresa ABC,Gerente
maria@startup.com,Maria Santos,Startup XYZ,CEO
```

## 🔧 Personalização

Use estas variáveis nos emails:
- `{nome}` - Nome do contato
- `{email}` - Email do contato  
- `{empresa}` - Empresa do contato
- `{cargo}` - Cargo do contato

## 💡 Dicas

1. **Sempre teste primeiro:** Use o modo teste antes de enviar em massa
2. **Personalize os emails:** Use as variáveis para tornar os emails mais relevantes
3. **Monitore os resultados:** Acompanhe as estatísticas regularmente
4. **Respeite os limites:** Configure adequadamente o limite diário

## 🆘 Problemas Comuns

**Erro ao importar CSV:**
- Verifique se o arquivo tem as colunas corretas
- Confirme que o arquivo é um CSV válido

**Emails não sendo enviados:**
- Verifique se há contatos importados
- Confirme as configurações do Mailgun
- Verifique o limite diário

**Interface não carrega:**
- Confirme que a aplicação está rodando
- Verifique se a porta 5000 está livre
- Consulte os logs no terminal

## 📞 Suporte

Se precisar de ajuda:
1. Verifique os logs no terminal onde executou `python app.py`
2. Confirme que todas as dependências estão instaladas
3. Verifique se o arquivo `.env` está configurado corretamente
