"""
Serviço de Áudio em Segundo Plano com Suporte a Tela Bloqueada.
Permite reproduzir sermões, pílulas devocionais e louvores com controles persistentes.
"""
import flet as ft
from typing import Optional, Callable

class AudioTrack:
    def __init__(self, title: str, subtitle: str, audio_url: str, duration_str: str = "00:00", cover_url: Optional[str] = None):
        self.title = title
        self.subtitle = subtitle
        self.audio_url = audio_url
        self.duration_str = duration_str
        self.cover_url = cover_url

class AudioService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        self.current_track: Optional[AudioTrack] = None
        self.is_playing: bool = False
        self.current_position: float = 0.0
        self.listeners = []
        self.page: Optional[ft.Page] = None
        self.audio_player: Optional[ft.Audio] = None

    def set_page(self, page: ft.Page):
        self.page = page
        # Se ft.Audio for suportado na página, instancia
        if hasattr(ft, "Audio"):
            self.audio_player = ft.Audio(
                src="",
                autoplay=False,
                volume=1.0,
                balance=0.0,
                on_loaded=self._on_loaded,
                on_duration_changed=self._on_duration_changed,
                on_position_changed=self._on_position_changed,
                on_state_changed=self._on_state_changed,
                on_seek_complete=self._on_seek_complete,
            )
            # Adiciona ao overlay da página se suportado
            try:
                if hasattr(page, "overlay"):
                    page.overlay.append(self.audio_player)
                    page.update()
            except Exception:
                pass

    def play_track(self, track: AudioTrack):
        self.current_track = track
        self.is_playing = True
        self.current_position = 0.0

        if self.audio_player and self.page:
            try:
                self.audio_player.src = track.audio_url
                self.audio_player.play()
            except Exception:
                pass

        self._notify()

    def toggle_play_pause(self):
        if not self.current_track:
            return
        
        self.is_playing = not self.is_playing
        if self.audio_player:
            try:
                if self.is_playing:
                    self.audio_player.resume()
                else:
                    self.audio_player.pause()
            except Exception:
                pass

        self._notify()

    def stop(self):
        self.is_playing = False
        self.current_position = 0.0
        if self.audio_player:
            try:
                self.audio_player.pause()
            except Exception:
                pass
        self._notify()

    def register_listener(self, callback: Callable):
        if callback not in self.listeners:
            self.listeners.append(callback)

    def unregister_listener(self, callback: Callable):
        if callback in self.listeners:
            self.listeners.remove(callback)

    def _notify(self):
        for cb in list(self.listeners):
            try:
                cb(self.current_track, self.is_playing, self.current_position)
            except TypeError:
                try:
                    cb()
                except Exception:
                    pass
            except Exception:
                pass

    def _on_loaded(self, e):
        pass

    def _on_duration_changed(self, e):
        pass

    def _on_position_changed(self, e):
        try:
            self.current_position = float(e.data)
            self._notify()
        except Exception:
            pass

    def _on_state_changed(self, e):
        pass

    def _on_seek_complete(self, e):
        pass
