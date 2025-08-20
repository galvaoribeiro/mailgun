#!/usr/bin/env python3
"""
Script de teste para verificar se a configuração do sistema está correta.
Execute este script antes de usar o sistema pela primeira vez.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Testa se todas as dependências estão instaladas"""
    print("🔍 Testando imports...")
    
    try:
        import flask
        print("✅ Flask OK")
    except ImportError:
        print("❌ Flask não encontrado. Execute: pip install flask")
        return False
    except Exception as e:
        print(f"❌ Erro ao importar Flask: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests OK")
    except ImportError:
        print("❌ Requests não encontrado. Execute: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Erro ao importar Requests: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas OK")
    except ImportError:
        print("❌ Pandas não encontrado. Execute: pip install pandas")
        return False
    except Exception as e:
        print(f"❌ Erro ao importar Pandas: {e}")
        print("💡 Execute: python fix_dependencies.py para corrigir")
        return False
    
    try:
        from flask_cors import CORS
        print("✅ Flask-CORS OK")
    except ImportError:
        print("❌ Flask-CORS não encontrado. Execute: pip install flask-cors")
        return False
    except Exception as e:
        print(f"❌ Erro ao importar Flask-CORS: {e}")
        return False
    
    return True

def test_config():
    """Testa se as configurações estão corretas"""
    print("\n🔧 Testando configurações...")
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica variáveis obrigatórias
    required_vars = ['MAILGUN_API_KEY', 'MAILGUN_DOMAIN']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis de ambiente faltando: {', '.join(missing_vars)}")
        print("📝 Crie um arquivo .env baseado no env_example.txt")
        return False
    
    print("✅ Configurações OK")
    return True

def test_modules():
    """Testa se os módulos do sistema podem ser importados"""
    print("\n📦 Testando módulos do sistema...")
    
    try:
        from config import Config
        print("✅ Config OK")
    except Exception as e:
        print(f"❌ Erro ao importar Config: {e}")
        return False
    
    try:
        from database import Database
        print("✅ Database OK")
    except Exception as e:
        print(f"❌ Erro ao importar Database: {e}")
        return False
    
    try:
        from mailgun_client import MailgunClient
        print("✅ MailgunClient OK")
    except Exception as e:
        print(f"❌ Erro ao importar MailgunClient: {e}")
        return False
    
    try:
        from email_service import EmailService
        print("✅ EmailService OK")
    except Exception as e:
        print(f"❌ Erro ao importar EmailService: {e}")
        return False
    
    return True

def test_database():
    """Testa se o banco de dados pode ser criado"""
    print("\n🗄️ Testando banco de dados...")
    
    try:
        from database import Database
        db = Database('test.db')
        print("✅ Banco de dados criado com sucesso")
        
        # Testa operações básicas
        contact_id = db.add_contact(
            email='teste@exemplo.com',
            name='Teste',
            company='Empresa Teste',
            position='Testador'
        )
        print(f"✅ Contato adicionado com ID: {contact_id}")
        
        contacts = db.get_contacts()
        print(f"✅ Contatos recuperados: {len(contacts)}")
        
        # Remove arquivo de teste
        import os
        if os.path.exists('test.db'):
            os.remove('test.db')
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_mailgun_connection():
    """Testa se a conexão com o Mailgun está funcionando"""
    print("\n📧 Testando conexão com Mailgun...")
    
    try:
        from mailgun_client import MailgunClient
        client = MailgunClient()
        
        # Testa validação de email
        result = client.validate_email('teste@exemplo.com')
        print("✅ Validação de email OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com Mailgun: {e}")
        print("💡 Verifique se sua API_KEY está correta")
        return False

def test_flask_app():
    """Testa se a aplicação Flask pode ser iniciada"""
    print("\n🌐 Testando aplicação Flask...")
    
    try:
        from app import app
        print("✅ Aplicação Flask OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro na aplicação Flask: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Teste de Configuração - Sistema de Cold Emails")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configurações", test_config),
        ("Módulos", test_modules),
        ("Banco de Dados", test_database),
        ("Conexão Mailgun", test_mailgun_connection),
        ("Aplicação Flask", test_flask_app)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O sistema está pronto para uso.")
        print("\n📝 Próximos passos:")
        print("1. Execute: python app.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Execute: python example_usage.py")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique os erros acima.")
        print("\n💡 Dicas:")
        print("- Execute: python fix_dependencies.py para corrigir problemas de compatibilidade")
        print("- Verifique se todas as dependências estão instaladas")
        print("- Confirme se o arquivo .env está configurado corretamente")
        print("- Verifique se sua API_KEY do Mailgun está válida")

if __name__ == "__main__":
    main()
