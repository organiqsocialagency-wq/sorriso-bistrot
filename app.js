'use strict';
const navToggle=document.querySelector('.nav-toggle');
navToggle?.addEventListener('click',()=>{const on=navToggle.getAttribute('aria-expanded')!=='true';navToggle.setAttribute('aria-expanded',String(on));document.querySelector('#nav').classList.toggle('open',on)});
document.querySelectorAll('#nav a').forEach(a=>a.addEventListener('click',()=>{navToggle.setAttribute('aria-expanded','false');document.querySelector('#nav').classList.remove('open')}));
// Add the three supplied video files to videos/ and set their URLs here.
const videoSources=['','',''];
const slides=[...document.querySelectorAll('[data-slide]')],dots=[...document.querySelectorAll('[data-video]')];
if(slides.length){
 let active=0,paused=matchMedia('(prefers-reduced-motion: reduce)').matches,timer,hovered=false,focused=false;
 const rotateButton=document.querySelector('.rotation');
 function updateButton(){rotateButton.textContent=paused?'▷':'Ⅱ';rotateButton.setAttribute('aria-label',paused?'Riprendi la rotazione':'Metti in pausa la rotazione')}
 function show(i){active=i;slides.forEach((s,n)=>{s.hidden=n!==i;if(n!==i)s.querySelector('video').pause()});dots.forEach((d,n)=>{d.classList.toggle('selected',n===i);d.setAttribute('aria-pressed',String(n===i))});document.querySelector('#video-count').textContent=`0${i+1} / 03`}
 function schedule(){clearInterval(timer);if(!paused&&!hovered&&!focused&&!document.hidden)timer=setInterval(()=>show((active+1)%3),6500)}
 slides.forEach((s,i)=>{const v=s.querySelector('video');if(videoSources[i]){document.querySelector('.video-area').classList.remove('awaiting-video');v.src=videoSources[i];v.hidden=false;s.querySelector('.video-placeholder').hidden=true;s.classList.add('has-video');v.addEventListener('play',()=>{paused=true;updateButton();schedule()});v.addEventListener('error',()=>{v.hidden=true;s.classList.remove('has-video');s.querySelector('.video-placeholder').hidden=false})}});
 dots.forEach((d,i)=>d.addEventListener('click',()=>{show(i);paused=true;updateButton();schedule()}));
 rotateButton.addEventListener('click',()=>{paused=!paused;updateButton();schedule()});
 const frame=document.querySelector('.video-frame');frame.addEventListener('mouseenter',()=>{hovered=true;schedule()});frame.addEventListener('mouseleave',()=>{hovered=false;schedule()});frame.addEventListener('focusin',()=>{focused=true;schedule()});frame.addEventListener('focusout',e=>{if(!frame.contains(e.relatedTarget)){focused=false;schedule()}});document.addEventListener('visibilitychange',schedule);updateButton();schedule();
}
const form=document.querySelector('#booking-form');
if(form){
 const date=form.elements.data,time=form.elements.ora,message=document.querySelector('#form-message'),send=document.querySelector('#send-request');
 const today=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Rome',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());date.min=today();
 function reset(){send.hidden=true;send.removeAttribute('href');message.textContent=''}
 function service(value){form.querySelector('[type="submit"]').textContent=value==='asporto'?'Prepara ordine da asporto ↗':'Prepara richiesta tavolo ↗';document.querySelector('#booking-title').textContent=value==='asporto'?'Richiedi un ordine da asporto':'Richiedi un tavolo';document.querySelector('#booking-intro').textContent=value==='asporto'?'Indica prodotti, quantità, impasti e orario di ritiro. Invia il messaggio su WhatsApp e attendi la nostra conferma.':'Compila il modulo e invia il messaggio su WhatsApp. Ti risponderemo per confermare la disponibilità.';form.elements.servizio.value=value;document.querySelectorAll('[data-service]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.service===value)));document.querySelector('#people-field').hidden=value==='asporto';form.elements.persone.disabled=value==='asporto';form.elements.note.required=value==='asporto';document.querySelector('#note-label').textContent=value==='asporto'?'Il tuo ordine: prodotti, quantità e impasti':'Allergie, esigenze alimentari o altre richieste (facoltativo)';form.elements.note.placeholder=value==='asporto'?'Es. 2 Margherite senza glutine e 2 supplì':'Indica eventuali allergie o altre esigenze';reset()}
 document.querySelectorAll('[data-service]').forEach(b=>b.addEventListener('click',()=>service(b.dataset.service)));
 document.querySelectorAll('[data-asporto]').forEach(a=>a.addEventListener('click',()=>service('asporto')));
 document.querySelectorAll('a[href="#prenota"]:not([data-asporto])').forEach(a=>a.addEventListener('click',()=>service('tavolo')));
 if(new URLSearchParams(location.search).get('servizio')==='asporto')service('asporto');
 function validateDate(){date.min=today();date.setCustomValidity('');time.setCustomValidity('');if(date.value&&new Date(date.value+'T12:00:00').getDay()===1)date.setCustomValidity('Il lunedì siamo chiusi. Scegli un altro giorno.');if(date.value===today()&&time.value){const now=new Intl.DateTimeFormat('it-IT',{timeZone:'Europe/Rome',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).format(new Date());if(time.value<=now)time.setCustomValidity('Scegli un orario futuro.')}}
 form.addEventListener('input',()=>{reset();validateDate()});form.addEventListener('change',()=>{reset();validateDate()});
 form.addEventListener('submit',e=>{e.preventDefault();validateDate();if(!form.reportValidity())return;const f=new FormData(form),isTake=f.get('servizio')==='asporto';const when=new Date(f.get('data')+'T12:00:00').toLocaleDateString('it-IT',{weekday:'long',day:'numeric',month:'long',year:'numeric'});let text=`Ciao Sorriso Bistrot! Vorrei richiedere ${isTake?'un ordine da asporto':'un tavolo'} a Via Sarnano.\nNome: ${f.get('nome').trim()}\nTelefono: ${f.get('telefono')}\nData: ${when}\nOrario: ${f.get('ora')}`;if(!isTake)text+=`\nPersone: ${f.get('persone')}`;if(f.get('note').trim())text+=`\n${isTake?'Ordine':'Note'}: ${f.get('note').trim()}`;text+='\nAttendo una vostra conferma. Grazie!';send.href='https://wa.me/393455834226?text='+encodeURIComponent(text);send.hidden=false;message.textContent=`Richiesta pronta: ${isTake?'asporto':'tavolo'}, ${when} alle ${f.get('ora')}. Apri WhatsApp per inviarla al locale. La richiesta è confermata solo dopo la risposta dello staff.`;send.focus()});
}
const search=document.querySelector('#search-menu');
if(search){const category=document.querySelector('#category'),price=document.querySelector('#price-mode');const selected=new URLSearchParams(location.search).get('categoria');if([...category.options].some(o=>o.value===selected))category.value=selected;
 const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 function filter(){let count=0;document.querySelectorAll('.menu-category').forEach(section=>{let visible=0;section.querySelectorAll('.product').forEach(product=>{const match=(category.value==='tutte'||category.value===section.dataset.category)&&normalize(product.dataset.search).includes(normalize(search.value.trim()));product.hidden=!match;if(match)visible++});section.hidden=!visible;count+=visible});document.querySelector('#result-count').textContent=`${count} prodotti nel menù`;document.querySelector('#empty-menu').hidden=count!==0;document.querySelectorAll('.product-price b').forEach(b=>{b.textContent=b.dataset[price.value];const label=b.nextElementSibling;if(b.dataset.gf!==b.dataset.classica)label.textContent=price.value==='gf'?'senza glutine':'classica · con glutine'})}
 search.addEventListener('input',filter);category.addEventListener('change',filter);price.addEventListener('change',filter);filter();
}

// Reference experience: native smooth anchors, scroll progress and three-step story.
(()=>{
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const story=document.querySelector('#impasti'),cards=[...document.querySelectorAll('.dough')],labels=[...document.querySelectorAll('[data-dough]')];
 const desktop=matchMedia('(min-width:901px)');let framePending=false;
 function activeStory(i){cards.forEach((c,n)=>{c.classList.toggle('is-active',i===n);c.inert=story.classList.contains('scroll-story')&&n!==i});labels.forEach((b,n)=>b.setAttribute('aria-pressed',String(i===n)))}
 function update(){framePending=false;const max=document.documentElement.scrollHeight-innerHeight;document.querySelector('.scroll-progress').style.width=(max>0?scrollY/max*100:0)+'%';if(story?.classList.contains('scroll-story')){const r=story.getBoundingClientRect(),distance=story.offsetHeight-innerHeight+84,progress=Math.max(0,Math.min(.999,(84-r.top)/distance));activeStory(Math.floor(progress*3))}}
 function configure(){if(story){story.classList.toggle('scroll-story',desktop.matches&&!reduced.matches);activeStory(0)}update()}
 labels.forEach((b,i)=>b.addEventListener('click',()=>{const start=story.getBoundingClientRect().top+scrollY-84,distance=story.offsetHeight-innerHeight+84;scrollTo({top:start+distance*(i+.15)/3,behavior:reduced.matches?'instant':'smooth'})}));
 addEventListener('scroll',()=>{if(!framePending){framePending=true;requestAnimationFrame(update)}},{passive:true});addEventListener('resize',configure);desktop.addEventListener('change',configure);reduced.addEventListener('change',configure);configure();
 // Keep content readable if scripting or motion preferences change.
 if(!reduced.matches&&'IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('pending');observer.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('#pizzeria,#menu,.comparison,#sedi').forEach(el=>{el.classList.add('reveal-section','pending');observer.observe(el)})}
 const marquee=document.querySelector('.reviews-marquee');if(marquee){const row=marquee.querySelector('.reviews-row'),track=row.querySelector('.reviews-track');const originals=[...track.children];originals.forEach(c=>{const copy=c.cloneNode(true);copy.setAttribute('aria-hidden','true');copy.inert=true;track.append(copy)});const second=row.cloneNode(true);second.setAttribute('aria-hidden','true');second.inert=true;marquee.append(second);document.addEventListener('visibilitychange',()=>{marquee.classList.toggle('page-hidden',document.hidden)})}
})();

// Accessible social tabs with native horizontal scrolling; all panels remain visible without JS.
(()=>{
 const section=document.querySelector('.social-section');if(!section)return;
 const tabs=[...section.querySelectorAll('.social-tab')],panels=[...section.querySelectorAll('.social-panel')];
 section.classList.add('enhanced');section.querySelector('.social-tabs').setAttribute('role','tablist');
 function activate(index,focus=false){panels.forEach((panel,i)=>{if(i!==index)panel.querySelectorAll('.social-player iframe').forEach(frame=>frame.contentWindow?.postMessage({type:'pause','x-tiktok-player':true},'https://www.tiktok.com'))});tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;panels[i].hidden=i!==index});if(focus)tabs[index].focus();requestAnimationFrame(updateControls)}
 tabs.forEach((tab,i)=>{tab.setAttribute('role','tab');tab.id='social-tab-'+i;tab.setAttribute('aria-controls',panels[i].id);panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',tab.id);tab.addEventListener('click',e=>{e.preventDefault();activate(i)});tab.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%tabs.length;if(e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;if(e.key==='Home')next=0;if(e.key==='End')next=tabs.length-1;if(next!==undefined){e.preventDefault();activate(next,true)}})});
 function updateControls(){panels.filter(p=>!p.hidden).forEach(panel=>{const track=panel.querySelector('.social-track'),controls=panel.querySelector('.social-carousel-controls');const max=track.scrollWidth-track.clientWidth;controls.hidden=max<2;controls.querySelector('[data-social-step="-1"]').disabled=track.scrollLeft<2;controls.querySelector('[data-social-step="1"]').disabled=track.scrollLeft>=max-2})}
 panels.forEach(panel=>{const track=panel.querySelector('.social-track');track.addEventListener('scroll',updateControls,{passive:true});panel.querySelectorAll('[data-social-step]').forEach(button=>button.addEventListener('click',()=>{const card=track.firstElementChild;const gap=parseFloat(getComputedStyle(track).columnGap)||0;const perView=innerWidth<=700?1:3;track.scrollBy({left:(card.getBoundingClientRect().width+gap)*perView*Number(button.dataset.socialStep),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})}))});
 addEventListener('resize',updateControls);activate(0);
})();
