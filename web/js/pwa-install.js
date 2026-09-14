/**
 * Gerenciador de Instalação PWA - IBPM CR
 * Captura o evento beforeinstallprompt e gerencia instalação no Android/iOS/Desktop.
 */

let deferredPrompt = null;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  
  // Exibe banner de instalação PWA se disponível
  const installBanner = document.getElementById('pwa-install-banner');
  if (installBanner) {
    installBanner.style.display = 'flex';
  }
});

window.addEventListener('appinstalled', () => {
  console.log('[PWA] Aplicativo instalado com sucesso!');
  deferredPrompt = null;
  const installBanner = document.getElementById('pwa-install-banner');
  if (installBanner) {
    installBanner.style.display = 'none';
  }
});

function instalarPWA() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('[PWA] Usuário aceitou instalar');
      }
      deferredPrompt = null;
      const installBanner = document.getElementById('pwa-install-banner');
      if (installBanner) installBanner.style.display = 'none';
    });
  } else {
    // Verificação de iOS Safari
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    if (isIOS) {
      alert("📱 Para instalar no iPhone/iPad:\n1. Toque no botão Compartilhar (ícone do quadrado com a seta para cima);\n2. Role para baixo e selecione 'Adicionar à Tela de Início'.");
    } else {
      alert("✅ O aplicativo já está instalado ou pronto para uso no seu navegador!");
    }
  }
}

window.instalarPWA = instalarPWA;
