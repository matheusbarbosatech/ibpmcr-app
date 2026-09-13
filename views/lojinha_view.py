"""
Módulo de Lojinha & Cantina Oficial da IBPM CR e Inscrições Nativas em Eventos.
Permite aos membros comprar produtos da igreja (camisas, quentinhas de almoço, livros, canecas)
e realizar inscrições 100% no app com pagamento via PIX e envio para o WhatsApp da secretaria.
"""
import flet as ft
from typing import Optional, Callable
from core.theme import (
    AppColors, FontScaleManager, Icons, AppPadding, AppMargin, AppBorder, AppAlignment
)
from services.db_service import DatabaseService
from services.share_engine import ShareEngine
from models.midia import EventoIgreja, ProdutoLoja, InscricaoEvento

CHAVE_PIX_OFICIAL = "21964314284"  # Chave PIX da Igreja (Telefone/CNPJ)
WHATSAPP_SECRETARIA = "5521964314284"
WHATSAPP_INTERCESSAO = "5521989913903"

class InscricaoEventoModal:
    """Modal nativo para inscrição direta em eventos da igreja (ex: Retiro Face a Face)."""
    @staticmethod
    def abrir(page: ft.Page, evento: EventoIgreja, on_sucesso: Optional[Callable] = None):
        db = DatabaseService()
        
        txt_nome = ft.TextField(
            label="Nome Completo *",
            hint_text="Digite seu nome completo",
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(14),
        )
        
        txt_whatsapp = ft.TextField(
            label="WhatsApp (com DDD) *",
            hint_text="Ex: 21999999999",
            keyboard_type=ft.KeyboardType.PHONE,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(14),
        )
        
        txt_idade = ft.TextField(
            label="Idade *",
            hint_text="Ex: 35",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=120,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(14),
        )
        
        txt_bairro = ft.TextField(
            label="Bairro / Cidade *",
            hint_text="Ex: Campo Grande, RJ",
            expand=True,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(14),
        )
        
        dd_vinculo = ft.Dropdown(
            label="Vínculo com a Igreja *",
            value="Membro IBPM CR",
            options=[
                ft.dropdown.Option("Membro IBPM CR"),
                ft.dropdown.Option("Visitante / Convidado"),
                ft.dropdown.Option("Frequentador Assíduo"),
            ],
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(13),
        )
        
        dd_tamanho = ft.Dropdown(
            label="Tamanho da Camisa",
            value="G",
            options=[
                ft.dropdown.Option("P"),
                ft.dropdown.Option("M"),
                ft.dropdown.Option("G"),
                ft.dropdown.Option("GG"),
                ft.dropdown.Option("XGG"),
            ],
            visible=True,
            width=140,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(13),
        )
        
        txt_restricoes = ft.TextField(
            label="Observações Médicas / Restrições (Opcional)",
            hint_text="Ex: Alergia a frutos do mar, hipertensão, etc.",
            multiline=True,
            min_lines=2,
            max_lines=3,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(13),
        )
        
        lbl_valor_total = ft.Text(
            f"R$ {evento.valor_inscricao + evento.valor_camisa:.2f}",
            size=FontScaleManager.s(18),
            weight=ft.FontWeight.BOLD,
            color=AppColors.SECONDARY_GOLD,
        )
        
        def atualizar_total(e):
            total = evento.valor_inscricao
            if chk_camisa.value:
                total += evento.valor_camisa
                dd_tamanho.visible = True
            else:
                dd_tamanho.visible = False
            lbl_valor_total.value = f"R$ {total:.2f}"
            page.update()
            
        chk_camisa = ft.Checkbox(
            label=f"Incluir Camisa Oficial do Retiro (+ R$ {evento.valor_camisa:.2f})",
            value=True,
            check_color="#000000",
            active_color=AppColors.SECONDARY_GOLD,
            on_change=atualizar_total,
        )
        
        def fechar(e=None):
            try:
                page.close(dlg)
            except Exception:
                dlg.open = False
                page.update()
                
        def submeter_inscricao(e):
            nome = txt_nome.value.strip() if txt_nome.value else ""
            whatsapp = txt_whatsapp.value.strip() if txt_whatsapp.value else ""
            bairro = txt_bairro.value.strip() if txt_bairro.value else ""
            idade_str = txt_idade.value.strip() if txt_idade.value else "0"
            
            if not nome:
                ShareEngine.show_feedback(page, "Por favor, preencha seu nome completo.")
                return
            if not whatsapp:
                ShareEngine.show_feedback(page, "Por favor, informe seu WhatsApp para contato.")
                return
                
            try:
                idade = int(idade_str)
            except ValueError:
                idade = 0
                
            valor_final = evento.valor_inscricao + (evento.valor_camisa if chk_camisa.value else 0.0)
            tamanho = dd_tamanho.value if chk_camisa.value else None
            
            inscricao = InscricaoEvento(
                id=None,
                evento_id=evento.id,
                nome_completo=nome,
                whatsapp=whatsapp,
                idade=idade,
                bairro=bairro,
                vinculo=dd_vinculo.value or "Membro IBPM CR",
                incluir_camisa=bool(chk_camisa.value),
                tamanho_camisa=tamanho,
                restricoes=txt_restricoes.value or "",
                valor_total=valor_final,
                status_pagamento="pendente"
            )
            
            # Salva no banco de dados local (SQLite)
            db.salvar_inscricao_evento(inscricao)
            fechar()
            
            # Abre modal de confirmação e pagamento PIX
            InscricaoEventoModal.abrir_modal_pagamento_pix(page, evento, inscricao)
            if on_sucesso:
                on_sucesso()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.EVENT_AVAILABLE, color=AppColors.SECONDARY_GOLD, size=24),
                    ft.Text(f"Inscrição: {evento.titulo}", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(16), color=AppColors.TEXT_WHITE, expand=True),
                    ft.IconButton(icon=Icons.CLOSE, icon_color=AppColors.TEXT_MUTED, on_click=fechar),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(Icons.LOCAL_FIRE_DEPARTMENT, color=AppColors.PRIMARY_RUBI, size=20),
                                    ft.Text(evento.slogan, size=FontScaleManager.s(12), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                                ],
                                spacing=6,
                            ),
                            bgcolor=AppColors.BG_SURFACE_ALT,
                            padding=AppPadding.all(8),
                            border_radius=8,
                        ),
                        ft.Text(f"📅 Data: {evento.data_evento}", size=FontScaleManager.s(12), color=AppColors.TEXT_WHITE),
                        ft.Text(f"📍 Local: {evento.local}", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                        ft.Divider(color=AppColors.DIVIDER, height=10),
                        txt_nome,
                        txt_whatsapp,
                        ft.Row(controls=[txt_idade, txt_bairro], spacing=8),
                        dd_vinculo,
                        chk_camisa,
                        dd_tamanho,
                        txt_restricoes,
                        ft.Container(height=4),
                        ft.Row(
                            controls=[
                                ft.Text("Investimento Total:", size=FontScaleManager.s(14), color=AppColors.TEXT_WHITE),
                                lbl_valor_total,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=380,
                height=520,
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(Icons.CHECK_CIRCLE, color="#000000", size=18),
                            ft.Text("Confirmar Inscrição & Pagar", color="#000000", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(13)),
                        ],
                        spacing=6,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    style=ft.ButtonStyle(
                        bgcolor=AppColors.SECONDARY_GOLD,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=AppPadding.symmetric(horizontal=16, vertical=12),
                    ),
                    on_click=submeter_inscricao,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=AppColors.BG_SURFACE,
        )
        
        page.open(dlg)
        page.update()

    @staticmethod
    def abrir_modal_pagamento_pix(page: ft.Page, evento: EventoIgreja, inscricao: InscricaoEvento):
        def fechar(e=None):
            try:
                page.close(dlg_pix)
            except Exception:
                dlg_pix.open = False
                page.update()

        def copiar_pix(e):
            ShareEngine.copy_to_clipboard(page, CHAVE_PIX_OFICIAL, "Chave PIX copiada!")

        def enviar_whatsapp_secretaria(e):
            camisa_info = f"Sim (Tamanho {inscricao.tamanho_camisa})" if inscricao.incluir_camisa else "Não"
            mensagem = (
                f"🔥 *NOVA INSCRIÇÃO - RETIRO FACE A FACE COM DEUS*\n\n"
                f"👤 *Nome:* {inscricao.nome_completo}\n"
                f"📱 *WhatsApp:* {inscricao.whatsapp}\n"
                f"🎂 *Idade:* {inscricao.idade} anos\n"
                f"🏠 *Bairro:* {inscricao.bairro}\n"
                f"⛪ *Vínculo:* {inscricao.vinculo}\n"
                f"👕 *Camisa Oficial:* {camisa_info}\n"
                f"⚠️ *Observações/Saúde:* {inscricao.restricoes or 'Nenhuma'}\n\n"
                f"💰 *Valor Total:* R$ {inscricao.valor_total:.2f}\n"
                f"💳 *Pagamento:* Chave PIX ({CHAVE_PIX_OFICIAL})\n\n"
                f"📌 _Estou enviando o meu comprovante de pagamento em anexo!_"
            )
            fechar()
            ShareEngine.share_whatsapp_status(page, mensagem)

        dlg_pix = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.CHECK_CIRCLE, color=AppColors.ACCENT_GREEN, size=24),
                    ft.Text("Inscrição Realizada com Sucesso!", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(15), color=AppColors.TEXT_WHITE),
                ],
                spacing=8,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(f"Parabéns, {inscricao.nome_completo}! Sua vaga está pré-reservada.", size=FontScaleManager.s(13), color=AppColors.TEXT_SECONDARY),
                        ft.Container(height=6),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("VALOR TOTAL:", size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED),
                                    ft.Text(f"R$ {inscricao.valor_total:.2f}", size=FontScaleManager.s(22), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                                    ft.Divider(color=AppColors.DIVIDER, height=8),
                                    ft.Text("CHAVE PIX OFICIAL (TELEFONE):", size=FontScaleManager.s(10), color=AppColors.TEXT_MUTED),
                                    ft.Text(CHAVE_PIX_OFICIAL, size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=AppColors.BG_DARK,
                            padding=AppPadding.all(12),
                            border_radius=10,
                            border=AppBorder.all(1, AppColors.SECONDARY_GOLD),
                            alignment=AppAlignment.CENTER,
                        ),
                        ft.Container(height=6),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(Icons.CONTENT_COPY, color="#000000", size=18),
                                    ft.Text("Copiar Chave PIX", color="#000000", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(13)),
                                ],
                                spacing=6,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=AppColors.SECONDARY_GOLD,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=AppPadding.all(12),
                            ),
                            on_click=copiar_pix,
                        ),
                        ft.Container(height=4),
                        ft.Text("Após o pagamento, envie o comprovante para a Secretaria confirmar sua inscrição:", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(Icons.SEND, color="#FFFFFF", size=18),
                                    ft.Text("Enviar Comprovante no WhatsApp", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(13)),
                                ],
                                spacing=6,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=AppColors.ACCENT_GREEN,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=AppPadding.all(12),
                            ),
                            on_click=enviar_whatsapp_secretaria,
                        ),
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=380,
                height=420,
            ),
            actions=[
                ft.TextButton("Fechar", on_click=fechar, style=ft.ButtonStyle(color=AppColors.TEXT_MUTED))
            ],
            bgcolor=AppColors.BG_SURFACE,
        )
        
        page.open(dlg_pix)
        page.update()


