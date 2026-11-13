const menu = document.querySelector('.menu-button');
menu?.addEventListener('click', () => {
  const opened = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(opened));
  menu.setAttribute('aria-label', opened ? 'Tutup navigasi' : 'Buka navigasi');
  document.body.classList.toggle('nav-open', opened);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && document.body.classList.contains('nav-open')) menu?.click();
});
document.querySelector('[aria-invalid="true"]')?.focus();
