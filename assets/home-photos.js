(() => {
  'use strict';
  const root = document.querySelector('[data-photo-carousel]');
  if (!root) return;
  const slides = [...root.querySelectorAll('.photo-slide')];
  const controls = root.querySelector('.photo-controls');
  if (slides.length < 2 || !controls) return;
  const wall = root.querySelector('.photo-wall');
  const page = root.closest('[data-page]');
  const play = root.querySelector('[data-photo-play]');
  const selector = root.querySelector('[data-photo-select]');
  const label = controls.querySelector('[data-photo-label]');
  const announcement = root.querySelector('.photo-announcement');
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const interval = Math.max(3000, Number(root.dataset.interval) || 3000);
  const preparations = new Map();
  let index = 0;
  let paused = motion.matches;
  let hovering = false;
  let onscreen = !('IntersectionObserver' in window);
  let timer;
  let request = 0;

  function canRotate() {
    return !paused && !hovering && onscreen && !page?.hidden &&
      document.visibilityState === 'visible' && !document.querySelector('dialog[open]');
  }

  function schedule() {
    window.clearTimeout(timer);
    if (canRotate()) timer = window.setTimeout(() => change(index + 1), interval);
  }

  function updatePlay() {
    play.setAttribute('aria-label', paused ? 'Play photo rotation' : 'Pause photo rotation');
    play.querySelector('[data-photo-play-icon]').textContent = paused ? '▶' : 'Ⅱ';
    play.querySelector('[data-photo-play-text]').textContent = paused ? 'Play' : 'Pause';
    root.dataset.paused = String(paused);
  }

  function setPaused(value) {
    paused = value;
    updatePlay();
    schedule();
  }

  function prepare(slideIndex) {
    if (preparations.has(slideIndex)) return preparations.get(slideIndex);
    const promise = Promise.all([...slides[slideIndex].querySelectorAll('img')].map(image => {
      image.loading = 'eager';
      if (typeof image.decode === 'function') return image.decode();
      if (image.complete && image.naturalWidth) return Promise.resolve();
      return new Promise((resolve, reject) => {
        image.addEventListener('load', resolve, { once: true });
        image.addEventListener('error', reject, { once: true });
      });
    })).then(() => true).catch(() => {
      preparations.delete(slideIndex);
      return false;
    });
    preparations.set(slideIndex, promise);
    return promise;
  }

  async function change(nextIndex, manual = false) {
    window.clearTimeout(timer);
    if (manual) setPaused(true);
    const ticket = ++request;
    const target = (nextIndex + slides.length) % slides.length;
    root.setAttribute('aria-busy', 'true');
    const ready = await prepare(target);
    if (ticket !== request) return;
    root.removeAttribute('aria-busy');
    if (!ready) {
      if (manual) announcement.textContent = 'Photographs could not be loaded. Please try again.';
      schedule();
      return;
    }
    if (!manual && !canRotate()) {
      schedule();
      return;
    }
    const moveFocus = manual && slides[index].contains(document.activeElement);
    for (const [i, slide] of slides.entries()) {
      slide.hidden = i !== target;
      slide.classList.remove('is-entering');
    }
    index = target;
    if (!motion.matches) slides[index].classList.add('is-entering');
    label.textContent = slides[index].dataset.photoLabel;
    selector.value = String(index);
    if (manual) announcement.textContent = `Photo set ${index + 1} of ${slides.length}: ${label.textContent}`;
    if (moveFocus) slides[index].querySelector('a').focus({ preventScroll: true });
    prepare((index + 1) % slides.length);
    schedule();
  }

  play.addEventListener('click', () => setPaused(!paused));
  root.querySelector('[data-photo-prev]').addEventListener('click', () => change(index - 1, true));
  root.querySelector('[data-photo-next]').addEventListener('click', () => change(index + 1, true));
  selector.addEventListener('change', () => change(Number(selector.value), true));
  root.addEventListener('focusin', event => {
    if (event.target !== play && !play.contains(event.target)) setPaused(true);
  });
  root.addEventListener('click', event => {
    if (event.target.closest('[data-media]')) setPaused(true);
  });
  root.addEventListener('keydown', event => {
    if (event.target instanceof HTMLSelectElement) return;
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      change(index + (event.key === 'ArrowLeft' ? -1 : 1), true);
    }
  });
  wall.addEventListener('pointerenter', event => {
    if (event.pointerType === 'mouse') { hovering = true; schedule(); }
  });
  wall.addEventListener('pointerleave', event => {
    if (event.pointerType === 'mouse') { hovering = false; schedule(); }
  });
  wall.addEventListener('animationend', event => event.target.classList.remove('is-entering'));
  document.addEventListener('visibilitychange', schedule);
  window.addEventListener('hashchange', schedule);
  motion.addEventListener('change', event => { if (event.matches) setPaused(true); });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      onscreen = entries[0].isIntersecting;
      schedule();
    });
    observer.observe(root);
  }
  controls.hidden = false;
  updatePlay();
  prepare(1);
  schedule();
})();
