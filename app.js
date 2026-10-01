'use strict';
// Native React Bits-inspired motion: no runtime dependencies or scroll hijacking.
const motionPreference = matchMedia('(prefers-reduced-motion: reduce)');
const runningMotion = new Set();
const elementMotion = new WeakMap();
function animateElement(element, frames, options = {}) {
 elementMotion.get(element)?.cancel();
 if (motionPreference.matches || !element.animate) return null;
 const animation = element.animate(frames, {
  duration: 600, easing: 'cubic-bezier(.22,1,.36,1)', ...options
 });
 elementMotion.set(element, animation);
 runningMotion.add(animation);
 const cleanup = () => {
  runningMotion.delete(animation);
  if (elementMotion.get(element) === animation) elementMotion.delete(element);
 };
 animation.finished.then(cleanup, cleanup);
 return animation;
}
motionPreference.addEventListener('change', () => {
 if (motionPreference.matches) [...runningMotion].forEach(animation => animation.cancel());
});
const navToggle=document.querySelector('.nav-toggle');
navToggle?.addEventListener('click',()=>{const on=navToggle.getAttribute('aria-expanded')!=='true';navToggle.setAttribute('aria-expanded',String(on));document.querySelector('#nav').classList.toggle('open',on)});
document.querySelectorAll('#nav a').forEach(a=>a.addEventListener('click',()=>{navToggle.setAttribute('aria-expanded','false');document.querySelector('#nav').classList.remove('open')}));
// Add the three supplied video files to videos/ and set their URLs here.
const videoSources=['','',''];
const slides=[...document.querySelectorAll('[data-slide]')],dots=[...document.querySelectorAll('[data-video]')];
if (slides.length) {
 let active = 0, paused = motionPreference.matches, timer;
 let hovered = false, focused = false, onScreen = true, dragStart = null;
 const frame = document.querySelector('.video-frame');
 const rotateButton = document.querySelector('.rotation');
 frame.classList.add('motion-carousel');
 frame.tabIndex = 0;
 function updateButton() {
  rotateButton.textContent = paused ? '▷' : 'Ⅱ';
  rotateButton.setAttribute('aria-label', paused ? 'Riprendi la rotazione' : 'Metti in pausa la rotazione');
 }
 function show(index) {
  const next = (index + slides.length) % slides.length;
  if (next === active) return;
  const outgoing = slides[active], incoming = slides[next];
  const direction = index > active ? 1 : -1;
  active = next;
  slides.forEach((slide, n) => {
   elementMotion.get(slide)?.cancel();
   slide.inert = n !== active;
   slide.setAttribute('aria-hidden', String(n !== active));
   if (n !== active) slide.querySelector('video').pause();
   if (slide !== outgoing && slide !== incoming) slide.hidden = true;
  });
  incoming.hidden = false;
  incoming.style.zIndex = '1';
  outgoing.style.zIndex = '0';
  const exit = animateElement(outgoing, [{opacity: 1}, {opacity: 0}], {duration: 420});
  const hideOutgoing = () => { if (slides[active] !== outgoing) outgoing.hidden = true; };
  if (exit) exit.finished.then(hideOutgoing, hideOutgoing); else hideOutgoing();
  animateElement(incoming, [
   {opacity: 0, transform: 'translateX(' + direction * 18 + 'px)'},
   {opacity: 1, transform: 'translateX(0)'}
  ], {duration: 460});
  dots.forEach((dot, n) => {
   dot.classList.toggle('selected', n === active);
   dot.setAttribute('aria-pressed', String(n === active));
  });
  document.querySelector('#video-count').textContent = '0' + (active + 1) + ' / 0' + slides.length;
 }
 function schedule() {
  clearInterval(timer);
  if (!paused && !hovered && !focused && onScreen && !document.hidden)
   timer = setInterval(() => show((active + 1) % slides.length), 6500);
 }
 function select(index) { show(index); paused = true; updateButton(); schedule(); }
 slides.forEach((slide, i) => {
  const video = slide.querySelector('video');
  slide.inert = i !== active;
  slide.setAttribute('aria-hidden', String(i !== active));
  slide.querySelectorAll('img').forEach(image => { image.draggable = false; });
  if (videoSources[i]) {
   document.querySelector('.video-area').classList.remove('awaiting-video');
   video.src = videoSources[i]; video.hidden = false;
   slide.querySelector('.video-placeholder').hidden = true;
   slide.classList.add('has-video');
   video.addEventListener('play', () => { paused = true; updateButton(); schedule(); });
   video.addEventListener('error', () => {
    video.hidden = true; slide.classList.remove('has-video');
    slide.querySelector('.video-placeholder').hidden = false;
   });
  }
 });
 dots.forEach((dot, i) => dot.addEventListener('click', () => select(i)));
 rotateButton.addEventListener('click', () => { paused = !paused; updateButton(); schedule(); });
 frame.addEventListener('mouseenter', () => { hovered = true; schedule(); });
 frame.addEventListener('mouseleave', () => { hovered = false; schedule(); });
 frame.addEventListener('focusin', () => { focused = true; schedule(); });
 frame.addEventListener('focusout', event => {
  if (!frame.contains(event.relatedTarget)) { focused = false; schedule(); }
 });
 frame.addEventListener('keydown', event => {
  if (event.target !== frame || !['ArrowLeft','ArrowRight'].includes(event.key)) return;
  event.preventDefault(); select(active + (event.key === 'ArrowRight' ? 1 : -1));
 });
 frame.addEventListener('pointerdown', event => {
  if (!event.isPrimary || event.button !== 0 || event.target.closest('button,a,video')) return;
  dragStart = {x: event.clientX, y: event.clientY};
 });
 frame.addEventListener('pointercancel', () => { dragStart = null; });
 frame.addEventListener('pointerup', event => {
  if (!dragStart) return;
  const dx = event.clientX - dragStart.x, dy = event.clientY - dragStart.y;
  dragStart = null;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) select(active + (dx < 0 ? 1 : -1));
 });
 if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
  onScreen = entries[0].isIntersecting; schedule();
 }).observe(frame);
 motionPreference.addEventListener('change', () => {
  if (motionPreference.matches) { paused = true; updateButton(); schedule(); }
 });
 document.addEventListener('visibilitychange', schedule);
 updateButton(); schedule();
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
if(search){
 const chips=[...document.querySelectorAll('[data-category-filter]')];
 const categoryList=document.querySelector('.category-list');
 const catalog=document.querySelector('#catalogo');
 const header=document.querySelector('.header');
 const normalize=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const fromURL=()=>{const value=new URLSearchParams(location.search).get('categoria');return chips.some(c=>c.dataset.categoryFilter===value)?value:'tutte'};
 let category=fromURL();
 function revealCategory(){
  const active=chips.find(c=>c.dataset.categoryFilter===category);
  if(active&&categoryList.scrollWidth>categoryList.clientWidth){
   const listRect=categoryList.getBoundingClientRect(),activeRect=active.getBoundingClientRect();
   categoryList.scrollTo({left:categoryList.scrollLeft+activeRect.left-listRect.left-(listRect.width-activeRect.width)/2,behavior:'instant'});
  }
 }
 function filter(animate = false){
  let count=0;
  const term=normalize(search.value.trim());
  document.querySelectorAll('.menu-category').forEach(section=>{
   let visible=0;
   section.querySelectorAll('.product').forEach(product=>{
    const match=(category==='tutte'||category===section.dataset.category)&&normalize(product.dataset.search).includes(term);
    product.hidden=!match;if(match)visible++;
   });
   section.hidden=!visible;count+=visible;
  });
  chips.forEach(c=>c.setAttribute('aria-pressed',String(c.dataset.categoryFilter===category)));
  document.querySelector('#result-count').textContent=`${count} ${count===1?'prodotto':'prodotti'} nel menù`;
  document.querySelector('#empty-menu').hidden=count!==0;
  if (animate) animateElement(document.querySelector('#menu-results'), [
   {opacity: .55, transform: 'translateY(6px)'}, {opacity: 1, transform: 'translateY(0)'}
  ], {duration: 230});
 }
 function updateOffset(){
  const height=Math.ceil(header.getBoundingClientRect().height);
  catalog.style.setProperty('--menu-nav-top',`${height}px`);
  catalog.style.scrollMarginTop=`${height+12}px`;
 }
 function scrollResults(){
  const resultsTop=document.querySelector('#menu-results').getBoundingClientRect().top+scrollY;
  window.scrollTo({top:resultsTop-catalog.offsetHeight-header.getBoundingClientRect().height-12,behavior:'instant'});
 }
 chips.forEach(chip=>chip.addEventListener('click',()=>{
  category=chip.dataset.categoryFilter;
  const url=new URL(location.href);
  if(category==='tutte')url.searchParams.delete('categoria');else url.searchParams.set('categoria',category);
  if(url.href!==location.href)history.pushState(null,'',url);
  filter(true);revealCategory();
  scrollResults();
 }));
 search.addEventListener('input',()=>{filter();scrollResults()});
 addEventListener('popstate',()=>{category=fromURL();filter(true);revealCategory()});
 addEventListener('resize',()=>{updateOffset();revealCategory()});
 if('ResizeObserver' in window)new ResizeObserver(updateOffset).observe(header);
 updateOffset();filter();requestAnimationFrame(revealCategory);
}

