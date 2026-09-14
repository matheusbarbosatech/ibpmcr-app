/**
 * Aba 3: Palavra & Estudos - IBPM CR WebApp PWA
 */

class PalavraView {
  constructor() {
    this.activeSubtab = 0; // 0: Devocional, 1: Bíblia, 2: Livros, 3: Escola, 4: Hinário
    this.diaDevocional = 1;
    this.livroAtivo = "Salmos";
    this.capituloAtivo = "23";
    this.buscaLouvor = "";
    this.quizModuloAtivo = 1;
    this.quizRespostas = {};
  }

  render() {
    const subtabs = [
      { label: 'Devocional 365', icon: '📖', idx: 0 },
      { label: 'Bíblia Sagrada', icon: '📜', idx: 1 },
      { label: 'Livros & E-books', icon: '📚', idx: 2 },
      { label: 'Escola de Líderes', icon: '🎓', idx: 3 },
      { label: 'Coletânea Louvores', icon: '🎵', idx: 4 }
    ];

    const pillsHtml = subtabs.map(s => `
      <button class="subtab-pill ${this.activeSubtab === s.idx ? 'active' : ''}" onclick="window.palavraView.mudarSubtab(${s.idx})">
        <span>${s.icon}</span>
        <span>${s.label}</span>
      </button>
    `).join('');

    let contentHtml = '';
    if (this.activeSubtab === 0) contentHtml = this.renderDevocional();
    else if (this.activeSubtab === 1) contentHtml = this.renderBiblia();
    else if (this.activeSubtab === 2) contentHtml = this.renderLivros();
    else if (this.activeSubtab === 3) contentHtml = this.renderEscola();
    else if (this.activeSubtab === 4) contentHtml = this.renderHinario();

    return `
      <!-- NAVEGAÇÃO DE SUB-ABAS -->
      <div class="subtabs-nav">
        ${pillsHtml}
      </div>

      <!-- CONTEÚDO DA SUB-ABA -->
      <div>
        ${contentHtml}
      </div>
    `;
  }

  mudarSubtab(idx) {
    this.activeSubtab = idx;
    window.app.renderCurrentView();
  }

  // 1. DEVOCIONAL DIÁRIO '365 DIAS NO ALTAR'
  renderDevocional() {
    const dev = DEVOCIONAIS_SEED.find(d => d.dia === this.diaDevocional) || DEVOCIONAIS_SEED[0];

    return `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <!-- Card do Dia & Navegação -->
        <div style="display: flex; align-items: center; justify-content: space-between; background: var(--bg-surface); padding: 10px 14px; border-radius: var(--radius-md); border: 1px solid var(--border-default);">
          <span style="font-size: calc(14px * var(--font-scale)); font-weight: 800; color: var(--secondary-gold);">
            🔥 Dia ${dev.dia} de 365
          </span>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-outlined-gold" style="min-height: 32px; padding: 4px 10px; font-size: 11px;" onclick="window.palavraView.mudarDiaDevocional(-1)">◀ Anterior</button>
            <button class="btn btn-secondary-gold" style="min-height: 32px; padding: 4px 10px; font-size: 11px;" onclick="window.palavraView.mudarDiaDevocional(1)">Próximo ▶</button>
          </div>
        </div>

        <!-- Título do Devocional -->
        <div class="card card-gold">
          <div style="font-size: calc(18px * var(--font-scale)); font-weight: 800; color: var(--text-white);">${dev.titulo}</div>
          <div style="font-size: calc(13px * var(--font-scale)); font-weight: 700; color: var(--secondary-gold);">📖 Versículo Chave • ${dev.versiculo_chave}</div>
          <div style="font-size: calc(14px * var(--font-scale)); font-style: italic; color: var(--text-white); line-height: 1.45; background: var(--bg-dark); padding: 12px; border-radius: var(--radius-sm); border-left: 3px solid var(--secondary-gold);">
            "${dev.texto}"
          </div>
        </div>

        <!-- Reflexão Pastoral -->
        <div class="card">
          <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white);">📖 Reflexão Pastoral</div>
          <div style="font-size: calc(13px * var(--font-scale)); color: var(--text-secondary); line-height: 1.5;">${dev.reflexao}</div>
          
          <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--secondary-gold); margin-top: 6px;">🙏 Oração do Dia</div>
          <div style="font-size: calc(13px * var(--font-scale)); font-style: italic; color: var(--text-white); line-height: 1.45;">"${dev.oracao}"</div>

          <!-- Desafio Prático -->
          <div style="background: var(--bg-surface-alt); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 12px; display: flex; align-items: center; gap: 10px; margin-top: 6px;">
            <span style="font-size: 20px;">💡</span>
            <span style="font-size: calc(12px * var(--font-scale)); font-weight: 600; color: var(--text-white);">
              Desafio de Hoje: ${dev.desafio}
            </span>
          </div>

          <!-- Ações -->
          <div style="display: flex; gap: 8px; margin-top: 6px;">
            <button class="btn btn-secondary-gold" style="flex: 1;" onclick="window.palavraView.tocarDevocionalAudio(${dev.dia})">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
              Ouvir Áudio
            </button>
            <button class="btn btn-green-whatsapp" style="flex: 1;" onclick="window.palavraView.compartilharDevocional(${dev.dia})">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12.04 2c-5.46 0-9.91 4.45-9.91 9.91 0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2z"/></svg>
              WhatsApp
            </button>
          </div>
        </div>
      </div>
    `;
  }

