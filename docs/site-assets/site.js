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
