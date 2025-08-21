# Sistema de Lotes de Contatos - Cold Email Service

## Visão Geral

O sistema de lotes de contatos foi implementado para resolver o problema de contatos antigos sendo enviados repetidamente em campanhas. Agora, cada importação de CSV cria um novo lote, e apenas os contatos do lote ativo são enviados em campanhas.

## Como Funciona

### 1. **Importação de Contatos**
- Cada vez que você importa um arquivo CSV, um novo lote é criado automaticamente
- O sistema gera um ID único para o lote (ex: `batch_a1b2c3d4_1703123456`)
- **Contatos antigos são automaticamente desativados** quando novos são importados
- Apenas os contatos do lote mais recente ficam ativos

### 2. **Controle de Lotes**
- **Lote Ativo**: Contatos que serão enviados em campanhas
- **Lotes Inativos**: Contatos que não serão enviados (mantidos para histórico)
- Você pode ativar/desativar lotes manualmente através da interface

### 3. **Vantagens**
- ✅ **Não envia contatos duplicados** em campanhas
- ✅ **Controle total** sobre quais contatos estão ativos
- ✅ **Histórico completo** de todas as importações
- ✅ **Performance melhorada** com índices no banco de dados

## Como Usar

### **Passo 1: Executar Migração**
Se você já tem contatos no banco, execute primeiro:

```bash
python migrate_database.py
```

### **Passo 2: Importar Novos Contatos**
1. Vá para a aba "📁 Upload CSV"
2. Selecione seu arquivo CSV
3. Clique em "📥 Importar Contatos"
4. O sistema criará automaticamente um novo lote

### **Passo 3: Gerenciar Lotes**
1. Vá para a aba "📦 Gerenciar Lotes"
2. Visualize todos os lotes importados
3. **Ative** o lote que deseja usar
4. **Desative** lotes antigos se necessário

### **Passo 4: Enviar Campanhas**
1. Vá para a aba "🚀 Enviar"
2. Selecione sua campanha
3. Apenas contatos do lote ativo serão enviados

## Estrutura do Banco de Dados

### Tabela `contacts`
```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    company TEXT,
    position TEXT,
    source TEXT,
    status TEXT DEFAULT 'active',
    batch_id TEXT,                    -- NOVO: ID do lote
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Campos Importantes
- `batch_id`: Identifica a qual lote o contato pertence
- `status`: 'active', 'inactive', 'bounced'
- `created_at`: Quando o contato foi criado
- `updated_at`: Quando foi atualizado pela última vez

## API Endpoints

### **GET /contacts/batches**
Lista todos os lotes de contatos

### **POST /contacts/batches/{batch_id}/activate**
Ativa um lote específico (desativa todos os outros)

### **POST /contacts/batches/{batch_id}/deactivate**
Desativa um lote específico

### **GET /contacts/batches/{batch_id}**
Retorna contatos de um lote específico

### **PUT /contacts/{contact_id}/status**
Atualiza status de um contato individual

### **DELETE /contacts/{contact_id}**
Exclui um contato específico

## Exemplos de Uso

### **Cenário 1: Primeira Importação**
```bash
# Importa contatos do CSV
curl -X POST /contacts/import -F "file=@contatos.csv"
# Resultado: Lote criado automaticamente e ativado
```

### **Cenário 2: Segunda Importação**
```bash
# Importa novos contatos
curl -X POST /contacts/import -F "file=@novos_contatos.csv"
# Resultado: 
# - Novo lote criado e ativado
# - Lote anterior automaticamente desativado
```

### **Cenário 3: Ativar Lote Antigo**
```bash
# Ativa um lote específico
curl -X POST /contacts/batches/batch_abc123/activate
# Resultado: Todos os outros lotes são desativados
```

## Troubleshooting

### **Problema: Contatos antigos ainda sendo enviados**
**Solução**: Verifique se o lote correto está ativo na aba "Gerenciar Lotes"

### **Problema: Erro ao importar CSV**
**Solução**: Execute o script de migração primeiro

### **Problema: Performance lenta**
**Solução**: Os índices são criados automaticamente durante a migração

## Migração de Dados Existentes

O script `migrate_database.py` faz automaticamente:

1. ✅ Adiciona coluna `batch_id` se não existir
2. ✅ Migra contatos existentes para um lote "legacy"
3. ✅ Remove contatos duplicados por email
4. ✅ Cria índices para melhorar performance
5. ✅ Verifica integridade dos dados

## Monitoramento

### **Estatísticas Importantes**
- Total de contatos por lote
- Contatos ativos vs. inativos
- Histórico de importações
- Performance de envio

### **Logs**
- Todas as operações são logadas
- Erros são capturados e exibidos na interface
- Histórico completo de mudanças de status

## Próximos Passos

### **Funcionalidades Futuras**
- [ ] Backup automático de lotes
- [ ] Agendamento de ativação de lotes
- [ ] Relatórios detalhados por lote
- [ ] Integração com CRM
- [ ] Validação de emails em lote

### **Melhorias de Performance**
- [ ] Cache de contatos ativos
- [ ] Paginação de resultados
- [ ] Filtros avançados
- [ ] Exportação de dados

---

**Nota**: Este sistema resolve o problema principal de contatos duplicados sendo enviados, garantindo que apenas os contatos mais recentes (do lote ativo) sejam utilizados em campanhas.
