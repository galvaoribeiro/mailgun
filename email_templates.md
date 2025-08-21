# 📧 Templates de Cold Email

Este arquivo contém exemplos de templates eficazes para cold emails que você pode usar como base para suas campanhas.

## 🎯 Como Funcionam as Tags de Personalização

**IMPORTANTE**: O sistema converte automaticamente as tags do formato `{name}` para o formato `%recipient.name%` que o Mailgun entende. Cada contato receberá um email personalizado com suas informações específicas.

### Variáveis Disponíveis
- `{name}` - Nome do contato (ex: João Silva)
- `{company}` - Nome da empresa (ex: TechCorp Ltda)
- `{position}` - Cargo/função (ex: Gerente de Marketing)
- `{source}` - Origem do contato (ex: LinkedIn, CSV import)

### Exemplo de Funcionamento
Se você tiver um template com:
```
Olá {name},
Como {position} na {company}, você deve enfrentar desafios específicos...
```

E enviar para 3 contatos:
1. João Silva, CEO, TechCorp
2. Maria Santos, Marketing, Inovação Ltda
3. Pedro Costa, Vendas, VendasPro

Cada um receberá:
- João: "Olá João Silva, Como CEO na TechCorp, você deve enfrentar desafios específicos..."
- Maria: "Olá Maria Santos, Como Marketing na Inovação Ltda, você deve enfrentar desafios específicos..."
- Pedro: "Olá Pedro Costa, Como Vendas na VendasPro, você deve enfrentar desafios específicos..."

## 🎯 Template 1: Apresentação de Produto/Serviço

**Assunto:** `Olá {name}, solução para {company} economizar tempo e dinheiro`

**Corpo:**
```
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
```

## 🤝 Template 2: Networking/Parceria

**Assunto:** `{name}, parceria estratégica para {company}`

**Corpo:**
```
Olá {name},

Espero que esteja bem! Vi seu perfil e fiquei impressionado com o trabalho que vocês fazem na {company}.

Estou sempre buscando conectar com profissionais como você para trocar experiências e possivelmente identificar oportunidades de colaboração.

Você teria 15 minutos para uma conversa rápida na próxima semana?

Aguardo seu retorno!

Abraços,
[Seu Nome]
[Seu Email]
```

## 💼 Template 3: Oferta Especial

**Assunto:** `{name}, oferta exclusiva para {company} - 50% de desconto`

**Corpo:**
```
Olá {name},

Espero que esteja bem! Como {position} na {company}, sei que você entende a importância de otimizar processos.

Estou oferecendo uma oportunidade exclusiva para sua empresa: 50% de desconto em nossa solução de automação para os primeiros 3 meses.

Esta oferta é válida apenas até o final do mês e está limitada a 10 empresas.

Gostaria de saber mais detalhes?

Aguardo seu contato!

Atenciosamente,
[Seu Nome]
[Seu Email]
```

## 📊 Template 4: Case de Sucesso

**Assunto:** `{name}, como a {company} pode replicar este resultado`

**Corpo:**
```
Olá {name},

Espero que esteja bem! Recentemente ajudamos uma empresa similar à {company} a economizar R$ 50.000 por mês com nossa solução.

Como {position}, imagino que você esteja sempre buscando formas de otimizar custos e processos.

Gostaria de compartilhar como conseguimos esse resultado e ver se faz sentido para vocês?

Posso agendar uma conversa de 15 minutos?

Aguardo seu retorno!

Atenciosamente,
[Seu Nome]
[Seu Email]
```

## 🎁 Template 5: Recursos Gratuitos

**Assunto:** `{name}, material exclusivo para {company}`

**Corpo:**
```
Olá {name},

Espero que esteja bem! Como {position} na {company}, sei que você está sempre buscando se manter atualizado.

Criei um material exclusivo sobre "Como Otimizar Processos em 2024" que pode ser útil para vocês.

O material inclui:
📋 Checklist de otimização
📊 Templates de relatórios
🎯 Estratégias comprovadas

Gostaria que eu enviasse o material para você?

Aguardo seu retorno!

Atenciosamente,
[Seu Nome]
[Seu Email]
```

## 🔥 Template 6: Urgência/Scarcity

**Assunto:** `{name}, última chance - vaga limitada para {company}`

**Corpo:**
```
Olá {name},

Espero que esteja bem! Estou entrando em contato porque temos apenas 2 vagas restantes para nosso programa de consultoria exclusivo.

Como {position} na {company}, sei que vocês podem se beneficiar muito com nossa metodologia.

As vagas são limitadas porque trabalhamos com apenas 5 empresas por mês para garantir resultados excepcionais.

Gostaria de saber mais antes que as vagas acabem?

Aguardo seu contato urgente!

Atenciosamente,
[Seu Nome]
[Seu Email]
```

## 📈 Template 7: Análise Personalizada

**Assunto:** `{name}, análise gratuita para {company}`

**Corpo:**
```
Olá {name},

Espero que esteja bem! Analisei o perfil da {company} e identifiquei algumas oportunidades interessantes de otimização.

Como {position}, imagino que você esteja sempre buscando formas de melhorar os resultados da empresa.

Gostaria de compartilhar minha análise gratuita com você? Não leva mais de 15 minutos.

Posso agendar para esta semana?

Aguardo seu retorno!

Atenciosamente,
[Seu Nome]
[Seu Email]
```

## 💡 Dicas para Personalização

### Variáveis Disponíveis
- `{name}` - Nome do contato
- `{company}` - Nome da empresa
- `{position}` - Cargo/função
- `{source}` - Origem do contato

### Exemplos de Personalização
```python
# Template dinâmico
subject = f"Olá {name}, solução específica para {company}"
body = f"""
Olá {name},

Como {position} na {company}, você deve enfrentar desafios específicos...
"""
```

### Call-to-Actions Eficazes
- "Gostaria de agendar uma conversa de 15 minutos?"
- "Posso enviar mais detalhes?"
- "Você teria interesse em saber mais?"
- "Podemos conversar esta semana?"

### Assuntos que Funcionam
- Personalizados com nome/empresa
- Específicos e relevantes
- Criam curiosidade
- Oferecem valor claro
- Evitam spam words

## ⚠️ Boas Práticas

1. **Seja pessoal** - Use o nome e empresa
2. **Seja específico** - Mencione o cargo/função
3. **Ofereça valor** - O que o destinatário ganha?
4. **Seja breve** - Máximo 3-4 parágrafos
5. **Tenha um CTA claro** - O que você quer que ele faça?
6. **Teste diferentes versões** - A/B testing
7. **Monitore resultados** - Acompanhe taxas de resposta

## 📊 Métricas para Acompanhar

- **Taxa de abertura** - Ideal: 20-30%
- **Taxa de resposta** - Ideal: 2-5%
- **Taxa de clique** - Se incluir links
- **Taxa de bounce** - Manter abaixo de 5%

Lembre-se: Cold emails são sobre construir relacionamentos, não apenas vender!
