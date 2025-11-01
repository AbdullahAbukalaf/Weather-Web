(() => {
  "use strict";
  const forms = document.querySelectorAll('.needs-validation');
  const input = document.querySelector('input[name="city"]');
  const searchBtn = document.getElementById('searchBtn');
  const themeBtn = document.getElementById('themeToggle');

  // Theme init
  const THEME_KEY = 'theme';
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem(THEME_KEY) || (prefersDark ? 'dark' : 'light');
  const applyTheme = (mode) => {
    document.documentElement.setAttribute('data-theme', mode);
    if (themeBtn) themeBtn.innerHTML = mode === 'dark'
      ? '<i class="bi bi-sun"></i><span class="ms-1 d-none d-sm-inline">Light</span>'
      : '<i class="bi bi-moon-stars"></i><span class="ms-1 d-none d-sm-inline">Dark</span>';
  };
  applyTheme(savedTheme);

  themeBtn?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  });

  // Validation + submit feedback
  Array.from(forms).forEach((form) => {
    form.addEventListener('submit', (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      } else {
        // quick visual feedback on submit
        searchBtn?.setAttribute('disabled', 'true');
        if (input) input.setAttribute('readonly', 'true');
        if (searchBtn) searchBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Searching...';
      }
      form.classList.add('was-validated');
    }, false);
  });

  // Autofocus
  input?.focus();

  // Quick city chips
  document.querySelectorAll('[data-city]')?.forEach((chip) => {
    chip.addEventListener('click', () => {
      const city = chip.getAttribute('data-city');
      if (!city || !input) return;
      input.value = city;
      input.focus();
    });
  });
})();

