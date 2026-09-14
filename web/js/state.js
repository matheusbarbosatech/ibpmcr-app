/**
 * Gerenciador de Estado e Sementes de Dados - IBPM CR WebApp PWA
 * Mantém sincronização offline com LocalStorage.
 */

const CHURCH_CONFIG = {
  name: "Igreja Batista Pentecostal Mundial",
  subname: "Carvalho Ramos / Campo Grande - RJ",
  address: "Rua Carvalho Ramos, Campo Grande, Rio de Janeiro - RJ",
  mapsUrl: "https://maps.google.com/?q=Rua+Carvalho+Ramos+Campo+Grande+RJ",
  pixKey: "21964314284",
  pixName: "IGREJA BATISTA PENTECOSTAL MUNDIAL",
  pixCity: "RIO DE JANEIRO",
  whatsappSecretaria: "5521964314284",
  whatsappIntercessao: "5521989913903",
  youtubeLiveUrl: "https://www.youtube.com/@ibpmcr/live",
  radioStreamUrl: "https://stream.zeno.fm/f3wvbbqmdg8uv", // Stream de rádio cristã / hinos
  audioPilulaDefault: "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/audios/devocionais/devocional_001.mp3"
};

// 1. Devocionais Diários (365 Dias no Altar)
const DEVOCIONAIS_SEED = [
  {
    id: 1,
    dia: 1,
    titulo: "O Fogo Nunca se Apagará",
    livro: "Levítico",
    versiculo_chave: "Lv 6:13",
    texto: "O fogo arderá continuamente sobre o altar; não se apagará.",
    reflexao: "O altar do Senhor em nosso coração requer lenha diária. Não viva das experiências de ontem. Apresente-se hoje diante de Deus com oração fervorosa.",
    oracao: "Senhor, renova a chama do Teu Espírito em mim. Não permitas que a frieza do mundo apague o Teu fogo no meu peito. Amém.",
    desafio: "Separe 15 minutos hoje em silêncio absoluto com a Bíblia aberta.",
    audio_url: "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/audios/devocionais/devocional_001.mp3"
  },
  {
    id: 2,
    dia: 2,
    titulo: "Força na Fraqueza",
    livro: "2 Coríntios",
    versiculo_chave: "2Co 12:9",
    texto: "A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza.",
    reflexao: "Quando reconhecemos que não conseguimos sozinhos, o poder de Cristo repousa sobre nós. Sua fraqueza não é o seu fim; é o cenário do milagre de Deus.",
    oracao: "Pai Celestial, entrego minha fraqueza e cansaço em Tuas mãos. Que a Tua força se manifeste na minha vida hoje. Amém.",
    desafio: "Não reclame das suas limitações hoje; glorifique a Deus por sustentá-lo.",
    audio_url: "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/audios/devocionais/devocional_002.mp3"
  },
  {
    id: 3,
    dia: 3,
    titulo: "A Paz que Guarda a Mente",
    livro: "Filipenses",
    versiculo_chave: "Fp 4:7",
    texto: "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações.",
    reflexao: "Em tempos de ansiedade, o Senhor não nos promete ausência de tempestades, mas a Sua paz como uma fortaleza protegendo nossos pensamentos.",
    oracao: "Jesus, acalma meu coração angustiado. Liberta minha mente de pensamentos de medo e ansiedade. Tua paz é o meu refúgio. Amém.",
    desafio: "Respire fundo, ore 3 vezes ao longo do dia e entregue o futuro a Deus.",
    audio_url: "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/audios/devocionais/devocional_003.mp3"
  },
  {
    id: 4,
    dia: 4,
    titulo: "Deus Não Se Esqueceu de Você",
    livro: "Isaías",
    versiculo_chave: "Is 49:15",
    texto: "Pode uma mulher esquecer-se do seu filho que ainda mama? Todavia eu não me esquecerei de ti.",
    reflexao: "Mesmo que você se sinta invisível na multidão ou abandonado pelos que ama, nas palmas das mãos do Pai o seu nome está gravado para sempre.",
    oracao: "Meu Pai querido, obrigado por Teu amor eterno. Quando a solidão bater, lembra-me de que nunca estive só. Amém.",
    desafio: "Ligue para alguém da família ou envie uma mensagem de encorajamento.",
    audio_url: "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/audios/devocionais/devocional_004.mp3"
  },
  {
    id: 5,
    dia: 5,
    titulo: "O Banquete no Deserto",
    livro: "Salmos",
    versiculo_chave: "Sl 23:5",
    texto: "Preparas uma mesa perante mim na presença dos meus inimigos, unges a minha cabeça com óleo.",
    reflexao: "Deus não apenas livra você; Ele o honra no mesmo lugar onde tentaram envergonhá-lo. O banquete da graça é servido na presença de qualquer oposição.",
    oracao: "Senhor, unges minha cabeça com o óleo da alegria. Eu declaro que meu cálice transborda da Tua presença e favor. Amém.",
    desafio: "Agradeça a Deus por três livramentos que Ele já operou na sua história.",
    audio_url: "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/audios/devocionais/devocional_005.mp3"
  }
];

