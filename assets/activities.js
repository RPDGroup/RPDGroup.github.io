(() => {
  'use strict';
  const page = document.getElementById('activities');
  if (!page) return;
  const photographs = [...page.querySelectorAll('[data-activity-record]')];
  const buttons = [...page.querySelectorAll('[data-activity-filter]')];
  const count = document.getElementById('activity-count');
  const empty = page.querySelector('.activity-empty');
  for (const button of buttons) button.addEventListener('click', () => {
    const category = button.dataset.activityFilter;
    let visible = 0;
    for (const photo of photographs) {
      photo.hidden = category !== 'all' && photo.dataset.activityCategory !== category;
      if (!photo.hidden) visible += 1;
    }
    for (const item of buttons) item.setAttribute('aria-pressed', String(item === button));
    count.textContent = `${visible} ${visible === 1 ? 'photograph' : 'photographs'}`;
    empty.hidden = visible > 0;
  });
  page.querySelector('.activity-filters').hidden = false;
})();
