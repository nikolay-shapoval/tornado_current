(() => {
  const menuButton = document.querySelector('.menu-button');
  const navigation = document.querySelector('.navigation');
  const catalogDropdown = document.querySelector('.catalog-dropdown');
  menuButton?.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(expanded));
    navigation.classList.toggle('is-open', expanded);
  });
  document.addEventListener('click', event => {
    if (!catalogDropdown?.contains(event.target)) {
      catalogDropdown?.removeAttribute('open');
    }
    if (!navigation?.contains(event.target) && !menuButton?.contains(event.target)) {
      navigation?.classList.remove('is-open');
      menuButton?.setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      navigation?.classList.remove('is-open');
      menuButton?.setAttribute('aria-expanded', 'false');
      catalogDropdown?.removeAttribute('open');
    }
  });
  const input = document.querySelector('#catalog-search');
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.catalog-grid .category-card')];
  let activeFilter = 'Все';
  const normalize = text => text.toLocaleLowerCase('ru').replaceAll('ё', 'е');
  function filterCatalog() {
    const query = normalize(input?.value || '').trim();
    let shown = 0;
    for (const card of cards) {
      const matches = (activeFilter === 'Все' || card.dataset.group === activeFilter) && normalize(card.dataset.search || '').includes(query);
      card.hidden = !matches;
      if (matches) shown++;
    }
    const count = document.querySelector('#catalog-count');
    if (count) count.textContent = `Разделов: ${shown}`;
    const empty = document.querySelector('.empty-search');
    if (empty) empty.hidden = shown !== 0;
  }
  input?.addEventListener('input', filterCatalog);
  filterButtons.forEach(button => button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach(item => {
      const selected = item === button;
      item.classList.toggle('selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    filterCatalog();
  }));
  const dialog = document.querySelector('#image-dialog');
  document.querySelectorAll('[data-image]').forEach(button => button.addEventListener('click', () => {
    const img = dialog.querySelector('img');
    img.src = button.dataset.image;
    img.alt = button.dataset.caption;
    dialog.querySelector('p').textContent = button.dataset.caption;
    dialog.showModal();
  }));
  dialog?.querySelector('.dialog-close')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  document.querySelector('[data-copy]')?.addEventListener('click', async event => {
    const button = event.currentTarget;
    const status = document.querySelector('.copy-status');
    try {
      if (!navigator.clipboard) throw new Error('clipboard unavailable');
      await navigator.clipboard.writeText(button.dataset.copy);
      status.textContent = 'Номер скопирован.';
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = button.dataset.copy;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.append(textarea);
      textarea.select();
      const copied = document.execCommand('copy');
      textarea.remove();
      status.textContent = copied ? 'Номер скопирован.' : `Номер телефона: ${button.dataset.copy}`;
    }
  });
})();
