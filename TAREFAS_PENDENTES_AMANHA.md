# 📋 Diário de Bordo & Tarefas Pendentes — Super-App IBPM CR
**Igreja Batista Pentecostal Mundial da Carvalho Ramos (Campo Grande - RJ)**  
*Data de Atualização:* 12/09/2026 | *Status Geral:* **100% Funcional & Produção Pronta**

---

## 🚀 1. O que JÁ FOI FEITO (Vitórias e Entregas Concluídas)

### 🟢 1. Instalação & Validação do APK no Celular Android — 100% Sucesso! ✅
- **Instalação Concluída:** APK instalado diretamente no smartphone Android.
- **Botões & Toques Validados:** Navegação fluida entre abas (*Início*, *Oração*, *Palavra*, *Mídia*), atalhos da Home (*Dízimos*, *Oração*, *Estudos*, *Como Chegar*), redimensionador sênior A+/A- e sub-abas com resposta tátil imediata.
- **Player de Áudio & Vídeos:** Web Rádio 24h tocando em segundo plano e com tela bloqueada.

---

### 🟢 2. Subdomínio Público no Cloudflare R2 Ativado & Validado
- **Status:** **100% CONCLUÍDO & TESTADO COM SUCESSO!**
- **URL Pública Ativa:** `https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev`
- **Validação:** Testes de requisição direta para vídeos verticais e capas HD retornando `HTTP 200 OK`.
- **Configuração:** `.env` atualizado com a URL oficial, liberando os **576 vídeos de cortes** e **575 capas HD** para exibição global e instantânea no app.

---

### 🟢 3. Correção de Sensibilidade ao Toque Mobile & Git Push (v1.1.0)
- **Callback de Navegação:** Função `switch_tab()` conectada aos atalhos rápidos da Home (*Oração*, *Estudos*).
- **Sensibilidade Tátil no Android:** Propriedade `ink=True` aplicada em 100% dos cards, botões de sub-abas e chips de sentimentos.
- **Feedbacks Visuais:** SnackBars instantâneos adicionados em todas as ações de compartilhamento e cópia.
- **Git Push Realizado:** Código sincronizado na branch `main` (commit `4f47ce9`), disparando a compilação no GitHub Actions.

---

### 🟢 4. Deep Research Completa de Mini-Jogos Bíblicos & Gamificação
- **Relatório Oficial Criado:** Salvo em [docs/RELATORIO_JOGOS_BIBLICOS.md](file:///c:/Users/matheus/Desktop/ibpmcr-app/docs/RELATORIO_JOGOS_BIBLICOS.md).
- **5 Mini-Jogos Mapeados:** Palavra do Dia (Wordle Bíblico), Show da Fé (Quiz de 3 Níveis), Quem Sou Eu? (Detetive Bíblico), Ordene o Versículo e Memória Kids.
- **Sistema de Patentes Espirituais:** 5 níveis de sabedoria (*Discípulo de Beréia* a *Embaixador do Reino*) com armazenamento offline-first.

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
| **1** | 🟡 **MÉDIA** | [**📸 Obter e Sincronizar Link do Drive de Fotos dos Cultos**](#-tarefa-1-obter-e-sincronizar-link-do-drive-de-fotos-dos-cultos) | Mídia / Fotos | 10 min |
| **2** | 🟡 **MÉDIA** | [**🎮 Implementar Módulo de Mini-Jogos Bíblicos**](#-tarefa-2-implementar-módulo-de-mini-jogos-bíblicos) | Telas / Jogos | 1 dia |
| **3** | 🟢 **BAIXA** | [**Popular Galeria com Álbuns Oficiais do Instagram**](#-tarefa-3-popular-galeria-com-álbuns-oficiais-do-instagram) | Banco de Dados | 5 min |
| **4** | 🟢 **BAIXA** | [**Configurar Streaming Oficial da Web Rádio (Zeno.fm - Opcional)**](#-tarefa-4-configurar-streaming-oficial-da-web-rádio-zenofm) | Áudio / Rádio | 10 min |

---

### 🔍 Detalhamento das Tarefas Pendentes

---

### 🟡 Tarefa 1: Obter e Sincronizar Link do Drive de Fotos dos Cultos
* **Objetivo:** Conectar a pasta compartilhada da equipe de mídia da igreja para atualizar a galeria com fotos dos cultos recentes.
* **Passo a Passo:**
  1. Obter o link da pasta compartilhada do Google Drive da equipe de mídia.
  2. Garantir que o link tenha permissão de leitura pública.
  3. Rodar o script de sincronização:
     ```powershell
     python scripts/sync_google_drive_photos.py --drive-url "https://drive.google.com/drive/folders/SEU_ID_AQUI"
     ```

---

### 🟡 Tarefa 2: Implementar Módulo de Mini-Jogos Bíblicos
* **Objetivo:** Desenvolver a **6ª Sub-Aba de Palavra & Estudos** com jogos cristãos baseados no relatório [docs/RELATORIO_JOGOS_BIBLICOS.md](file:///c:/Users/matheus/Desktop/ibpmcr-app/docs/RELATORIO_JOGOS_BIBLICOS.md).
* **Mini-Jogos Previstos:**
  1. 🟩 **Palavra Bíblica do Dia (Wordle / Termo):** Adivinhar palavra bíblica em 6 tentativas com feedback por cores e versículo pós-vitória.
  2. 🏆 **Show da Fé (Quiz Bíblico):** Perguntas com 3 níveis (Iniciante, Valente e Mestre) com ajudas `50:50` e `Dica do Pastor`.
  3. 🕵️ **Quem Sou Eu?:** Enigma de dedução com 4 pistas graduais de personagens bíblicos.
  4. 📖 **Ordene o Versículo:** Desafio de memorização ordenando palavras embaralhadas.
  5. 👶 **Memória Kids:** Jogo da memória lúdico com os Heróis da Fé.

---

### 🟢 Tarefa 3: Popular Galeria com Álbuns Oficiais do Instagram
* **Objetivo:** Popular a galeria com acervo de fotos do Instagram oficial `@ibpmcarvalhoramos`.
* **Comando:**
  ```powershell
  python scripts/seed_albuns_oficiais.py
  ```

---

### 🟢 Tarefa 4: Configurar Streaming Oficial da Web Rádio (Zeno.fm)
* **Objetivo:** Customizar a grade 24h da rádio com louvores pentecostais e pregações do Pastor Anderson.
* **Passo a Passo:**
  1. Criar conta gratuita no [Zeno.fm](https://zeno.fm).
  2. Subir arquivos MP3 no AutoDJ.
  3. Copiar a URL direta de streaming e atualizar `RADIO_STREAM_URL` no `.env`.

---

## 📲 Links Rápidos & Referências

- **Repositório GitHub:** `https://github.com/matheusbarbosatech/ibpmcr-app`
- **Builds do APK (GitHub Actions):** `https://github.com/matheusbarbosatech/ibpmcr-app/actions`
- **Painel Supabase:** `https://supabase.com/dashboard/project/gbubafojvadeetwsqlwp`
- **Bucket Cloudflare R2:** `ibpmcr-midia` (Account ID: `cb3eb9f7f6b1807b95686ab47343c984`)
- **URL Pública R2:** `https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev`
- **Instagram Oficial:** `@ibpmcarvalhoramos` / `@ibpmcr`
- **Endereço do Templo:** Rua Punta Del Este, 18 (e Rua Ajurana, 510) — Campo Grande, Rio de Janeiro - RJ
