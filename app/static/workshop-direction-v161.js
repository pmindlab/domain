(()=>{
  const $=(s,r=document)=>r.querySelector(s);
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const title=s=>s ? s.charAt(0).toUpperCase()+s.slice(1) : '';

  function bothDirectionsVisible(){
    const before=$('#beforeSection'),after=$('#afterSection');
    return !!before&&!!after&&!before.classList.contains('hidden')&&!after.classList.contains('hidden');
  }

  function ensureChooser(){
    let chooser=$('#pairDirectionChoices');
    if(chooser)return chooser;
    chooser=document.createElement('div');
    chooser.id='pairDirectionChoices';
    chooser.className='pair-direction-choices hidden';
    const semantic=$('#pairSemantic');
    if(semantic)semantic.insertAdjacentElement('afterend',chooser);
    return chooser;
  }

  function clearPreviewForChoice(){
    const score=$('#pairScore'),semantic=$('#pairSemantic'),reasons=$('#pairReasons'),live=$('#pairLive');
    if(score)score.classList.add('hidden');
    if(semantic){semantic.classList.add('hidden');semantic.innerHTML=''}
    if(reasons)reasons.innerHTML='';
    if(live){live.classList.add('hidden');live.innerHTML=''}
  }

  function showDirectionChoice(partner,recommendedPosition){
    const root=String($('#workshopRoot')?.textContent||'').trim().toLowerCase().replace(/[^a-z]/g,'');
    partner=String(partner||'').trim().toLowerCase().replace(/[^a-z]/g,'');
    if(!root||!partner||!window.MianemWorkshop?.selectPair)return;
    clearPreviewForChoice();
    const chooser=ensureChooser();
    const beforeName=`${title(partner)} ${title(root)}`;
    const afterName=`${title(root)} ${title(partner)}`;
    const pairName=$('#pairName');
    if(pairName)pairName.textContent=`${title(partner)} + ${title(root)} — wybierz kolejność`;
    chooser.innerHTML=`
      <div class="direction-choice-copy">
        <b>Najpierw wybierz kolejność</b>
        <span>Te same dwa słowa mogą znaczyć i brzmieć inaczej zależnie od pozycji.</span>
      </div>
      <div class="direction-choice-actions">
        <button type="button" data-workshop-direction="before">
          <strong>${esc(beforeName)}</strong>
          <span>${esc(partner+root)}.com</span>
          ${recommendedPosition==='before'?'<em>polecane</em>':''}
        </button>
        <button type="button" data-workshop-direction="after">
          <strong>${esc(afterName)}</strong>
          <span>${esc(root+partner)}.com</span>
          ${recommendedPosition==='after'?'<em>polecane</em>':''}
        </button>
      </div>`;
    chooser.classList.remove('hidden');
    chooser.querySelectorAll('[data-workshop-direction]').forEach(btn=>{
      btn.addEventListener('click',()=>{
        chooser.classList.add('hidden');
        window.MianemWorkshop.selectPair(partner,btn.dataset.workshopDirection);
      });
    });
    chooser.scrollIntoView({block:'nearest',behavior:'smooth'});
  }

  document.addEventListener('click',event=>{
    const card=event.target.closest('#workshopDialog .best-item');
    if(!card||!bothDirectionsVisible())return;
    const key=card.dataset.key||'';
    const split=key.indexOf(':');
    if(split<1)return;
    const position=key.slice(0,split);
    const partner=key.slice(split+1);
    if(!['before','after'].includes(position)||!partner)return;
    event.preventDefault();
    event.stopImmediatePropagation();
    showDirectionChoice(partner,position);
  },true);
})();
