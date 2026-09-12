(()=>{
  document.documentElement.dataset.pmindlabUiVersion='1';

  const ui=document.createElement('link');
  ui.rel='stylesheet';
  ui.href='/static/pmindlab-ui-v1.css';
  document.head.appendChild(ui);

  const syncBrandLogo=()=>{
    const logo=document.querySelector('.brand-logo');
    if(!logo)return;
    logo.src=document.documentElement.dataset.theme==='dark'?'/static/logo-dark.svg':'/static/logo.svg';
  };
  syncBrandLogo();
  new MutationObserver(syncBrandLogo).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});

  const css=document.createElement('link');
  css.rel='stylesheet';
  css.href='/static/length-mode-v15.css';
  document.head.appendChild(css);

  const load=src=>new Promise((resolve,reject)=>{
    const s=document.createElement('script');
    s.src=src;
    s.onload=resolve;
    s.onerror=()=>reject(new Error(`Nie udało się wczytać ${src}`));
    document.head.appendChild(s);
  });

  load('/static/workshop-v15.js')
    .then(()=>load('/static/core-v15a.js'))
    .then(()=>load('/static/length-mode-v15.js'))
    .then(()=>load('/static/core-v15b1.js'))
    .then(()=>load('/static/core-v15b2.js'))
    .then(()=>load('/static/core-v15b3.js'))
    .catch(err=>{
      console.error(err);
      document.body.insertAdjacentHTML('afterbegin',`<div style="padding:12px;background:#fee;color:#900">Mianem v1.5: ${String(err.message||err)}</div>`);
    });
})();
