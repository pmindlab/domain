(()=>{
  window.PMINDLAB_PRODUCT_UI_VERSION=1;
  const light=document.querySelector('.brand-logo');
  if(light&&!document.querySelector('.brand-logo-dark')){
    light.classList.add('brand-logo-light');
    const dark=light.cloneNode(false);
    dark.src='/static/logo-dark.svg';
    dark.classList.remove('brand-logo-light');
    dark.classList.add('brand-logo-dark');
    dark.alt='';
    dark.setAttribute('aria-hidden','true');
    light.insertAdjacentElement('afterend',dark);
  }
})();
