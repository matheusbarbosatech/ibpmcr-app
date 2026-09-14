/**
 * Aba 4: Mídia & Fotos & Shorts - IBPM CR WebApp PWA
 */

class MidiaView {
  constructor() {
    this.activeSubtab = 0; // 0: Galeria de Fotos, 1: Cortes Verticais
    this.fotoModalUrl = null;
    this.fotoModalTitulo = null;
  }

  render() {
    const subtabs = [
      { label: 'Galeria de Fotos', icon: '📸', idx: 0 },
      { label: 'Cortes Verticais (Shorts)', icon: '📱', idx: 1 }
    ];

    const pillsHtml = subtabs.map(s => `
      <button class="subtab-pill ${this.activeSubtab === s.idx ? 'active' : ''}" onclick="window.midiaView.mudarSubtab(${s.idx})">
        <span>${s.icon}</span>
        <span>${s.label}</span>
      </button>
    `).join('');

    let contentHtml = '';
    if (this.activeSubtab === 0) contentHtml = this.renderFotos();
    else contentHtml = this.renderShorts();

    return `
      <!-- NAVEGAÇÃO DE SUB-ABAS -->
      <div class="subtabs-nav">
        ${pillsHtml}
      </div>

      <!-- CONTEÚDO DA SUB-ABA -->
      <div>
        ${contentHtml}
      </div>

      <!-- MODAL LIGHTBOX FULLSCREEN -->
      <div id="modal-foto-lightbox" class="modal-overlay">
        <div class="modal-content" style="max-width: 500px; padding: 12px; background: #000000; border-color: var(--secondary-gold);">
          <div class="modal-header" style="border: none; padding-bottom: 4px;">
            <div id="lightbox-titulo" style="font-size: calc(13px * var(--font-scale)); font-weight: 700; color: var(--text-white);"></div>
            <button class="modal-close-btn" onclick="window.midiaView.fecharLightbox()">✕</button>
          </div>
          <img id="lightbox-img" src="" style="width: 100%; border-radius: var(--radius-sm); max-height: 70vh; object-fit: contain;" />
          <div style="display: flex; gap: 8px; margin-top: 8px;">
            <button class="btn btn-secondary-gold btn-full" onclick="window.midiaView.baixarFotoHD()">
              📥 Baixar Foto em Alta Resolução (HD)
            </button>
          </div>
        </div>
      </div>
    `;
  }

  mudarSubtab(idx) {
    this.activeSubtab = idx;
    window.app.renderCurrentView();
  }

  // 1. GALERIA DE FOTOS DOS CULTOS
  renderFotos() {
    const fotosHtml = FOTOS_SEED.map(f => `
      <div class="card" style="padding: 12px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
          <span style="font-size: calc(14px * var(--font-scale)); font-weight: 800; color: var(--text-white);">${f.album}</span>
          <span class="badge-gold">${f.categoria}</span>
        </div>
        <div style="font-size: calc(11px * var(--font-scale)); color: var(--text-muted); margin-bottom: 8px;">📅 Data: ${f.data}</div>
        
        <div style="position: relative; cursor: pointer; border-radius: var(--radius-md); overflow: hidden;" onclick="window.midiaView.abrirLightbox('${f.foto}', '${f.album}')">
          <img src="${f.foto}" style="width: 100%; height: 210px; object-fit: cover; display: block; transition: transform 0.3s ease;" />
          <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.7); padding: 4px 8px; border-radius: var(--radius-sm); font-size: 11px; color: #FFFFFF;">
            🔍 Toque para expandir
          </div>
        </div>

        <div style="display: flex; gap: 8px; margin-top: 10px;">
          <button class="btn btn-green-whatsapp" style="flex: 1; min-height: 40px; padding: 6px 12px; font-size: calc(11px * var(--font-scale));" onclick="window.midiaView.compartilharFoto('${f.album}', '${f.foto}')">
            WhatsApp Status
          </button>
          <button class="btn btn-outlined-gold" style="flex: 1; min-height: 40px; padding: 6px 12px; font-size: calc(11px * var(--font-scale));" onclick="window.midiaView.abrirLightbox('${f.foto}', '${f.album}')">
            Download HD
          </button>
        </div>
      </div>
    `).join('');

    return `
      <div style="display: flex; flex-direction: column; gap: 14px;">
        ${fotosHtml}
      </div>
    `;
  }

  abrirLightbox(url, titulo) {
    this.fotoModalUrl = url;
    this.fotoModalTitulo = titulo;
    const modal = document.getElementById('modal-foto-lightbox');
    const img = document.getElementById('lightbox-img');
    const tit = document.getElementById('lightbox-titulo');
    if (modal && img && tit) {
      img.src = url;
      tit.textContent = titulo;
      modal.classList.add('active');
    }
  }

  fecharLightbox() {
    const modal = document.getElementById('modal-foto-lightbox');
    if (modal) modal.classList.remove('active');
  }

  baixarFotoHD() {
    if (this.fotoModalUrl) {
      window.open(this.fotoModalUrl, '_blank');
    }
  }

  compartilharFoto(titulo, url) {
    const texto = encodeURIComponent(`📸 *Galeria Oficial - IBPM Carvalho Ramos*\n${titulo}\nVeja as fotos no Super-App Oficial!\n👉 ${url}`);
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  }

  // 2. CORTES VERTICAIS (SHORTS 9:16)
  renderShorts() {
    const shortsHtml = SHORTS_SEED.map(s => `
      <div class="card card-rubi" style="padding: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
          <span class="badge-gold">🔥 Viral Score: ${s.viral_score}%</span>
          <span style="font-size: calc(11px * var(--font-scale)); color: var(--text-muted);">⏱️ ${s.duracao}</span>
        </div>
        <div style="font-size: calc(14px * var(--font-scale)); font-weight: 800; color: var(--text-white); margin-bottom: 10px;">
          "${s.titulo}"
        </div>

        <div style="border-radius: var(--radius-md); overflow: hidden; background: #000000; display: flex; justify-content: center;">
          <video src="${s.video_url}" controls style="width: 100%; max-height: 380px; border-radius: var(--radius-md);" poster="icons/icon-512.png"></video>
        </div>

        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 10px;">
          <span style="font-size: calc(12px * var(--font-scale)); color: var(--secondary-gold); font-weight: 700;">
            💬 ${s.shares} compartilhamentos
          </span>
          <button class="btn btn-green-whatsapp" style="min-height: 38px; padding: 6px 14px;" onclick="window.midiaView.compartilharShort('${s.titulo}', '${s.video_url}')">
            Status WhatsApp
          </button>
        </div>
      </div>
    `).join('');

    return `
      <div style="display: flex; flex-direction: column; gap: 14px;">
        ${shortsHtml}
      </div>
    `;
  }

  compartilharShort(titulo, url) {
    const texto = encodeURIComponent(`🔥 *Corte Profético - IBPM Carvalho Ramos*\n"${titulo}"\nAssista no Super-App Oficial!\n👉 ${url}`);
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  }
}

window.midiaView = new MidiaView();
