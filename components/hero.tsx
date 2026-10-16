import {Component, useLayoutEffect, useState, type ReactNode} from 'react';
import {createRoot} from 'react-dom/client';
import AccordionGallery, {type AccordionGalleryItem} from './AccordionGallery';

const host = document.getElementById('hero-gallery');
const fallback = document.getElementById('hero-gallery-fallback');
const items: AccordionGalleryItem[] = Array.from(fallback?.querySelectorAll('img') || []).map(image => ({
 image: image.getAttribute('src')!,
 srcSet: image.getAttribute('srcset') || undefined,
 sizes: image.getAttribute('sizes') || undefined,
 alt: image.alt,
 label: image.dataset.label
}));

class GalleryBoundary extends Component<{children: ReactNode}, {failed: boolean}> {
 state = {failed: false};
 static getDerivedStateFromError() { return {failed: true}; }
 componentDidCatch() { if (fallback) fallback.hidden = false; }
 render() { return this.state.failed ? null : this.props.children; }
}

function HeroGallery() {
 const [width, setWidth] = useState(host!.parentElement!.clientWidth);
 const [reduced, setReduced] = useState(matchMedia('(prefers-reduced-motion: reduce)').matches);
 const [touch, setTouch] = useState(matchMedia('(hover: none)').matches);
 useLayoutEffect(() => {
  fallback!.hidden = true;
  const resize = new ResizeObserver(([entry]) => setWidth(entry.contentRect.width));
  resize.observe(host!);
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const pointer = matchMedia('(hover: none)');
  const updateMotion = () => setReduced(motion.matches);
  const updatePointer = () => setTouch(pointer.matches);
  motion.addEventListener('change', updateMotion);
  pointer.addEventListener('change', updatePointer);
  host!.dataset.ready = 'true';
  return () => {
   resize.disconnect();
   motion.removeEventListener('change', updateMotion);
   pointer.removeEventListener('change', updatePointer);
  };
 }, []);
 const vertical = width < 560;
 return <AccordionGallery items={items} defaultIndex={2}
  className="sorriso-accordion" accentColor="#f2e8dc" overlayColor="#392316" textColor="#fbf7f2"
  orientation={vertical ? 'vertical' : 'horizontal'} height={vertical ? 350 : width < 850 ? 520 : 620}
  expandRatio={vertical ? 0.72 : 0.5} gap={vertical ? 10 : 14} radius={16}
  trigger={touch ? 'click' : 'hover'} grayscale={false}
  duration={reduced ? 0 : 0.65} tilt={reduced || vertical ? 0 : 4}
  parallax={reduced ? 0 : 0.25} stagger={reduced ? 0 : 0.06} />;
}

if (host && fallback && items.length) createRoot(host).render(<GalleryBoundary><HeroGallery /></GalleryBoundary>);
