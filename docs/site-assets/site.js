(() => {
  'use strict';
  const root = document.documentElement;
  const bilingual = document.body.hasAttribute('data-bilingual');
  function setLanguage(lang) {
    const next = lang === 'zh' ? 'zh' : 'en';
    root.dataset.lang = next;
    root.lang = next === 'zh' ? 'zh-CN' : 'en';
    document.querySelectorAll('[data-set-lang]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.setLang === next));
    });
    document.title = next === 'zh'
      ? 'FCoP 4.0 — 让 Agent 的工作，留在对话之外'
      : 'FCoP 4.0 — Keep agent work beyond the conversation';
  }
  if (bilingual) {
    let saved = null;
    try { saved = localStorage.getItem('fcop-lang'); } catch (_) {}
    const requested = new URLSearchParams(location.search).get('lang');
    const preferred = ['zh', 'en'].includes(requested) ? requested : saved;
    setLanguage(['zh', 'en'].includes(preferred) ? preferred : ((navigator.language || 'en').toLowerCase().startsWith('zh') ? 'zh' : 'en'));
    document.querySelectorAll('[data-set-lang]').forEach(button => {
      button.addEventListener('click', () => {
        setLanguage(button.dataset.setLang);
        try { localStorage.setItem('fcop-lang', root.dataset.lang); } catch (_) {}
      });
    });
  }
  const motionButton = document.querySelector('[data-motion-toggle]');
  if (motionButton) {
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let motionPaused = false;
    try { motionPaused = localStorage.getItem('fcop-motion-paused') === 'true'; } catch (_) {}
    function syncMotion() {
      const paused = reducedMotion.matches || motionPaused;
      root.dataset.motionPaused = String(paused);
      motionButton.setAttribute('aria-pressed', String(paused));
      motionButton.disabled = reducedMotion.matches;
      motionButton.querySelector('[data-motion-label="en"]').textContent = reducedMotion.matches
        ? 'Motion off' : (paused ? 'Resume motion' : 'Pause motion');
      motionButton.querySelector('[data-motion-label="zh"]').textContent = reducedMotion.matches
        ? '动效已关' : (paused ? '开启动效' : '暂停动效');
    }
    syncMotion();
    motionButton.hidden = false;
    motionButton.addEventListener('click', () => {
      motionPaused = !motionPaused;
      try { localStorage.setItem('fcop-motion-paused', String(motionPaused)); } catch (_) {}
      syncMotion();
    });
    reducedMotion.addEventListener('change', syncMotion);
    function syncVisibility() { root.dataset.motionSuspended = String(document.hidden); }
    syncVisibility();
    document.addEventListener('visibilitychange', syncVisibility);
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => { entry.target.dataset.motionOffscreen = String(!entry.isIntersecting); });
      });
      document.querySelectorAll('.motion-scene').forEach(scene => observer.observe(scene));
    }
  }
  document.querySelectorAll('[data-copy]').forEach(button => {
    button.addEventListener('click', async () => {
      const code = document.getElementById(button.dataset.copy);
      const status = document.querySelector('.copy-status');
      if (!code) return;
      const label = button.textContent;
      try {
        await navigator.clipboard.writeText(code.textContent);
        const text = root.dataset.lang === 'zh' ? '已复制' : 'Copied';
        button.textContent = text;
        if (status) status.textContent = text;
      } catch (_) {
        const text = root.dataset.lang === 'zh' ? '请手动选择代码' : 'Select code to copy';
        button.textContent = text;
        if (status) status.textContent = text;
      }
      setTimeout(() => { button.textContent = label; }, 2200);
    });
  });
})();
