#!/usr/bin/env python3
"""
Script de migração para atualizar o banco de dados existente
e adicionar suporte ao sistema de lotes de contatos.
"""

import sqlite3
from datetime import datetime

def migrate_database():
    """Executa a migração do banco de dados"""
    db_path = 'cold_emails.db'
    
    print("🔄 Iniciando migração do banco de dados...")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Adiciona coluna batch_id se não existir
            print("📝 Adicionando coluna batch_id...")
            try:
                cursor.execute('ALTER TABLE contacts ADD COLUMN batch_id TEXT')
                print("✅ Coluna batch_id adicionada com sucesso")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print("ℹ️ Coluna batch_id já existe")
                else:
                    print(f"⚠️ Erro ao adicionar coluna batch_id: {e}")
            
            # 2. Atualiza contatos existentes com um batch_id padrão
            print("📝 Atualizando contatos existentes...")
            cursor.execute('SELECT COUNT(*) FROM contacts WHERE batch_id IS NULL')
            existing_contacts = cursor.fetchone()[0]
            
            if existing_contacts > 0:
                # Cria um batch_id para contatos existentes
                default_batch_id = f"legacy_batch_{int(datetime.now().timestamp())}"
                
                cursor.execute('''
                    UPDATE contacts 
                    SET batch_id = ?, updated_at = ? 
                    WHERE batch_id IS NULL
                ''', (default_batch_id, datetime.now()))
                
                print(f"✅ {existing_contacts} contatos existentes migrados para o lote {default_batch_id}")
            else:
                print("ℹ️ Nenhum contato existente para migrar")
            
            # 3. Verifica se há contatos duplicados por email e resolve conflitos
            print("🔍 Verificando contatos duplicados...")
            cursor.execute('''
                SELECT email, COUNT(*) as count, GROUP_CONCAT(id) as ids
                FROM contacts 
                GROUP BY email 
                HAVING COUNT(*) > 1
            ''')
            
            duplicates = cursor.fetchall()
            if duplicates:
                print(f"⚠️ Encontrados {len(duplicates)} emails duplicados")
                
                for email, count, ids in duplicates:
                    id_list = [int(id_str) for id_str in ids.split(',')]
                    # Mantém o contato mais recente e remove os outros
                    keep_id = max(id_list)
                    remove_ids = [id for id in id_list if id != keep_id]
                    
                    if remove_ids:
                        placeholders = ','.join(['?' for _ in remove_ids])
                        cursor.execute(f'DELETE FROM contacts WHERE id IN ({placeholders})', remove_ids)
                        print(f"✅ Removidos {len(remove_ids)} contatos duplicados para {email}")
            else:
                print("✅ Nenhum contato duplicado encontrado")
            
            # 4. Cria índices para melhorar performance
            print("📝 Criando índices...")
            try:
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_batch_id ON contacts(batch_id)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_status ON contacts(status)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email)')
                print("✅ Índices criados com sucesso")
            except Exception as e:
                print(f"⚠️ Erro ao criar índices: {e}")
            
            # 5. Verifica integridade dos dados
            print("🔍 Verificando integridade dos dados...")
            cursor.execute('SELECT COUNT(*) FROM contacts')
            total_contacts = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM contacts WHERE batch_id IS NOT NULL')
            contacts_with_batch = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM contacts WHERE status = "active"')
            active_contacts = cursor.fetchone()[0]
            
            print(f"📊 Estatísticas da migração:")
            print(f"   - Total de contatos: {total_contacts}")
            print(f"   - Contatos com batch_id: {contacts_with_batch}")
            print(f"   - Contatos ativos: {active_contacts}")
            
            conn.commit()
            print("✅ Migração concluída com sucesso!")
            
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        return False
    
    return True

if __name__ == '__main__':
    migrate_database()
