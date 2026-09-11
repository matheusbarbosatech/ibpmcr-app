"""
Design System e Constantes Visuais do IBPM CR App.
Compatibilidade universal 100% resiliente com qualquer versão do Flet (incluindo Flet 0.28+).
"""
import flet as ft

# Compatibilidade universal de ícones, cores e navegação
Icons = getattr(ft, "Icons", getattr(ft, "icons", None))
Colors = getattr(ft, "Colors", getattr(ft, "colors", None))
NavigationDestination = getattr(ft, "NavigationBarDestination", getattr(ft, "NavigationDestination", None))

# Helpers de Layout Universais (Padding, Margin, Border, Alignment)
class AppAlignment:
    CENTER = ft.Alignment(0, 0) if hasattr(ft, "Alignment") else getattr(ft.alignment, "center", None)
    TOP_LEFT = ft.Alignment(-1, -1) if hasattr(ft, "Alignment") else getattr(ft.alignment, "top_left", None)
    TOP_RIGHT = ft.Alignment(1, -1) if hasattr(ft, "Alignment") else getattr(ft.alignment, "top_right", None)
    BOTTOM_LEFT = ft.Alignment(-1, 1) if hasattr(ft, "Alignment") else getattr(ft.alignment, "bottom_left", None)
    BOTTOM_RIGHT = ft.Alignment(1, 1) if hasattr(ft, "Alignment") else getattr(ft.alignment, "bottom_right", None)

class AppPadding:
    @staticmethod
    def all(value: float):
        if hasattr(ft, "Padding"):
            return ft.Padding(left=value, top=value, right=value, bottom=value)
        return value

    @staticmethod
    def symmetric(horizontal: float = 0, vertical: float = 0):
        if hasattr(ft, "Padding"):
            return ft.Padding(left=horizontal, top=vertical, right=horizontal, bottom=vertical)
        return vertical

    @staticmethod
    def only(left: float = 0, top: float = 0, right: float = 0, bottom: float = 0):
        if hasattr(ft, "Padding"):
            return ft.Padding(left=left, top=top, right=right, bottom=bottom)
        return top

class AppMargin:
    @staticmethod
    def only(left: float = 0, top: float = 0, right: float = 0, bottom: float = 0):
        if hasattr(ft, "Margin"):
            return ft.Margin(left=left, top=top, right=right, bottom=bottom)
        return top

    @staticmethod
    def all(value: float):
        if hasattr(ft, "Margin"):
            return ft.Margin(left=value, top=value, right=value, bottom=value)
        return value

class AppBorder:
    @staticmethod
    def all(width: float = 1, color: str = "#334155"):
        try:
            if hasattr(ft.Border, "all"):
                return ft.Border.all(width, color)
        except Exception:
            pass
        try:
            side = ft.BorderSide(width, color)
            return ft.Border(top=side, right=side, bottom=side, left=side)
        except Exception:
            return None

class AppColors:
    # Fundos
    BG_MAIN = "#0B1120"          # Fundo principal profundo
    BG_SURFACE = "#1E293B"       # Superfície de cards e containers
    BG_SURFACE_ALT = "#162032"   # Variação sutil de superfície
    BG_SELECTED = "#2D2619"      # Fundo âmbar escuro para item ativo
    TRANSPARENT = "transparent"
    
    # Acentos e Destaque
    PRIMARY = "#F59E0B"          # Âmbar/Dourado caloroso
    PRIMARY_DARK = "#D97706"     # Âmbar escuro para gradientes/hover
    ACCENT = "#FBBF24"           # Dourado brilhante
    
    # Textos
    TEXT_PRIMARY = "#F8FAFC"     # Branco suave (leitura confortável)
    TEXT_SECONDARY = "#94A3B8"   # Cinza ardósia para legendas
    TEXT_MUTED = "#64748B"       # Cinza discreto
    TEXT_GOLD = "#FCD34D"        # Texto em destaque dourado
    
    # Bordas e Linhas
    BORDER_DEFAULT = "#334155"   # Borda neutra elegante
    BORDER_SELECTED = "#F59E0B"  # Borda dourada de seleção
    DIVIDER = "#1E293B"
    
    # Estados
    SUCCESS = "#10B981"          # Verde esmeralda (oração atendida)
    INFO = "#38BDF8"             # Azul suave
    DANGER = "#EF4444"           # Alerta

SENTIMENTOS_PADRAO = [
    {
        "id": "cansado",
        "emoji": "🕊️",
        "texto": "Estou cansado e não sei explicar o que sinto."
    },
    {
        "id": "peito_pesado",
        "emoji": "🙏",
        "texto": "O peito está pesado hoje, só peço uma oração em silêncio."
    },
    {
        "id": "invisivel",
        "emoji": "🫂",
        "texto": "Me sinto invisível e sozinho no meio da multidão."
    },
    {
        "id": "paz_descanso",
        "emoji": "✨",
        "texto": "Preciso apenas de paz para conseguir descansar hoje."
    },
    {
        "id": "outro",
        "emoji": "✍️",
        "texto": "Outro motivo / Quero escrever uma linha..."
    }
]