class CompraProdutoModal:
    """Modal de checkout e compra de itens da Lojinha ou Cantina da igreja."""
    @staticmethod
    def abrir(page: ft.Page, produto: ProdutoLoja):
        txt_nome = ft.TextField(
            label="Seu Nome Completo *",
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(13),
        )
        
        txt_whatsapp = ft.TextField(
            label="Seu WhatsApp *",
            keyboard_type=ft.KeyboardType.PHONE,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(13),
        )
        
        txt_qtd = ft.TextField(
            label="Quantidade",
            value="1",
            keyboard_type=ft.KeyboardType.NUMBER,
            width=80,
            color=AppColors.TEXT_WHITE,
            border_color=AppColors.BORDER_DEFAULT,
            focused_border_color=AppColors.SECONDARY_GOLD,
            text_size=FontScaleManager.s(13),
        )
        
        tamanhos = [t.strip() for t in produto.tamanhos_disponiveis.split(",")] if produto.tamanhos_disponiveis else []
        dd_tamanho = None
        if tamanhos:
            dd_tamanho = ft.Dropdown(
                label="Tamanho",
                value=tamanhos[0],
                options=[ft.dropdown.Option(t) for t in tamanhos],
                width=120,
                color=AppColors.TEXT_WHITE,
                border_color=AppColors.BORDER_DEFAULT,
                focused_border_color=AppColors.SECONDARY_GOLD,
                text_size=FontScaleManager.s(13),
            )
            
        lbl_total = ft.Text(f"R$ {produto.preco:.2f}", size=FontScaleManager.s(18), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD)
        
        def atualizar_total(e):
            try:
                qtd = max(1, int(txt_qtd.value))
            except ValueError:
                qtd = 1
            total = produto.preco * qtd
            lbl_total.value = f"R$ {total:.2f}"
            page.update()
            
        txt_qtd.on_change = atualizar_total
        
        def fechar(e=None):
            try:
                page.close(dlg)
            except Exception:
                dlg.open = False
                page.update()
                
        def copiar_pix(e):
            ShareEngine.copy_to_clipboard(page, CHAVE_PIX_OFICIAL, "Chave PIX copiada!")

        def enviar_pedido_whatsapp(e):
            nome = txt_nome.value.strip() if txt_nome.value else ""
            whats = txt_whatsapp.value.strip() if txt_whatsapp.value else ""
            if not nome:
                ShareEngine.show_feedback(page, "Por favor, informe seu nome.")
                return
            try:
                qtd = max(1, int(txt_qtd.value))
            except ValueError:
                qtd = 1
            total = produto.preco * qtd
            tam_str = f" | Tamanho: {dd_tamanho.value}" if dd_tamanho else ""
            
            msg = (
                f"🛍️ *PEDIDO - LOJINHA & CANTINA IBPM CR*\n\n"
                f"👤 *Cliente:* {nome}\n"
                f"📱 *WhatsApp:* {whats}\n"
                f"🛒 *Produto:* {produto.nome}{tam_str}\n"
                f"🔢 *Quantidade:* {qtd}\n"
                f"💰 *Total a Pagar:* R$ {total:.2f}\n\n"
                f"💳 *Chave PIX:* {CHAVE_PIX_OFICIAL}\n"
                f"📌 _Estou enviando o comprovante de pagamento em anexo para separar meu pedido!_"
            )
            fechar()
            ShareEngine.share_whatsapp_status(page, msg)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.STOREFRONT, color=AppColors.SECONDARY_GOLD, size=24),
                    ft.Text(f"Comprar: {produto.nome}", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(15), color=AppColors.TEXT_WHITE, expand=True),
                    ft.IconButton(icon=Icons.CLOSE, icon_color=AppColors.TEXT_MUTED, on_click=fechar),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(produto.descricao, size=FontScaleManager.s(12), color=AppColors.TEXT_SECONDARY),
                        ft.Container(height=4),
                        txt_nome,
                        txt_whatsapp,
                        ft.Row(controls=[txt_qtd, dd_tamanho] if dd_tamanho else [txt_qtd], spacing=8),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text("Total do Pedido:", size=FontScaleManager.s(14), color=AppColors.TEXT_WHITE),
                                    lbl_total,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            bgcolor=AppColors.BG_DARK,
                            padding=AppPadding.all(10),
                            border_radius=8,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(Icons.CONTENT_COPY, color="#000000", size=16),
                                    ft.Text("Copiar Chave PIX", color="#000000", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                ],
                                spacing=4,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=AppColors.SECONDARY_GOLD,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=AppPadding.all(10),
                            ),
                            on_click=copiar_pix,
                        ),
                        ft.ElevatedButton(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(Icons.SEND, color="#FFFFFF", size=16),
                                    ft.Text("Confirmar Pedido no WhatsApp", color="#FFFFFF", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(12)),
                                ],
                                spacing=4,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            style=ft.ButtonStyle(
                                bgcolor=AppColors.ACCENT_GREEN,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                padding=AppPadding.all(10),
                            ),
                            on_click=enviar_pedido_whatsapp,
                        ),
                    ],
                    spacing=6,
                    scroll=ft.ScrollMode.AUTO,
                ),
                width=360,
                height=420,
            ),
            bgcolor=AppColors.BG_SURFACE,
        )
        page.open(dlg)
        page.update()


