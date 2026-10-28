(() => {
  'use strict';
  const directory = document.querySelector('.people-directory');
  if (!directory) return;
  const records = [...directory.querySelectorAll('[data-member-record]')];
  const filters = [...directory.querySelectorAll('[data-member-filter]')];
  const search = document.getElementById('member-search');
  const reset = document.getElementById('member-reset');
  const count = document.getElementById('member-count');
  const empty = document.getElementById('members-empty');
  const sections = [...directory.querySelectorAll('[data-member-section]')];
  const index = records.map(record => ({ record, text: record.textContent.toLocaleLowerCase() }));
  let category = 'all';

  function filterMembers() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const item of index) {
      const match = (category === 'all' || item.record.dataset.memberGroup === category)
        && terms.every(term => item.text.includes(term));
      item.record.hidden = !match;
      if (match) visible += 1;
    }
    for (const section of sections) {
      const total = [...section.querySelectorAll('[data-member-record]')].filter(record => !record.hidden).length;
      section.hidden = total === 0;
      section.querySelector('[data-member-section-count]').textContent = `${total} ${total === 1 ? 'member' : 'members'}`;
    }
    for (const button of filters) button.setAttribute('aria-pressed', String(button.dataset.memberFilter === category));
    count.textContent = records.length ? `${visible} ${visible === 1 ? 'profile' : 'profiles'}` : '';
    reset.hidden = category === 'all' && !terms.length;
    empty.hidden = visible > 0;
  }

  for (const button of filters) button.addEventListener('click', () => {
    category = button.dataset.memberFilter;
    filterMembers();
  });
  search.addEventListener('input', filterMembers);
  reset.addEventListener('click', () => {
    category = 'all';
    search.value = '';
    filterMembers();
    search.focus();
  });

  const viewer = document.getElementById('member-viewer');
  if (viewer && typeof viewer.showModal === 'function') {
    const title = document.getElementById('member-profile-title');
    const localName = viewer.querySelector('.member-viewer-local');
    const role = viewer.querySelector('.member-viewer-role');
    const portrait = viewer.querySelector('.member-viewer-portrait');
    const details = viewer.querySelector('.member-viewer-details');
    let trigger;
    for (const record of records) {
      const summary = record.querySelector('summary');
      summary.addEventListener('click', event => {
        // Modified clicks retain the browser's native disclosure behavior.
        if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        trigger = summary;
        title.textContent = record.querySelector('.member-name').textContent;
        localName.textContent = record.querySelector('.member-local')?.textContent || '';
        localName.hidden = !localName.textContent;
        role.textContent = record.querySelector('.member-role')?.textContent || '';
        role.hidden = !role.textContent;
        portrait.replaceChildren(record.querySelector('.member-portrait').cloneNode(true));
        details.replaceChildren(record.querySelector('.member-details').cloneNode(true));
        document.body.classList.add('has-member-viewer');
        viewer.showModal();
        viewer.scrollTop = 0;
      });
    }
    viewer.querySelector('.member-viewer-close').addEventListener('click', () => viewer.close());
    viewer.addEventListener('click', event => {
      if (event.target !== viewer) return;
      const rect = viewer.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) viewer.close();
    });
    viewer.addEventListener('close', () => {
      document.body.classList.remove('has-member-viewer');
      portrait.replaceChildren();
      details.replaceChildren();
      trigger?.focus({ preventScroll: true });
    });
  }

  directory.querySelector('.people-controls').hidden = false;
  directory.querySelector('.member-result-bar').hidden = false;
  filterMembers();
})();
