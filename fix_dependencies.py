#!/usr/bin/env python3
"""
Script para corrigir problemas de dependências do sistema de cold emails.
Execute este script se encontrar erros de compatibilidade.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} - Erro")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

def main():
    """Corrige problemas de dependências"""
    print("🔧 Corrigindo Dependências - Sistema de Cold Emails")
    print("=" * 60)
    
    # Verifica se pip está disponível
    if not run_command("pip --version", "Verificando pip"):
        print("❌ pip não encontrado. Instale o Python e pip primeiro.")
        return
    
    # Remove versões conflitantes
    print("\n🧹 Removendo versões conflitantes...")
    packages_to_remove = [
        "pandas",
        "numpy",
        "flask",
        "requests",
        "python-dotenv",
        "flask-cors"
    ]
    
    for package in packages_to_remove:
        run_command(f"pip uninstall {package} -y", f"Removendo {package}")
    
    # Instala versões compatíveis
    print("\n📦 Instalando versões compatíveis...")
    
    # Instala numpy primeiro (dependência base)
    run_command("pip install numpy==1.24.3", "Instalando numpy")
    
    # Instala pandas com versão compatível
    run_command("pip install pandas==2.0.3", "Instalando pandas")
    
    # Instala outras dependências
    dependencies = [
        "Flask==2.3.3",
        "requests==2.31.0", 
        "python-dotenv==1.0.0",
        "schedule==1.2.0",
        "flask-cors==4.0.0"
    ]
    
    for dep in dependencies:
        run_command(f"pip install {dep}", f"Instalando {dep}")
    
    # Verifica instalação
    print("\n🔍 Verificando instalação...")
    
    test_imports = [
        "import numpy",
        "import pandas", 
        "import flask",
        "import requests",
        "from dotenv import load_dotenv",
        "from flask_cors import CORS"
    ]
    
    for import_test in test_imports:
        if run_command(f"python -c '{import_test}'", f"Testando {import_test}"):
            print(f"✅ {import_test} - OK")
        else:
            print(f"❌ {import_test} - FALHOU")
    
    print("\n" + "=" * 60)
    print("🎉 Correção de dependências concluída!")
    print("\n📝 Próximos passos:")
    print("1. Execute: python test_setup.py")
    print("2. Se tudo estiver OK, execute: python app.py")
    print("3. Acesse: http://localhost:5000")

if __name__ == "__main__":
    main()
