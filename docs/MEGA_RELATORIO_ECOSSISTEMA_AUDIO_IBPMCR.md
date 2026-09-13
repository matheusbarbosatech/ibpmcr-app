# 🎙️ Mega-Relatório de Arquitetura: Ecossistema de Áudio & Web Rádio 24h
**Super-App Oficial — Igreja Batista Pentecostal Mundial da Carvalho Ramos**  
*Elaborado em:* 12/09/2026 | *Status:* **Planejamento & Engenharia de Produção de Áudio**

---

## 🏛️ 1. Visão Geral & Propósito Espiritual

O **Ecossistema de Áudio IBPM CR** foi projetado para transformar o Super-App em uma **fonte ininterrupta de alimento espiritual e adoração**, acompanhando o membro 24 horas por dia (em casa, no trânsito, no trabalho, na academia ou no leito de oração).

A estratégia une:
1. **A autenticidade da voz do Pastor Anderson Medeiros** (nos 460 cultos gravados e 576 cortes proféticos).
2. **A clareza e fidelidade das Vozes Neurais de IA** (narrando os 365 devocionais, os 3 livros digitais e os 52 módulos de liderança com trilha de adoração ao fundo).
3. **A fluidez da Web Rádio 24 Horas** (streaming contínuo e inteligente no Altar do app).

---

## 🎧 2. Os 5 Pilares do Acervo de Áudio

```
                                      ┌───────────────────────────────────────────────────────────┐
                                      │             ECOSSISTEMA TOTAL DE ÁUDIO IBPM CR            │
                                      └─────────────────────────────┬─────────────────────────────┘
                                                                    │
         ┌──────────────────────────────┬───────────────────────────┼───────────────────────────┬──────────────────────────────┐
         ▼                              ▼                           ▼                           ▼                              ▼
  📻 1. WEB RÁDIO 24H            📖 2. 365 DEVOCIONAIS       📚 3. 3 AUDIOBOOKS          🎓 4. 52 PODCASTS             🏛️ 5. ACERVO DOS 460
     NO ALTAR DO APP                DIÁRIOS EM ÁUDIO            DOS LIVROS                  ESCOLA DE LÍDERES             CULTOS GRAVADOS
  Fluxo contínuo misto           1 áudio por dia (1-2 min)   Audiobooks completos de     52 lições de discipulado      Pregações e ministrações
  de louvores, vinhetas,         com reflexão bíblica e      *Vitória na Família*,       para formação de líderes      históricas completas
  cortes e grandes mensagens.    oração da manhã.            *Guerra* e *Fundamentos*.   e obreiros da igreja.         para ouvir na íntegra.
```

---

## 📊 3. Tabela Comparativa dos Formatos de Áudio

| Pilar | Tipo de Conteúdo | Duração Média | Voz / Origem | Onde Fica no App | Função na Web Rádio 24h |
|---|---|---|---|---|---|
| **1. Web Rádio 24h** | Streaming Contínuo | 24 Horas | Mix Múltiplo | Card Destaque no topo da Home | Canal Principal |
| **2. Devocionais 365** | Reflexão & Oração Diária | 1 a 2 min | Voz Neural IA + Piano | Aba Palavra -> Sub-aba Devocional | Vinheta da Hora na Rádio |
| **3. Audiobooks (3 Livros)** | Capítulos dos Livros Oficiais | 15 a 30 min | Voz Neural Solene IA | Aba Palavra -> Sub-aba Livros | Programa da Noite / Madrugada |
| **4. Escola de Líderes** | 52 Aulas Teológicas | 5 a 8 min | Voz Didática IA | Aba Palavra -> Sub-aba Escola | Pílula de Liderança Semanal |
| **5. Cortes Proféticos (576)** | Trechos de Alto Impacto | 30s a 2 min | Pastor Anderson Medeiros | Aba Mídia -> Cortes Verticais | Pílula de Impacto entre Louvores |
| **6. Cultos Históricos (460)** | Sermões Completos | 35 a 60 min | Pastor Anderson Medeiros | Player de Cultos / Rádio | Grandes Mensagens da Grade |

---

## 📻 4. A Grade de Programação da Web Rádio 24h (O "Mix Perfeito")

Para garantir alta retenção sem cansar o ouvinte, a rádio segue a fórmula dinâmica das maiores emissoras cristãs:

```
  [00:00] 🎵 2 Louvores Pentecostais / Adoração (Harpa Cristã / Corinhos) — ~8 min
  [08:00] ⚡ Pílula Profética do Pastor Anderson Medeiros (Dos 576 Cortes) — ~2 min
  [10:00] 📖 Momento Altar: Devocional do Dia narrado com fundo de piano — ~2 min
  [12:00] 🎵 2 Louvores de Celebração e Avivamento — ~8 min
  [20:00] 🏛️ Mensagem Magna: Pregação Completa de um Culto Histórico do Pastor — ~40 min
  --------------------------------------------------------------------------------------
  (O ciclo se renova a cada hora com conteúdos diferentes e sem repetições ao longo de semanas)
```

---

## 🛠️ 5. Pipeline Tecnológico de Produção dos Áudios

### 🔊 1. Motor de Síntese de Voz (Neural Text-to-Speech)
* **Tecnologia Primária:** Microsoft Edge Neural TTS (100% Gratuito, Estável e Ilimitado via Python).
* **Vozes Selecionadas:**
  - `pt-BR-AntonioNeural`: Voz masculina madura, firme, respeitosa e solene — ideal para devocionais, orações pastorais e audiobooks.
  - `pt-BR-FranciscaNeural`: Voz feminina clara, expressiva e acolhedora — ideal para introduções e vinhetas.

### 🎹 2. Mixagem & Masterização com Trilha de Fundo (Worship Pad / Piano)
* Cada texto narrado pela IA é sobreposto a uma trilha instrumental suave de adoração (piano suave / pad celestial) masterizada a **-18 dB** (para manter a voz em primeiro plano com máxima inteligibilidade).
* Fade-in de 1.5s na abertura e Fade-out de 2.5s no encerramento.

### ☁️ 3. Hospedagem & Distribuição Global (Cloudflare R2)
* Todos os arquivos são compactados em formato **MP3 128 kbps Stereo** (ótima qualidade auditiva com peso de apenas ~1 MB por devocional).
* Armazenamento no bucket `ibpmcr-midia` sob o subdomínio público ativo: `https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev`.

---

## 📱 6. Integração com a Interface e o Player do Super-App

1. **Player Persistente em Segundo Plano (Background Audio):**
   - Utiliza a classe `AudioService` já integrada no app com suporte à tela bloqueada do Android.
   - Notificação com controles de áudio (Play, Pause, Próxima Faixa) e título pastoral.
2. **Mini-Player Flutuante:**
   - Barra na base da tela permitindo pausar ou fechar o áudio enquanto o membro continua lendo a Bíblia offline ou navegando pelas fotos.
3. **Botão de 1 Toque "Ouvir em Áudio":**
   - Presente em todos os 365 devocionais, 3 livros e 52 módulos de liderança.

---

## 📋 7. Próximos Passos de Execução

1. **Executar o Script de Geração de Áudio IA:** Criar e rodar o script para sintetizar em lote os 365 devocionais e os 3 audiobooks.
2. **Subir os Áudios para o Cloudflare R2:** Hospedar o acervo com links permanentes.
3. **Ligar a Playlist Inteligente da Web Rádio:** Configurar o player da Home para tocar a rotação automática contínua de louvores + mensagens + devocionais.