// 2. Frases Proféticas
const FRASES_SEED = [
  { id: 1, frase: "A tempestade que você enfrenta hoje não veio para te afundar, veio para te ensinar a andar sobre as águas.", tag: "ansiedade", ref: "Mt 14:29" },
  { id: 2, frase: "O medo olha para o tamanho do gigante; a fé olha para o tamanho do Deus que derruba o gigante.", tag: "medo", ref: "1Sm 17:45" },
  { id: 3, frase: "Deus trabalha no silêncio. Enquanto você chora no altar, Ele já está dando a ordem da sua vitória.", tag: "desanimo", ref: "Sl 126:5" },
  { id: 4, frase: "A gratidão abre as comportas do céu. Quem louva no pouco será colocado sobre o muito.", tag: "gratidao", ref: "1Ts 5:18" },
  { id: 5, frase: "Não limite o agir de Deus pelo que seus olhos naturais estão vendo. O invisível de Deus já começou a se mover.", tag: "fe", ref: "Hb 11:1" },
  { id: 6, frase: "Você não nasceu para ficar caído na beira do caminho. Levante-se, porque a unção de Deus é sobre a sua casa!", tag: "vitoria", ref: "Is 60:1" },
  { id: 7, frase: "O que o inimigo armou contra você se tornará o palco da maior reviravolta da sua vida.", tag: "vitoria", ref: "Gn 50:20" },
  { id: 8, frase: "Descanse o seu coração. Nenhuma oração sincera bate no teto e volta; todas sobem ao trono do Pai.", tag: "ansiedade", ref: "Ap 8:4" }
];

// 3. Eventos da Igreja
const EVENTOS_SEED = [
  {
    id: 1,
    titulo: "Retiro Face a Face com Deus",
    slogan: "Um Encontro de Coração Ardente!",
    data: "20 a 22 de Outubro de 2026",
    local: "Rua Punta Del Este, 18, Campo Grande - RJ",
    descricao: "Três dias de imersão espiritual profunda, cura interior, quebra de maldições e renovo pentecostal. Venha viver um divisor de águas na sua história!",
    valor_inscricao: 150.0,
    valor_camisa: 45.0,
    imagem_url: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=800",
    link_maps: "https://maps.google.com/?q=Rua+Punta+Del+Este+18+Campo+Grande+RJ"
  }
];

// 4. Produtos da Lojinha & Cantina
const PRODUTOS_SEED = [
  {
    id: 1,
    nome: "Camisa Oficial - Retiro Face a Face",
    categoria: "Vestuário",
    preco: 45.00,
    descricao: "Camisa 100% algodão penteado premium com a estampa oficial do Retiro Face a Face com Deus.",
    imagem: "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500",
    tamanhos: ["P", "M", "G", "GG", "XGG"]
  },
  {
    id: 2,
    nome: "Quentinha Especial de Domingo (Cantina)",
    categoria: "Cantina",
    preco: 25.00,
    descricao: "Almoço completo caseiro com churrasco misto, arroz, farofa e vinagrete. Retire na cantina após o culto!",
    imagem: "https://images.unsplash.com/photo-1544025162-d76694265947?w=500"
  },
  {
    id: 3,
    nome: "Kit 3 Livros Físicos do Pastor Anderson",
    categoria: "Livros",
    preco: 60.00,
    descricao: "Os 3 livros oficiais impressos em capa luxo: Vitória na Família, Guerra Espiritual e Fundamentos da Fé.",
    imagem: "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500"
  },
  {
    id: 4,
    nome: "Caneca Porcelana Oficial IBPM CR",
    categoria: "Lembranças",
    preco: 30.00,
    descricao: "Caneca resinada de alta durabilidade com o brasão oficial da Igreja Batista Pentecostal Mundial.",
    imagem: "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500"
  },
  {
    id: 5,
    nome: "Bolo & Refrigerante da Cantina",
    categoria: "Cantina",
    preco: 12.00,
    descricao: "Fatia generosa de bolo confeitado artesanal acompanhado de refrigerante gelado.",
    imagem: "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500"
  }
];

