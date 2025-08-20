# 🔧 Guia de Solução de Problemas

Este guia ajuda a resolver problemas comuns do sistema de cold emails.

## 🚨 Erro: `numpy.dtype size changed, may indicate binary incompatibility`

### Problema
```
❌ Erro inesperado em Imports: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
```

### Causa
Este erro ocorre quando há conflitos entre versões de bibliotecas, especialmente:
- NumPy e Pandas com versões incompatíveis
- Bibliotecas compiladas com diferentes versões do Python
- Conflitos entre versões do sistema e do ambiente virtual

### Solução Rápida

#### Opção 1: Script Automático (Recomendado)
```bash
python fix_dependencies.py
```

#### Opção 2: Correção Manual
```bash
# 1. Remover versões conflitantes
pip uninstall pandas numpy flask requests python-dotenv flask-cors -y

# 2. Instalar versões compatíveis
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install Flask==2.3.3
pip install requests==2.31.0
pip install python-dotenv==1.0.0
pip install schedule==1.2.0
pip install flask-cors==4.0.0
```

#### Opção 3: Ambiente Virtual Limpo
```bash
# 1. Criar novo ambiente virtual
python -m venv venv_clean

# 2. Ativar ambiente
# Windows:
venv_clean\Scripts\activate
# Linux/Mac:
source venv_clean/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt
```

### Verificação
Após a correção, execute:
```bash
python test_setup.py
```

## 🔍 Outros Problemas Comuns

### Erro: `ModuleNotFoundError: No module named 'flask'`
**Solução:**
```bash
pip install Flask==2.3.3
```

### Erro: `ModuleNotFoundError: No module named 'requests'`
**Solução:**
```bash
pip install requests==2.31.0
```

### Erro: `ModuleNotFoundError: No module named 'pandas'`
**Solução:**
```bash
pip install pandas==2.0.3
```

### Erro: `MAILGUN_API_KEY é obrigatória`
**Solução:**
1. Crie um arquivo `.env` baseado no `env_example.txt`
2. Adicione sua API key do Mailgun:
```bash
MAILGUN_API_KEY=sua_api_key_aqui
MAILGUN_DOMAIN=mg.auditor-simples.com
```

### Erro: `sqlite3.OperationalError: no such table`
**Solução:**
O banco de dados será criado automaticamente. Se persistir:
```bash
# Remover banco corrompido
rm cold_emails.db

# Executar novamente
python app.py
```

### Erro: `requests.exceptions.ConnectionError`
**Solução:**
- Verifique sua conexão com a internet
- Confirme se a API key do Mailgun está correta
- Verifique se o domínio está ativo no Mailgun

## 🛠️ Comandos Úteis

### Verificar Versões Instaladas
```bash
pip list | grep -E "(numpy|pandas|flask|requests)"
```

### Verificar Ambiente Python
```bash
python --version
pip --version
```

### Limpar Cache do Pip
```bash
pip cache purge
```

### Reinstalar Todas as Dependências
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📋 Checklist de Diagnóstico

Antes de reportar um problema, verifique:

- [ ] Python 3.7+ instalado
- [ ] Pip atualizado
- [ ] Ambiente virtual ativado (se usando)
- [ ] Arquivo `.env` configurado
- [ ] API key do Mailgun válida
- [ ] Domínio do Mailgun ativo
- [ ] Conexão com internet funcionando

## 🆘 Ainda com Problemas?

Se os problemas persistirem:

1. **Execute o script de correção:**
   ```bash
   python fix_dependencies.py
   ```

2. **Verifique o ambiente:**
   ```bash
   python test_setup.py
   ```

3. **Consulte os logs:**
   ```bash
   python app.py
   ```

4. **Verifique a documentação do Mailgun:**
   - [Mailgun Documentation](https://documentation.mailgun.com/)
   - [API Reference](https://documentation.mailgun.com/en/latest/api_reference.html)

## 📞 Suporte

Para problemas específicos:
1. Execute `python test_setup.py` e compartilhe o resultado completo
2. Verifique se seguiu todos os passos do `QUICKSTART.md`
3. Confirme se sua API key do Mailgun está funcionando

---

**💡 Dica:** Sempre execute `python fix_dependencies.py` primeiro se encontrar problemas de compatibilidade!
