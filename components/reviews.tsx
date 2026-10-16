import {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import DriftWall from './DriftWall';

const host = document.getElementById('reviews-wall');
const fallback = document.getElementById('reviews-readable');
const toggle = document.getElementById('reviews-view');
const items = Array.from(fallback?.querySelectorAll('article') || []).map((card, i) => ({
 image: `img/reviews/review-${i + 1}.svg`,
 title: `${card.querySelector('blockquote')?.textContent} — ${card.querySelector('.review-author b')?.textContent}`,
 href: card.querySelector('a')!.href
}));
function Reviews() {
 const [width, setWidth] = useState(host!.clientWidth);
 const [reduced, setReduced] = useState(matchMedia('(prefers-reduced-motion: reduce)').matches);
 const [reading, setReading] = useState(false);
 const [visible, setVisible] = useState(false);
 useEffect(() => {
  const resize = new ResizeObserver(([entry]) => setWidth(entry.contentRect.width));
  resize.observe(host!);
  const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting), {rootMargin:'150px'});
  observer.observe(host!);
  const mq = matchMedia('(prefers-reduced-motion: reduce)');
  const change = () => setReduced(mq.matches);
  const click = () => setReading(value => !value);
  mq.addEventListener('change', change); toggle!.addEventListener('click', click);
  toggle!.hidden = false;
  return () => {resize.disconnect(); observer.disconnect(); mq.removeEventListener('change',change); toggle!.removeEventListener('click',click);};
 }, []);
 useEffect(() => {
  const staticView = reading || reduced;
  fallback!.hidden = !staticView;
  host!.classList.toggle('is-static',staticView);
  toggle!.hidden = reduced;
  toggle!.textContent = reading ? 'Torna alle recensioni animate' : 'Leggi tutte le recensioni';
  toggle!.setAttribute('aria-expanded',String(staticView));
 }, [reading,reduced]);
 if (reading || reduced || !visible) return null;
 return <DriftWall items={items} columns={width < 650 ? 1 : width < 1000 ? 2 : 3}
  tileWidth={width < 650 ? Math.min(330,width-32) : 340} tileHeight={240}
  gap={22} radius={16} tilt={12} turn={-10} roll={0} perspective={1200}
  depth={70} speed={22} direction="up" variance={0.35} parallax={0.35}
  pauseOnHover={true} lift={35} fade={0.12} dim={1} overlayColor="transparent" />;
}
if (host && fallback && items.length) createRoot(host).render(<Reviews/>);
