/**
 * Módulo de Lojinha, Inscrições em Eventos, Dízimos e Localização - IBPM CR WebApp PWA
 */

class LojinhaView {
  constructor() {
    this.incluirCamisaInscricao = true;
  }

  // 1. MODAL DA LOJINHA & CANTINA
  abrirLojinhaModal() {
    const modal = document.getElementById('modal-lojinha');
    if (modal) {
      const container = document.getElementById('lojinha-produtos-container');
      if (container) {
        container.innerHTML = PRODUTOS_SEED.map(p => `
          <div class="card" style="display: flex; flex-direction: row; gap: 12px; align-items: center; padding: 10px;">
            <img src="${p.imagem}" style="width: 75px; height: 75px; object-fit: cover; border-radius: var(--radius-sm); border: 1px solid var(--border-gold);" />
            <div style="flex: 1; display: flex; flex-direction: column; gap: 2px;">
              <span class="badge-gold" style="align-self: flex-start; font-size: 9px; padding: 1px 6px;">${p.categoria}</span>
              <div style="font-size: calc(13px * var(--font-scale)); font-weight: 700; color: var(--text-white);">${p.nome}</div>
              <div style="font-size: calc(14px * var(--font-scale)); font-weight: 800; color: var(--secondary-gold);">R$ ${p.preco.toFixed(2)}</div>
              <button class="btn btn-green-whatsapp" style="min-height: 32px; padding: 4px 10px; font-size: 11px; margin-top: 4px; align-self: flex-start;" onclick="window.lojinhaView.pedirProduto('${p.nome}', ${p.preco})">
                Comprar via WhatsApp
              </button>
            </div>
          </div>
        `).join('');
      }
      modal.classList.add('active');
    }
  }

  fecharLojinhaModal() {
    const modal = document.getElementById('modal-lojinha');
    if (modal) modal.classList.remove('active');
  }

  pedirProduto(nome, preco) {
    const texto = encodeURIComponent(`🛍️ *Pedido na Lojinha/Cantina - IBPM CR*\nOlá! Gostaria de encomendar:\n- *Produto:* ${nome}\n- *Valor:* R$ ${preco.toFixed(2)}\n\nPoderia me enviar a confirmação para pagamento via PIX?`);
    window.open(`https://wa.me/${CHURCH_CONFIG.whatsappSecretaria}?text=${texto}`, '_blank');
  }

  // 2. MODAL DE INSCRIÇÃO NO RETIRO FACE A FACE
  abrirInscricaoModal() {
    const modal = document.getElementById('modal-inscricao-retiro');
    if (modal) {
      this.atualizarTotalInscricao();
      modal.classList.add('active');
    }
  }

  fecharInscricaoModal() {
    const modal = document.getElementById('modal-inscricao-retiro');
    if (modal) modal.classList.remove('active');
  }

  abrirCamisaRetiro() {
    this.abrirInscricaoModal();
  }

  toggleCamisa(checked) {
    this.incluirCamisaInscricao = checked;
    const tamRow = document.getElementById('row-tamanho-camisa');
    if (tamRow) tamRow.style.display = checked ? 'flex' : 'none';
    this.atualizarTotalInscricao();
  }

  atualizarTotalInscricao() {
    const ev = EVENTOS_SEED[0];
    let total = ev.valor_inscricao;
    if (this.incluirCamisaInscricao) total += ev.valor_camisa;

    const el = document.getElementById('inscricao-valor-total');
    if (el) el.textContent = `R$ ${total.toFixed(2)}`;
  }

  submeterInscricao() {
    const nome = document.getElementById('inscricao-nome')?.value.trim();
    const whatsapp = document.getElementById('inscricao-whatsapp')?.value.trim();
    const idade = document.getElementById('inscricao-idade')?.value.trim();
    const bairro = document.getElementById('inscricao-bairro')?.value.trim();
    const vinculo = document.getElementById('inscricao-vinculo')?.value;
    const tamanho = document.getElementById('inscricao-tamanho')?.value;
    const restricoes = document.getElementById('inscricao-restricoes')?.value.trim();

    if (!nome || !whatsapp || !bairro) {
      alert("Por favor, preencha todos os campos obrigatórios (*).");
      return;
    }

    const ev = EVENTOS_SEED[0];
    let total = ev.valor_inscricao + (this.incluirCamisaInscricao ? ev.valor_camisa : 0);

    const resumo = `🔥 *Inscrição Oficial - ${ev.titulo}*\n` +
      `👤 *Nome:* ${nome}\n` +
      `📱 *WhatsApp:* ${whatsapp}\n` +
      `🎂 *Idade:* ${idade || 'N/A'}\n` +
      `📍 *Bairro:* ${bairro}\n` +
      `⛪ *Vínculo:* ${vinculo}\n` +
      `👕 *Camisa Oficial:* ${this.incluirCamisaInscricao ? `SIM (Tamanho ${tamanho})` : 'NÃO'}\n` +
      `🩺 *Restrições Médicas:* ${restricoes || 'Nenhuma'}\n` +
      `💰 *Valor Total:* R$ ${total.toFixed(2)}\n\n` +
      `🔑 *Chave PIX da Igreja:* ${CHURCH_CONFIG.pixKey} (IBPM)\n` +
      `Por favor, envie o comprovante do PIX nesta conversa para confirmar sua vaga!`;

    const url = `https://wa.me/${CHURCH_CONFIG.whatsappSecretaria}?text=${encodeURIComponent(resumo)}`;
    window.open(url, '_blank');
    this.fecharInscricaoModal();
    alert("✅ Inscrição gerada com sucesso! Você será redirecionado para o WhatsApp da secretaria para envio do comprovante.");
  }

  // 3. MODAL DE DÍZIMOS & OFERTAS
  abrirDizimosModal() {
    const modal = document.getElementById('modal-dizimos');
    if (modal) modal.classList.add('active');
  }

  fecharDizimosModal() {
    const modal = document.getElementById('modal-dizimos');
    if (modal) modal.classList.remove('active');
  }

  copiarChavePix() {
    navigator.clipboard.writeText(CHURCH_CONFIG.pixKey).then(() => {
      alert(`✅ Chave PIX copiada: ${CHURCH_CONFIG.pixKey}\nAbra o app do seu banco e selecione PIX Copia e Cola / Telefone.`);
    });
  }

  enviarComprovantePix() {
    const texto = encodeURIComponent("🕊️ *Comprovante de Dízimo / Oferta - IBPM CR*\nPaz do Senhor! Segue em anexo o comprovante da minha contribuição para a obra de Deus.");
    window.open(`https://wa.me/${CHURCH_CONFIG.whatsappSecretaria}?text=${texto}`, '_blank');
  }

  // 4. MODAL COMO CHEGAR / LOCALIZAÇÃO
  abrirComoChegarModal() {
    const modal = document.getElementById('modal-como-chegar');
    if (modal) modal.classList.add('active');
  }

  fecharComoChegarModal() {
    const modal = document.getElementById('modal-como-chegar');
    if (modal) modal.classList.remove('active');
  }
}

window.lojinhaView = new LojinhaView();