// Scroll Stack: dough cards driven by native document scroll.
(() => {
 const story = document.querySelector('#impasti');
 const cards = [...document.querySelectorAll('.dough')];
 const labels = [...document.querySelectorAll('[data-dough]')];
 const header = document.querySelector('.header');
 const progressBar = document.querySelector('.scroll-progress');
 let framePending = false, enabled = false, top = 0, travel = 1, cardHeight = 0;
 const clamp = (value, max = 1) => Math.max(0, Math.min(max, value));
 function update() {
  framePending = false;
  const max = document.documentElement.scrollHeight - innerHeight;
  if (progressBar) progressBar.style.width = (max > 0 ? scrollY / max * 100 : 0) + '%';
  if (!enabled) return;
  const step = clamp((top - story.getBoundingClientRect().top) / travel) * (cards.length - 1);
  const active = Math.min(cards.length - 1, Math.floor(step + .35));
  cards.forEach((card, i) => {
   const enter = i === 0 ? 1 : clamp(step - i + 1);
   const passed = clamp(step - i, cards.length - 1);
   const y = (1 - enter) * (cardHeight + 50) - passed * 18;
   card.style.transform = 'translateY(' + y.toFixed(2) + 'px) scale(' + (1 - passed * .035).toFixed(4) + ')';
   card.style.visibility = enter === 0 ? 'hidden' : 'visible';
   card.inert = i !== active;
   card.setAttribute('aria-hidden', String(i !== active));
   card.classList.toggle('is-active', i === active);
  });
  labels.forEach((button, i) => button.setAttribute('aria-pressed', String(i === active)));
 }
 function configure() {
  top = Math.ceil(header.getBoundingClientRect().height);
  const available = innerHeight - top;
  enabled = Boolean(story) && innerWidth >= 1000 && available >= 660 && !motionPreference.matches;
  if (story) {
   story.classList.toggle('dough-stack', enabled);
   story.style.setProperty('--stack-top', top + 'px');
   story.style.setProperty('--stack-view', available + 'px');
   travel = Math.round(innerHeight * 1.65);
   story.style.setProperty('--stack-travel', travel + 'px');
   cards.forEach((card, i) => {
    card.style.zIndex = String(i + 1);
    if (!enabled) {
     card.style.removeProperty('transform'); card.style.removeProperty('visibility');
     card.inert = false; card.removeAttribute('aria-hidden'); card.classList.remove('is-active');
    }
   });
   cardHeight = cards[0].offsetHeight;
  }
  update();
 }
 labels.forEach((button, i) => button.addEventListener('click', () => {
  if (!enabled) return;
  const start = story.getBoundingClientRect().top + scrollY - top;
  scrollTo({top: start + travel * i / (cards.length - 1), behavior: 'smooth'});
 }));
 addEventListener('scroll', () => {
  if (!framePending) { framePending = true; requestAnimationFrame(update); }
 }, {passive: true});
 addEventListener('resize', configure);
 motionPreference.addEventListener('change', configure);
 if ('ResizeObserver' in window) new ResizeObserver(configure).observe(header);
 document.fonts?.ready.then(configure);
 configure();
 const marquee=document.querySelector('.reviews-marquee');if(marquee){const row=marquee.querySelector('.reviews-row'),track=row.querySelector('.reviews-track');const originals=[...track.children];originals.forEach(c=>{const copy=c.cloneNode(true);copy.setAttribute('aria-hidden','true');copy.inert=true;track.append(copy)});const second=row.cloneNode(true);second.setAttribute('aria-hidden','true');second.inert=true;marquee.append(second);document.addEventListener('visibilitychange',()=>{marquee.classList.toggle('page-hidden',document.hidden)})}
})();

