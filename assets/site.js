(() => {
  'use strict';
  const pages = [...document.querySelectorAll('[data-page]')];
  const pageNames = new Set(pages.map(page => page.dataset.page));
  const navigation = document.getElementById('navigation');
  const navLinks = [...navigation.querySelectorAll('a[href^="#"]')];
  const toggle = document.querySelector('.menu-toggle');
  const infoMenu = document.querySelector('.nav-info');
  const main = document.getElementById('main');
  const researchAnchors = new Map([
    ['dynamics', 'research-dynamics'],
    ['interactions', 'research-interactions'],
    ['sequences', 'research-sequences'],
  ]);
  // The router positions each view; avoid a saved browser position overriding
  // a direct link while the document is loading.
  if ('scrollRestoration' in window.history) window.history.scrollRestoration = 'manual';

  function closeMenu(restoreFocus = false) {
    navigation.classList.remove('open');
    infoMenu.open = false;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    if (restoreFocus) toggle.focus();
  }

  function route(moveFocus = false) {
    let fragment;
    try {
      fragment = decodeURIComponent(window.location.hash.slice(1));
    } catch {
      fragment = 'home';
    }
    if (fragment === 'main') {
      closeMenu();
      main.focus({ preventScroll: true });
      main.scrollIntoView({ block: 'start' });
      return;
    }
    const nativeAnchor = [...researchAnchors].find(([, id]) => id === fragment);
    const [requestedPage, section] = nativeAnchor
      ? ['research', nativeAnchor[0]]
      : fragment.split('/');
    const key = pageNames.has(requestedPage) ? requestedPage : 'home';
    const currentPage = pages.find(page => page.dataset.page === key);
    for (const page of pages) page.hidden = page !== currentPage;
    for (const link of navLinks) {
      if (link.hash === `#${key}`) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    }
    const name = key === 'home' ? 'Ren Protein Design Group' : `${key[0].toUpperCase()}${key.slice(1)} | Ren Protein Design Group`;
    document.title = `${name} · RPDGroup`;
    closeMenu();
    let target;
    if (fragment === 'highlights') target = document.getElementById('highlights');
    else if (key === 'research' && researchAnchors.has(section)) target = document.getElementById(researchAnchors.get(section));
    // Wait until the newly shown section has a layout before positioning it.
    requestAnimationFrame(() => {
      if (currentPage.hidden) return;
      if (moveFocus) currentPage.querySelector('h1')?.focus({ preventScroll: true });
      if (target) target.scrollIntoView({ block: 'start' });
      else window.scrollTo(0, 0);
    });
  }

  toggle.addEventListener('click', () => {
    const open = navigation.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (infoMenu.open) {
      infoMenu.open = false;
      infoMenu.querySelector('summary').focus();
    } else if (navigation.classList.contains('open')) closeMenu(true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.nav-info')) infoMenu.open = false;
    if (!event.target.closest('.site-header') && navigation.classList.contains('open')) closeMenu();
  });
  for (const link of navLinks) {
    link.addEventListener('click', () => {
      if (link.hash === window.location.hash) {
        closeMenu();
        window.scrollTo(0, 0);
      }
    });
  }
  window.matchMedia('(min-width: 1021px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
  });

  const search = document.getElementById('resource-search');
  const cards = [...document.querySelectorAll('.resource-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const count = document.getElementById('resource-count');
  const reset = document.querySelector('.reset-filters');
  const empty = document.querySelector('.empty-state');
  let category = 'all';
  const index = cards.map(card => ({ card, text: card.textContent.toLowerCase() }));

  function filterResources() {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const item of index) {
      const inCategory = category === 'all' || item.card.dataset.category === category;
      const matches = inCategory && terms.every(term => item.text.includes(term));
      item.card.hidden = !matches;
      if (matches) visible += 1;
    }
    for (const button of filters) button.setAttribute('aria-pressed', String(button.dataset.filter === category));
    count.textContent = `${visible} ${visible === 1 ? 'resource' : 'resources'}`;
    empty.hidden = visible !== 0;
    reset.hidden = category === 'all' && terms.length === 0;
  }

  search.addEventListener('input', filterResources);
  for (const button of filters) {
    button.addEventListener('click', () => {
      category = button.dataset.filter;
      filterResources();
    });
  }
  reset.addEventListener('click', () => {
    category = 'all';
    search.value = '';
    filterResources();
    search.focus();
  });

  const viewer = document.getElementById('media-viewer');
  if (viewer && typeof viewer.showModal === 'function') {
    const image = viewer.querySelector('.media-viewer-image');
    const title = document.getElementById('media-viewer-title');
    const source = viewer.querySelector('.media-viewer-source');
    let trigger;
    for (const link of document.querySelectorAll('[data-media]')) {
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        trigger = link;
        image.src = link.href;
        image.alt = link.querySelector('img')?.alt || link.dataset.title;
        title.textContent = link.dataset.title;
        source.href = link.dataset.source || link.href;
        source.textContent = link.dataset.source ? 'Original figure on GitHub ↗' : 'Open photograph ↗';
        document.body.classList.add('has-media-viewer');
        viewer.showModal();
      });
    }
    viewer.querySelector('.media-viewer-close').addEventListener('click', () => viewer.close());
    viewer.addEventListener('click', event => {
      if (event.target !== viewer) return;
      const bounds = viewer.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
    });
    viewer.addEventListener('close', () => {
      document.body.classList.remove('has-media-viewer');
      image.removeAttribute('src');
      trigger?.focus({ preventScroll: true });
    });
  }

  // All content is readable as native anchor sections if JavaScript is disabled.
  for (const page of pages) page.hidden = page.dataset.page !== 'home';
  document.body.classList.add('js');
  document.querySelector('.resource-controls').hidden = false;
  document.querySelector('.result-bar').hidden = false;
  window.addEventListener('hashchange', () => route(true));
  window.addEventListener('load', () => route(false), { once: true });
  route(false);
})();