// 5. Livros & E-books
const LIVROS_SEED = [
  {
    id: 1,
    titulo: "Vitória na Família",
    subtitulo: "Princípios Inabaláveis para Restaurar o seu Lar",
    capa: "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600",
    sinopse: "Um guia prático e espiritual com 12 capítulos para transformar conflitos em bênçãos, curar feridas no casamento e proteger os filhos.",
    capitulos: 12
  },
  {
    id: 2,
    titulo: "Guerra Espiritual",
    subtitulo: "As Armas Poderosas para Vencer as Batalhas Invisíveis",
    capa: "https://images.unsplash.com/photo-1507692049790-de58290a4334?w=600",
    sinopse: "Descubra as estratégias bíblicas de autoridade e oração para desbaratar as armadilhas das trevas e andar em vitória contínua.",
    capitulos: 12
  },
  {
    id: 3,
    titulo: "Fundamentos da Fé",
    subtitulo: "Da Conversão ao Discipulado de Alto Impacto",
    capa: "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=600",
    sinopse: "As doutrinas essenciais da vida cristã explicadas com profundidade e simplicidade pastoral para todo discípulo de Cristo.",
    capitulos: 12
  }
];

// 6. Escola de Líderes (Módulos & Quiz)
const ESCOLA_SEED = [
  {
    id: 1,
    numero: 1,
    titulo: "O Caráter do Líder Servo",
    tema: "Liderança Bíblica",
    conteudo: "O verdadeiro líder do Reino de Deus não busca palcos ou títulos para ser servido; busca toalhas e bacias para lavar os pés dos discípulos, seguindo o exemplo de Jesus Cristo na última ceia.",
    quiz: [
      { pergunta: "Qual é a lenha diária do altar do líder?", opcoes: ["Oração e Jejum", "Falar bem em público", "Estar no palco"], correta: 0, explicacao: "A oração e o jejum mantêm o altar espiritual aquecido continuamente." },
      { pergunta: "O líder cristão lidera prioritariamente pelo:", opcoes: ["Medo e imposição", "Exemplo e Serviço", "Título e cargo"], correta: 1, explicacao: "Jesus nos ensinou que o maior no Reino é o que serve." }
    ]
  },
  {
    id: 2,
    numero: 2,
    titulo: "A Visão de Células Multiplicadoras",
    tema: "Discipulado e Crescimento",
    conteudo: "As reuniões nos lares foram a chave da igreja primitiva no livro de Atos. O pastoreio próximo gera comunhão, cuidado pastoral aos enfermos e multiplicação saudável.",
    quiz: [
      { pergunta: "Onde a igreja primitiva mais se reunia?", opcoes: ["Em templos suntuosos", "Nos lares e no templo", "Apenas no deserto"], correta: 1, explicacao: "Atos 5:42 relata que diariamente no templo e de casa em casa proclamavam a Palavra." }
    ]
  }
];

// 7. Galeria de Fotos dos Cultos
const FOTOS_SEED = [
  {
    id: 1,
    album: "Domingo de Celebração - Santa Ceia",
    data: "06/09/2026",
    categoria: "Santa Ceia",
    foto: "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200",
    downloads: 87
  },
  {
    id: 2,
    album: "Conferência de Jovens Coração Ardente",
    data: "29/08/2026",
    categoria: "Conferência",
    foto: "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=1200",
    downloads: 142
  },
  {
    id: 3,
    album: "Batismo nas Águas - Vida Nova",
    data: "16/08/2026",
    categoria: "Batismo",
    foto: "https://images.unsplash.com/photo-1507692049790-de58290a4334?w=1200",
    downloads: 215
  },
  {
    id: 4,
    album: "Quinta Profética de Milagres",
    data: "03/09/2026",
    categoria: "Culto",
    foto: "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1200",
    downloads: 63
  }
];

