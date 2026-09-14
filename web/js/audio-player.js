/**
 * Gerenciador de Áudio & MediaSession - IBPM CR WebApp PWA
 * Suporta reprodução em segundo plano e controles na tela de bloqueio do celular.
 */

class AudioService {
  constructor() {
    this.audio = new Audio();
    this.currentTrack = null;
    this.isPlaying = false;
    this.listeners = [];

    this._setupAudioEvents();
  }

  _setupAudioEvents() {
    this.audio.addEventListener('play', () => {
      this.isPlaying = true;
      this._updateMediaSession();
      this._notify();
    });

    this.audio.addEventListener('pause', () => {
      this.isPlaying = false;
      this._notify();
    });

    this.audio.addEventListener('ended', () => {
      this.isPlaying = false;
      this._notify();
    });

    this.audio.addEventListener('error', (err) => {
      console.warn('[Audio] Erro de reprodução:', err);
      this.isPlaying = false;
      this._notify();
    });
  }

  playTrack(track) {
    if (this.currentTrack && this.currentTrack.url === track.url) {
      if (this.isPlaying) {
        this.pause();
      } else {
        this.resume();
      }
      return;
    }

    this.currentTrack = track;
    this.audio.src = track.url;
    this.audio.play().then(() => {
      this.isPlaying = true;
      this._updateMediaSession();
      this._notify();
    }).catch(err => {
      console.warn('[Audio Play Promise Failed]:', err);
    });
  }

  togglePlayPause() {
    if (!this.currentTrack) return;
    if (this.isPlaying) {
      this.pause();
    } else {
      this.resume();
    }
  }

  pause() {
    this.audio.pause();
    this.isPlaying = false;
    this._notify();
  }

  resume() {
    if (this.audio.src) {
      this.audio.play().catch(e => console.warn(e));
    }
  }

  stop() {
    this.audio.pause();
    this.audio.src = '';
    this.currentTrack = null;
    this.isPlaying = false;
    this._notify();
  }

  subscribe(callback) {
    this.listeners.push(callback);
  }

  _notify() {
    this.listeners.forEach(cb => {
      try { cb(this.currentTrack, this.isPlaying); } catch(e) {}
    });
    this._updateMiniPlayerUI();
  }

  _updateMediaSession() {
    if ('mediaSession' in navigator && this.currentTrack) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: this.currentTrack.title || 'Ministração Pastoral',
        artist: this.currentTrack.artist || 'IBPM Carvalho Ramos',
        album: 'Super-App Oficial',
        artwork: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' }
        ]
      });

      navigator.mediaSession.setActionHandler('play', () => this.resume());
      navigator.mediaSession.setActionHandler('pause', () => this.pause());
      navigator.mediaSession.setActionHandler('stop', () => this.stop());
    }
  }

  _updateMiniPlayerUI() {
    const miniPlayer = document.getElementById('floating-mini-player');
    if (!miniPlayer) return;

    if (this.currentTrack) {
      miniPlayer.style.display = 'flex';
      
      const titleEl = miniPlayer.querySelector('.mini-player-title');
      const subEl = miniPlayer.querySelector('.mini-player-sub');
      const playBtn = miniPlayer.querySelector('#mini-play-btn');

      if (titleEl) titleEl.textContent = this.currentTrack.title;
      if (subEl) subEl.textContent = this.currentTrack.subtitle || 'IBPM CR';
      if (playBtn) {
        playBtn.innerHTML = this.isPlaying 
          ? `<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>`
          : `<svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>`;
      }
    } else {
      miniPlayer.style.display = 'none';
    }
  }
}

window.audioService = new AudioService();
