# 👁️ Visualização de Campanhas

## Funcionalidade Implementada

A aplicação agora permite visualizar o conteúdo completo das campanhas existentes através de um modal elegante e interativo.

## 🚀 Como Usar

1. **Acesse a aba "Campanhas"** na interface principal
2. **Clique no botão "👁️ Visualizar"** de qualquer campanha existente
3. **Visualize o conteúdo completo** da campanha no modal que se abre

## ✨ Recursos do Modal

### 📋 Informações da Campanha
- Nome da campanha
- ID único
- Data de criação

### 📧 Conteúdo do Email
- **Assunto**: Exibido em destaque
- **Corpo**: Conteúdo completo com formatação preservada
- **Variáveis**: Lista de variáveis disponíveis para personalização

### 📊 Estatísticas (se disponíveis)
- Emails enviados
- Emails entregues
- Emails retornados (bounced)
- Emails abertos

### 🔧 Ações Disponíveis
- **🚀 Enviar Campanha**: Redireciona para a aba de envio com a campanha pré-selecionada
- **Fechar**: Fecha o modal

## 🎯 Variáveis Disponíveis

As seguintes variáveis podem ser usadas no assunto e corpo dos emails:

| Variável | Descrição |
|----------|-----------|
| `{nome}` | Nome do destinatário |
| `{email}` | Email do destinatário |
| `{empresa}` | Nome da empresa |
| `{cargo}` | Cargo/função |
| `{telefone}` | Número de telefone |
| `{linkedin}` | Perfil do LinkedIn |

## ⌨️ Controles de Navegação

- **Clique fora do modal**: Fecha o modal
- **Tecla ESC**: Fecha o modal
- **Botão X**: Fecha o modal

## 📱 Design Responsivo

O modal se adapta automaticamente a diferentes tamanhos de tela:
- **Desktop**: Modal com largura máxima de 800px
- **Mobile**: Modal ocupa 95% da tela com espaçamento otimizado

## 🔧 Arquivos Modificados

### Backend (`app.py`)
```python
@app.route('/campaigns/<int:campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Retorna uma campanha específica"""
```

### Frontend (`static/js/app.js`)
- Função `viewCampaign(campaignId)`
- Função `sendCampaignFromView(campaignId)`
- Função `closeModal()`
- Event listeners para tecla ESC

### Estilos (`static/css/style.css`)
- Estilos do modal de visualização
- Estilos das estatísticas da campanha
- Estilos responsivos para mobile

## 🧪 Como Testar

1. **Inicie a aplicação**:
   ```bash
   python app.py
   ```

2. **Acesse a interface**:
   ```
   http://localhost:5000
   ```

3. **Navegue para Campanhas**:
   - Clique na aba "Campanhas"
   - Clique em "👁️ Visualizar" de uma campanha existente

4. **Teste as funcionalidades**:
   - Visualize o conteúdo
   - Teste o fechamento (ESC, clique fora, botão X)
   - Use o botão "Enviar Campanha"

## 🎨 Personalização

O modal pode ser facilmente personalizado editando:
- **Cores**: Modifique as variáveis CSS no arquivo `style.css`
- **Layout**: Ajuste os estilos das classes `.campaign-view-*`
- **Funcionalidades**: Modifique as funções JavaScript em `app.js`

## 🔍 Solução de Problemas

### Modal não abre
- Verifique se a rota `/campaigns/<id>` está funcionando
- Confirme se o JavaScript está sendo carregado
- Verifique o console do navegador para erros

### Estatísticas não aparecem
- A API de estatísticas pode não estar implementada
- Verifique se a rota `/campaigns/<id>/stats` existe
- Confirme se há dados de estatísticas no banco

### Problemas de responsividade
- Teste em diferentes tamanhos de tela
- Verifique se os media queries estão funcionando
- Confirme se o viewport meta tag está presente

## 📈 Próximas Melhorias

- [ ] Edição inline de campanhas
- [ ] Histórico de envios
- [ ] Preview com dados reais
- [ ] Exportação de campanhas
- [ ] Templates pré-definidos
- [ ] A/B testing de campanhas

---

**Implementado com ❤️ para melhorar a experiência do usuário na gestão de campanhas de email.**
