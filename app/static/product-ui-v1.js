(()=>{
  window.PMINDLAB_PRODUCT_UI_VERSION=1;
  const logo=document.querySelector('.brand-logo');
  if(!logo)return;
  const lightSrc='/static/logo.svg';
  let darkSrc='';
  let darkPromise=null;

  async function buildDarkLogo(){
    if(darkSrc)return darkSrc;
    if(!darkPromise){
      darkPromise=fetch(lightSrc,{cache:'no-store'})
        .then(r=>{if(!r.ok)throw new Error(`logo ${r.status}`);return r.text()})
        .then(svg=>{
          const dark=svg
            .replaceAll('rgb(59,114,181)','#6A9DD8')
            .replaceAll('rgb(22,50,92)','#C3D9F0')
            .replaceAll('#3B72B5','#6A9DD8')
            .replaceAll('#16325C','#C3D9F0');
          darkSrc=`data:image/svg+xml;charset=utf-8,${encodeURIComponent(dark)}`;
          return darkSrc;
        });
    }
    return darkPromise;
  }

  async function syncLogo(){
    const dark=document.documentElement.dataset.theme==='dark';
    if(!dark){logo.src=lightSrc;return}
    try{logo.src=await buildDarkLogo()}catch(err){console.error('PMindLab dark logo:',err);logo.src=lightSrc}
  }

  new MutationObserver(muts=>{
    if(muts.some(m=>m.attributeName==='data-theme'))syncLogo();
  }).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
  syncLogo();
})();
