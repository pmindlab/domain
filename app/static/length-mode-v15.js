let lengthMode=localStorage.getItem('mianem-length-mode')||'range';

function setLengthMode(next){
  lengthMode=next==='exact'?'exact':'range';
  localStorage.setItem('mianem-length-mode',lengthMode);
  $$('#lengthModeControl [data-length-mode]').forEach(b=>b.classList.toggle('active',b.dataset.lengthMode===lengthMode));
  $$('#lengthControl [data-length-panel]').forEach(p=>p.classList.toggle('hidden',p.dataset.lengthPanel!==lengthMode));
  const help=$('#lengthHelp');
  if(help)help.textContent=lengthMode==='exact'?'Szukaj nazw o jednej, dokładnie wskazanej długości.':'Szukaj nazw mieszczących się w wybranym przedziale.';
}

range=function(){
  if(lengthMode==='exact'){
    const n=clampLen($('#exactLen')?.value,6);
    return{min_len:n,max_len:n};
  }
  const min=clampLen($('#minLen')?.value,5),max=clampLen($('#maxLen')?.value,9);
  return{min_len:Math.min(min,max),max_len:Math.max(min,max)};
};

upgradeV15UI=function(){
  document.title='Mianem v1.5 — PMindLab';
  const ver=$('.app-id span');if(ver)ver.textContent='v1.5';
  const old=$('#lengthPreset');
  if(old){
    const block=old.closest('.setting-block');
    block.id='lengthControl';
    block.classList.add('length-control');
    block.innerHTML=`
      <div class="setting-label">DŁUGOŚĆ NAZWY</div>
      <div class="length-mode-selector" id="lengthModeControl" role="group" aria-label="Sposób określenia długości">
        <button type="button" data-length-mode="range">Zakres</button>
        <button type="button" data-length-mode="exact">Dokładnie</button>
      </div>
      <div class="length-panels">
        <div class="length-fields length-range" data-length-panel="range">
          <label><span>Min</span><input id="minLen" type="number" min="3" max="20" value="5"></label>
          <label><span>Max</span><input id="maxLen" type="number" min="3" max="20" value="9"></label>
        </div>
        <div class="length-fields length-exact hidden" data-length-panel="exact">
          <label><span>Dokładnie</span><input id="exactLen" type="number" min="3" max="20" value="6"></label>
        </div>
      </div>
      <p class="field-help" id="lengthHelp"></p>`;
    $('#lengthModeControl').onclick=e=>{const b=e.target.closest('[data-length-mode]');if(b)setLengthMode(b.dataset.lengthMode)};
    setLengthMode(lengthMode);
  }
  const explore=$('#exploreBtn');if(explore)explore.textContent='✦ Sprawdź inne obszary';
  const mf=$('.manual-form');
  if(mf&&!$('#manualWorkshopBtn')){
    mf.classList.add('manual-form-v15');
    const b=document.createElement('button');b.id='manualWorkshopBtn';b.type='button';b.className='secondary-action';b.textContent='Warsztat';
    b.onclick=()=>{const n=$('#manualName').value.trim();if(n)window.MianemWorkshop?.open(n,'manual')};
    mf.appendChild(b);
  }
};
