#!/usr/bin/env python3
"""
Script para corrigir as configurações do Mailgun
"""

import os
from config import Config

def fix_config():
    """Corrige as configurações do Mailgun"""
    print("🔧 Corrigindo configurações do Mailgun...")
    print("=" * 50)
    
    # Verifica se as variáveis de ambiente estão configuradas
    api_key = os.environ.get('MAILGUN_API_KEY')
    domain = os.environ.get('MAILGUN_DOMAIN')
    
    print(f"API Key configurada: {'✅' if api_key else '❌'}")
    print(f"Domínio configurado: {domain or '❌ Não configurado'}")
    
    if not api_key:
        print("\n❌ MAILGUN_API_KEY não está configurada!")
        print("Para configurar, execute no PowerShell:")
        print("$env:MAILGUN_API_KEY='sua_api_key_aqui'")
        print("$env:MAILGUN_DOMAIN='seu_dominio.mailgun.org'")
        return False
    
    if not domain:
        print("\n❌ MAILGUN_DOMAIN não está configurado!")
        print("Para configurar, execute no PowerShell:")
        print("$env:MAILGUN_DOMAIN='seu_dominio.mailgun.org'")
        return False
    
    # Testa a conexão com o domínio configurado
    print(f"\n🌐 Testando domínio: {domain}")
    
    import requests
    from requests.auth import HTTPBasicAuth
    
    base_url = f'https://api.mailgun.net/v3/{domain}'
    
    try:
        response = requests.get(
            f'{base_url}/domains',
            auth=HTTPBasicAuth('api', api_key)
        )
        
        if response.status_code == 200:
            print("✅ Domínio configurado corretamente!")
            return True
        else:
            print(f"❌ Erro com domínio {domain}: {response.status_code}")
            print(f"Resposta: {response.text}")
            
            # Sugere usar domínio sandbox
            print("\n💡 Sugestão: Use um domínio sandbox do Mailgun para testes")
            print("Exemplo: sandbox123456789.mailgun.org")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar domínio: {e}")
        return False

def create_env_file():
    """Cria um arquivo .env de exemplo"""
    print("\n📝 Criando arquivo .env de exemplo...")
    
    env_content = """# Configurações do Mailgun
# IMPORTANTE: Substitua pelos seus valores reais
MAILGUN_API_KEY=sua_api_key_aqui
MAILGUN_DOMAIN=seu_dominio.mailgun.org

# Configurações da aplicação
PORT=5000
DEBUG=True

# Configurações de envio
BATCH_SIZE=1000
DELAY_BETWEEN_BATCHES=60
MAX_EMAILS_PER_DAY=10000
"""
    
    try:
        with open('.env.example', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Arquivo .env.example criado!")
        print("📋 Copie este arquivo para .env e configure suas credenciais")
    except Exception as e:
        print(f"❌ Erro ao criar arquivo: {e}")

def main():
    """Executa a correção de configurações"""
    print("🚀 Correção de Configurações do Mailgun")
    print("=" * 50)
    
    if fix_config():
        print("\n✅ Configurações estão corretas!")
    else:
        print("\n❌ Configurações precisam ser corrigidas")
        create_env_file()
        
        print("\n📋 Próximos passos:")
        print("1. Obtenha sua API Key do Mailgun")
        print("2. Configure um domínio válido no Mailgun")
        print("3. Crie um arquivo .env com suas credenciais")
        print("4. Execute novamente o teste")

if __name__ == "__main__":
    main()
