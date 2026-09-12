(()=>{
  const href='/static/workshop-v172.css';
  if(!document.querySelector(`link[href="${href}"]`)){
    const css=document.createElement('link');css.rel='stylesheet';css.href=href;document.head.appendChild(css);
  }

  const dialog=document.querySelector('#workshopDialog');
  const reasons=document.querySelector('#pairReasons');
  const preview=document.querySelector('.pair-preview');
  if(!dialog||!reasons||!preview||!window.MianemWorkshop?.selectPair)return;

  const FIXED_FAMILY_LABELS=[
    'Forma marki',
    'Relacja / przyimek',
    'Akcja / produkt',
    'Kontakt / komunikacja',
    'Przynależność',
    'Deskryptor po rdzeniu',
  ];

  let selected=null;
  let control=document.querySelector('#pairDirectionSwitch');
  if(!control){
    control=document.createElement('div');
    control.id='pairDirectionSwitch';
    control.className='pair-direction-switch hidden';
    const semantic=document.querySelector('#pairSemantic');
    preview.insertBefore(control,semantic||null);
  }

  const clean=value=>String(value||'').trim().toLowerCase().replace(/[^a-z]/g,'');
  const title=value=>String(value||'').replace(/\b\w/g,m=>m.toUpperCase());
  const root=()=>clean(document.querySelector('#workshopRoot')?.textContent||'');
  const phrase=position=>position==='before'?`${selected.partner} ${root()}`:`${root()} ${selected.partner}`;

  function hideControl(){
    control.classList.add('hidden');
    control.innerHTML='';
  }

  function familyIsFixed(){
    const text=reasons.textContent||'';
    return FIXED_FAMILY_LABELS.some(label=>text.includes(`rodzina konstrukcji: ${label}`));
  }

  function activate(position){
    if(!selected||position===selected.position)return;
    selected.position=position;
    renderControl();
    window.MianemWorkshop.selectPair(selected.partner,position);
  }

  function renderControl(){
    if(!selected||!root())return hideControl();
    const fixed=familyIsFixed();
    control.classList.remove('hidden');
    if(fixed){
      control.innerHTML=`<div class="pair-direction-label"><small>UKŁAD NAZWY</small><span>${title(phrase(selected.position))}</span></div><p>Ten typ konstrukcji ma ustalony naturalny szyk. Mianem nie tworzy automatycznie odwrotnej, nienaturalnej wersji.</p>`;
      return;
    }
    const before=title(phrase('before'));
    const after=title(phrase('after'));
    control.innerHTML=`<div class="pair-direction-label"><small>UKŁAD NAZWY</small><span>Wybierz szyk członu względem rdzenia</span></div><div class="pair-direction-options"><button type="button" data-pair-position="before" class="${selected.position==='before'?'active':''}">${before}</button><button type="button" data-pair-position="after" class="${selected.position==='after'?'active':''}">${after}</button></div><p>Każdy szyk jest oceniany osobno. Odwrotna wersja może dostać niższą rekomendację albo alert o abstrakcyjnym znaczeniu.</p>`;
    control.querySelectorAll('[data-pair-position]').forEach(button=>{
      button.addEventListener('click',()=>activate(button.dataset.pairPosition));
    });
  }

  function selectFromKey(key){
    const match=/^(before|after):([a-z]+)$/i.exec(String(key||''));
    if(!match)return;
    selected={position:match[1].toLowerCase(),partner:clean(match[2])};
    hideControl();
  }

  document.addEventListener('click',event=>{
    const keyed=event.target.closest('[data-key]');
    if(keyed){selectFromKey(keyed.dataset.key);return;}
    if(event.target.closest('#customBeforeBtn')){
      const partner=clean(document.querySelector('#customPartner')?.value);
      if(partner){selected={partner,position:'before'};hideControl()}
      return;
    }
    if(event.target.closest('#customAfterBtn')){
      const partner=clean(document.querySelector('#customPartner')?.value);
      if(partner){selected={partner,position:'after'};hideControl()}
    }
  },true);

  const observer=new MutationObserver(()=>{
    if(selected)renderControl();
  });
  observer.observe(reasons,{childList:true,subtree:true,characterData:true});

  dialog.addEventListener('close',()=>{selected=null;hideControl()});
})();
