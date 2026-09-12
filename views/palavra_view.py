"""
Aba 3: Palavra & Estudos - Super-App IBPM CR.
Contém:
1. Devocional Diário '365 Dias no Altar' (com áudio e 1 toque WhatsApp)
2. Bíblia Sagrada Offline (leitura com controle de fonte)
3. Livros Oficiais do Pastor (leitura e download de e-books em PDF)
4. Escola de Líderes (52 Módulos com apostilas e quiz interativo)
"""
import flet as ft
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
)
from core.audio_service import AudioService, AudioTrack
from services.db_service import DatabaseService
from services.share_engine import ShareEngine

class PalavraView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.app_page = page
        self.db = DatabaseService()
        self.audio_service = AudioService()
        self.active_tab_index = 0  # 0: Devocional, 1: Bíblia, 2: Livros, 3: Escola, 4: Hinário
        self.dynamic_content_container = ft.Container(expand=True)
        self.dia_devocional_ativo = 1
        self.busca_louvor = ""
        self.cat_louvor_ativa = "Todos"

        FontScaleManager.register_listener(self.on_font_scale_changed)
        self.build_ui()

    def on_font_scale_changed(self):
        self.render_active_tab()
        try:
            self.app_page.update()
        except Exception:
            pass

    def build_ui(self):
        self.padding = AppPadding.all(12)

        sub_abas = [
            ("Devocional 365", Icons.AUTO_STORIES, 0),
            ("Bíblia Sagrada", Icons.MENU_BOOK, 1),
            ("Livros & E-books", Icons.IMPORT_CONTACTS, 2),
            ("Escola de Líderes", Icons.SCHOOL, 3),
            ("Coletânea de Louvores", Icons.MUSIC_NOTE, 4),
        ]

        botoes_sub_abas = []
        for rotulo, icone, idx in sub_abas:
            is_active = (self.active_tab_index == idx)
            btn = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icone, color=AppColors.TEXT_WHITE if is_active else AppColors.SECONDARY_GOLD, size=18),
                        ft.Text(
                            rotulo,
                            size=FontScaleManager.s(13),
                            weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                            color=AppColors.TEXT_WHITE if is_active else AppColors.TEXT_SECONDARY,
                        ),
                    ],
                    spacing=6,
                ),
                bgcolor=AppColors.PRIMARY_RUBI if is_active else AppColors.BG_SURFACE_ALT,
                padding=AppPadding.symmetric(horizontal=12, vertical=10),
                border_radius=10,
                border=AppBorder.all(1, AppColors.PRIMARY_RUBI if is_active else AppColors.BORDER_DEFAULT),
                on_click=lambda e, i=idx: self.mudar_sub_aba(i),
            )
            botoes_sub_abas.append(btn)

        barra_selecao = ft.Row(
            controls=botoes_sub_abas,
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
        )

        self.render_active_tab()

        self.content = ft.Column(
            controls=[
                barra_selecao,
                ft.Divider(color=AppColors.DIVIDER, height=15),
                self.dynamic_content_container,
            ],
            expand=True,
            spacing=8,
        )

    def mudar_sub_aba(self, idx: int):
        self.active_tab_index = idx
        self.build_ui()
        try:
            self.app_page.update()
        except Exception:
            pass

    def render_active_tab(self):
        if self.active_tab_index == 0:
            self.dynamic_content_container.content = self._render_devocional_view()
        elif self.active_tab_index == 1:
            self.dynamic_content_container.content = self._render_biblia_view()
        elif self.active_tab_index == 2:
            self.dynamic_content_container.content = self._render_livros_view()
        elif self.active_tab_index == 3:
            self.dynamic_content_container.content = self._render_escola_view()
        elif self.active_tab_index == 4:
            self.dynamic_content_container.content = self._render_hinario_view()

    # 1. SUB-ABA DEVOCIONAL '365 DIAS NO ALTAR'
    def _render_devocional_view(self):
        dev = self.db.get_devocional_hoje(self.dia_devocional_ativo)
        if not dev:
            return ft.Text("Devocional não encontrado.", color=AppColors.TEXT_MUTED)

        card_versiculo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(Icons.FORMAT_QUOTE, color=AppColors.SECONDARY_GOLD, size=24),
                            ft.Text(f"Versículo Chave • {dev.versiculo_chave}", size=FontScaleManager.s(13), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                        ],
                        spacing=6,
                    ),
                    ft.Text(f"\"{dev.texto_versiculo}\"", size=FontScaleManager.s(15), weight=ft.FontWeight.W_600, color=AppColors.TEXT_WHITE, italic=True),
                ],
                spacing=6,
            ),
            bgcolor=AppColors.BG_DARK,
            padding=AppPadding.all(14),
            border_radius=12,
            border=AppBorder.all(1, AppColors.BORDER_GOLD),
        )

        card_reflexao = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("📖 Reflexão Pastoral", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                    ft.Text(dev.reflexao_pastoral, size=FontScaleManager.s(14), color=AppColors.TEXT_SECONDARY),
                    ft.Container(height=6),
                    ft.Text("🙏 Oração do Dia", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                    ft.Text(dev.oracao_do_dia, size=FontScaleManager.s(14), color=AppColors.TEXT_WHITE, italic=True),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(Icons.LIGHTBULB_OUTLINE, color=AppColors.SECONDARY_GOLD, size=20),
                                ft.Text(f"Desafio de Hoje: {dev.desafio_pratico}", size=FontScaleManager.s(13), color=AppColors.TEXT_WHITE, weight=ft.FontWeight.W_500, expand=True),
                            ],
                            spacing=8,
                        ),
                        bgcolor=AppColors.BG_SURFACE_ALT,
                        padding=AppPadding.all(10),
                        border_radius=10,
                    )
                ],
                spacing=8,
            ),
            bgcolor=AppColors.BG_SURFACE,
            padding=AppPadding.all(16),
            border_radius=14,
            border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
        )

        # Barra de Ações 1 Toque para o Devocional
        botoes_acao_devocional = ft.Row(
            controls=[
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(Icons.HEADPHONES, color="#000000", size=18),
                            ft.Text("Ouvir em Áudio", color="#000000", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                        ],
                        spacing=6,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=AppColors.SECONDARY_GOLD,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=AppPadding.symmetric(horizontal=12, vertical=12),
                    ),
                    on_click=lambda e, d=dev: self.ouvir_devocional_audio(d),
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(Icons.SEND, color="#FFFFFF", size=18),
                            ft.Text("Mandar no WhatsApp", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                        ],
                        spacing=6,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=AppColors.ACCENT_GREEN,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=AppPadding.symmetric(horizontal=12, vertical=12),
                    ),
                    on_click=lambda e, d=dev: self.compartilhar_devocional_whatsapp(d),
                ),
                ft.OutlinedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(Icons.PHOTO_CAMERA, color=AppColors.PRIMARY_RUBI, size=18),
                            ft.Text("Stories", color=AppColors.PRIMARY_RUBI, weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                        ],
                        spacing=6,
                    ),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, AppColors.PRIMARY_RUBI),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=AppPadding.symmetric(horizontal=12, vertical=12),
                    ),
                    on_click=lambda e: ShareEngine.share_instagram_stories(self.app_page),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(icon=Icons.CHEVRON_LEFT, icon_color=AppColors.SECONDARY_GOLD, tooltip="Dia anterior", on_click=self.voltar_dia_devocional),
                        ft.Text(f"Dia {dev.dia_ano} de 365 no Altar", size=FontScaleManager.s(16), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ft.IconButton(icon=Icons.CHEVRON_RIGHT, icon_color=AppColors.SECONDARY_GOLD, tooltip="Próximo dia", on_click=self.avancar_dia_devocional),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(dev.titulo, size=FontScaleManager.s(20), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                card_versiculo,
                card_reflexao,
                ft.Container(height=4),
                botoes_acao_devocional,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    def ouvir_devocional_audio(self, dev):
        track = AudioTrack(
            title=f"Devocional {dev.dia_ano}: {dev.titulo}",
            subtitle=f"{dev.versiculo_chave} • IBPM CR",
            audio_url=dev.audio_url or "https://midia.ibpmcr.com.br/audios/devocional_01.mp3"
        )
        self.audio_service.play_track(track)
        ShareEngine.show_feedback(self.app_page, "🎧 Reproduzindo ministração devocional! Pode bloquear a tela que o áudio continuará.")

    def compartilhar_devocional_whatsapp(self, dev):
        mensagem = (
            f"🔥 *365 DIAS NO ALTAR - IBPM CR (Dia {dev.dia_ano})*\n"
            f"*{dev.titulo}*\n\n"
            f"📖 *{dev.versiculo_chave}:* \"{dev.texto_versiculo}\"\n\n"
            f"💡 *Reflexão:* {dev.reflexao_pastoral}\n\n"
            f"🙏 *Oração:* {dev.oracao_do_dia}\n\n"
            f"🎯 *Desafio Prático:* {dev.desafio_pratico}"
        )
        ShareEngine.share_whatsapp_status(self.app_page, mensagem)

    def voltar_dia_devocional(self, e):
        if self.dia_devocional_ativo > 1:
            self.dia_devocional_ativo -= 1
            self.render_active_tab()
            self.app_page.update()

    def avancar_dia_devocional(self, e):
        if self.dia_devocional_ativo < 365:
            self.dia_devocional_ativo += 1
            self.render_active_tab()
            self.app_page.update()

    # 2. SUB-ABA BÍBLIA SAGRADA OFFLINE
    def _render_biblia_view(self):
        # Exemplo de leitura offline com textos da Escritura
        capitulos_amostra = [
            ("Salmos 23:1-6", "1 O Senhor é o meu pastor, nada me faltará. 2 Deitar-me faz em verdes pastos, guia-me mansamente a águas tranqüilas. 3 Refrigera a minha alma; guia-me pelas veredas da justiça, por amor do seu nome. 4 Ainda que eu andasse pelo vale da sombra da morte, não temeria mal algum, porque tu estás comigo; a tua vara e o teu cajado me consolam. 5 Preparas uma mesa perante mim na presença dos meus inimigos, unges a minha cabeça com óleo, o meu cálice transborda. 6 Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida; e habitarei na casa do Senhor por longos dias."),
            ("Salmos 91:1-4", "1 Aquele que habita no esconderijo do Altíssimo, à sombra do Onipotente descansará. 2 Direi do Senhor: Ele é o meu Deus, o meu refúgio, a minha fortaleza, e nele confiarei. 3 Porque ele te livrará do laço do passarinheiro, e da peste perniciosa. 4 Ele te cobrirá com as suas penas, e debaixo das suas asas te confiarás; a sua verdade será o teu escudo e broquel."),
            ("Isaías 40:29-31", "29 Dá força ao cansado, e multiplica as forças ao que não tem nenhum vigor. 30 Os jovens se cansarão e se fatigarão, e os moços certamente cairão; 31 Mas os que esperam no Senhor renovarão as forças, subirão com asas como águias; correrão, e não se cansarão; caminharão, e não se fatigarão."),
            ("Filipenses 4:6-7", "6 Não estejais inquietos por coisa alguma; antes as vossas petições sejam em tudo conhecidas diante de Deus pela oração e súplica, com ação de graças. 7 E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentimentos em Cristo Jesus.")
        ]

        cards_biblia = []
        for ref, texto in capitulos_amostra:
            c = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(ref, size=FontScaleManager.s(16), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                                ft.IconButton(
                                    icon=Icons.SEND,
                                    icon_color=AppColors.ACCENT_GREEN,
                                    tooltip="Compartilhar no WhatsApp",
                                    on_click=lambda e, r=ref, t=texto: ShareEngine.share_whatsapp_status(self.app_page, f"📖 *{r}*\n\n{t}")
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(texto, size=FontScaleManager.s(15), color=AppColors.TEXT_WHITE, selectable=True),
                    ],
                    spacing=6,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(16),
                border_radius=14,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=10),
            )
            cards_biblia.append(c)

        return ft.ListView(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("📖 Bíblia Sagrada (Modo 100% Offline)", size=FontScaleManager.s(16), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                        ft.Container(
                            content=ft.Text("OFFLINE ATIVO", size=FontScaleManager.s(10), weight=ft.FontWeight.BOLD, color=AppColors.ACCENT_GREEN),
                            bgcolor="#0E2E20",
                            padding=AppPadding.symmetric(horizontal=8, vertical=4),
                            border_radius=8,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text("Texto sagrado com tipografia ampliada sênior-friendly. Não necessita de internet.", size=FontScaleManager.s(13), color=AppColors.TEXT_MUTED),
                ft.Container(height=6),
                *cards_biblia,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    # 3. SUB-ABA LIVROS OFICIAIS DO PASTOR
    def _render_livros_view(self):
        livros = self.db.get_livros()
        cards_livros = []

        for liv in livros:
            c = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(Icons.MENU_BOOK, color="#FFFFFF", size=28),
                                    bgcolor=AppColors.PRIMARY_RUBI,
                                    width=50,
                                    height=50,
                                    border_radius=12,
                                    alignment=AppAlignment.CENTER,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(liv.titulo_livro, size=FontScaleManager.s(16), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                        ft.Text(liv.subtitulo, size=FontScaleManager.s(12), color=AppColors.SECONDARY_GOLD),
                                    ],
                                    expand=True,
                                    spacing=2,
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=6),
                        ft.Text(liv.sinopse, size=FontScaleManager.s(13), color=AppColors.TEXT_SECONDARY),
                        ft.Container(height=8),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.DOWNLOAD, color="#FFFFFF", size=18),
                                            ft.Text("Baixar Livro (PDF)", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=6,
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor=AppColors.PRIMARY_RUBI,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=12, vertical=10),
                                    ),
                                    on_click=lambda e, l=liv: ShareEngine.download_to_device(self.app_page, l.pdf_url, f"{l.titulo_livro}.pdf"),
                                ),
                                ft.OutlinedButton(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(Icons.SHARE, color=AppColors.SECONDARY_GOLD, size=18),
                                            ft.Text("Compartilhar", color=AppColors.SECONDARY_GOLD, weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                        ],
                                        spacing=6,
                                    ),
                                    style=ft.ButtonStyle(
                                        side=ft.BorderSide(1, AppColors.SECONDARY_GOLD),
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                        padding=AppPadding.symmetric(horizontal=12, vertical=10),
                                    ),
                                    on_click=lambda e, l=liv: ShareEngine.share_whatsapp_status(
                                        self.app_page,
                                        f"📚 *E-book Oficial - IBPM CR*\n*{l.titulo_livro}* - {l.subtitulo}\n\n\"{l.sinopse}\"\nBaixe gratuitamente no App Oficial!"
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    spacing=6,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(16),
                border_radius=14,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=10),
            )
            cards_livros.append(c)

        return ft.ListView(
            controls=[
                ft.Text("📚 Livros & E-books Oficiais do Pastor", size=FontScaleManager.s(18), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                ft.Text("Edição com 12 capítulos para estudo na família ou célula. Download gratuito em PDF.", size=FontScaleManager.s(13), color=AppColors.TEXT_MUTED),
                ft.Container(height=6),
                *cards_livros,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    # 4. SUB-ABA ESCOLA DE LÍDERES
    def _render_escola_view(self):
        modulos = self.db.get_modulos_lideranca()
        cards_modulos = []

        for m in modulos:
            c = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(f"M{m.numero_modulo}", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    bgcolor=AppColors.PRIMARY_RUBI,
                                    width=40,
                                    height=40,
                                    border_radius=10,
                                    alignment=AppAlignment.CENTER,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(m.titulo_modulo, size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                        ft.Text(f"Tema: {m.tema_central}", size=FontScaleManager.s(12), color=AppColors.SECONDARY_GOLD),
                                    ],
                                    expand=True,
                                    spacing=2,
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=4),
                        ft.Text(m.conteudo_apostila, size=FontScaleManager.s(13), color=AppColors.TEXT_SECONDARY),
                        ft.Container(height=6),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Fazer Quiz do Módulo",
                                    icon=Icons.CHECK_CIRCLE_OUTLINE,
                                    style=ft.ButtonStyle(bgcolor=AppColors.BG_SURFACE_ALT, color=AppColors.SECONDARY_GOLD),
                                    on_click=lambda e, mod=m: self.iniciar_quiz_modal(mod),
                                ),
                                ft.TextButton(
                                    "Apostila PDF",
                                    icon=Icons.PICTURE_AS_PDF,
                                    style=ft.ButtonStyle(color=AppColors.PRIMARY_RUBI),
                                    on_click=lambda e: ShareEngine.show_feedback(self.app_page, "📥 Download da apostila do módulo iniciado!"),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                    spacing=4,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(14),
                border_radius=14,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                margin=AppMargin.only(bottom=10),
            )
            cards_modulos.append(c)

        return ft.ListView(
            controls=[
                ft.Text("🎓 Escola de Líderes (52 Módulos)", size=FontScaleManager.s(18), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                ft.Text("Curso anual de capacitação bíblica para líderes de células e ministérios da IBPM CR.", size=FontScaleManager.s(13), color=AppColors.TEXT_MUTED),
                ft.Container(height=6),
                *cards_modulos,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    def iniciar_quiz_modal(self, modulo):
        questoes = modulo.questoes_quiz or []
        if not questoes:
            ShareEngine.show_feedback(self.app_page, "Este módulo não possui quiz no momento.")
            return

        def fechar(e=None):
            try:
                self.app_page.close(dlg)
            except Exception:
                dlg.open = False
                self.app_page.update()

        q = questoes[0]
        pergunta = q.get("pergunta", "")
        opcoes = q.get("opcoes", [])
        correta = q.get("resposta", 0)

        def responder(indice):
            fechar()
            if indice == correta:
                ShareEngine.show_feedback(self.app_page, "🎉 Resposta Correta! Glória a Deus, você foi aprovado nesta questão!")
            else:
                ShareEngine.show_feedback(self.app_page, "❌ Quase lá! Revise a apostila e tente novamente.")

        botoes_opcoes = []
        for i, op in enumerate(opcoes):
            btn = ft.ElevatedButton(
                op,
                bgcolor=AppColors.BG_SURFACE_ALT,
                color=AppColors.TEXT_WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=AppPadding.all(12),
                ),
                on_click=lambda e, idx=i: responder(idx),
            )
            botoes_opcoes.append(btn)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Quiz - {modulo.titulo_modulo}", weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, size=FontScaleManager.s(16)),
            content=ft.Column(
                controls=[
                    ft.Text(f"Pergunta: {pergunta}", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                    ft.Container(height=6),
                    *botoes_opcoes,
                ],
                tight=True,
                spacing=8,
            ),
            actions=[ft.TextButton("Voltar", on_click=fechar)],
            bgcolor=AppColors.BG_SURFACE,
        )

        try:
            self.app_page.open(dlg)
        except Exception:
            self.app_page.dialog = dlg
            dlg.open = True
            self.app_page.update()

    # 5. SUB-ABA COLETÂNEA DE LOUVORES & HINÁRIO DO ALTAR (ESTILO MARANATA)
    def _render_hinario_view(self):
        louvores = [
            {
                "numero": 1,
                "titulo": "Porque Ele Vive",
                "categoria": "Harpa & Clássicos",
                "autor": "Bill & Gloria Gaither",
                "letra": "Deus enviou Seu Filho amado\nPra me salvar e perdoar\nNa cruz morreu por meus pecados\nMas ressurgiu e vivo com o Pai está!\n\nPorque Ele vive, posso crer no amanhã\nPorque Ele vive, temor não há!\nMas eu bem sei, eu sei que a minha vida\nEstá nas mãos de meu Jesus que vivo está!\n\nE quando, enfim, chegar a hora\nEm que a morte enfrentarei\nSem medo, então, terei vitória\nIrei à Glória, ao meu Jesus que vivo está!"
            },
            {
                "numero": 2,
                "titulo": "Alvo Mais Que a Neve",
                "categoria": "Harpa & Clássicos",
                "autor": "Harpa Cristã Nº 39",
                "letra": "Bendito seja o Cordeiro\nQue na cruz por nós padeceu!\nBendito seja o Seu sangue\nQue por nós ali Ele verteu!\n\nAlvo mais que a neve!\nAlvo mais que a neve!\nSim, nesse sangue lavado\nMais alvo que a neve serei!\n\nQuão quebrantado e contrito\nVenho a Ti, Senhor, me prostrar\nPara que o sangue bendito\nVenha a minha alma lavar!"
            },
            {
                "numero": 3,
                "titulo": "Em Fervente Oração",
                "categoria": "Adoração & Oração",
                "autor": "Harpa Cristã Nº 577",
                "letra": "Em fervente oração, vem o teu coração\nNa presença de Deus derramar!\nMas não podes fruir o que estás a pedir\nSe tudo no altar não deixar!\n\nDeixa tudo no altar!\nDeixa tudo no altar!\nE a bênção de Deus, prometida dos céus\nNa tua alma irá transbordar!"
            },
            {
                "numero": 4,
                "titulo": "Grandioso És Tu",
                "categoria": "Harpa & Clássicos",
                "autor": "Harpa Cristã Nº 526",
                "letra": "Senhor meu Deus, quando eu maravilhado\nFico a pensar nas obras de Tuas mãos\nNo céu azul de estrelas pontilhado\nO Seu poder mostrando a criação!\n\nEntão minh'alma canta a Ti, Senhor:\nGrandioso és Tu! Grandioso és Tu!\nEntão minh'alma canta a Ti, Senhor:\nGrandioso és Tu! Grandioso és Tu!"
            },
            {
                "numero": 5,
                "titulo": "Os Guerreiros se Preparam",
                "categoria": "Guerra Espiritual",
                "autor": "Harpa Cristã Nº 212",
                "letra": "Os guerreiros se preparam para a grande voz de Deus\nEia avante, ó soldados de Sião!\nJá ouvimos o estrondo dos inimigos nos céus\nMas em Cristo nós temos a salvação!\n\nQuem irá lutar por Cristo? Quem a fronte erguerá?\nQuem na cruz achou perdão e vida traz?\nEis que o Mestre está chamando, quem a voz escutará?\nEis-me aqui, envia-me a mim, Senhor!"
            },
            {
                "numero": 6,
                "titulo": "Vem, Senhor, e Faz de Novo",
                "categoria": "Corinhos de Fogo",
                "autor": "Avivamento Pentecostal",
                "letra": "Vem, Senhor, e faz de novo\nO Teu fogo descer sobre este povo!\nAcende o altar, batiza com poder\nNós queremos Tua glória e Teu mover!\n\nDesce fogo do altar!\nDesce fogo do altar!\nA Igreja clama, a Igreja adora\nO Espírito Santo desce agora!"
            },
            {
                "numero": 7,
                "titulo": "Ele é o Deus dos Deuses",
                "categoria": "Vitória & Celebração",
                "autor": "Louvor do Altar",
                "letra": "Ele é o Deus dos deuses, Senhor dos senhores\nA Ele a glória, a força e o louvor!\nCadeias se quebram, muralhas vão cair\nQuando a Igreja de joelhos começa a pedir!\n\nAleluia, aleluia! O Todo-Poderoso reina aqui!\nAleluia, aleluia! Ninguém pode impedir o Teu agir!"
            },
            {
                "numero": 8,
                "titulo": "A Mensagem da Cruz",
                "categoria": "Harpa & Clássicos",
                "autor": "Harpa Cristã Nº 291",
                "letra": "Rude cruz se erigiu, dela o dia fugiu\nComo emblema de vergonha e dor\nMas eu amo essa cruz, sobre a qual meu Jesus\nDeu a vida por mim, pecador!\n\nSim, eu amo a mensagem da cruz\n'Té morrer eu a vou proclamar\nLevarei eu também minha cruz\n'Té por uma coroa trocar!"
            }
        ]

        # Filtro de busca e categoria
        filtrados = []
        for l in louvores:
            matches_busca = (
                not self.busca_louvor or 
                self.busca_louvor.lower() in l["titulo"].lower() or 
                self.busca_louvor.lower() in l["letra"].lower() or
                self.busca_louvor in str(l["numero"])
            )
            matches_cat = (self.cat_louvor_ativa == "Todos" or l["categoria"] == self.cat_louvor_ativa)
            if matches_busca and matches_cat:
                filtrados.append(l)

        # Barra de Pesquisa
        campo_busca = ft.TextField(
            hint_text="Buscar louvor por nome, número ou trecho...",
            prefix_icon=Icons.SEARCH,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.PRIMARY_RUBI,
            text_style=ft.TextStyle(color=AppColors.TEXT_WHITE),
            value=self.busca_louvor,
            on_change=lambda e: self._filtrar_hinario(e.control.value),
        )

        categorias = ["Todos", "Harpa & Clássicos", "Corinhos de Fogo", "Adoração & Oração", "Guerra Espiritual"]
        chips = []
        for cat in categorias:
            is_active = (self.cat_louvor_ativa == cat)
            chip = ft.Container(
                content=ft.Text(cat, size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL, color=AppColors.TEXT_WHITE if is_active else AppColors.TEXT_SECONDARY),
                bgcolor=AppColors.PRIMARY_RUBI if is_active else AppColors.BG_SURFACE_ALT,
                padding=AppPadding.symmetric(horizontal=10, vertical=6),
                border_radius=8,
                on_click=lambda e, c=cat: self._mudar_cat_hinario(c),
            )
            chips.append(chip)

        # Cards dos Louvores
        cards_louvores = []
        for l in filtrados:
            card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(f"#{l['numero']:02d}", size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                            bgcolor=AppColors.PRIMARY_RUBI,
                            padding=AppPadding.all(10),
                            border_radius=10,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(l["titulo"], size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                ft.Text(f"{l['categoria']} • {l['autor']}", size=FontScaleManager.s(12), color=AppColors.SECONDARY_GOLD),
                            ],
                            expand=True,
                            spacing=2,
                        ),
                        ft.IconButton(
                            icon=Icons.VISIBILITY,
                            icon_color=AppColors.TEXT_WHITE,
                            tooltip="Ver Letra Completa",
                            on_click=lambda e, louv=l: self._abrir_modal_louvor(louv),
                        )
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                bgcolor=AppColors.BG_SURFACE,
                padding=AppPadding.all(12),
                border_radius=12,
                border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                on_click=lambda e, louv=l: self._abrir_modal_louvor(louv),
            )
            cards_louvores.append(card)

        return ft.ListView(
            controls=[
                campo_busca,
                ft.Container(height=4),
                ft.Row(controls=chips, scroll=ft.ScrollMode.AUTO, spacing=6),
                ft.Container(height=6),
                *cards_louvores,
                ft.Container(height=30),
            ],
            expand=True,
            spacing=8,
        )

    def _filtrar_hinario(self, texto: str):
        self.busca_louvor = texto
        self.render_active_tab()
        try:
            self.app_page.update()
        except Exception:
            pass

    def _mudar_cat_hinario(self, cat: str):
        self.cat_louvor_ativa = cat
        self.render_active_tab()
        try:
            self.app_page.update()
        except Exception:
            pass

    def _abrir_modal_louvor(self, louvor: dict):
        def fechar(e):
            try:
                self.app_page.close(dlg)
            except Exception:
                dlg.open = False
                self.app_page.update()

        dlg = ft.AlertDialog(
            modal=False,
            title=ft.Row(
                controls=[
                    ft.Text(f"#{louvor['numero']:02d} • {louvor['titulo']}", weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, size=FontScaleManager.s(16)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"🎵 {louvor['categoria']} ({louvor['autor']})", size=FontScaleManager.s(12), color=AppColors.SECONDARY_GOLD, weight=ft.FontWeight.BOLD),
                        ft.Divider(color=AppColors.DIVIDER),
                        ft.Text(louvor["letra"], size=FontScaleManager.s(14), color=AppColors.TEXT_WHITE, selectable=True),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=8,
                ),
                width=450,
                height=400,
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Row([ft.Icon(Icons.SHARE, size=16), ft.Text("Compartilhar Letra")]),
                    style=ft.ButtonStyle(bgcolor=AppColors.PRIMARY_RUBI),
                    on_click=lambda e: ShareEngine.share_whatsapp_status(
                        self.app_page,
                        f"🎵 *{louvor['titulo']}*\n\n{louvor['letra']}\n\n🙏 Louvado na IBPM CR"
                    ),
                ),
                ft.TextButton("Fechar", on_click=fechar),
            ],
            bgcolor=AppColors.BG_SURFACE,
        )

        try:
            self.app_page.open(dlg)
        except Exception:
            self.app_page.dialog = dlg
            dlg.open = True
            self.app_page.update()

