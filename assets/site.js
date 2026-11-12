(() => {
  'use strict';
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) => [...parent.querySelectorAll(selector)];

  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
  const menu = $('.menu-button');
  const nav = $('.nav');
  const closeMenu = () => {
    if (!menu || !nav) return;
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', '打开导航');
  };
  menu?.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? '关闭导航' : '打开导航');
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menu.focus();
    }
  });
  window.matchMedia('(min-width:901px)').addEventListener('change', closeMenu);

  const tabs = $$('[data-choice]');
  function activateTab(tab) {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      const panel = document.getElementById(item.getAttribute('aria-controls'));
      if (panel) panel.hidden = !selected;
    });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activateTab(tab));
    tab.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = tabs[(index + 1) % tabs.length];
      if (event.key === 'ArrowLeft') target = tabs[(index - 1 + tabs.length) % tabs.length];
      if (event.key === 'Home') target = tabs[0];
      if (event.key === 'End') target = tabs[tabs.length - 1];
      if (target) { event.preventDefault(); activateTab(target); target.focus(); }
    });
  });

  const search = $('#faq-search');
  if (search) {
    const filters = $$('[data-filter]');
    const items = $$('.faq-results .faq-item');
    let category = '全部问题';
    const update = () => {
      const words = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      items.forEach(item => {
        const matchCategory = category === '全部问题' || item.dataset.category === category;
        const text = item.textContent.toLocaleLowerCase();
        const visible = matchCategory && words.every(word => text.includes(word));
        item.hidden = !visible;
        if (visible) count++;
      });
      const countLabel = $('[data-faq-count]');
      if (countLabel) countLabel.textContent = count;
      $('.empty-state').hidden = count > 0;
    };
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.filter;
      filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      update();
    }));
    search.addEventListener('input', update);
  }

  const qr = $('.qr-dialog');
  $$('[data-open-qr]').forEach(button => button.addEventListener('click', () => {
    if (qr?.showModal) qr.showModal();
    else window.open('https://wmqm.wmou.com/assets/wechat.jpg', '_blank', 'noopener');
  }));
  $('.dialog-close', qr || document)?.addEventListener('click', () => qr.close());
  qr?.addEventListener('click', event => {
    const rect = qr.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) qr.close();
  });

  const thanksTitle = $('[data-thanks-title]');
  if (thanksTitle) {
    try {
      if (sessionStorage.getItem('wmqm-inquiry-received') === '1') {
        thanksTitle.textContent = '您的业务需求已收到';
        $('[data-thanks-message]').textContent = '业务人员将根据您填写的信息进一步联系。如需及时核对规格、租期或交付安排，也可直接电话沟通。';
        sessionStorage.removeItem('wmqm-inquiry-received');
      }
    } catch (_) { /* Keep the neutral thank-you message. */ }
  }
})();