// Accessible social tabs with native horizontal scrolling; all panels remain visible without JS.
(()=>{
 const section=document.querySelector('.social-section');if(!section)return;
 const tabs=[...section.querySelectorAll('.social-tab')],panels=[...section.querySelectorAll('.social-panel')];
 section.classList.add('enhanced');section.querySelector('.social-tabs').setAttribute('role','tablist');
 function activate(index,focus=false,animate=false){panels.forEach((panel,i)=>{if(i!==index)panel.querySelectorAll('.social-player iframe').forEach(frame=>frame.contentWindow?.postMessage({type:'pause','x-tiktok-player':true},'https://www.tiktok.com'))});tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;panels[i].hidden=i!==index});if(focus)tabs[index].focus();if(animate)animateElement(panels[index],[{opacity:.35,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:320});requestAnimationFrame(updateControls)}
 tabs.forEach((tab,i)=>{tab.setAttribute('role','tab');tab.id='social-tab-'+i;tab.setAttribute('aria-controls',panels[i].id);panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',tab.id);tab.addEventListener('click',e=>{e.preventDefault();activate(i,false,true)});tab.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%tabs.length;if(e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;if(e.key==='Home')next=0;if(e.key==='End')next=tabs.length-1;if(next!==undefined){e.preventDefault();activate(next,true,true)}})});
 function updateControls(){panels.filter(p=>!p.hidden).forEach(panel=>{const track=panel.querySelector('.social-track'),controls=panel.querySelector('.social-carousel-controls');const max=track.scrollWidth-track.clientWidth;controls.hidden=max<2;controls.querySelector('[data-social-step="-1"]').disabled=track.scrollLeft<2;controls.querySelector('[data-social-step="1"]').disabled=track.scrollLeft>=max-2})}
 panels.forEach(panel=>{const track=panel.querySelector('.social-track');track.addEventListener('scroll',updateControls,{passive:true});panel.querySelectorAll('[data-social-step]').forEach(button=>button.addEventListener('click',()=>{const card=track.firstElementChild;const gap=parseFloat(getComputedStyle(track).columnGap)||0;const perView=innerWidth<=700?1:3;track.scrollBy({left:(card.getBoundingClientRect().width+gap)*perView*Number(button.dataset.socialStep),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'})}))});
 addEventListener('resize',updateControls);activate(0);
})();

// Split Text and Animated Content: semantic HTML remains readable without scripting.
(() => {
 if (motionPreference.matches || !('IntersectionObserver' in window)) return;
 const pending = new Map();
 const observer = new IntersectionObserver(entries => entries.forEach(entry => {
  if (!entry.isIntersecting) return;
  const reveal = pending.get(entry.target);
  observer.unobserve(entry.target); pending.delete(entry.target); reveal?.();
 }), {threshold: .08});
 const observe = (element, callback) => { pending.set(element, callback); observer.observe(element); };
 const title = document.querySelector('.hero-title-main');
 if (title) {
  const heading = title.closest('h1');
  heading.setAttribute('aria-label', [...heading.children].map(part => part.textContent.trim()).join(' '));
  const walker = document.createTreeWalker(title, NodeFilter.SHOW_TEXT);
  const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(node => {
   const fragment = document.createDocumentFragment();
   node.textContent.split(/(\s+)/).forEach(part => {
    if (!part.trim()) { fragment.append(document.createTextNode(part)); return; }
    const word = document.createElement('span');
    word.className = 'hero-word'; word.textContent = part; word.setAttribute('aria-hidden','true');
    fragment.append(word);
   });
   node.replaceWith(fragment);
  });
  observe(title, () => title.querySelectorAll('.hero-word').forEach((word, i) => {
   animateElement(word, [{opacity: 0, transform: 'translateY(22px)'}, {opacity: 1, transform: 'translateY(0)'}],
    {duration: 580, delay: i * 55, fill: 'backwards'});
  }));
 }
 const reveal = (elements, trigger = elements[0]) => {
  elements.forEach(element => element.classList.add('motion-pending'));
  observe(trigger, () => elements.forEach((element, i) => {
   element.classList.remove('motion-pending');
   animateElement(element, [{opacity: 0, transform: 'translateY(22px)'}, {opacity: 1, transform: 'translateY(0)'}],
    {duration: 620, delay: elements.length > 2 ? i * 60 : 0, fill: 'backwards'});
  }));
 };
 document.querySelectorAll('#pizzeria > *, #menu .menu-intro > *, #sedi > *, #recensioni .section-head, #differenza .section-head, #social .section-head')
  .forEach(element => reveal([element]));
 const teasers = [...document.querySelectorAll('.menu-teasers .teaser')];
 if (innerWidth > 700 && teasers.length) reveal(teasers, document.querySelector('.menu-teasers'));
 else teasers.forEach(element => reveal([element]));
 const before = [...document.querySelectorAll('.compare-before li')];
 const after = [...document.querySelectorAll('.compare-after li')];
 if (innerWidth > 700) before.forEach((element, i) => reveal([element, after[i]].filter(Boolean)));
 else [...before, ...after].forEach(element => reveal([element]));
 const finish = () => {
  observer.disconnect(); pending.clear();
  document.querySelectorAll('.motion-pending').forEach(element => element.classList.remove('motion-pending'));
 };
 motionPreference.addEventListener('change', () => { if (motionPreference.matches) finish(); });
 addEventListener('beforeprint', finish);
 matchMedia('(min-width:701px)').addEventListener('change', finish);
 // Keyboard users must never focus an invisible link or wait for a reveal.
 document.addEventListener('focusin', event => {
  const container = event.target.closest('.motion-pending');
  if (container) {
   const callback = pending.get(container);
   if (callback) { pending.delete(container); observer.unobserve(container); callback(); }
   container.classList.remove('motion-pending');
   elementMotion.get(container)?.cancel();
  }
 });
})();

// Tilted Card: photographs move slightly, titles and links stay still.
(() => {
 const pointer = matchMedia('(hover: hover) and (pointer: fine)');
 document.querySelectorAll('.menu-teasers .teaser').forEach(card => {
  const photo = card.querySelector('.food-photo');
  let frame = 0, bounds;
  const reset = () => {
   cancelAnimationFrame(frame); frame = 0; bounds = null;
   photo.style.removeProperty('transform');
  };
  card.addEventListener('pointerenter', () => { bounds = card.getBoundingClientRect(); });
  card.addEventListener('pointermove', event => {
   if (!pointer.matches || motionPreference.matches || event.pointerType === 'touch') return;
   cancelAnimationFrame(frame);
   frame = requestAnimationFrame(() => {
    bounds ||= card.getBoundingClientRect();
    const x = Math.max(-1, Math.min(1, (event.clientX - bounds.left) / bounds.width * 2 - 1));
    const y = Math.max(-1, Math.min(1, (event.clientY - bounds.top) / bounds.height * 2 - 1));
    photo.style.transform = 'perspective(900px) rotateX(' + -y * 3 + 'deg) rotateY(' + x * 3 + 'deg) scale(1.025)';
   });
  });
  card.addEventListener('pointerleave', reset); card.addEventListener('pointercancel', reset);
  motionPreference.addEventListener('change', reset); pointer.addEventListener('change', reset);
 });
})();