// 8. Cortes Verticais (Shorts 9:16)
const SHORTS_SEED = [
  {
    id: 1,
    titulo: "JESUS FUNCIONA COMO UM ESPELHO QUE MOSTRA QUEM VOCÊ É",
    categoria: "Revelação",
    video_url: "https://assets.mixkit.co/videos/preview/mixkit-clouds-and-blue-sky-2408-large.mp4",
    duracao: "0:45",
    shares: 154,
    viral_score: 94
  },
  {
    id: 2,
    titulo: "QUANDO VOCÊ ENTREGA SUA DOR NO ALTAR, DEUS TRANSFORMA EM UNÇÃO",
    categoria: "Cura",
    video_url: "https://assets.mixkit.co/videos/preview/mixkit-sun-shining-through-the-trees-1189-large.mp4",
    duracao: "0:38",
    shares: 240,
    viral_score: 96
  },
  {
    id: 3,
    titulo: "O INIMIGO QUER QUE VOCÊ DESISTA HOJE, MAS O SEU MILAGRE VEM AMANHÃ",
    categoria: "Guerra Espiritual",
    video_url: "https://assets.mixkit.co/videos/preview/mixkit-waves-in-the-water-1164-large.mp4",
    duracao: "0:52",
    shares: 310,
    viral_score: 98
  }
];

// 9. Pedidos de Oração Iniciais
const PEDIDOS_SEED = [
  {
    id: "ped-1",
    nome: "Maria Aparecida (67 anos)",
    motivo: "Saúde & Cura",
    detalhes: "Peço oração pelos exames do coração do meu esposo João e pela paz na nossa casa.",
    anonimo: false,
    orando_count: 14,
    data: "Hoje"
  },
  {
    id: "ped-2",
    nome: "Anônimo",
    motivo: "Causas na Justiça",
    detalhes: "Estou passando por uma causa trabalhista injusta há 2 anos. Peço um milagre da justiça de Deus.",
    anonimo: true,
    orando_count: 28,
    data: "Ontem"
  },
  {
    id: "ped-3",
    nome: "Lucas Gabriel (28 anos)",
    motivo: "Paz na Mente / Ansiedade",
    detalhes: "Me sinto sobrecarregado e com o peito apertado. Peço apenas que a igreja ore por mim em silêncio.",
    anonimo: false,
    orando_count: 42,
    data: "Há 2 dias"
  },
  {
    id: "ped-4",
    nome: "Família Silva",
    motivo: "Libertação Espiritual",
    detalhes: "Oração pelo meu filho mais velho voltar para os caminhos do Senhor.",
    anonimo: false,
    orando_count: 19,
    data: "Há 3 dias"
  }
];

// 10. Coletânea de Louvores / Hinário
const LOUVORES_SEED = [
  { id: 1, titulo: "Porque Ele Vive", numero: 545, autor: "Harpa Cristã", letra: "Deus enviou Seu Filho amado / Para morrer em meu lugar / Na cruz pagou por meus pecados / Mas o sepulcro vazio está porque Ele vive!" },
  { id: 2, titulo: "Grandioso És Tu", numero: 526, autor: "Hinário", letra: "Senhor meu Deus, quando eu maravilhado / Fico a pensar nas obras de Tuas mãos / No céu azul de estrelas pontilhado / O Teu poder mostrando a criação..." },
  { id: 3, titulo: "Em Fervente Oração", numero: 577, autor: "Harpa Cristã", letra: "Em fervente oração, vem o teu coração / Na presença de Deus derramar / Mas não podes pedir, nem ousar prosseguir / Sem que tudo no altar venhas pôr!" }
];

