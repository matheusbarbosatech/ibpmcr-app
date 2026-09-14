/**
 * Aba 1: Início - IBPM CR WebApp PWA
 */

class HomeView {
  constructor() {
    this.selectedSentiment = 'todos';
  }

  render() {
    const devHoje = DEVOCIONAIS_SEED[0];
    const eventoFace = EVENTOS_SEED[0];
    const fraseAtual = this.getFraseAtual();

    const sentimentos = [
      { label: 'Todos', tag: 'todos' },
      { label: 'Ansiedade', tag: 'ansiedade' },
      { label: 'Medo', tag: 'medo' },
      { label: 'Fé', tag: 'fe' },
      { label: 'Gratidão', tag: 'gratidao' },
      { label: 'Vitória', tag: 'vitoria' },
      { label: 'Desânimo', tag: 'desanimo' }
    ];

    const chipsHtml = sentimentos.map(s => `
      <button class="chip-btn ${this.selectedSentiment === s.tag ? 'active' : ''}" onclick="window.homeView.filtrarSentimento('${s.tag}')">
        ${s.label}
      </button>
    `).join('');

    return `
      <!-- 0. BANNER DE INSTALAÇÃO PWA (Se aplicável) -->
      <div id="pwa-install-banner" class="pwa-install-banner" style="display: none;">
        <div class="pwa-install-info">
          <div class="pwa-install-icon">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM17 13l-5 5-5-5h3V9h4v4h3z"/></svg>
          </div>
          <div>
            <div class="pwa-install-text">Instalar Aplicativo Oficial</div>
            <div class="pwa-install-sub">Acesso rápido e offline na tela inicial</div>
          </div>
        </div>
        <button class="btn btn-secondary-gold" style="min-height: 38px; padding: 6px 12px;" onclick="window.instalarPWA()">
          Instalar
        </button>
      </div>

      <!-- 1. BANNER DO CULTO AO VIVO -->
      <div class="banner-live">
        <div class="banner-header">
          <div class="badge-live">
            <span class="live-dot"></span>
            AO VIVO NO TEMPLO
          </div>
          <span style="font-size: calc(11px * var(--font-scale)); color: var(--text-muted); font-weight: 600;">Domingo às 19h</span>
        </div>
        <div class="banner-title">Culto da Família & Celebração Profética</div>
        <div class="banner-subtitle">Venha adorar presencialmente na Carvalho Ramos ou acompanhe a transmissão ao vivo pelo canal oficial.</div>
        <div class="banner-actions">
          <button class="btn btn-primary-rubi" onclick="window.open('${CHURCH_CONFIG.youtubeLiveUrl}', '_blank')">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
            Assistir Culto
          </button>
          <button class="btn btn-outlined-gold" onclick="window.homeView.convidarWhatsApp()">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92z"/></svg>
            Convidar
          </button>
        </div>
      </div>

      <!-- 2. BANNER DESTAQUE: RETIRO FACE A FACE COM DEUS -->
      <div class="card card-gold">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <span class="badge-gold">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
            GRANDE EVENTO OFICIAL
          </span>
          <span style="font-size: calc(11px * var(--font-scale)); font-weight: 800; color: var(--secondary-gold);">📅 ${eventoFace.data}</span>
        </div>
        <div style="font-size: calc(16px * var(--font-scale)); font-weight: 800; color: var(--text-white);">${eventoFace.titulo}</div>
        <div style="font-size: calc(12px * var(--font-scale)); font-weight: 700; color: var(--secondary-gold);">🔥 ${eventoFace.slogan}</div>
        <div style="font-size: calc(12px * var(--font-scale)); color: var(--text-secondary); line-height: 1.4;">${eventoFace.descricao}</div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px;">
          <button class="btn btn-secondary-gold" style="flex: 1; min-height: 42px; font-size: calc(12px * var(--font-scale));" onclick="window.lojinhaView.abrirInscricaoModal()">
            ✍️ Inscrição no App
          </button>
          <button class="btn btn-primary-rubi" style="flex: 1; min-height: 42px; font-size: calc(12px * var(--font-scale));" onclick="window.lojinhaView.abrirCamisaRetiro()">
            👕 Camisa Oficial
          </button>
        </div>
      </div>

      <!-- 3. PÍLULA PASTORAL EM ÁUDIO -->
      <div class="card-media-row" onclick="window.homeView.tocarPilulaPastoral()">
        <button class="media-play-btn gold">
          <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
        </button>
        <div class="media-info">
          <div class="media-info-header">
            <span class="media-title">Pílula Pastoral do Dia</span>
            <span class="badge-gold" style="font-size: 9px; padding: 2px 6px;">ÁUDIO</span>
          </div>
          <div class="media-subtitle">Uma Palavra de Ânimo para a sua Semana</div>
          <div class="media-status">Toque para ouvir a ministração no celular</div>
        </div>
        <svg viewBox="0 0 24 24" width="22" height="22" fill="var(--text-muted)"><path d="M12 3v9.28c-.47-.17-.97-.28-1.5-.28C8.01 12 6 14.01 6 16.5S8.01 21 10.5 21c2.31 0 4.2-1.75 4.45-4H15V6h4V3h-7z"/></svg>
      </div>

      <!-- 4. RÁDIO IBPM CR 24 HORAS -->
      <div class="card-media-row" style="border-color: var(--secondary-gold);" onclick="window.homeView.tocarRadio()">
        <button class="media-play-btn rubi">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M3.24 6.15C2.51 7.43 2 8.91 2 10.5c0 3.03 1.7 5.66 4.19 6.99l.77-1.34C4.84 15.08 3.5 12.94 3.5 10.5c0-1.19.39-2.3 1.05-3.21L3.24 6.15zM7.05 8.35C6.7 8.99 6.5 9.72 6.5 10.5c0 1.62.91 3.03 2.25 3.75l.75-1.3C8.78 12.44 8 11.55 8 10.5c0-.52.14-1.01.37-1.44L7.05 8.35zM12 8c-1.38 0-2.5 1.12-2.5 2.5s1.12 2.5 2.5 2.5 2.5-1.12 2.5-2.5S13.38 8 12 8zm4.95.35l-.75 1.3c.23.43.37.92.37 1.44 0 1.05-.78 1.94-1.8 2.25l.75 1.3c1.34-.72 2.25-2.13 2.25-3.75 0-.78-.2-1.51-.55-2.15zM20.76 6.15l-1.31 1.14c.66.91 1.05 2.02 1.05 3.21 0 2.44-1.34 4.58-3.46 5.65l.77 1.34C20.3 16.16 22 13.53 22 10.5c0-1.59-.51-3.07-1.24-4.35z"/></svg>
        </button>
        <div class="media-info">
          <div class="media-info-header">
            <span class="media-title">Rádio IBPM CR</span>
            <span class="badge-live" style="font-size: 9px; padding: 2px 6px;">AO VIVO 24H</span>
          </div>
          <div class="media-subtitle">Sintonize a Presença de Deus no Altar</div>
          <div class="media-status" style="color: var(--secondary-gold);">🔴 NO AR • Louvores & Pregações Contínuas</div>
        </div>
        <button class="btn-scale" title="Pedir Oração / Louvor na Rádio" onclick="event.stopPropagation(); window.homeView.pedirLouvorRadio();">
          ❤️
        </button>
      </div>

      <!-- 5. FRASE PROFÉTICA DO DIA (INTERATIVO) -->
      <div class="card">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 18px;">✨</span>
          <span style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white);">Frase Profética para o Seu Dia</span>
        </div>
        
        <!-- Carrossel de sentimentos -->
        <div class="chips-scroll">
          ${chipsHtml}
        </div>

        <!-- Card da frase -->
        <div class="prophetic-card">
          <div class="prophetic-text">"${fraseAtual.frase}"</div>
          <div class="prophetic-ref">📖 ${fraseAtual.ref}</div>
        </div>

        <!-- Botões de Ação da Frase -->
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
          <button class="btn btn-green-whatsapp" style="flex: 1; min-height: 40px; padding: 8px 12px;" onclick="window.homeView.compartilharWhatsAppFrase()">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2z"/></svg>
            Status
          </button>
          <button class="btn btn-outlined-rubi" style="flex: 1; min-height: 40px; padding: 8px 12px;" onclick="window.homeView.copiarFrase()">
            📋 Copiar
          </button>
        </div>
      </div>

      <!-- 6. GRID DE ATALHOS RÁPIDOS SÊNIOR -->
      <div style="margin-top: 6px;">
        <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white); margin-bottom: 10px;">
          Acesso Rápido da Congregação
        </div>
        <div class="shortcuts-grid">
          <button class="shortcut-card" onclick="window.lojinhaView.abrirLojinhaModal()">
            <span style="font-size: 26px;">🛍️</span>
            <div class="shortcut-title">Lojinha</div>
            <div class="shortcut-desc">Cantina & Loja</div>
          </button>

          <button class="shortcut-card" onclick="window.lojinhaView.abrirDizimosModal()">
            <span style="font-size: 26px;">💳</span>
            <div class="shortcut-title">Dízimos</div>
            <div class="shortcut-desc">Chave PIX</div>
          </button>

          <button class="shortcut-card" onclick="window.app.navigateToTab(1)">
            <span style="font-size: 26px;">🙏</span>
            <div class="shortcut-title">Oração</div>
            <div class="shortcut-desc">Mural Social</div>
          </button>

          <button class="shortcut-card" onclick="window.app.navigateToTab(2)">
            <span style="font-size: 26px;">📖</span>
            <div class="shortcut-title">Palavra</div>
            <div class="shortcut-desc">Bíblia & Estudos</div>
          </button>

          <button class="shortcut-card" onclick="window.app.navigateToTab(3)">
            <span style="font-size: 26px;">📸</span>
            <div class="shortcut-title">Fotos</div>
            <div class="shortcut-desc">Cultos & Shorts</div>
          </button>

          <button class="shortcut-card" onclick="window.lojinhaView.abrirComoChegarModal()">
            <span style="font-size: 26px;">📍</span>
            <div class="shortcut-title">Como Chegar</div>
            <div class="shortcut-desc">Templo & GPS</div>
          </button>
        </div>
      </div>
    `;
  }

