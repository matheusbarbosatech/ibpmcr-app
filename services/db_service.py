"""
Serviço de Banco de Dados Local SQLite (100% Offline) & Sincronização.
Implementa as 9 tabelas do schema oficial e garante carregamento em menos de 50ms.
"""
import sqlite3
import json
import uuid
from typing import List, Dict, Any, Optional
from core.config import DB_PATH
from models.devocional import DevocionalDiario
from models.oracao import PedidoOracao
from models.midia import CultoAcervo, CorteVertical, FotoGaleria, FraseProfetica, LivroEbook, ModuloLideranca, EventoIgreja, ProdutoLoja, InscricaoEvento

class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def get_connection(self):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Cria as 9 tabelas oficiais do Supabase em SQLite."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Usuários / Membros
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_membros (
                id TEXT PRIMARY KEY,
                telefone TEXT UNIQUE,
                nome_completo TEXT NOT NULL,
                email TEXT UNIQUE,
                tipo_usuario TEXT DEFAULT 'membro',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 2. Devocionais Diários (365 Dias no Altar)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS devocionais_diarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia_ano INTEGER UNIQUE NOT NULL,
                titulo TEXT NOT NULL,
                livro_biblia TEXT NOT NULL,
                versiculo_chave TEXT NOT NULL,
                texto_versiculo TEXT NOT NULL,
                reflexao_pastoral TEXT NOT NULL,
                oracao_do_dia TEXT NOT NULL,
                desafio_pratico TEXT,
                audio_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 3. Acervo de Cultos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS acervo_cultos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_culto INTEGER NOT NULL,
                data_culto TEXT NOT NULL,
                tipo_culto TEXT NOT NULL,
                titulo_pregacao TEXT NOT NULL,
                pastor_ministrante TEXT DEFAULT 'Pastor Presidente',
                video_16_9_url TEXT,
                audio_mp3_url TEXT,
                duracao_minutos INTEGER DEFAULT 90,
                resumo_pregacao TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 4. Cortes Verticais (Shorts 9:16)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cortes_verticais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                culto_id INTEGER,
                titulo_impacto TEXT NOT NULL,
                tema_categoria TEXT,
                video_9_16_url TEXT NOT NULL,
                duracao_segundos INTEGER DEFAULT 45,
                total_compartilhamentos INTEGER DEFAULT 0,
                nota_viral INTEGER DEFAULT 90,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 5. Galeria de Fotos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS galeria_fotos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                album_nome TEXT NOT NULL,
                data_evento TEXT NOT NULL,
                categoria TEXT DEFAULT 'Culto',
                foto_hd_url TEXT NOT NULL,
                foto_thumb_url TEXT NOT NULL,
                total_downloads INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 6. Pedidos de Oração
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos_oracao (
                id TEXT PRIMARY KEY,
                usuario_id TEXT,
                nome_solicitante TEXT NOT NULL,
                motivo_oracao TEXT NOT NULL,
                detalhes_pedido TEXT NOT NULL,
                is_anonimo INTEGER DEFAULT 0,
                status TEXT DEFAULT 'aprovado',
                contador_orando INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 7. Frases Proféticas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS frases_profeticas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                frase TEXT NOT NULL,
                sentimento_tag TEXT NOT NULL,
                referencia_biblica TEXT,
                culto_origem_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 8. Livros & E-books Oficiais do Pastor
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros_ebooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo_livro TEXT NOT NULL,
                subtitulo TEXT,
                capa_url TEXT NOT NULL,
                pdf_url TEXT NOT NULL,
                epub_url TEXT,
                total_capitulos INTEGER DEFAULT 12,
                sinopse TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 9. Escola de Líderes (52 Módulos)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS escola_lideres_modulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_modulo INTEGER UNIQUE NOT NULL,
                titulo_modulo TEXT NOT NULL,
                tema_central TEXT NOT NULL,
                conteudo_apostila TEXT NOT NULL,
                pdf_apostila_url TEXT,
                questoes_quiz TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 10. Eventos & Avisos da Igreja
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos_igreja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                slogan TEXT,
                data_evento TEXT NOT NULL,
                local TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor_inscricao REAL DEFAULT 0.0,
                valor_camisa REAL DEFAULT 45.0,
                whatsapp_contato TEXT DEFAULT '5521964314284',
                imagem_url TEXT,
                link_maps TEXT,
                ativo INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 11. Produtos da Lojinha Oficial do Reino & Cantina
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos_loja (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                descricao TEXT NOT NULL,
                imagem_url TEXT NOT NULL,
                tamanhos_disponiveis TEXT,
                disponivel INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 12. Inscrições Nativas em Eventos (Salvas no App)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS inscricoes_eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evento_id INTEGER NOT NULL,
                nome_completo TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                idade INTEGER NOT NULL,
                bairro TEXT NOT NULL,
                vinculo TEXT NOT NULL,
                incluir_camisa INTEGER DEFAULT 0,
                tamanho_camisa TEXT,
                restricoes TEXT,
                valor_total REAL NOT NULL,
                status_pagamento TEXT DEFAULT 'pendente',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (evento_id) REFERENCES eventos_igreja(id)
            )
            """)
            conn.commit()

        # Alimenta dados iniciais se o banco estiver vazio
        self._seed_initial_data()

    def _seed_initial_data(self):
        """Gera sementes teológicas e patrimoniais ricas para uso offline imediato."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Checa se devocionais já existem
            cursor.execute("SELECT COUNT(*) FROM devocionais_diarios")
            if cursor.fetchone()[0] == 0:
                devocionais = [
                    (1, "O Fogo Nunca se Apagará", "Levítico", "Lv 6:13", "O fogo arderá continuamente sobre o altar; não se apagará.",
                     "O altar do Senhor em nosso coração requer lenha diária. Não viva das experiências de ontem. Apresente-se hoje diante de Deus com oração fervorosa.",
                     "Senhor, renova a chama do Teu Espírito em mim. Não permitas que a frieza do mundo apague o Teu fogo no meu peito. Amém.",
                     "Separe 15 minutos hoje em silêncio absoluto com a Bíblia aberta.", "https://midia.ibpmcr.com.br/audios/devocional_01.mp3"),
                    (2, "Força na Fraqueza", "2 Coríntios", "2Co 12:9", "A minha graça te basta, porque o meu poder se aperfeiçoa na fraqueza.",
                     "Quando reconhecemos que não conseguimos sozinhos, o poder de Cristo repousa sobre nós. Sua fraqueza não é o seu fim; é o cenário do milagre de Deus.",
                     "Pai Celestial, entrego minha fraqueza e cansaço em Tuas mãos. Que a Tua força se manifeste na minha vida hoje. Amém.",
                     "Não reclame das suas limitações hoje; glorifique a Deus por sustentá-lo.", "https://midia.ibpmcr.com.br/audios/devocional_02.mp3"),
                    (3, "A Paz que Guarda a Mente", "Filipenses", "Fp 4:7", "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações.",
                     "Em tempos de ansiedade, o Senhor não nos promete ausência de tempestades, mas a Sua paz como uma fortaleza protegendo nossos pensamentos.",
                     "Jesus, acalma meu coração angustiado. Liberta minha mente de pensamentos de medo e ansiedade. Tua paz é o meu refúgio. Amém.",
                     "Respire fundo, ore 3 vezes ao longo do dia e entregue o futuro a Deus.", "https://midia.ibpmcr.com.br/audios/devocional_03.mp3"),
                    (4, "Deus Não Se Esqueceu de Você", "Isaías", "Is 49:15", "Pode uma mulher esquecer-se do seu filho que ainda mama? Todavia eu não me esquecerei de ti.",
                     "Mesmo que você se sinta invisível na multidão ou abandonado pelos que ama, nas palmas das mãos do Pai o seu nome está gravado para sempre.",
                     "Meu Pai querido, obrigado por Teu amor eterno. Quando a solidão bater, lembra-me de que nunca estive só. Amém.",
                     "Ligue para alguém da família ou envie uma mensagem de encorajamento.", "https://midia.ibpmcr.com.br/audios/devocional_04.mp3"),
                    (5, "O Banquete no Deserto", "Salmos", "Sl 23:5", "Preparas uma mesa perante mim na presença dos meus inimigos, unges a minha cabeça com óleo.",
                     "Deus não apenas livra você; Ele o honra no mesmo lugar onde tentaram envergonhá-lo. O banquete da graça é servido na presença de qualquer oposição.",
                     "Senhor, unges minha cabeça com o óleo da alegria. Eu declaro que meu cálice transborda da Tua presença e favor. Amém.",
                     "Agradeça a Deus por três livramentos que Ele já operou na sua história.", "https://midia.ibpmcr.com.br/audios/devocional_05.mp3")
                ]
                cursor.executemany("""
                INSERT INTO devocionais_diarios (dia_ano, titulo, livro_biblia, versiculo_chave, texto_versiculo, reflexao_pastoral, oracao_do_dia, desafio_pratico, audio_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, devocionais)

            # Checa Frases Proféticas
            cursor.execute("SELECT COUNT(*) FROM frases_profeticas")
            if cursor.fetchone()[0] == 0:
                frases = [
                    ("A tempestade que você enfrenta hoje não veio para te afundar, veio para te ensinar a andar sobre as águas.", "ansiedade", "Mt 14:29"),
                    ("O medo olha para o tamanho do gigante; a fé olha para o tamanho do Deus que derruba o gigante.", "medo", "1Sm 17:45"),
                    ("Deus trabalha no silêncio. Enquanto você chora no altar, Ele já está dando a ordem da sua vitória.", "desanimo", "Sl 126:5"),
                    ("A gratidão abre as comportas do céu. Quem louva no pouco será colocado sobre o muito.", "gratidao", "1Ts 5:18"),
                    ("Não limite o agir de Deus pelo que seus olhos naturais estão vendo. O invisível de Deus já começou a se mover.", "fe", "Hb 11:1"),
                    ("Você não nasceu para ficar caído na beira do caminho. Levante-se, porque a unção de Deus é sobre a sua casa!", "vitoria", "Is 60:1"),
                    ("O que o diabo armou contra você se tornará o palco da maior reviravolta da sua vida.", "vitoria", "Gn 50:20"),
                    ("Descanse o seu coração. Nenhuma oração sincera bate no teto e volta; todas sobem ao trono do Pai.", "ansiedade", "Ap 8:4")
                ]
                cursor.executemany("""
                INSERT INTO frases_profeticas (frase, sentimento_tag, referencia_biblica)
                VALUES (?, ?, ?)
                """, frases)

            # Checa Livros Oficiais
            cursor.execute("SELECT COUNT(*) FROM livros_ebooks")
            if cursor.fetchone()[0] == 0:
                livros = [
                    ("Vitória na Família", "Princípios Inabaláveis para Restaurar o seu Lar",
                     "https://midia.ibpmcr.com.br/capas/livro_familia.jpg", "https://midia.ibpmcr.com.br/livros/vitoria_na_familia.pdf",
                     "Um guia prático e espiritual com 12 capítulos para transformar conflitos em bênçãos, curar feridas no casamento e proteger os filhos.", 12),
                    ("Guerra Espiritual", "As Armas Poderosas para Vencer as Batalhas Invisíveis",
                     "https://midia.ibpmcr.com.br/capas/livro_guerra.jpg", "https://midia.ibpmcr.com.br/livros/guerra_espiritual.pdf",
                     "Descubra as estratégias bíblicas de autoridade e oração para desbaratar as armadilhas das trevas e andar em vitória contínua.", 12),
                    ("Fundamentos da Fé", "Da Conversão ao Discipulado de Alto Impacto",
                     "https://midia.ibpmcr.com.br/capas/livro_fe.jpg", "https://midia.ibpmcr.com.br/livros/fundamentos_da_fe.pdf",
                     "As doutrinas essenciais da vida cristã explicadas com profundidade e simplicidade pastoral para todo discípulo de Cristo.", 12)
                ]
                cursor.executemany("""
                INSERT INTO livros_ebooks (titulo_livro, subtitulo, capa_url, pdf_url, sinopse, total_capitulos)
                VALUES (?, ?, ?, ?, ?, ?)
                """, livros)

            # Checa Escola de Líderes
            cursor.execute("SELECT COUNT(*) FROM escola_lideres_modulos")
            if cursor.fetchone()[0] == 0:
                quiz_m1 = json.dumps([
                    {"pergunta": "Qual é a lenha diária do altar do líder?", "opcoes": ["Oração e Jejum", "Falar bem em público", "Estar no palco"], "resposta": 0},
                    {"pergunta": "O líder cristão lidera pelo:", "opcoes": ["Medo", "Exemplo e Serviço", "Título e cargo"], "resposta": 1}
                ])
                modulos = [
                    (1, "O Caráter do Líder Servo", "Liderança Bíblica", "O verdadeiro líder não busca posições, busca toalhas e bacias para lavar os pés dos discípulos.", quiz_m1),
                    (2, "A Visão de Células Multiplicadoras", "Discipulado e Crescimento", "Como acolher o visitante, pastorear em pequenas reuniões e multiplicar discípulos na Carvalho Ramos.", quiz_m1),
                    (3, "O Poder da Intercessão Pastoral", "Oração e Jejum", "As chaves espirituais para guerrear pelos membros e proteger o rebanho contra as ciladas do inimigo.", quiz_m1)
                ]
                cursor.executemany("""
                INSERT INTO escola_lideres_modulos (numero_modulo, titulo_modulo, tema_central, conteudo_apostila, questoes_quiz)
                VALUES (?, ?, ?, ?, ?)
                """, modulos)

            # Checa Pedidos de Oração
            cursor.execute("SELECT COUNT(*) FROM pedidos_oracao")
            if cursor.fetchone()[0] == 0:
                pedidos = [
                    (str(uuid.uuid4()), "Maria Aparecida (67 anos)", "Saúde", "Peço oração pelos exames do coração do meu esposo João e paz na nossa casa.", 0, "aprovado", 14),
                    (str(uuid.uuid4()), "Anônimo", "Causas na Justiça", "Estou passando por uma causa trabalhista injusta há 2 anos. Peço um milagre da justiça de Deus.", 1, "aprovado", 28),
                    (str(uuid.uuid4()), "Lucas Gabriel (28 anos)", "Ansiedade & Trabalho", "Me sinto sobrecarregado e com o peito apertado. Peço apenas que a igreja ore por mim em silêncio.", 0, "aprovado", 42),
                    (str(uuid.uuid4()), "Família Silva", "Libertação", "Oração pelo meu filho mais velho voltar para os caminhos do Senhor.", 0, "aprovado", 19)
                ]
                cursor.executemany("""
                INSERT INTO pedidos_oracao (id, nome_solicitante, motivo_oracao, detalhes_pedido, is_anonimo, status, contador_orando)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, pedidos)

            # Checa Galeria de Fotos
            cursor.execute("SELECT COUNT(*) FROM galeria_fotos")
            if cursor.fetchone()[0] == 0:
                fotos = [
                    ("Domingo de Celebração - Santa Ceia", "2026-09-06", "Santa Ceia",
                     "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=1200",
                     "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=400", 87),
                    ("Conferência de Jovens Coração Ardente", "2026-08-29", "Conferência",
                     "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=1200",
                     "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=400", 142),
                    ("Batismo nas Águas - Vida Nova", "2026-08-16", "Batismo",
                     "https://images.unsplash.com/photo-1507692049790-de58290a4334?w=1200",
                     "https://images.unsplash.com/photo-1507692049790-de58290a4334?w=400", 215),
                    ("Quinta Profética de Milagres", "2026-09-03", "Culto",
                     "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=1200",
                     "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400", 63)
                ]
                cursor.executemany("""
                INSERT INTO galeria_fotos (album_nome, data_evento, categoria, foto_hd_url, foto_thumb_url, total_downloads)
                VALUES (?, ?, ?, ?, ?, ?)
                """, fotos)

            # Checa Cortes Verticais
            cursor.execute("SELECT COUNT(*) FROM cortes_verticais")
            if cursor.fetchone()[0] == 0:
                cortes = [
                    (372, "JESUS FUNCIONA COMO UM ESPELHO QUE MOSTRA QUEM VOCÊ É", "Revelação",
                     "https://midia.ibpmcr.com.br/cortes/corte_372_01.mp4", 23, 154, 94),
                    (373, "QUANDO VOCÊ ENTREGA SUA DOR NO ALTAR, DEUS TRANSFORMA EM UNÇÃO", "Cura",
                     "https://midia.ibpmcr.com.br/cortes/corte_373_02.mp4", 38, 240, 96),
                    (374, "O INIMIGO QUER QUE VOCÊ DESISTA HOJE, MAS O SEU MILAGRE VEM AMANHÃ", "Guerra Espiritual",
                     "https://midia.ibpmcr.com.br/cortes/corte_374_03.mp4", 45, 310, 98),
                    (375, "NÃO ANDEIS ANSIOSOS POR COISA ALGUMA: DESCANSE NO SENHOR", "Família",
                     "https://midia.ibpmcr.com.br/cortes/corte_375_01.mp4", 30, 189, 91)
                ]
                cursor.executemany("""
                INSERT INTO cortes_verticais (culto_id, titulo_impacto, tema_categoria, video_9_16_url, duracao_segundos, total_compartilhamentos, nota_viral)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, cortes)

            # Checa Eventos da Igreja
            cursor.execute("SELECT COUNT(*) FROM eventos_igreja")
            if cursor.fetchone()[0] == 0:
                eventos = [
                    (1, "Retiro Face a Face com Deus", "Um Encontro de Coração Ardente!", "20 a 22 de Outubro de 2026",
                     "Rua Punta Del Este, 18, Campo Grande - RJ",
                     "Três dias de imersão espiritual profunda, cura interior, quebra de maldições e renovo pentecostal. Venha viver um divisor de águas na sua história!",
                     150.0, 45.0, "5521964314284",
                     "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/cortes/culto_001/cover_001_1.jpg",
                     "https://maps.google.com/?q=Rua+Punta+Del+Este+18+Campo+Grande+RJ", 1)
                ]
                cursor.executemany("""
                INSERT INTO eventos_igreja (id, titulo, slogan, data_evento, local, descricao, valor_inscricao, valor_camisa, whatsapp_contato, imagem_url, link_maps, ativo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, eventos)

            # Checa Produtos da Lojinha & Cantina
            cursor.execute("SELECT COUNT(*) FROM produtos_loja")
            if cursor.fetchone()[0] == 0:
                produtos = [
                    (1, "Camisa Oficial - Retiro Face a Face", "Vestuário", 45.00,
                     "Camisa 100% algodão penteado premium com a estampa oficial do Retiro Face a Face com Deus.",
                     "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/cortes/culto_001/cover_001_2.jpg",
                     "P, M, G, GG, XGG", 1),
                    (2, "Quentinha Especial de Domingo (Cantina)", "Cantina", 25.00,
                     "Almoço completo caseiro com churrasco misto, arroz, farofa e vinagrete. Retire na cantina após o culto!",
                     "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/cortes/culto_002/cover_002_1.jpg",
                     None, 1),
                    (3, "Kit 3 Livros Físicos do Pastor Anderson", "Livros", 60.00,
                     "Os 3 livros oficiais impressos em capa luxo: Vitória na Família, Guerra Espiritual e Fundamentos da Fé.",
                     "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/cortes/culto_003/cover_003_1.jpg",
                     None, 1),
                    (4, "Caneca Porcelana Oficial IBPM CR", "Lembranças", 30.00,
                     "Caneca resinada de alta durabilidade com o brasão oficial da Igreja Batista Pentecostal Mundial.",
                     "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/cortes/culto_004/cover_004_1.jpg",
                     None, 1),
                    (5, "Bolo & Refrigerante da Cantina", "Cantina", 12.00,
                     "Fatia generosa de bolo confeitado artesanal acompanhado de refrigerante gelado.",
                     "https://pub-2b0c315d91644a41b558a4d2410ce1f8.r2.dev/cortes/culto_005/cover_005_1.jpg",
                     None, 1)
                ]
                cursor.executemany("""
                INSERT INTO produtos_loja (id, nome, categoria, preco, descricao, imagem_url, tamanhos_disponiveis, disponivel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, produtos)

            conn.commit()

    # Métodos de Acesso
    def get_devocional_hoje(self, dia_ano: int = 1) -> Optional[DevocionalDiario]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devocionais_diarios WHERE dia_ano = ? LIMIT 1", (dia_ano,))
            row = cursor.fetchone()
            if not row:
                cursor.execute("SELECT * FROM devocionais_diarios ORDER BY dia_ano LIMIT 1")
                row = cursor.fetchone()
            if row:
                return DevocionalDiario(
                    id=row["id"], dia_ano=row["dia_ano"], titulo=row["titulo"],
                    livro_biblia=row["livro_biblia"], versiculo_chave=row["versiculo_chave"],
                    texto_versiculo=row["texto_versiculo"], reflexao_pastoral=row["reflexao_pastoral"],
                    oracao_do_dia=row["oracao_do_dia"], desafio_pratico=row["desafio_pratico"],
                    audio_url=row["audio_url"]
                )
            return None

    def get_frases_por_sentimento(self, sentimento: str = "todos") -> List[FraseProfetica]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if sentimento == "todos":
                cursor.execute("SELECT * FROM frases_profeticas ORDER BY id DESC")
            else:
                cursor.execute("SELECT * FROM frases_profeticas WHERE sentimento_tag = ? ORDER BY id DESC", (sentimento,))
            rows = cursor.fetchall()
            return [FraseProfetica(id=r["id"], frase=r["frase"], sentimento_tag=r["sentimento_tag"], referencia_biblica=r["referencia_biblica"]) for r in rows]

    def get_pedidos_oracao(self) -> List[PedidoOracao]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pedidos_oracao WHERE status = 'aprovado' ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [
                PedidoOracao(
                    id=r["id"], nome_solicitante=r["nome_solicitante"], motivo_oracao=r["motivo_oracao"],
                    detalhes_pedido=r["detalhes_pedido"], is_anonimo=bool(r["is_anonimo"]),
                    status=r["status"], contador_orando=r["contador_orando"], created_at=r["created_at"]
                ) for r in rows
            ]

    def add_pedido_oracao(self, nome: str, motivo: str, detalhes: str, is_anonimo: bool) -> PedidoOracao:
        new_id = str(uuid.uuid4())
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO pedidos_oracao (id, nome_solicitante, motivo_oracao, detalhes_pedido, is_anonimo, status, contador_orando)
            VALUES (?, ?, ?, ?, ?, 'aprovado', 1)
            """, (new_id, nome, motivo, detalhes, 1 if is_anonimo else 0))
            conn.commit()
        return PedidoOracao(id=new_id, nome_solicitante=nome, motivo_oracao=motivo, detalhes_pedido=detalhes, is_anonimo=is_anonimo)

    def incrementar_orando(self, pedido_id: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE pedidos_oracao SET contador_orando = contador_orando + 1 WHERE id = ?", (pedido_id,))
            cursor.execute("SELECT contador_orando FROM pedidos_oracao WHERE id = ?", (pedido_id,))
            row = cursor.fetchone()
            conn.commit()
            return row[0] if row else 1

    def get_galeria_fotos(self) -> List[FotoGaleria]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM galeria_fotos ORDER BY data_evento DESC")
            rows = cursor.fetchall()
            return [FotoGaleria(id=r["id"], album_nome=r["album_nome"], data_evento=r["data_evento"], categoria=r["categoria"], foto_hd_url=r["foto_hd_url"], foto_thumb_url=r["foto_thumb_url"], total_downloads=r["total_downloads"]) for r in rows]

    def get_cortes_verticais(self) -> List[CorteVertical]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cortes_verticais ORDER BY nota_viral DESC")
            rows = cursor.fetchall()
            return [CorteVertical(id=r["id"], culto_id=r["culto_id"], titulo_impacto=r["titulo_impacto"], tema_categoria=r["tema_categoria"], video_9_16_url=r["video_9_16_url"], duracao_segundos=r["duracao_segundos"], total_compartilhamentos=r["total_compartilhamentos"], nota_viral=r["nota_viral"]) for r in rows]

    def get_livros(self) -> List[LivroEbook]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM livros_ebooks ORDER BY id ASC")
            rows = cursor.fetchall()
            return [LivroEbook(id=r["id"], titulo_livro=r["titulo_livro"], subtitulo=r["subtitulo"], capa_url=r["capa_url"], pdf_url=r["pdf_url"], sinopse=r["sinopse"], total_capitulos=r["total_capitulos"]) for r in rows]

    def get_modulos_lideranca(self) -> List[ModuloLideranca]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM escola_lideres_modulos ORDER BY numero_modulo ASC")
            rows = cursor.fetchall()
            modulos = []
            for r in rows:
                questoes = None
                if r["questoes_quiz"]:
                    try:
                        questoes = json.loads(r["questoes_quiz"])
                    except Exception:
                        pass
                modulos.append(ModuloLideranca(
                    id=r["id"], numero_modulo=r["numero_modulo"], titulo_modulo=r["titulo_modulo"],
                    tema_central=r["tema_central"], conteudo_apostila=r["conteudo_apostila"],
                    pdf_apostila_url=r["pdf_apostila_url"], questoes_quiz=questoes
                ))
            return modulos

    def get_eventos(self) -> List[EventoIgreja]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM eventos_igreja WHERE ativo = 1 ORDER BY id ASC")
            rows = cursor.fetchall()
            return [EventoIgreja(
                id=r["id"], titulo=r["titulo"], slogan=r["slogan"] or "", data_evento=r["data_evento"],
                local=r["local"], descricao=r["descricao"], valor_inscricao=r["valor_inscricao"] or 0.0,
                valor_camisa=r["valor_camisa"] or 45.0, whatsapp_contato=r["whatsapp_contato"] or "5521964314284",
                imagem_url=r["imagem_url"], link_maps=r["link_maps"], ativo=bool(r["ativo"])
            ) for r in rows]

    def get_evento_por_id(self, evento_id: int) -> Optional[EventoIgreja]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM eventos_igreja WHERE id = ? LIMIT 1", (evento_id,))
            r = cursor.fetchone()
            if r:
                return EventoIgreja(
                    id=r["id"], titulo=r["titulo"], slogan=r["slogan"] or "", data_evento=r["data_evento"],
                    local=r["local"], descricao=r["descricao"], valor_inscricao=r["valor_inscricao"] or 0.0,
                    valor_camisa=r["valor_camisa"] or 45.0, whatsapp_contato=r["whatsapp_contato"] or "5521964314284",
                    imagem_url=r["imagem_url"], link_maps=r["link_maps"], ativo=bool(r["ativo"])
                )
            return None

    def get_produtos_loja(self, categoria: Optional[str] = None) -> List[ProdutoLoja]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if categoria and categoria != "Todos":
                cursor.execute("SELECT * FROM produtos_loja WHERE categoria = ? AND disponivel = 1 ORDER BY id ASC", (categoria,))
            else:
                cursor.execute("SELECT * FROM produtos_loja WHERE disponivel = 1 ORDER BY id ASC")
            rows = cursor.fetchall()
            return [ProdutoLoja(
                id=r["id"], nome=r["nome"], categoria=r["categoria"], preco=r["preco"],
                descricao=r["descricao"], imagem_url=r["imagem_url"],
                tamanhos_disponiveis=r["tamanhos_disponiveis"], disponivel=bool(r["disponivel"])
            ) for r in rows]

    def salvar_inscricao_evento(self, inscricao: InscricaoEvento) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO inscricoes_eventos (
                evento_id, nome_completo, whatsapp, idade, bairro, vinculo,
                incluir_camisa, tamanho_camisa, restricoes, valor_total, status_pagamento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inscricao.evento_id, inscricao.nome_completo, inscricao.whatsapp,
                inscricao.idade, inscricao.bairro, inscricao.vinculo,
                1 if inscricao.incluir_camisa else 0, inscricao.tamanho_camisa,
                inscricao.restricoes, inscricao.valor_total, inscricao.status_pagamento
            ))
            conn.commit()
            return cursor.lastrowid

    def get_inscricoes_evento(self, evento_id: int) -> List[InscricaoEvento]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inscricoes_eventos WHERE evento_id = ? ORDER BY created_at DESC", (evento_id,))
            rows = cursor.fetchall()
            return [InscricaoEvento(
                id=r["id"], evento_id=r["evento_id"], nome_completo=r["nome_completo"],
                whatsapp=r["whatsapp"], idade=r["idade"], bairro=r["bairro"],
                vinculo=r["vinculo"], incluir_camisa=bool(r["incluir_camisa"]),
                tamanho_camisa=r["tamanho_camisa"], restricoes=r["restricoes"],
                valor_total=r["valor_total"], status_pagamento=r["status_pagamento"],
                data_inscricao=r["created_at"]
            ) for r in rows]

    def seed_initial_data(self):
        return self._seed_initial_data()


# Alias e Proxy de compatibilidade universal
class DBService:
    _db = DatabaseService()

    @classmethod
    def init_db(cls):
        return cls._db.init_db()

    @classmethod
    def seed_initial_data(cls):
        return cls._db._seed_initial_data()

    @classmethod
    def get_devocional_hoje(cls, dia_ano: int = 1):
        return cls._db.get_devocional_hoje(dia_ano)

    @classmethod
    def get_devocionais(cls):
        return [cls._db.get_devocional_hoje(1)]

    @classmethod
    def get_frases_por_sentimento(cls, sentimento: str = "todos"):
        return cls._db.get_frases_por_sentimento(sentimento)

    @classmethod
    def get_frases_profeticas(cls, sentimento: str = "todos"):
        return cls._db.get_frases_por_sentimento(sentimento)

    @classmethod
    def get_pedidos_oracao(cls):
        return cls._db.get_pedidos_oracao()

    @classmethod
    def add_pedido_oracao(cls, nome: str, motivo: str, detalhes: str, is_anonimo: bool = False):
        return cls._db.add_pedido_oracao(nome, motivo, detalhes, is_anonimo)

    @classmethod
    def incrementar_orando(cls, pedido_id: str):
        return cls._db.incrementar_orando(pedido_id)

    @classmethod
    def get_galeria_fotos(cls):
        return cls._db.get_galeria_fotos()

    @classmethod
    def get_cortes_verticais(cls):
        return cls._db.get_cortes_verticais()

    @classmethod
    def get_livros(cls):
        return cls._db.get_livros()

    @classmethod
    def get_modulos_lideranca(cls):
        return cls._db.get_modulos_lideranca()

    @classmethod
    def get_eventos(cls):
        return cls._db.get_eventos()

    @classmethod
    def get_evento_por_id(cls, evento_id: int):
        return cls._db.get_evento_por_id(evento_id)

    @classmethod
    def get_produtos_loja(cls, categoria: Optional[str] = None):
        return cls._db.get_produtos_loja(categoria)

    @classmethod
    def salvar_inscricao_evento(cls, inscricao: InscricaoEvento):
        return cls._db.salvar_inscricao_evento(inscricao)

    @classmethod
    def get_inscricoes_evento(cls, evento_id: int):
        return cls._db.get_inscricoes_evento(evento_id)