// 11. Bíblia Rápida
const BIBLIA_SEED = {
  livros: ["Gênesis", "Salmos", "Provérbios", "Isaías", "Mateus", "João", "Romanos", "Filipenses", "Apocalipse"],
  capitulos: {
    "Salmos": {
      "23": [
        "1 O Senhor é o meu pastor, nada me faltará.",
        "2 Deitar-me faz em verdes pastos, guia-me mansamente a águas tranqüilas.",
        "3 Refrigera a minha alma; guia-me pelas veredas da justiça, por amor do seu nome.",
        "4 Ainda que eu andasse pelo vale da sombra da morte, não temeria mal algum, porque tu estás comigo; a tua vara e o teu cajado me consolam.",
        "5 Preparas uma mesa perante mim na presença dos meus inimigos, unges a minha cabeça com óleo, o meu cálice transborda.",
        "6 Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida; e habitarei na casa do Senhor por longos dias."
      ],
      "91": [
        "1 Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará.",
        "2 Direi do Senhor: Ele é o meu Deus, o meu refúgio, a minha fortaleza, e nele confiarei.",
        "3 Porque ele te livrará do laço do passarinheiro, e da peste perniciosa.",
        "4 Ele te cobrirá com as suas penas, e debaixo das suas asas te confiarás; a sua verdade será o teu escudo e broquel."
      ]
    },
    "Filipenses": {
      "4": [
        "4 Regozijai-vos sempre no Senhor; outra vez digo, regozijai-vos.",
        "6 Não estejais inquietos por coisa alguma; antes as vossas petições sejam em tudo conhecidas diante de Deus pela oração e súplica, com ação de graças.",
        "7 E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentimentos em Cristo Jesus.",
        "13 Posso todas as coisas em Cristo que me fortalece."
      ]
    }
  }
};

/**
 * Classe AppStore: Gerencia LocalStorage e Estado Global
 */
class AppStore {
  constructor() {
    this.init();
  }

  init() {
    // 1. Escala de Fonte (Acessibilidade Sênior)
    if (!localStorage.getItem('ibpm_font_scale')) {
      localStorage.setItem('ibpm_font_scale', '1.0');
    }

    // 2. Pedidos de Oração
    if (!localStorage.getItem('ibpm_pedidos_oracao')) {
      localStorage.setItem('ibpm_pedidos_oracao', JSON.stringify(PEDIDOS_SEED));
    }

    // 3. IDs dos pedidos em que o usuário clicou "Estou Orando"
    if (!localStorage.getItem('ibpm_minhas_oracoes')) {
      localStorage.setItem('ibpm_minhas_oracoes', JSON.stringify([]));
    }

    // 4. Carrinho da Lojinha
    if (!localStorage.getItem('ibpm_carrinho')) {
      localStorage.setItem('ibpm_carrinho', JSON.stringify([]));
    }
  }

  // Escala de Fonte
  getFontScale() {
    return parseFloat(localStorage.getItem('ibpm_font_scale') || '1.0');
  }

  setFontScale(scale) {
    localStorage.setItem('ibpm_font_scale', scale.toString());
    document.documentElement.style.setProperty('--font-scale', scale.toString());
  }

  // Pedidos de Oração
  getPedidos() {
    return JSON.parse(localStorage.getItem('ibpm_pedidos_oracao') || '[]');
  }

  adicionarPedido(nome, motivo, detalhes, isAnonimo) {
    const pedidos = this.getPedidos();
    const novo = {
      id: 'ped-' + Date.now(),
      nome: isAnonimo ? 'Anônimo' : (nome || 'Irmão(ã) em Cristo'),
      motivo: motivo || 'Intercessão Geral',
      detalhes: detalhes,
      anonimo: isAnonimo,
      orando_count: 1,
      data: 'Agora'
    };
    pedidos.unshift(novo);
    localStorage.setItem('ibpm_pedidos_oracao', JSON.stringify(pedidos));
    return novo;
  }

  incrementarOrando(pedidoId) {
    const pedidos = this.getPedidos();
    const minhas = this.getMinhasOracoes();
    
    let isAdded = false;
    if (minhas.includes(pedidoId)) {
      // Já orou: pode manter ou desmarcar
      return false;
    } else {
      minhas.push(pedidoId);
      localStorage.setItem('ibpm_minhas_oracoes', JSON.stringify(minhas));
      
      const ped = pedidos.find(p => p.id === pedidoId);
      if (ped) {
        ped.orando_count = (ped.orando_count || 0) + 1;
        localStorage.setItem('ibpm_pedidos_oracao', JSON.stringify(pedidos));
      }
      return true;
    }
  }

  getMinhasOracoes() {
    return JSON.parse(localStorage.getItem('ibpm_minhas_oracoes') || '[]');
  }
}

window.store = new AppStore();
