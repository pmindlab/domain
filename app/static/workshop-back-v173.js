(()=>{
  const dialog=document.querySelector('#workshopDialog');
  const head=dialog?.querySelector('.workshop-head');
  if(!dialog||!head)return;

  const href='/static/workshop-back-v173.css';
  if(!document.querySelector(`link[href="${href}"]`)){
    const css=document.createElement('link');
    css.rel='stylesheet';
    css.href=href;
    document.head.appendChild(css);
  }

  let returnState=null;
  let button=document.querySelector('#workshopBackResults');
  if(!button){
    button=document.createElement('button');
    button.id='workshopBackResults';
    button.type='button';
    button.className='workshop-back-results hidden';
    button.textContent='← Wróć do wyników';
    const titleBlock=head.firstElementChild;
    titleBlock?.insertBefore(button,titleBlock.firstChild);
  }

  function showBack(){button.classList.toggle('hidden',!returnState)}

  document.addEventListener('click',event=>{
    const opener=event.target.closest('.workshop-open');
    if(!opener)return;
    const card=opener.closest('.candidate-card');
    returnState={
      scrollY:window.scrollY,
      cardName:card?.querySelector('.candidate-name')?.textContent?.trim()||'',
    };
    showBack();
  },true);

  button.addEventListener('click',()=>{
    const state=returnState;
    returnState=null;
    showBack();
    dialog.close();
    requestAnimationFrame(()=>{
      window.scrollTo({top:state?.scrollY||0,left:0,behavior:'auto'});
    });
  });

  dialog.addEventListener('close',()=>{
    returnState=null;
    showBack();
  });
})();