class LojinhaModal:
    """Modal catálogo completo da Lojinha & Cantina da igreja."""
    @staticmethod
    def abrir(page: ft.Page):
        db = DatabaseService()
        categoria_ativa = ["Todos"]
        produtos_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        def render_produtos():
            cat = categoria_ativa[0]
            produtos = db.get_produtos_loja(cat)
            cards = []
            for p in produtos:
                card = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Image(
                                    src=p.imagem_url,
                                    width=80,
                                    height=80,
                                    fit="cover",
                                    border_radius=8,
                                ),
                                width=80,
                                height=80,
                                border_radius=8,
                                bgcolor=AppColors.BG_DARK,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(p.nome, size=FontScaleManager.s(14), weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE),
                                    ft.Text(p.descricao, size=FontScaleManager.s(11), color=AppColors.TEXT_MUTED, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                                    ft.Row(
                                        controls=[
                                            ft.Text(f"R$ {p.preco:.2f}", size=FontScaleManager.s(15), weight=ft.FontWeight.BOLD, color=AppColors.SECONDARY_GOLD),
                                            ft.ElevatedButton(
                                                "Comprar",
                                                icon=Icons.SHOPPING_BAG,
                                                style=ft.ButtonStyle(
                                                    bgcolor=AppColors.PRIMARY_RUBI,
                                                    color="#FFFFFF",
                                                    shape=ft.RoundedRectangleBorder(radius=6),
                                                    padding=AppPadding.symmetric(horizontal=10, vertical=6),
                                                ),
                                                on_click=lambda e, prod=p: CompraProdutoModal.abrir(page, prod),
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    )
                                ],
                                expand=True,
                                spacing=2,
                            )
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=AppColors.BG_SURFACE_ALT,
                    padding=AppPadding.all(10),
                    border_radius=10,
                    border=AppBorder.all(1, AppColors.BORDER_DEFAULT),
                )
                cards.append(card)
            produtos_container.controls = cards
            page.update()

        def set_categoria(cat):
            categoria_ativa[0] = cat
            btn_row.controls = [criar_chip(c) for c in ["Todos", "Vestuário", "Cantina", "Livros", "Lembranças"]]
            render_produtos()

        def criar_chip(c):
            ativo = (c == categoria_ativa[0])
            return ft.Container(
                content=ft.Text(c, size=FontScaleManager.s(11), weight=ft.FontWeight.BOLD if ativo else ft.FontWeight.NORMAL, color=AppColors.TEXT_WHITE if ativo else AppColors.TEXT_SECONDARY),
                bgcolor=AppColors.PRIMARY_RUBI if ativo else AppColors.BG_DARK,
                padding=AppPadding.symmetric(horizontal=10, vertical=6),
                border_radius=14,
                border=AppBorder.all(1, AppColors.PRIMARY_RUBI if ativo else AppColors.BORDER_DEFAULT),
                ink=True,
                on_click=lambda e, cat=c: set_categoria(cat),
            )

        btn_row = ft.Row(
            controls=[criar_chip(c) for c in ["Todos", "Vestuário", "Cantina", "Livros", "Lembranças"]],
            scroll=ft.ScrollMode.AUTO,
            spacing=6,
        )

        def fechar(e=None):
            try:
                page.close(dlg)
            except Exception:
                dlg.open = False
                page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(Icons.STOREFRONT, color=AppColors.SECONDARY_GOLD, size=24),
                    ft.Text("Lojinha do Reino & Cantina IBPM", weight=ft.FontWeight.BOLD, size=FontScaleManager.s(15), color=AppColors.TEXT_WHITE, expand=True),
                    ft.IconButton(icon=Icons.CLOSE, icon_color=AppColors.TEXT_MUTED, on_click=fechar),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Camisas oficiais de eventos, quentinhas da cantina de domingo, livros e brindes da igreja.", size=FontScaleManager.s(12), color=AppColors.TEXT_MUTED),
                        ft.Container(height=4),
                        btn_row,
                        ft.Divider(color=AppColors.DIVIDER, height=10),
                        ft.Container(content=produtos_container, height=360),
                    ],
                    spacing=4,
                ),
                width=380,
                height=480,
            ),
            bgcolor=AppColors.BG_SURFACE,
        )

        render_produtos()
        page.open(dlg)
        page.update()
