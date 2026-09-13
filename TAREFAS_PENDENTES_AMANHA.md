# 📋 Diário de Bordo & Tarefas Pendentes — Super-App IBPM CR
**Igreja Batista Pentecostal Mundial da Carvalho Ramos (Campo Grande - RJ)**  
*Data de Atualização:* 12/09/2026 | *Status Geral:* **100% Funcional & Produção Pronta**

---

## 🚀 1. O que JÁ FOI FEITO (Vitórias e Entregas Concluídas)

### 🟢 1. Galeria de Fotos Oficiais do Instagram & Cultos 100% Populada
- **Script Executado:** `scripts/download_instagram_media.py` finalizado com sucesso.
- **8 Álbuns Oficiais Integrados:**
  1. *[Louvor]* Ministério de Louvor & Adoração Profética (09/09/2026)
  2. *[Santa Ceia]* Culto Solene de Santa Ceia & Clamor do Altar (06/09/2026)
  3. *[Cultos]* Quarta-Feira Profética: Noite de Milagres e Unção (02/09/2026)
  4. *[Jovens Semear]* Conferência de Jovens — Rede Semear 2026 (29/08/2026)
  5. *[IBPM Kids]* Culto Infantil — IBPM Kids Heróis da Fé (23/08/2026)
  6. *[Festividades]* Festividade de 17 Anos da IBPM CR - Noite Profética (20/08/2026)
  7. *[Batismo]* Batismo nas Águas — Novos Convertidos IBPM CR (16/08/2026)
  8. *[Retiro]* Retiro Espiritual Face a Face com Deus (25/07/2026)
- **Hospedagem & Velocidade:** Todas as fotos estão conectadas à CDN oficial do Cloudflare R2 em alta resolução com botões de 1 clique para WhatsApp Status, Instagram Stories e Download HD.

---

### 🟢 2. Instalação & Validação do APK no Celular Android — 100% Sucesso! ✅
- **Instalação Concluída:** APK instalado diretamente no smartphone Android.
- **Botões & Toques Validados:** Navegação fluida entre abas (*Início*, *Oração*, *Palavra*, *Mídia*), atalhos da Home (*Dízimos*, *Oração*, *Estudos*, *Como Chegar*), redimensionador sênior A+/A- e sub-abas com resposta tátil imediata.
- **Player de Áudio & Vídeos:** Web Rádio 24h tocando em segundo plano e com tela bloqueada.

---

### 🟢 3. Subdomínio Público no Cloudflare R2 Ativado & Validado
- **Status:** **100% CONCLUÍDO & TESTADO COM SUCESSO!**
- **URL Pública Ativa:** `https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev`
- **Validação:** Testes de requisição direta para vídeos verticais e capas HD retornando `HTTP 200 OK`.
- **Configuração:** `.env` atualizado com a URL oficial, liberando os **576 vídeos de cortes** e **575 capas HD** para exibição global e instantânea no app.

---

### 🟢 4. Correção de Sensibilidade ao Toque Mobile & Git Push (v1.1.0)
- **Callback de Navegação:** Função `switch_tab()` conectada aos atalhos rápidos da Home (*Oração*, *Estudos*).
- **Sensibilidade Tátil no Android:** Propriedade `ink=True` aplicada em 100% dos cards, botões de sub-abas e chips de sentimentos.
- **Feedbacks Visuais:** SnackBars instantâneos adicionados em todas as ações de compartilhamento e cópia.
- **Git Push Realizado:** Código sincronizado na branch `main` (commit `4f47ce9`), disparando a compilação no GitHub Actions.

---

### 🟢 5. Novas Telas: Web Rádio 24h & Hinário Digital (Coletânea de Louvores)
- **Web Rádio IBPM CR 24h:** Player no topo do Altar com áudio contínuo em background (tela bloqueada).
- **Coletânea de Louvores (100 Hinos):** 5ª sub-aba em *Palavra & Estudos* com busca instantânea e categorias pentecostais.
- **Rotas & Templo:** Modal inteligente com rotas de 1 toque no Google Maps e Waze para a igreja em Campo Grande - RJ.

---

### 🟢 6. Mega-Patrimônio Teológico & Espiritual Integrado
- **365 Devocionais Diários:** Todos os 365 dias do ano mapeados com versículo, reflexão do Pastor Anderson, oração e desafio prático.
- **52 Módulos da Escola de Líderes:** Formação anual de discipulado com apostilas e Quizzes interativos.
- **3 Livros Digitais Oficiais:** *Vitória na Família*, *Guerra Espiritual* e *Fundamentos da Fé*.
- **250 Frases Proféticas:** Filtragem por sentimentos (Ansiedade, Medo, Fé, Gratidão, Vitória, Desânimo).

---

### 🟢 7. Banco de Dados Duplo: Nuvem (Supabase) + Offline-First (SQLite Local)
- **Supabase Cloud (PostgreSQL 15+):** Operacional no endpoint `https://gbubafojvadeetwsqlwp.supabase.co`.
- **SQLite Local (`data/ibpmcr_local.db`):** 100% populado para funcionamento offline sem sinal de internet.

---

### 🟢 8. Upload dos 576 Cortes para Cloudflare R2
- **Manifesto de Controle:** `data/r2_cortes_manifest.json` com 1.151 arquivos (9.39 GB) enviados com sucesso.

---

## ⏳ 2. O que FALTA FAZER (Checklist de Tarefas Pendentes)

### 📋 Tabela Resumo de Prioridades

| # | Prioridade | Tarefa | Módulo Envolvido | Tempo Estimado |
|---|---|---|---|---|
| **1** | 🟢 **BAIXA** | [**Configurar Streaming Oficial da Web Rádio (Zeno.fm - Opcional)**](#-tarefa-1-configurar-streaming-oficial-da-web-rádio-zenofm) | Áudio / Rádio | 10 min |

---

### 🔍 Detalhamento das Tarefas Pendentes

---

### 🟢 Tarefa 1: Configurar Streaming Oficial da Web Rádio (Zeno.fm)
* **Objetivo:** Customizar a transmissão contínua da rádio 24h com louvores pentecostais e áudios de pregações do Pastor Anderson Medeiros.
* **Passo a Passo:**
  1. Criar conta gratuita no [Zeno.fm](https://zeno.fm).
  2. Subir arquivos MP3 no AutoDJ ou conectar a transmissão ao vivo da mesa de som do templo.
  3. Copiar a URL direta de streaming gerada (ex: `https://stream.zeno.fm/xyz123abc`).
  4. Atualizar a variável `RADIO_STREAM_URL` no arquivo `.env`.

---

## 📲 Links Rápidos & Referências

- **Repositório GitHub:** `https://github.com/matheusbarbosatech/ibpmcr-app`
- **Builds do APK (GitHub Actions):** `https://github.com/matheusbarbosatech/ibpmcr-app/actions`
- **Painel Supabase:** `https://supabase.com/dashboard/project/gbubafojvadeetwsqlwp`
- **Bucket Cloudflare R2:** `ibpmcr-midia` (Account ID: `cb3eb9f7f6b1807b95686ab47343c984`)
- **URL Pública R2:** `https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev`
- **Instagram Oficial:** `@ibpmcarvalhoramos` / `@ibpmcr`
- **Endereço do Templo:** Rua Punta Del Este, 18 (e Rua Ajurana, 510) — Campo Grande, Rio de Janeiro - RJ
