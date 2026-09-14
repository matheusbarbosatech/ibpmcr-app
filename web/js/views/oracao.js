/**
 * Aba 2: Mural de Oração & Intercessão - IBPM CR WebApp PWA
 */

class OracaoView {
  render() {
    const pedidos = window.store.getPedidos();
    const minhas = window.store.getMinhasOracoes();

    const pedidosHtml = pedidos.map(p => {
      const jaOrou = minhas.includes(p.id);
      return `
        <div class="prayer-card" id="card-${p.id}">
          <div class="prayer-header">
            <span class="prayer-user">👤 ${p.nome}</span>
            <span class="prayer-badge">${p.motivo}</span>
          </div>
          <div class="prayer-details">"${p.detalhes}"</div>
          <div class="prayer-actions">
            <button class="btn-orando ${jaOrou ? 'active' : ''}" onclick="window.oracaoView.clicarOrando('${p.id}')">
              ${jaOrou ? '❤️ Você está orando' : '🙏 Estou Orando'} (${p.orando_count || 1})
            </button>
            <button class="btn-scale" title="Compartilhar no WhatsApp" onclick="window.oracaoView.compartilharPedido('${p.id}')">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="var(--accent-green)"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2z"/></svg>
            </button>
          </div>
        </div>
      `;
    }).join('');

    return `
      <!-- CABEÇALHO DO MURAL -->
      <div class="card" style="text-align: center; gap: 8px;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
          <svg viewBox="0 0 24 24" width="26" height="26" fill="var(--primary-rubi)"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
          <span style="font-size: calc(18px * var(--font-scale)); font-weight: 800; color: var(--text-white);">Mural de Intercessão</span>
        </div>
        <div style="font-size: calc(12px * var(--font-scale)); color: var(--secondary-gold); font-style: italic;">
          "Orai uns pelos outros para que sejais curados." (Tiago 5:16)
        </div>
        <div style="font-size: calc(12px * var(--font-scale)); color: var(--text-muted); line-height: 1.4;">
          Toque em "Estou Orando" para fortalecer um irmão ou coloque o seu clamor no altar da igreja.
        </div>
        
        <button class="btn btn-primary-rubi btn-full" style="margin-top: 6px;" onclick="window.oracaoView.abrirModalNovoPedido()">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
          COLOCAR MEU PEDIDO NO ALTAR
        </button>
      </div>

      <!-- LISTA DE PEDIDOS -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 6px;">
        <span style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white);">Pedidos Recentes</span>
        <span style="font-size: calc(12px * var(--font-scale)); color: var(--secondary-gold); font-weight: 600;">${pedidos.length} clamores ativos</span>
      </div>

      <div style="display: flex; flex-direction: column; gap: 12px;">
        ${pedidosHtml}
      </div>

      <!-- MODAL DE NOVO PEDIDO -->
      <div id="modal-novo-pedido" class="modal-overlay">
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-title">
              <span>🙏</span>
              Novo Pedido de Oração
            </div>
            <button class="modal-close-btn" onclick="window.oracaoView.fecharModalNovoPedido()">✕</button>
          </div>

          <div class="form-group">
            <label class="form-label">Seu Nome ou Apelido *</label>
            <input type="text" id="input-oracao-nome" class="form-input" placeholder="Ex: Maria Aparecida" />
          </div>

          <div class="form-group">
            <label class="form-label">Motivo do Pedido *</label>
            <select id="select-oracao-motivo" class="form-select">
              <option value="Saúde & Cura">Saúde & Cura</option>
              <option value="Família & Casamento">Família & Casamento</option>
              <option value="Causas na Justiça">Causas na Justiça</option>
              <option value="Libertação Espiritual">Libertação Espiritual</option>
              <option value="Vida Financeira & Trabalho">Vida Financeira & Trabalho</option>
              <option value="Paz na Mente / Ansiedade">Paz na Mente / Ansiedade</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Descreva brevemente o seu motivo *</label>
            <textarea id="textarea-oracao-detalhes" class="form-textarea" placeholder="Ex: Peço oração pela minha família e livramento de Deus..."></textarea>
          </div>

          <div style="display: flex; align-items: center; gap: 8px;">
            <input type="checkbox" id="check-oracao-anonimo" style="width: 18px; height: 18px; accent-color: var(--primary-rubi);" />
            <label for="check-oracao-anonimo" style="font-size: calc(12px * var(--font-scale)); color: var(--text-secondary); cursor: pointer;">
              Publicar como Anônimo (ocultar meu nome)
            </label>
          </div>

          <button class="btn btn-primary-rubi btn-full" style="margin-top: 8px;" onclick="window.oracaoView.enviarPedido()">
            ENVIAR PEDIDO AO ALTAR
          </button>
        </div>
      </div>
    `;
  }

  clicarOrando(pedidoId) {
    const success = window.store.incrementarOrando(pedidoId);
    if (success) {
      window.app.renderCurrentView();
    }
  }

  abrirModalNovoPedido() {
    const modal = document.getElementById('modal-novo-pedido');
    if (modal) modal.classList.add('active');
  }

  fecharModalNovoPedido() {
    const modal = document.getElementById('modal-novo-pedido');
    if (modal) modal.classList.remove('active');
  }

  enviarPedido() {
    const nome = document.getElementById('input-oracao-nome')?.value.trim();
    const motivo = document.getElementById('select-oracao-motivo')?.value;
    const detalhes = document.getElementById('textarea-oracao-detalhes')?.value.trim();
    const isAnonimo = document.getElementById('check-oracao-anonimo')?.checked || false;

    if (!detalhes) {
      alert("Por favor, descreva o seu pedido de oração.");
      return;
    }

    window.store.adicionarPedido(nome, motivo, detalhes, isAnonimo);
    this.fecharModalNovoPedido();
    window.app.renderCurrentView();

    alert("🙏 Seu pedido foi colocado no Altar com sucesso! Toda a igreja estará em intercessão por você.");
  }

  compartilharPedido(pedidoId) {
    const pedidos = window.store.getPedidos();
    const p = pedidos.find(item => item.id === pedidoId);
    if (p) {
      const texto = encodeURIComponent(`🙏 *Pedido de Intercessão - IBPM Carvalho Ramos*\nMotivo: *${p.motivo}*\n"${p.detalhes}"\n\nJunte-se a nós em oração no Super-App Oficial!`);
      window.open(`https://wa.me/?text=${texto}`, '_blank');
    }
  }
}

window.oracaoView = new OracaoView();