  mudarDiaDevocional(delta) {
    let novo = this.diaDevocional + delta;
    if (novo < 1) novo = DEVOCIONAIS_SEED.length;
    if (novo > DEVOCIONAIS_SEED.length) novo = 1;
    this.diaDevocional = novo;
    window.app.renderCurrentView();
  }

  tocarDevocionalAudio(dia) {
    const dev = DEVOCIONAIS_SEED.find(d => d.dia === dia) || DEVOCIONAIS_SEED[0];
    window.audioService.playTrack({
      title: `Devocional Dia ${dev.dia} - ${dev.titulo}`,
      subtitle: "365 Dias no Altar • IBPM CR",
      url: dev.audio_url,
      artist: "Pastor Presidente"
    });
  }

  compartilharDevocional(dia) {
    const dev = DEVOCIONAIS_SEED.find(d => d.dia === dia) || DEVOCIONAIS_SEED[0];
    const texto = encodeURIComponent(`🔥 *Devocional Diário - 365 Dias no Altar*\n*Dia ${dev.dia}: ${dev.titulo}*\n\n📖 "${dev.texto}" (${dev.versiculo_chave})\n\n💡 *Reflexão:* ${dev.reflexao}\n\n🙏 *Oração:* ${dev.oracao}\n\n*Super-App Oficial IBPM CR*`);
    window.open(`https://wa.me/?text=${texto}`, '_blank');
  }

  // 2. BÍBLIA SAGRADA OFFLINE
  renderBiblia() {
    const versos = (BIBLIA_SEED.capitulos[this.livroAtivo] && BIBLIA_SEED.capitulos[this.livroAtivo][this.capituloAtivo]) 
      || BIBLIA_SEED.capitulos["Salmos"]["23"];

    const versosHtml = versos.map(v => `
      <p style="font-size: calc(15px * var(--font-scale)); line-height: 1.7; color: var(--text-white); margin-bottom: 8px;">
        ${v}
      </p>
    `).join('');

    return `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <div class="card" style="padding: 12px;">
          <div style="display: flex; gap: 8px;">
            <select class="form-select" style="flex: 2;" onchange="window.palavraView.mudarLivroBiblia(this.value)">
              ${BIBLIA_SEED.livros.map(l => `<option value="${l}" ${l === this.livroAtivo ? 'selected' : ''}>${l}</option>`).join('')}
            </select>
            <select class="form-select" style="flex: 1;" onchange="window.palavraView.mudarCapituloBiblia(this.value)">
              <option value="23" ${this.capituloAtivo === '23' ? 'selected' : ''}>Cap. 23</option>
              <option value="91" ${this.capituloAtivo === '91' ? 'selected' : ''}>Cap. 91</option>
              <option value="4" ${this.capituloAtivo === '4' ? 'selected' : ''}>Cap. 4</option>
            </select>
          </div>
        </div>

        <div class="card" style="background: var(--bg-dark); border-color: var(--border-gold); padding: 18px;">
          <div style="font-size: calc(16px * var(--font-scale)); font-weight: 800; color: var(--secondary-gold); margin-bottom: 12px; border-bottom: 1px solid var(--border-default); padding-bottom: 6px;">
            📖 ${this.livroAtivo} • Capítulo ${this.capituloAtivo}
          </div>
          ${versosHtml}
        </div>
      </div>
    `;
  }

  mudarLivroBiblia(livro) {
    this.livroAtivo = livro;
    this.capituloAtivo = livro === "Filipenses" ? "4" : "23";
    window.app.renderCurrentView();
  }

  mudarCapituloBiblia(cap) {
    this.capituloAtivo = cap;
    window.app.renderCurrentView();
  }

  // 3. LIVROS & E-BOOKS
  renderLivros() {
    const livrosHtml = LIVROS_SEED.map(livro => `
      <div class="card" style="display: flex; flex-direction: row; gap: 14px; align-items: center;">
        <img src="${livro.capa}" style="width: 85px; height: 120px; object-fit: cover; border-radius: var(--radius-sm); border: 1px solid var(--secondary-gold);" />
        <div style="flex: 1; display: flex; flex-direction: column; gap: 4px;">
          <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white);">${livro.titulo}</div>
          <div style="font-size: calc(11px * var(--font-scale)); color: var(--secondary-gold); font-weight: 600;">${livro.subtitulo}</div>
          <div style="font-size: calc(11px * var(--font-scale)); color: var(--text-muted); line-height: 1.3;">${livro.sinopse.substring(0, 90)}...</div>
          <button class="btn btn-secondary-gold" style="min-height: 36px; padding: 6px 12px; margin-top: 6px; font-size: calc(11px * var(--font-scale));" onclick="alert('📖 Abrindo E-book Oficial: ${livro.titulo}')">
            📥 Baixar / Ler E-book PDF
          </button>
        </div>
      </div>
    `).join('');

    return `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white);">
          E-books e Livros Oficiais do Pastor
        </div>
        ${livrosHtml}
      </div>
    `;
  }

