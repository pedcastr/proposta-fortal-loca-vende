// Cola no console do sistema da Zé Loc (local) para tirar os prints com a cara da Fortal.
(function () {
  if (window.__fortal) return; window.__fortal = true;
  var R = { 50:'#FEECEC',100:'#FDD3D4',200:'#FBA7AA',300:'#F7737A',400:'#F0414A',500:'#E3121B',600:'#C00F17',700:'#9E0D13',800:'#7F0B10',900:'#66090D',950:'#3A0507' };
  var base = Object.keys(R).map(function (k) { return '--brand-' + k + ':' + R[k] + ' !important;'; }).join('');
  var light = base +
    '--marca-logo:#E3121B!important;--sidebar-brilho:#E3121B!important;--sidebar-item-active-text:#F7737A!important;--sidebar-item-active-bar:#F0414A!important;' +
    '--primary:#C00F17!important;--primary-hover:#9E0D13!important;--primary-subtle:#FEECEC!important;--link:#9E0D13!important;--accent:#E3121B!important;' +
    '--focus-ring:#C00F17!important;--avatar-bg:#C00F17!important;--grafico-1:#E3121B!important;' +
    '--sidebar-gradiente:linear-gradient(180deg,#E3121B26 0%,#E3121B0A 22%,#E3121B00 46%),radial-gradient(120% 55% at 50% 100%,#E3121B1F 0%,#E3121B00 72%),linear-gradient(180deg,#141213 0%,#0B0A0B 100%)!important;';
  var dark = '--primary-subtle:#3A0507!important;--link:#F7737A!important;--accent:#F0414A!important;--accent-text:#3A0507!important;--focus-ring:#F0414A!important;--grafico-1:#F0414A!important;';
  var st = document.createElement('style');
  st.textContent = ':root{' + light + '}:root[data-theme="dark"]{' + dark + '}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){' + dark + '}}';
  document.head.appendChild(st);
  var LOGO = 'http://127.0.0.1:8765/img/logo-fortal.png', ICONE = 'http://127.0.0.1:8765/img/icone.png';
  var SOB = ['Lima','Souza','Oliveira','Costa','Pereira','Nunes','Rocha','Alves','Moura','Freitas','Barros','Teixeira','Cavalcante','Sampaio','Holanda'];
  var troca = function () {
    document.querySelectorAll('img').forEach(function (i) {
      if (i.dataset.f) return;
      if (/logo|simbolo|ze-?loc/i.test(i.src + ' ' + i.alt)) {
        var quad = i.width && i.height && Math.abs(i.width - i.height) < 8;
        i.src = quad ? ICONE : LOGO; i.dataset.f = 1;
        if (!quad) { i.style.objectFit = 'contain'; }
      }
    });
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), n;
    while ((n = w.nextNode())) {
      var t = n.nodeValue;
      if (/Z[ée] ?Loc|Check ?J[áa]|Auto ?Elite/i.test(t)) n.nodeValue = t.replace(/Z[ée] ?Loc Motos/gi, 'Fortal Loca & Vende').replace(/Z[ée] ?Loc/gi, 'Fortal').replace(/Check ?J[áa]/gi, 'SafeLock').replace(/Auto ?Elite/gi, 'ÁgilLock');
      if (/Demonstra[çc][ãa]o|DEMO0/.test(n.nodeValue)) { n.nodeValue = n.nodeValue.replace(/Demonstra[çc][ãa]o/g, function () { return SOB[(window.__si = (window.__si || 0) + 1) % SOB.length]; }).replace(/DEMO0+(\d+)/g, function (m, d) { return 'E' + (40817350 + (+d) * 7919); }); }
    }
    document.title = document.title.replace(/Z[ée] ?Loc( Motos)?/gi, 'Fortal Loca & Vende');
  };
  troca();
  new MutationObserver(troca).observe(document.body, { childList: true, subtree: true, characterData: true });

  // ---- maquiagem dos números (só na tela, para o print) ----
  var brl = function (v) { return 'R$ ' + v.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };
  window.__brl = brl;
  window.__txt = function (map, root) {
    var w = document.createTreeWalker(root || document.body, NodeFilter.SHOW_TEXT), n, k = 0;
    while ((n = w.nextNode())) { var t = n.nodeValue.replace(/ /g, ' ').trim(); if (map.hasOwnProperty(t)) { n.nodeValue = map[t]; k++; } }
    return k;
  };
  window.__zeros = function (root, min, max) {
    var w = document.createTreeWalker(root || document.body, NodeFilter.SHOW_TEXT), n, k = 0;
    while ((n = w.nextNode())) { if (n.nodeValue.replace(/ /g, ' ').trim() === 'R$ 0,00') { n.nodeValue = brl(Math.round((min + Math.random() * (max - min)) / 10) * 10); k++; } }
    return k;
  };
  // barras: cada coluna é um span flex-col com [rótulo, barra com height inline]
  window.__barras = function (titulo, serie) {
    var h = [].slice.call(document.querySelectorAll('*')).find(function (e) { return e.childElementCount === 0 && e.textContent.trim() === titulo; });
    if (!h) return 'sem ' + titulo;
    var c = h; for (var i = 0; i < 6 && c; i++) { if (c.querySelectorAll('span[style*="height"]').length > 3) break; c = c.parentElement; }
    var barras = [].slice.call(c.querySelectorAll('span[style*="height"]'));
    var max = Math.max.apply(null, serie), alt = 120;
    barras.forEach(function (b, i) {
      var v = serie[i % serie.length]; b.style.height = Math.max(4, Math.round(v / max * alt)) + 'px';
      var lab = b.previousElementSibling; if (lab) lab.textContent = brl(v);
    });
    return barras.length;
  };

  // esconde o que é do rastreador próprio da Zé Loc (a Fortal usa a ÁgilLock)
  window.__limpa = function () {
    var all = [].slice.call(document.querySelectorAll('a,button,div,section'));
    all.forEach(function (e) {
      var t = (e.innerText || '').trim();
      if (/manuten[çc][ãa]o(es)? de aparelho/i.test(t) && t.length < 140 && e.offsetHeight < 120) e.style.display = 'none';
    });
    [].slice.call(document.querySelectorAll('aside a, aside button, nav a, nav button')).forEach(function (e) {
      if (/^Rastreamento(\s*\d+)?$/.test((e.innerText || '').trim())) { var li = e.closest('li') || e; li.style.display = 'none'; }
    });
  };
  // percentual positivo: verde e seta para cima
  window.__positivo = function (root) {
    [].slice.call((root || document).querySelectorAll('*')).forEach(function (e) {
      if (e.childElementCount === 0 && /^\+\d/.test((e.textContent || '').trim()) && /vs\./.test(e.textContent)) {
        var box = e.parentElement; box.style.color = '#22c55e';
        var sv = box.querySelector('svg'); if (sv) { sv.style.transform = 'rotate(180deg)'; sv.style.color = '#22c55e'; }
      }
    });
  };
  window.__ir = function (p) { history.pushState({}, '', p); dispatchEvent(new PopStateEvent('popstate')); };
})();
