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
