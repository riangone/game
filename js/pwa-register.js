/**
 * Hyperion PWA Universal Register & Installation Controller
 */
(function () {
  'use strict';

  // 1. Ensure PWA Meta Tags & Manifest are present
  function ensurePwaMeta() {
    // Add Manifest link if missing
    if (!document.querySelector('link[rel="manifest"]')) {
      const manifestLink = document.createElement('link');
      manifestLink.rel = 'manifest';
      manifestLink.href = 'manifest.json';
      document.head.appendChild(manifestLink);
    }

    // Add theme-color if missing
    if (!document.querySelector('meta[name="theme-color"]')) {
      const themeMeta = document.createElement('meta');
      themeMeta.name = 'theme-color';
      themeMeta.content = '#0284c7';
      document.head.appendChild(themeMeta);
    }

    // Add iOS Safari meta tags
    if (!document.querySelector('meta[name="apple-mobile-web-app-capable"]')) {
      const iosCapable = document.createElement('meta');
      iosCapable.name = 'apple-mobile-web-app-capable';
      iosCapable.content = 'yes';
      document.head.appendChild(iosCapable);
    }

    if (!document.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]')) {
      const iosStatus = document.createElement('meta');
      iosStatus.name = 'apple-mobile-web-app-status-bar-style';
      iosStatus.content = 'default';
      document.head.appendChild(iosStatus);
    }

    // Add Apple Touch Icon if missing
    if (!document.querySelector('link[rel="apple-touch-icon"]')) {
      const appleIcon = document.createElement('link');
      appleIcon.rel = 'apple-touch-icon';
      appleIcon.sizes = '180x180';
      appleIcon.href = 'icons/apple-touch-icon.png';
      document.head.appendChild(appleIcon);
    }

    // Add Favicon SVG if missing
    if (!document.querySelector('link[rel="icon"]')) {
      const fav = document.createElement('link');
      fav.rel = 'icon';
      fav.type = 'image/svg+xml';
      fav.href = 'icons/favicon.svg';
      document.head.appendChild(fav);
    }
  }

  // 2. Service Worker Registration & Update Handling
  function registerServiceWorker() {
    if (!('serviceWorker' in navigator)) return;

    window.addEventListener('load', () => {
      // Determine correct sw path relative to root
      const swUrl = 'sw.js';

      navigator.serviceWorker
        .register(swUrl)
        .then((registration) => {
          // Listen for update found
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            if (!newWorker) return;

            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // New update available, notify user with subtle toast
                showUpdateToast(registration);
              }
            });
          });
        })
        .catch((error) => {
          console.warn('[PWA] ServiceWorker registration error:', error);
        });

      let refreshing = false;
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        if (!refreshing) {
          refreshing = true;
          window.location.reload();
        }
      });
    });
  }

  // Toast notification for PWA updates
  function showUpdateToast(registration) {
    if (document.getElementById('pwa-update-toast')) return;

    const toast = document.createElement('div');
    toast.id = 'pwa-update-toast';
    toast.innerHTML = `
      <div style="position:fixed;bottom:24px;right:24px;z-index:99999;background:#0f172a;color:#f8fafc;padding:12px 18px;border-radius:12px;box-shadow:0 10px 25px rgba(0,0,0,0.25);font-size:14px;display:flex;align-items:center;gap:12px;border:1px solid #334155;animation:pwaSlideUp 0.3s ease;">
        <span>✨ 发现新版本已就绪</span>
        <button id="pwa-refresh-btn" style="background:#0284c7;color:#fff;border:none;padding:6px 14px;border-radius:8px;cursor:pointer;font-weight:600;font-size:13px;">点击刷新</button>
        <button id="pwa-dismiss-btn" style="background:transparent;color:#94a3b8;border:none;cursor:pointer;font-size:16px;">×</button>
      </div>
      <style>
        @keyframes pwaSlideUp {
          from { transform: translateY(30px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
      </style>
    `;
    document.body.appendChild(toast);

    document.getElementById('pwa-refresh-btn').onclick = () => {
      if (registration.waiting) {
        registration.waiting.postMessage({ type: 'SKIP_WAITING' });
      }
    };

    document.getElementById('pwa-dismiss-btn').onclick = () => {
      toast.remove();
    };
  }

  // 3. Install Prompt (A2HS) Management
  let deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    // Reveal any existing install buttons on the page
    const installButtons = document.querySelectorAll('[data-pwa-install], #pwa-install-btn');
    installButtons.forEach((btn) => {
      btn.style.display = 'inline-flex';
      btn.onclick = () => triggerInstall(btn);
    });

    // Dispatch custom event for custom UI
    window.dispatchEvent(new CustomEvent('pwa-can-install', { detail: { prompt: e } }));
  });

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    const installButtons = document.querySelectorAll('[data-pwa-install], #pwa-install-btn');
    installButtons.forEach((btn) => {
      btn.style.display = 'none';
    });
    console.log('[PWA] Hyperion successfully installed as PWA.');
  });

  function triggerInstall(triggerElement) {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        if (triggerElement) triggerElement.style.display = 'none';
      }
      deferredPrompt = null;
    });
  }

  // Expose global controller
  window.HyperionPWA = {
    install: triggerInstall,
    getPrompt: () => deferredPrompt,
    isStandalone: () => window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true
  };

  // Run initialization
  ensurePwaMeta();
  registerServiceWorker();
})();
