function switchLang(lang) {
  var el = document.documentElement;
  var page = el.dataset.page || 'index.html';
  var paths = JSON.parse(el.dataset.langPaths || '{}');
  if (paths[lang]) {
    window.location.href = paths[lang] + page;
  }
}

function toggleMenu() {
  document.getElementById('nav-links').classList.toggle('open');
}

function toggleTheme() {
  var html = document.documentElement;
  var next = html.dataset.theme === 'dark' ? 'light' : 'dark';
  html.dataset.theme = next;
  localStorage.setItem('theme', next);
  // Mermaid diagrams are baked with theme colors at render time.
  // Reload so they re-render with the new theme.
  if (document.querySelector('.mermaid')) {
    location.reload();
  }
}
