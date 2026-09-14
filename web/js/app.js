/**
 * Controlador Principal da Aplicação - IBPM CR WebApp PWA
 */

class AppController {
  constructor() {
    this.currentTab = 0; // 0: Início, 1: Oração, 2: Palavra, 3: Mídia
    this.views = [
      window.homeView,
      window.oracaoView,
      window.palavraView,
      window.midiaView
    ];

    this.scaleLevels = [0.85, 1.0, 1.15, 1.30, 1.50];
    this.init();
  }

  init() {
    // 1. Aplica escala de fonte salva
    const savedScale = window.store.getFontScale();
    this.applyFontScale(savedScale);

    // 2. Registra Service Worker se suportado
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
          .then(reg => console.log('[SW] Registrado com sucesso:', reg.scope))
          .catch(err => console.warn('[SW] Falha no registro:', err));
      });
    }

    // 3. Lê parâmetros da URL
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    if (tabParam !== null && !isNaN(tabParam)) {
      this.currentTab = parseInt(tabParam, 10);
    }

    const actionParam = urlParams.get('action');
    if (actionParam === 'radio') {
      setTimeout(() => window.homeView.tocarRadio(), 500);
    } else if (actionParam === 'pix') {
      setTimeout(() => window.lojinhaView.abrirDizimosModal(), 500);
    }

    // 4. Renderiza view inicial
    this.renderCurrentView();
    this.updateNavUI();
  }

  navigateToTab(index) {
    if (index >= 0 && index < this.views.length) {
      this.currentTab = index;
      this.renderCurrentView();
      this.updateNavUI();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  renderCurrentView() {
    const container = document.getElementById('view-content');
    if (container && this.views[this.currentTab]) {
      container.innerHTML = this.views[this.currentTab].render();
    }
  }

  updateNavUI() {
    const navButtons = document.querySelectorAll('.bottom-nav .nav-item');
    navButtons.forEach((btn, idx) => {
      if (idx === this.currentTab) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  }

  // =========================================================================
  // ACESSIBILIDADE SÊNIOR (A- / A+)
  // =========================================================================
  applyFontScale(scale) {
    window.store.setFontScale(scale);
    const displayEl = document.getElementById('scale-display-value');
    if (displayEl) {
      displayEl.textContent = `${Math.round(scale * 100)}%`;
    }
  }

  increaseFont() {
    const current = window.store.getFontScale();
    const curIdx = this.scaleLevels.indexOf(current);
    if (curIdx !== -1 && curIdx < this.scaleLevels.length - 1) {
      const nextScale = this.scaleLevels[curIdx + 1];
      this.applyFontScale(nextScale);
      this.renderCurrentView();
    }
  }

  decreaseFont() {
    const current = window.store.getFontScale();
    const curIdx = this.scaleLevels.indexOf(current);
    if (curIdx !== -1 && curIdx > 0) {
      const prevScale = this.scaleLevels[curIdx - 1];
      this.applyFontScale(prevScale);
      this.renderCurrentView();
    }
  }
}

// Inicializa a aplicação quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  window.app = new AppController();
});
