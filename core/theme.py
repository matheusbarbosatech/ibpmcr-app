"""
Tema Oficial 'Coração Ardente' & Sistema de Acessibilidade Sênior - IBPM CR.
Atende rigorosamente aos critérios WCAG AAA de alto contraste e redimensionamento dinâmico.
"""
import flet as ft

# Compatibilidade universal de componentes entre versões do Flet
Icons = getattr(ft, "Icons", getattr(ft, "icons", None))
Colors = getattr(ft, "Colors", getattr(ft, "colors", None))
NavigationDestination = getattr(ft, "NavigationBarDestination", getattr(ft, "NavigationDestination", None))

class AppColors:
    # Fundo Principal e Superfícies
    BG_DARK = "#07090E"         # Dark Obsidian Profundo (evita cansaço visual)
    BG_SURFACE = "#131722"      # Superfície dos cards com efeito glassmorphism suave
    BG_SURFACE_ALT = "#1C2233"  # Variação sutil para cabeçalhos e destaques
    BG_SELECTED = "#2A1820"     # Fundo com leve tom rubi para itens ativos
    TRANSPARENT = "transparent"

    # Cores Principais 'Coração Ardente'
    PRIMARY_RUBI = "#E11D48"    # Rubi / Fogo Pentecostal
    PRIMARY_RUBI_DARK = "#BE123C"
    SECONDARY_GOLD = "#F59E0B"  # Ouro Imperial do Altar
    GOLD_LIGHT = "#FCD34D"

    # Textos de Máximo Contraste (WCAG AAA)
    TEXT_WHITE = "#FFFFFF"      # Branco Puro para contraste absoluto
    TEXT_SECONDARY = "#CBD5E1"  # Cinza claro para leitura longa confortável
    TEXT_MUTED = "#94A3B8"      # Cinza médio para legendas discretas
    
    # Acentos de Ação
    ACCENT_GREEN = "#10B981"    # Verde WhatsApp e Ações de Sucesso
    ACCENT_BLUE = "#38BDF8"     # Azul para informações e links
    DANGER = "#EF4444"          # Vermelho para cancelamento/alerta

    # Bordas e Divisores
    BORDER_DEFAULT = "#222B3D"  # Borda neutra elegante
    BORDER_GOLD = "#F59E0B"     # Borda dourada para cards em destaque
    BORDER_RUBI = "#E11D48"     # Borda rubi para itens ativos
    DIVIDER = "#1B2232"

class FontScaleManager:
    """
    Gerenciador Global de Acessibilidade Sênior para Idosos.
    Permite aumentar/diminuir a fonte em todo o aplicativo entre 80% e 150%.
    """
    SCALE_LEVELS = [0.85, 1.0, 1.15, 1.30, 1.50]
    _current_index = 1  # Inicia em 1.0 (100%)
    _listeners = []

    @classmethod
    def get_scale(cls) -> float:
        return cls.SCALE_LEVELS[cls._current_index]

    @classmethod
    def s(cls, base_size: float) -> float:
        """Retorna o tamanho da fonte proporcional à escala ativa."""
        return round(base_size * cls.get_scale(), 1)

    @classmethod
    def increase(cls):
        if cls._current_index < len(cls.SCALE_LEVELS) - 1:
            cls._current_index += 1
            cls._notify()

    @classmethod
    def decrease(cls):
        if cls._current_index > 0:
            cls._current_index -= 1
            cls._notify()

    @classmethod
    def register_listener(cls, callback):
        if callback not in cls._listeners:
            cls._listeners.append(callback)

    @classmethod
    def unregister_listener(cls, callback):
        if callback in cls._listeners:
            cls._listeners.remove(callback)

    @classmethod
    def _notify(cls):
        for cb in cls._listeners:
            try:
                cb()
            except Exception:
                pass

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
    def all(width: float = 1, color: str = "#222B3D"):
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