  // 4. ESCOLA DE LÍDERES
  renderEscola() {
    const mod = ESCOLA_SEED[0];

    const quizHtml = mod.quiz.map((q, qIdx) => {
      const respEscolhida = this.quizRespostas[qIdx];
      return `
        <div style="background: var(--bg-dark); padding: 12px; border-radius: var(--radius-md); border: 1px solid var(--border-default); margin-top: 8px;">
          <div style="font-size: calc(13px * var(--font-scale)); font-weight: 700; color: var(--text-white); margin-bottom: 8px;">
            ${qIdx + 1}. ${q.pergunta}
          </div>
          <div style="display: flex; flex-direction: column; gap: 6px;">
            ${q.opcoes.map((op, opIdx) => {
              let btnClass = 'btn-outlined-gold';
              if (respEscolhida !== undefined) {
                if (opIdx === q.correta) btnClass = 'btn-green-whatsapp';
                else if (respEscolhida === opIdx) btnClass = 'btn-primary-rubi';
              }
              return `
                <button class="btn ${btnClass}" style="min-height: 38px; justify-content: flex-start; text-align: left; padding: 8px 12px; font-size: calc(12px * var(--font-scale));" onclick="window.palavraView.responderQuiz(${qIdx}, ${opIdx})">
                  ${op}
                </button>
              `;
            }).join('')}
          </div>
          ${respEscolhida !== undefined ? `
            <div style="font-size: calc(11px * var(--font-scale)); color: ${respEscolhida === q.correta ? 'var(--accent-green)' : 'var(--danger)'}; margin-top: 6px; font-weight: 700;">
              ${respEscolhida === q.correta ? '✅ Correto!' : '❌ Incorreto.'} ${q.explicacao}
            </div>
          ` : ''}
        </div>
      `;
    }).join('');

    return `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <div class="card card-rubi">
          <span class="badge-gold" style="align-self: flex-start;">MÓDULO ${mod.numero} DE 52</span>
          <div style="font-size: calc(16px * var(--font-scale)); font-weight: 800; color: var(--text-white);">${mod.titulo}</div>
          <div style="font-size: calc(12px * var(--font-scale)); color: var(--secondary-gold); font-weight: 600;">Tema: ${mod.tema}</div>
          <div style="font-size: calc(13px * var(--font-scale)); color: var(--text-secondary); line-height: 1.5; margin-top: 4px;">
            ${mod.conteudo}
          </div>
        </div>

        <div class="card">
          <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--secondary-gold);">
            ✍️ Quiz de Fixação Pastoral
          </div>
          ${quizHtml}
        </div>
      </div>
    `;
  }

  responderQuiz(qIdx, opIdx) {
    this.quizRespostas[qIdx] = opIdx;
    window.app.renderCurrentView();
  }

  // 5. COLETÂNEA DE LOUVORES & HINÁRIO
  renderHinario() {
    const filtrados = LOUVORES_SEED.filter(l => 
      l.titulo.toLowerCase().includes(this.buscaLouvor.toLowerCase()) || 
      l.numero.toString().includes(this.buscaLouvor)
    );

    const louvoresHtml = filtrados.map(louvor => `
      <div class="card" style="padding: 14px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <div style="font-size: calc(15px * var(--font-scale)); font-weight: 800; color: var(--text-white);">
            ${louvor.titulo}
          </div>
          <span class="badge-gold">Nº ${louvor.numero}</span>
        </div>
        <div style="font-size: calc(11px * var(--font-scale)); color: var(--text-muted);">${louvor.autor}</div>
        <div style="font-size: calc(12px * var(--font-scale)); color: var(--text-secondary); line-height: 1.5; font-style: italic; background: var(--bg-dark); padding: 10px; border-radius: var(--radius-sm); margin-top: 4px;">
          "${louvor.letra}"
        </div>
      </div>
    `).join('');

    return `
      <div style="display: flex; flex-direction: column; gap: 12px;">
        <div class="card" style="padding: 10px;">
          <input type="text" class="form-input" placeholder="🔍 Buscar louvor por título ou número..." value="${this.buscaLouvor}" oninput="window.palavraView.buscarLouvor(this.value)" />
        </div>
        ${louvoresHtml}
      </div>
    `;
  }

  buscarLouvor(query) {
    this.buscaLouvor = query;
    window.app.renderCurrentView();
  }
}

window.palavraView = new PalavraView();
