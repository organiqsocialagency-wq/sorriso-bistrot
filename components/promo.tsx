import {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {flushSync} from 'react-dom';
import StarBorder from './StarBorder';

function PromoBooking() {
 const [reduced, setReduced] = useState(matchMedia('(prefers-reduced-motion: reduce)').matches);
 useEffect(() => {
  const query = matchMedia('(prefers-reduced-motion: reduce)');
  const change = () => setReduced(query.matches);
  query.addEventListener('change', change);
  return () => query.removeEventListener('change', change);
 }, []);
 if (reduced) return <a className="button full" href="tel:+393455834226">Prenota ora ↗</a>;
 return <StarBorder as="a" href="tel:+393455834226" className="button full"
  color="#fbf7f2" trailColor="#d9b78e" duration={4} direction="clockwise"
  stars={1} trailLength={0.3} thickness={1.5} radius={8} glow={0.75}
  hover="lap" sparkle={false} clickPulse theme="dark"
  backgroundColor="#6b3e26" textColor="#fbf7f2" borderColor="#a8613a">
  Prenota ora ↗
 </StarBorder>;
}

export function mountPromoStar(host: HTMLElement) {
 if (host.dataset.starReady) return;
 const focused = host.contains(document.activeElement);
 flushSync(() => createRoot(host).render(<PromoBooking/>));
 host.dataset.starReady = 'true';
 if (focused) host.querySelector('a')?.focus({preventScroll:true});
}
