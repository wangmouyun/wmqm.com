/* 字段与请求协议遵循所附官网 assets/inquiry.js。 */
(() => {
  'use strict';
  const form = document.querySelector('#inquiry');
  if (!form) return;
  const config = window.WMQM_CONFIG || {};
  const status = form.querySelector('.form-status');
  const button = form.querySelector('[type="submit"]');
  const label = form.querySelector('[data-submit-label]');
  const subject = form.elements.namedItem('subject');
  const message = form.elements.namedItem('message');
  const count = form.querySelector('[data-char-count]');
  const requested = new URLSearchParams(location.search).get('subject') || '';
  const value = name => (form.elements.namedItem(name)?.value || '').trim();
  const show = (text, error = false) => { status.textContent = text; status.dataset.state = error ? 'error' : 'success'; status.hidden = false; };
  if ([...subject.options].some(option => option.value === requested)) subject.value = requested;
  message.addEventListener('input', () => { if (count) count.textContent = String(message.value.length); });
  button.disabled = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (button.disabled) return;
    status.hidden = true;
    if (!form.reportValidity()) return;
    if (!value('name')) { show('请填写联系人。', true); form.elements.namedItem('name').focus(); return; }
    const digits = value('phone').replace(/\D/g, '');
    if (digits.length < 7 || digits.length > 20) { show('请填写有效的联系电话。', true); form.elements.namedItem('phone').focus(); return; }
    if (value('message').length < 10) { show('请补充需求说明，至少填写10个字。', true); message.focus(); return; }
    if (value('contact_guard_field')) { show('提交未完成，请刷新页面后重试。', true); return; }
    if (!['http:', 'https:'].includes(location.protocol)) { show('请通过网站提交需求，或直接拨打159-0083-3031联系王先生。', true); return; }
    button.disabled = true; label.textContent = '正在提交…';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), config.inquiryTimeoutMs || 18000);
    try {
      const payload = new FormData();
      ['subject','name','phone','email','company','message'].forEach(key => payload.append(key, value(key)));
      payload.append('site_name', config.siteName || '网谋汽贸');
      payload.append('source_url', location.origin + location.pathname);
      payload.append('ua', (navigator.userAgent || '').slice(0, 500));
      // Browser supplies Origin/Referer and multipart boundary. No token/type/manual Content-Type.
      const response = await fetch(config.inquiryEndpoint || form.action, { method:'POST', body:payload, mode:'cors', credentials:'omit', signal:controller.signal, redirect:'follow' });
      const raw = await response.text();
      let data = null;
      try { data = raw ? JSON.parse(raw) : null; } catch (_) { /* Unknown responses remain unconfirmed. */ }
      const rejected = !response.ok || data?.success === false || data?.ok === false || ['error','fail','failed'].includes(data?.status) || Number(data?.code) >= 400;
      if (rejected) throw new Error('rejected');
      const confirmed = data && (data.success === true || data.ok === true || ['success','ok'].includes(data.status) || [0,200,'0','200'].includes(data.code));
      if (!confirmed) { show('请求已发出，暂时无法确认是否收到。请先电话联系业务人员核实，避免重复提交。', true); return; }
      form.reset(); if (count) count.textContent = '0';
      try { sessionStorage.setItem('wmqm-inquiry-received', '1'); } catch (_) { /* Browser storage may be disabled. */ }
      location.assign('thanks.html');
    } catch (error) {
      if (error?.name === 'AbortError') show('请求超时，暂时无法确认是否收到。请先通过电话核实，避免重复提交。', true);
      else show('提交未完成，请联系王先生159-0083-3031或吴先生175-2108-3572。您填写的内容已保留。', true);
    } finally { clearTimeout(timeout); button.disabled = false; label.textContent = '提交业务需求'; }
  });
})();
