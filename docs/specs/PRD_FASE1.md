# 📋 PRD - FASE 1 (MVP COM ALMA): IBPM CR APP
**Documento de Requisitos de Produto (Product Requirements Document)**
*Versão: 1.0 | Data: Setembro de 2026 | Responsável: Matheus Barbosa (Product Manager & Arquiteto)*

---

## 1. 🎯 A Visão e a Dor Real (The Problem Space)

### O Problema: A Solidão do "Membro Invisível"
Na maioria das igrejas, existe um grupo significativo de pessoas que chegam perto do início do culto, sentam-se nos últimos bancos, não conversam com ninguém e saem apressadas logo após o amém. Elas carregam pesos emocionais, crises familiares, ansiedade ou esgotamento, mas **o atrito da vulnerabilidade** é alto demais para irem até a frente do altar ou procurarem um pastor.

### A Oportunidade
Construir o primeiro aplicativo eclesial desenhado **para acolher quem não consegue falar**, integrando o coração pastoral à tecnologia que a igreja já possui (automação de cortes e pregações em vídeo).

---

## 2. 👤 Personas Centrais

### Persona 1: O "Membro Silencioso" (Lucas, 28 anos)
- **Perfil:** Introvertido, sobrecarregado pelo trabalho, vai aos cultos domingo à noite.
- **Dores:** Sente vergonha de expor suas fraquezas; não tem ânimo para digitar desabafos longos; sente-se invisível na multidão.
- **Necessidade no App:** Clicar em um único botão que expresse o que sente sem julgamentos e saber que alguém orou por ele.

### Persona 2: O Pastor / Intercessor (Pastor Carlos, 49 anos)
- **Perfil:** Cuidador de almas, agenda corrida, atende membros a semana inteira.
- **Dores:** Não consegue saber quem está sofrendo em silêncio no fundo da nave do templo; sobrecarregado com mensagens soltas no WhatsApp.
- **Necessidade no App:** Um painel simples na palma da mão (no próprio celular) para ver os pedidos confidenciais, orar e saber se a pessoa autorizou um contato discreto.

---

## 3. 🛡️ O Escopo Cirúrgico da Fase 1 (MVP)

A Fase 1 foca estritamente em **3 Pilares**, cortando qualquer funcionalidade secundária (sem Kids, sem LMS, sem Cifras):

```
┌────────────────────────────────────────────────────────────────────────┐
│                        IBPM CR - FASE 1 (MVP)                          │
├───────────────────┬───────────────────────────┬────────────────────────┤
│ 1. REFÚGIO        │ 2. CORTES & MENSAGENS     │ 3. COMUNIDADE & AVISOS │
│   SILENCIOSO      │                           │                        │
│ • Botões 1 clique │ • Feed vertical de cortes │ • Avisos da semana     │
│ • Sigilo e opção  │ • Resumo IA do sermão     │ • Agenda de cultos     │
│   de anonimato    │ • Player rápido embutido  │ • Modo Pastoral com    │
│ • Alerta pastoral │ • Link culto completo     │   login para gerenciar │
└───────────────────┴───────────────────────────┴────────────────────────┘
```

---

## 4. 📱 Especificação Detalhada das Telas (User Stories & Critérios de Aceite)

### Tela 1: 🕊️ O Refúgio Silencioso (Coração do App)
* **Objetivo:** Zero fricção de digitação.
* **Componentes:**
  - Título acolhedor: *"Como está o seu coração hoje?"*
  - **Botões Rápidos de Sentimento:**
    1. 🔘 *"Estou cansado e não sei explicar o que sinto."*
    2. 🔘 *"O peito está pesado hoje, só peço uma oração em silêncio."*
    3. 🔘 *"Me sinto invisível e sozinho no meio da multidão."*
    4. 🔘 *"Preciso apenas de paz para conseguir descansar hoje."*
    5. 🔘 *"Outro motivo / Quero escrever uma linha..."* (campo opcional curto).
  - **Seletor de Privacidade:**
    - [x] *Totalmente Anônimo (Ninguém saberá quem enviou)*.
    - [ ] *Pode me procurar discretamente (Informa WhatsApp/Nome)*.
  - **Ação:** Botão *"Pedir Oração Agora"*.
  - **Feedback Imediato (Critério de Aceite):** Ao clicar, exibe animação suave e a mensagem: *"Seu pedido chegou ao coração da liderança. Você não está sozinho. Uma oração está sendo levantada por você."*

### Tela 2: 🎬 Mensagens & Cortes Virais
* **Objetivo:** Consumir a palavra de Deus no formato moderno de vídeos curtos.
* **Componentes:**
  - Carrossel ou feed vertical dos cortes gerados pela automação (`ibpmcr-automation-system`).
  - Card com Título da Mensagem, Pregador, Data e Versículo-chave.
  - Resumo de 3 linhas gerado por IA sobre o sermão de domingo.
  - Botão para assistir o culto completo no YouTube.

### Tela 3: 📅 Comunidade & Avisos
* **Objetivo:** Manter a igreja conectada à agenda semanal.
* **Componentes:**
  - Banners dos próximos eventos (Culto de Jovens, Escola Bíblica, Santa Ceia).
  - Horários oficiais de funcionamento e endereço com botão *"Abrir no Maps"*.
  - Botão de contribuição rápida: *"Dízimos e Ofertas"* (Copia e Cola da chave PIX oficial com 1 toque).

### Tela 4: 🔒 Gabinete Pastoral (Aba Exclusiva por Perfil)
* **Objetivo:** Gestão dos pedidos para o Pastor e equipe de intercessão.
* **Critério de Acesso:** Apenas usuários com `role = 'pastor'` ou `role = 'intercessor'` têm essa aba visível no app.
* **Componentes:**
  - Lista em tempo real dos pedidos recebidos no Refúgio.
  - Filtro: *Não Orados* / *Orados*.
  - Botão: *"Marcar como Orado"*.
  - Identificação clara: se é Anônimo ou se há contato para visita/mensagem discreta.
  - Formulário simples para criar/editar os Avisos da Semana.

---

## 5. 🗄️ Modelagem de Dados Inicial (Supabase)

```sql
-- 1. Tabela de Pedidos do Refúgio
CREATE TABLE pedidos_refugio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    tag_sentimento TEXT NOT NULL,
    mensagem_opcional TEXT,
    is_anonimo BOOLEAN DEFAULT TRUE,
    nome_contato TEXT,
    telefone_contato TEXT,
    status TEXT DEFAULT 'pendente' -- 'pendente', 'orado', 'em_acompanhamento'
);

-- 2. Tabela de Cortes e Sermões (Alimentada pela automação)
CREATE TABLE sermoes_cortes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    titulo TEXT NOT NULL,
    pregador TEXT,
    data_culto DATE,
    video_url TEXT NOT NULL,
    resumo_ia TEXT,
    destaque BOOLEAN DEFAULT FALSE
);

-- 3. Tabela de Avisos da Igreja
CREATE TABLE avisos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    data_evento TIMESTAMP WITH TIME ZONE,
    banner_url TEXT,
    ativo BOOLEAN DEFAULT TRUE
);
```

---

## 6. 🎯 Métricas de Sucesso do MVP (Como saber se deu certo?)
1. **Pelo menos 15 pedidos de oração silenciosos** registrados nas primeiras 3 semanas de uso piloto.
2. **Tempo médio para pedir oração < 15 segundos** (zero fricção).
3. **100% dos cortes semanais** disponibilizados dentro do app sem falhas de reprodução.
