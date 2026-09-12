(()=>{
  const $=(s,r=document)=>r.querySelector(s);
  const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  const api=async(url,opt={})=>{const r=await fetch(url,{headers:{'Content-Type':'application/json',...(opt.headers||{})},...opt});let d={};try{d=await r.json()}catch{}if(!r.ok)throw new Error(d.detail||`HTTP ${r.status}`);return d};

  if(!document.querySelector('link[href="/static/workshop.css"]')){
    const l=document.createElement('link');l.rel='stylesheet';l.href='/static/workshop.css';document.head.appendChild(l);
  }

  if(!$('#workshopDialog')){
    const wrap=document.createElement('div');
    wrap.innerHTML=`<dialog id="workshopDialog" class="workshop-dialog">
      <div class="workshop-shell">
        <div class="workshop-head">
          <div><div class="kicker">NAMING WORKSHOP</div><div class="workshop-title-row"><h2 id="workshopRoot">—</h2><span id="workshopContext" class="workshop-context"></span></div></div>
          <button class="icon-button" id="closeWorkshopBtn" type="button" aria-label="Zamknij">×</button>
        </div>
        <div id="workshopStatus" class="status hidden"></div>
        <div class="meaning-panel">
          <div class="meaning-card"><small>EN</small><p id="meaningEn">—</p></div>
          <div class="meaning-card"><small>PL</small><p id="meaningPl">—</p></div>
          <div class="meaning-meta"><div><small>TON</small><b id="meaningTone">—</b></div><div><small>MOTYW</small><b id="meaningVisual">—</b></div></div>
        </div>
        <div class="workshop-columns">
          <section><div class="workshop-column-head"><small>CO PASUJE PRZED</small><strong id="beforeLabel">—</strong></div><div id="beforeSuggestions" class="suggestion-list"></div></section>
          <section><div class="workshop-column-head"><small>CO PASUJE PO</small><strong id="afterLabel">—</strong></div><div id="afterSuggestions" class="suggestion-list"></div></section>
        </div>
        <div class="custom-pair">
          <label><span>Własny człon</span><input id="customPartner" placeholder="np. ember" autocomplete="off" /></label>
          <button id="customBeforeBtn" type="button">przed rdzeniem</button>
          <button id="customAfterBtn" type="button">po rdzeniu</button>
        </div>
        <section class="pair-preview" id="pairPreview">
          <div class="pair-preview-top"><div><small>WYBRANA KONSTRUKCJA</small><h3 id="pairName">Wybierz człon z lewej lub prawej.</h3></div><span id="pairScore" class="score hidden"></span></div>
          <div class="pair-meanings hidden" id="pairMeanings"><span id="pairMeaningEn"></span><span id="pairMeaningPl"></span></div>
          <div id="pairReasons" class="reason-row"></div>
          <div id="pairLive" class="pair-live hidden"></div>
        </section>
        <p class="workshop-note" id="workshopNote"></p>
      </div>
    </dialog>`;
    document.body.appendChild(wrap.firstElementChild);
  }

  let current={root:'',niche:'',data:null};
  const dialog=$('#workshopDialog');
  const status=(t,err=false)=>{const e=$('#workshopStatus');e.textContent=t||'';e.classList.toggle('hidden',!t);e.classList.toggle('error',err)};
  const pill=(text,kind)=>`<span class="pill ${kind}">${esc(text)}</span>`;

  function resetPreview(){
    $('#pairName').textContent='Wybierz człon z lewej lub prawej.';
    $('#pairScore').classList.add('hidden');
    $('#pairMeanings').classList.add('hidden');
    $('#pairReasons').innerHTML='';
    $('#pairLive').classList.add('hidden');
    $('#pairLive').innerHTML='';
  }

  function suggestionButton(term,position){
    const b=document.createElement('button');
    b.type='button';b.className='suggestion-item';
    const main=document.createElement('span');main.className='suggestion-main';
    const strong=document.createElement('b');strong.textContent=term.word;
    const small=document.createElement('small');small.textContent=term.pl||'';
    main.append(strong,small);
    const copy=document.createElement('span');copy.className='suggestion-copy';copy.textContent=term.en||'';
    const left=document.createElement('span');left.append(main,copy);
    const score=document.createElement('span');score.className='suggestion-score';score.textContent=Math.round(term.score||0);
    b.append(left,score);
    b.onclick=()=>selectPair(term.word,position,term);
    return b;
  }

  function render(data){
    current.data=data;
    const r=data.root||{};
    $('#workshopRoot').textContent=(r.word||current.root).toUpperCase();
    $('#workshopContext').textContent=current.niche||'własny rdzeń';
    $('#meaningEn').textContent=r.en||'—';
    $('#meaningPl').textContent=r.pl||'—';
    $('#meaningTone').textContent=r.tone||'—';
    $('#meaningVisual').textContent=r.visual||'—';
    $('#beforeLabel').textContent=r.word||current.root;
    $('#afterLabel').textContent=r.word||current.root;
    const before=$('#beforeSuggestions'),after=$('#afterSuggestions');before.innerHTML='';after.innerHTML='';
    (data.before||[]).forEach(x=>before.appendChild(suggestionButton(x,'before')));
    (data.after||[]).forEach(x=>after.appendChild(suggestionButton(x,'after')));
    if(!(data.before||[]).length) before.innerHTML='<div class="empty-state">Brak mocnych sugestii.</div>';
    if(!(data.after||[]).length) after.innerHTML='<div class="empty-state">Brak mocnych sugestii.</div>';
    $('#workshopNote').textContent=data.note||'';
    resetPreview();
  }

  async function selectPair(partner,position,term=null){
    partner=String(partner||'').trim().toLowerCase().replace(/[^a-z]/g,'');
    if(!partner)return;
    const root=current.root.toLowerCase().replace(/[^a-z]/g,'');
    const joined=position==='before'?partner+root:root+partner;
    $('#pairName').textContent=`${joined}.com`;
    $('#pairScore').classList.add('hidden');
    $('#pairMeanings').classList.toggle('hidden',!term);
    if(term){$('#pairMeaningEn').textContent=`EN · ${term.en||partner}`;$('#pairMeaningPl').textContent=`PL · ${term.pl||partner}`}
    $('#pairReasons').innerHTML='';
    const live=$('#pairLive');live.classList.remove('hidden');live.textContent='Sprawdzam semantykę, live .com i kolizje marki…';
    try{
      const d=await api('/api/workshop/check',{method:'POST',body:JSON.stringify({root:current.root,partner,position,niche:current.niche,brand_check:true})});
      $('#pairScore').textContent=Math.round(d.score||0);$('#pairScore').classList.remove('hidden');
      $('#pairReasons').innerHTML=(d.reasons||[]).map(x=>`<span class="reason">${esc(x)}</span>`).join('');
      if(!d.ok){live.innerHTML=`<div class="live-row">${pill('BLOCKED','bad')}<span>${esc((d.reasons||[]).join(' · '))}</span></div>`;return}
      const dk=d.domain_status==='available'?'ok':d.domain_status==='taken'?'bad':'warn';
      const bk=d.brand_status==='clear'?'ok':d.brand_status==='conflict'?'bad':'warn';
      live.innerHTML=`<div class="live-row"><span class="live-domain">${esc(d.domain)}</span>${pill(d.domain_status,dk)}${pill(`brand ${d.brand_status}`,bk)}</div>${(d.brand_notes||[]).length?`<div class="muted">${esc(d.brand_notes.join(' · '))}</div>`:''}`;
    }catch(e){live.innerHTML=`<div class="status error">${esc(e.message)}</div>`}
  }

  async function open(root,niche=''){
    root=String(root||'').trim();if(!root)return;
    current={root,niche,data:null};
    if(!dialog.open)dialog.showModal();
    status('Buduję semantyczne kierunki…');
    $('#workshopRoot').textContent=root.toUpperCase();$('#workshopContext').textContent=niche||'własny rdzeń';
    try{const d=await api('/api/workshop',{method:'POST',body:JSON.stringify({root,niche,limit:8})});render(d);status('')}catch(e){status(e.message,true)}
  }

  $('#closeWorkshopBtn').onclick=()=>dialog.close();
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
  $('#customBeforeBtn').onclick=()=>selectPair($('#customPartner').value,'before');
  $('#customAfterBtn').onclick=()=>selectPair($('#customPartner').value,'after');
  $('#customPartner').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();selectPair(e.target.value,'before')}});

  window.MianemWorkshop={open,selectPair};
})();