  getFraseAtual() {
    if (this.selectedSentiment === 'todos') {
      return FRASES_SEED[0];
    }
    const filtradas = FRASES_SEED.filter(f => f.tag === this.selectedSentiment);
    return filtradas.length > 0 ? filtradas[0] : FRASES_SEED[0];
  }

  filtrarSentimento(tag) {
    this.selectedSentiment = tag;
    window.app.renderCurrentView();
  }

  tocarPilulaPastoral() {
    const dev = DEVOCIONAIS_SEED[0];
    window.audioService.playTrack({
      title: `Pílula Pastoral - ${dev.titulo}`,
      subtitle: "Pastor Presidente • IBPM CR",
      url: dev.audio_url,
      artist: "Pastor Presidente"
    });
  }

  tocarRadio() {
    window.audioService.playTrack({
      title: "Rádio IBPM CR • Ao Vivo 24h",
      subtitle: "Louvores & Palavra no Altar",
      url: CHURCH_CONFIG.radioStreamUrl,
      artist: "IBPM Carvalho Ramos"
    });
  }

  pedirLouvorRadio() {
    const texto = encodeURIComponent("📻 *Pedido de Louvor & Oração - Rádio IBPM CR*\nPaz do Senhor! Gostaria de pedir oração e um louvor abençoado na Rádio IBPM CR!");
    window.open(`https://wa.me/${CHURCH_CONFIG.whatsappSecretaria}?text=${texto}`, '_blank');
  }

  convidarWhatsApp() {
    const texto = encodeURIComponent(`🔥 *Culto da Família - IBPM Carvalho Ramos*\nVenha adorar conosco ou assista a transmissão ao vivo!\n👉 ${CHURCH_CONFIG.youtubeLiveUrl}`);
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  }

  compartilharWhatsAppFrase() {
    const frase = this.getFraseAtual();
    const texto = encodeURIComponent(`✨ *Palavra do Dia - IBPM Carvalho Ramos*\n"${frase.frase}"\n📖 ${frase.ref}\n\nSuper-App Oficial IBPM CR`);
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  }

  copiarFrase() {
    const frase = this.getFraseAtual();
    navigator.clipboard.writeText(`"${frase.frase}" - ${frase.ref}`).then(() => {
      alert("✅ Frase profética copiada com sucesso!");
    });
  }
}

window.homeView = new HomeView();
