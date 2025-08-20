#!/usr/bin/env python3
"""
Script para testar as configurações do Mailgun e identificar problemas
"""

import os
from config import Config
from mailgun_client import MailgunClient
from database import Database

def test_config():
    """Testa as configurações básicas"""
    print("🔧 Testando configurações...")
    print("=" * 40)
    
    # Verifica variáveis de ambiente
    print(f"MAILGUN_API_KEY: {'✅ Configurada' if Config.MAILGUN_API_KEY else '❌ Não configurada'}")
    print(f"MAILGUN_DOMAIN: {Config.MAILGUN_DOMAIN}")
    print(f"BASE_URL: {Config.BASE_URL}")
    print(f"FROM_EMAIL: {Config.FROM_EMAIL}")
    
    if not Config.MAILGUN_API_KEY:
        print("\n❌ MAILGUN_API_KEY não está configurada!")
        print("Crie um arquivo .env com as seguintes variáveis:")
        print("MAILGUN_API_KEY=sua_api_key_aqui")
        print("MAILGUN_DOMAIN=seu_dominio.mailgun.org")
        return False
    
    return True

def test_mailgun_connection():
    """Testa a conexão com o Mailgun"""
    print("\n🌐 Testando conexão com Mailgun...")
    print("=" * 40)
    
    try:
        mailgun = MailgunClient()
        
        # Testa a API de domínios
        response = mailgun.session.get(f'{Config.BASE_URL}/domains')
        
        if response.status_code == 200:
            print("✅ Conexão com Mailgun estabelecida")
            domains = response.json().get('items', [])
            print(f"📧 Domínios configurados: {len(domains)}")
            for domain in domains:
                print(f"   - {domain.get('name')} ({domain.get('state')})")
            return True
        else:
            print(f"❌ Erro na conexão: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com Mailgun: {e}")
        return False

def test_database():
    """Testa o banco de dados"""
    print("\n🗄️ Testando banco de dados...")
    print("=" * 40)
    
    try:
        db = Database()
        
        # Verifica se as tabelas existem
        with db.db_path as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
        print(f"✅ Banco de dados conectado: {db.db_path}")
        print(f"📋 Tabelas encontradas: {', '.join(tables)}")
        
        # Conta contatos
        contacts = db.get_contacts()
        print(f"👥 Total de contatos ativos: {len(contacts)}")
        
        if contacts:
            print("📧 Contatos encontrados:")
            for contact in contacts[:3]:  # Mostra apenas os primeiros 3
                print(f"   - {contact['email']} ({contact['name']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_email_sending():
    """Testa o envio de email"""
    print("\n📧 Testando envio de email...")
    print("=" * 40)
    
    try:
        mailgun = MailgunClient()
        
        # Testa envio para um email de teste
        test_email = "test@example.com"  # Email de teste
        
        result = mailgun.send_single_email(
            to_email=test_email,
            subject="Teste de Configuração - Sistema Cold Emails",
            body="Este é um teste de configuração do sistema de cold emails.",
            tag="test-config"
        )
        
        if result['success']:
            print("✅ Email de teste enviado com sucesso!")
            print(f"📧 Message ID: {result['message_id']}")
            return True
        else:
            print(f"❌ Erro ao enviar email: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar envio: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Teste de Configuração do Sistema de Cold Emails")
    print("=" * 60)
    
    # Testa configurações
    if not test_config():
        return
    
    # Testa conexão com Mailgun
    if not test_mailgun_connection():
        return
    
    # Testa banco de dados
    if not test_database():
        return
    
    # Testa envio de email (opcional)
    print("\n❓ Deseja testar o envio de email? (s/n): ", end="")
    response = input().lower()
    if response == 's':
        test_email_sending()
    
    print("\n✅ Todos os testes básicos concluídos!")

if __name__ == "__main__":
    main()
