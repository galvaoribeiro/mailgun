#!/usr/bin/env python3
"""
Exemplo de uso do sistema de Cold Emails com Mailgun

Este arquivo demonstra como usar todas as funcionalidades do sistema.
"""

import requests
import json
import time
from email_service import EmailService

def main():
    """Exemplo completo de uso do sistema"""
    
    # Inicializa o serviço
    email_service = EmailService()
    
    print("🚀 Sistema de Cold Emails - Exemplo de Uso")
    print("=" * 50)
    
    # 1. Adicionar contatos manualmente
    print("\n1. 📧 Adicionando contatos...")
    contacts = [
        {
            'email': 'ronaldo_fab@hotmail.com',
            'name': 'ronaldo ribeiro',
            'company': 'Contabilidade Ronaldo',
            'position': 'CEO',
            'source': 'manual'
        }
    ]
    
    for contact in contacts:
        email_service.db.add_contact(**contact)
    
    print(f"✅ {len(contacts)} contatos adicionados")
    
    # 2. Criar uma campanha
    print("\n2. 📋 Criando campanha...")
    campaign_id = email_service.create_campaign(
        name="Oferta Especial - Auditor Simples",
        subject_template="Olá {name}, oferta exclusiva para {company}",
        body_template="""
Olá {name},

Espero que esteja bem! Vi que você é {position} na {company} e gostaria de apresentar uma solução que pode ajudar sua empresa a economizar tempo e dinheiro.

A Auditor Simples oferece:
✅ Automação completa de processos
✅ Economia de até 40% em tempo
✅ Relatórios em tempo real
✅ Suporte especializado

Gostaria de agendar uma demonstração gratuita de 15 minutos?

Aguardo seu retorno!

Atenciosamente,
Equipe Auditor Simples
contato@auditor-simples.com
        """.strip()
    )
    
    print(f"✅ Campanha criada com ID: {campaign_id}")
    
    # 3. Enviar campanha em modo teste
    print("\n3. 📤 Enviando campanha em modo teste...")
    result = email_service.send_campaign(
        campaign_id=campaign_id,
        test_mode=True  # Envia apenas para os primeiros 5 contatos
    )
    
    if result['success']:
        print(f"✅ Campanha enviada com sucesso!")
        print(f"   📊 Total de contatos: {result['total_contacts']}")
        print(f"   📧 Emails enviados: {result['successful_sends']}")
    else:
        print(f"❌ Erro ao enviar campanha: {result['error']}")
    
    # 4. Verificar estatísticas
    print("\n4. 📊 Verificando estatísticas...")
    stats = email_service.get_campaign_stats(campaign_id)
    print(f"   📈 Taxa de abertura: {stats['open_rate']:.1f}%")
    print(f"   🖱️  Taxa de clique: {stats['click_rate']:.1f}%")
    print(f"   📧 Total enviado: {stats['total_sent']}")
    
    # 5. Verificar estatísticas diárias
    print("\n5. 📅 Estatísticas do dia...")
    daily_stats = email_service.get_daily_stats()
    print(f"   📧 Enviados hoje: {daily_stats['sent_today']}")
    print(f"   📖 Abertos hoje: {daily_stats['opened_today']}")
    print(f"   🖱️  Clicados hoje: {daily_stats['clicked_today']}")
    print(f"   📊 Quota restante: {daily_stats['remaining_quota']}")
    
    print("\n🎉 Exemplo concluído com sucesso!")

def example_with_api():
    """Exemplo usando a API REST"""
    
    base_url = "http://localhost:5000"
    
    print("\n🌐 Exemplo usando API REST")
    print("=" * 30)
    
    # 1. Verificar saúde da API
    response = requests.get(f"{base_url}/health")
    if response.status_code == 200:
        health = response.json()
        print(f"✅ API saudável - Pode enviar emails: {health['can_send_emails']}")
    else:
        print("❌ API não está respondendo")
        return
    
    # 2. Criar campanha via API
    campaign_data = {
        "name": "Campanha via API",
        "subject": "Oferta especial para {name}",
        "body": "Olá {name}, temos uma oferta especial para você!"
    }
    
    response = requests.post(f"{base_url}/campaigns", json=campaign_data)
    if response.status_code == 200:
        result = response.json()
        campaign_id = result['campaign_id']
        print(f"✅ Campanha criada via API - ID: {campaign_id}")
        
        # 3. Enviar campanha via API
        send_data = {
            "test_mode": True,
            "async_mode": False
        }
        
        response = requests.post(f"{base_url}/campaigns/{campaign_id}/send", json=send_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Campanha enviada via API - {result['successful_sends']} emails")
        else:
            print(f"❌ Erro ao enviar campanha: {response.text}")
    
    # 4. Verificar estatísticas via API
    response = requests.get(f"{base_url}/stats/daily")
    if response.status_code == 200:
        stats = response.json()['stats']
        print(f"📊 Estatísticas via API - Enviados hoje: {stats['sent_today']}")

if __name__ == "__main__":
    # Executa exemplo direto
    main()
    
    # Executa exemplo via API (descomente se quiser testar)
    # example_with_api()
