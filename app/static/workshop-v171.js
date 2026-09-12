(()=>{
  const href='/static/workshop-v171.css';
  if(!document.querySelector(`link[href="${href}"]`)){
    const css=document.createElement('link');css.rel='stylesheet';css.href=href;document.head.appendChild(css);
  }
  const dialog=document.querySelector('#workshopDialog');
  if(!dialog)return;
  const sync=()=>document.documentElement.classList.toggle('workshop-modal-open',dialog.open);
  const observer=new MutationObserver(sync);
  observer.observe(dialog,{attributes:true,attributeFilter:['open']});
  dialog.addEventListener('close',sync);
  dialog.addEventListener('cancel',()=>queueMicrotask(sync));
  sync();
})();
