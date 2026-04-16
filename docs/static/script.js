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
  // Re-render mermaid diagrams if present
  if (typeof mermaid !== 'undefined') {
    document.querySelectorAll('.mermaid[data-processed]').forEach(function(el) {
      el.removeAttribute('data-processed');
      el.innerHTML = el.dataset.source || el.textContent;
    });
    mermaid.initialize({
      startOnLoad: false,
      theme: next === 'dark' ? 'dark' : 'default'
    });
    mermaid.run();
  }
}
