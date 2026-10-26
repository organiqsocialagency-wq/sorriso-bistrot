from pathlib import Path
import json,re,html,hashlib
from seo import structured_data, item_id
P=Path(__file__).parent
SITE_URL='https://sorrisobistrot.it'
def public_url(page='index.html'):
    return SITE_URL + ('/' if page == 'index.html' else '/' + page)
esc=html.escape
CSS_VERSION=hashlib.sha256((P/'styles.css').read_bytes()).hexdigest()[:12]
JS_VERSION=hashlib.sha256((P/'app.js').read_bytes()).hexdigest()[:12]
PROMO_STAR_VERSION=hashlib.sha256((P/'assets/promo.js').read_bytes()).hexdigest()[:12]
PROMO_STAR_CSS_VERSION=hashlib.sha256((P/'assets/promo.css').read_bytes()).hexdigest()[:12]
HERO_VERSION=hashlib.sha256((P/'assets/hero.js').read_bytes()).hexdigest()[:12]
HERO_CSS_VERSION=hashlib.sha256((P/'assets/hero.css').read_bytes()).hexdigest()[:12]
def hero_head(page):
    if page != 'index.html': return ''
    return f'<link rel="stylesheet" href="assets/hero.css?v={HERO_CSS_VERSION}"><script type="module" src="assets/hero.js?v={HERO_VERSION}"></script>'
data=json.loads((P/'menu.json').read_text())
data=[s for s in data if s['id'] != 'stagione']
(P/'menu.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
icons={
'leaf':'<path d="M5 21C4 9 11 3 21 3c0 10-5 17-16 18ZM5 21 17 7M10 14l-1-5m4 2 5 1"/>',
'pizza':'<path d="m4 5 8 17L22 5C16 0 9 1 4 5ZM5 8c5-3 10-3 15 0"/><circle cx="11" cy="11" r="1"/><circle cx="15" cy="14" r="1"/>',
'photo':'<rect x="3" y="5" width="18" height="15" rx="2"/><circle cx="8" cy="10" r="1.5"/><path d="m3 17 6-4 4 3 4-6 4 7"/>',
'pin':'<path d="M19 10c0 5-7 12-7 12S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2"/>',
'play':'<path d="m9 5 11 7-11 7Z"/>',
'bag':'<path d="M5 7h14l1 14H4L5 7Zm4 0V5a3 3 0 0 1 6 0v2"/>',
'check':'<path d="m5 12 4 4L19 6"/>',
'grain':'<path d="M12 22V3m0 7C5 10 4 5 5 3c5 0 7 3 7 7Zm0 6c7 0 8-5 7-7-5 0-7 3-7 7Zm0 4c-7 0-8-5-7-7 5 0 7 3 7 7Z"/>',
'pumpkin':'<path d="M12 6c-8-5-13 14-4 15 2 1 6 1 8 0 9-1 4-20-4-15Zm0 0c-5 0-5 15 0 15s5-15 0-15Zm0 0c-1-3 0-4 2-5"/>',
'arrow':'<path d="M4 12h16m-6-6 6 6-6 6"/>'}
def ico(n):return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+icons[n]+'</svg>'
# Every product has a category-qualified key; duplicate names never share images by accident.
image_assets=json.loads((P/'image-assets.json').read_text())
real_media=json.loads((P/'real-media.json').read_text())
image_assets.update(real_media)
image_aliases={
    'La pizzeria · Via Sarnano':'home/stesura',
    'Impasto: l’originale di sorriso':'home/dough-originale',
    'Impasto: semi di zucca':'home/dough-zucca',
    'Impasto: canapa':'home/dough-canapa',
    'Pizze':'pizze/Margherita',
    'Fritti':'home/fritti',
    'Dolci':'dolci/Cheesecake',
}
def image_tag(key, sizes='(max-width:600px) calc(100vw - 40px), (max-width:900px) 44vw, 380px', eager=False, decorative=False):
    asset=image_assets[key]
    variants=asset['variants']
    source=variants[-1]
    for variant in variants:
        if not (P/variant['src']).is_file():
            raise FileNotFoundError(variant['src'])
    srcset=', '.join(f"{v['src']} {v['width']}w" for v in variants)
    alt='' if decorative else asset['name']+(' — immagine illustrativa' if asset.get('illustrative',True) else '')
    priority=' fetchpriority="high"' if eager else ''
    return f'<img src="{esc(source["src"])}" srcset="{esc(srcset)}" sizes="{esc(sizes)}" width="{source["width"]}" height="{source["height"]}" alt="{esc(alt)}" loading="{"eager" if eager else "lazy"}" decoding="async"{priority}>'
def ph(label,kind='photo',cls='',key=None):
    key=key or image_aliases[label]
    sizes='(max-width:600px) calc(100vw - 40px), 560px' if key.startswith('home/') else '(max-width:600px) calc(100vw - 40px), (max-width:900px) 44vw, 380px'
    caption='<figcaption>Immagine illustrativa</figcaption>' if image_assets[key].get('illustrative',True) and (key.startswith('home/') or label in ('Dolci','Pizze')) else ''
    return f'<figure class="placeholder food-photo {cls}">{image_tag(key,sizes=sizes)}{caption}</figure>'
def head(title,desc,page='index.html'):return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#6B3E26"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:site_name" content="Sorriso Bistrot"><meta property="og:locale" content="it_IT"><meta property="og:image" content="{SITE_URL}/{image_assets["home/cottura"]["variants"][-1]["src"]}"><meta property="og:image:alt" content="Pizza appena sfornata da Sorriso Bistrot"><meta name="twitter:card" content="summary_large_image"><link rel="canonical" href="{public_url(page)}"><meta property="og:url" content="{public_url(page)}"><link rel="icon" type="image/png" sizes="96x96" href="img/favicon-96.png">{structured_data(page,title,desc,SITE_URL,real_media,json.loads((P/"social-videos.json").read_text()),data)}<link rel="stylesheet" href="assets/promo.css?v={PROMO_STAR_CSS_VERSION}">{hero_head(page)}<link rel="stylesheet" href="styles.css?v={CSS_VERSION}"><script src="app.js?v={JS_VERSION}" defer></script></head><body><div class="scroll-progress" aria-hidden="true"></div><a class="skip" href="#contenuto">Vai al contenuto</a>'''
def nav():return '''<header class="header"><a class="brand" href="./" aria-label="Sorriso Bistrot, homepage"><img src="img/logo-sorriso-web.webp" alt="" width="56" height="56"><span>Sorriso Bistrot<small>PIZZERIA · GLUTEN FREE · ROMA</small></span></a><button class="promo-trigger promo-mobile" type="button" data-open-promo aria-haspopup="dialog" aria-controls="promo-dialog">Promo in corso <span class="promo-badge" aria-label="1 promozione">1</span></button><button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu ☰</button><nav id="nav" aria-label="Principale"><a href="./#pizzeria">La pizzeria</a><a href="./#impasti">Gli impasti</a><button class="promo-trigger" type="button" data-open-promo aria-haspopup="dialog" aria-controls="promo-dialog">Promo in corso <span class="promo-badge" aria-label="1 promozione">1</span></button><a href="menu.html">Il menù</a><a href="./#sedi">Dove siamo</a><a href="./#recensioni">Recensioni</a><a href="#ordina">Ordina</a><a class="button small" href="./#prenota">Prenota un tavolo ↗</a></nav></header>''' + (P/'components/promotions.html').read_text().replace('{{PROMO_STAR_MODULE}}',f'./assets/promo.js?v={PROMO_STAR_VERSION}')
def ordering():return (P/'components/ordering.html').read_text()
def footer():return '''<footer><div class="wrap footer-grid"><a class="brand" href="./"><img src="img/logo-sorriso-avorio-web.webp" alt="Logo Sorriso" width="64" height="64"><span>Sorriso Bistrot<small>PIZZERIA · ROMA SAN BASILIO</small></span></a><p>Pizzeria con proposte senza glutine a Roma San Basilio.<br>Via Sarnano 4 · Tavoli e asporto.<br>Consegna tramite Deliveroo, Just Eat e Glovo.</p><div><a href="tel:+393455834226">345 583 4226</a><br><a href="menu.html">Consulta il menù</a></div></div><p class="wrap image-disclosure">Le foto e i video del locale sono reali. Le immagini contrassegnate come illustrative sono generate con IA: aspetto, porzioni e presentazione possono differire dai prodotti serviti.</p><div class="wrap foot-bottom"><span>© Sorriso Bistrot · Roma</span></div></footer><div class="mobile-actions"><a href="./#prenota">Prenota un tavolo</a><a href="./?servizio=asporto#prenota">Ordina d’asporto</a></div></body></html>'''
maps='https://www.google.com/maps/search/?api=1&query=Sorriso+Bistrot+Via+Sarnano+4+Roma'
REVIEWS_VERSION=hashlib.sha256((P/'assets/reviews.js').read_bytes()).hexdigest()[:12]
REVIEWS_CSS_VERSION=hashlib.sha256((P/'assets/reviews.css').read_bytes()).hexdigest()[:12]
review_source='https://restaurantguru.com/Junior-Pizza-Chef-Gluten-Free-Roma-Rome-2'
s=head('Pizzeria senza glutine a Roma San Basilio | Sorriso Bistrot','Sorriso Bistrot, Via Sarnano 4 a Roma San Basilio. Pizza senza glutine, impasti senza lattosio e laboratorio separato. Menù, prenotazioni e asporto.')+nav()
s+=f'<link rel="stylesheet" href="assets/reviews.css?v={REVIEWS_CSS_VERSION}"><script type="module" src="assets/reviews.js?v={REVIEWS_VERSION}"></script>'
s+='''<main id="contenuto"><section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="dot"></span> SORRISO BISTROT · ROMA, SAN BASILIO</p><h1><span class="hero-title-main">La tua pizzeria <em>SENZA GLUTINE E SENZA LATTOSIO</em></span><span class="hero-title-top">a Roma, a San Basilio</span></h1><p class="lead">Il menù comprende pizze, antipasti, fritti, calzoni, bruschette, primi e dolci senza glutine e senza lattosio!</p><div class="dough-assurance"><p><strong>I nostri impasti senza glutine</strong></p><ul aria-label="Caratteristiche degli impasti senza glutine"><li>Senza glutine</li><li>Senza frumento deglutinato</li><li>Senza lattosio</li><li>Senza proteine del latte</li></ul><p class="dough-assurance-note">Le indicazioni riguardano gli impasti, non i condimenti o gli altri prodotti.</p></div><div class="actions"><a class="button" href="#prenota">Prenota un tavolo ↗</a><a class="button outline" href="menu.html">Visualizza Menù ↗</a></div><div class="hero-notes"><span>Via Sarnano 4, Roma</span><span>Asporto</span><span>Consegna a domicilio</span></div></div>'''
s+='<div class="hero-gallery-shell"><div id="hero-gallery"></div><div id="hero-gallery-fallback" class="hero-gallery-fallback" aria-label="Preparazione delle pizze di Sorriso Bistrot">'
hero_photos=[
    ('preparazione','La preparazione','Mani del pizzaiolo che aggiungono il condimento a una pizza tonda con zucca'),
    ('condimento','Il condimento','Un filo d’olio sulla pizza tonda con zucca e formaggio'),
    ('finitura','La finitura','Il pizzaiolo grattugia il formaggio su una pizza tonda appena preparata'),
]
for i,(name,label,alt) in enumerate(hero_photos):
    variants=', '.join(f'img/hero/{name}-tonda-v1-{w}.webp {w}w' for w in (480,768,1024))
    for w in (480,768,1024):
        if not (P/f'img/hero/{name}-tonda-v1-{w}.webp').is_file(): raise FileNotFoundError(name)
    priority='high' if i==2 else 'auto'
    s+=f'<figure class="hero-fallback-panel"><img src="img/hero/{name}-tonda-v1-1024.webp" srcset="{variants}" sizes="(max-width:655px) calc(100vw - 40px), (max-width:1176px) 60vw, 640px" width="1024" height="1536" loading="eager" decoding="async" fetchpriority="{priority}" alt="{esc(alt)}" data-label="{esc(label)}"><figcaption>{label}</figcaption></figure>'
s+='</div></div></section>'
s+=f'''<section id="pizzeria" class="wrap section split"><figure class="placeholder restaurant-video"><video data-loop-video id="restaurant-video" autoplay muted loop playsinline preload="none" data-src="{esc(real_media["home/sala"]["video"])}" poster="{esc(real_media["home/sala"]["variants"][-1]["src"])}" width="720" height="1280" aria-label="La sala di Sorriso Bistrot in Via Sarnano"></video><button class="restaurant-video-toggle" type="button" aria-controls="restaurant-video" hidden>Metti in pausa</button><noscript><a class="restaurant-video-link" href="{esc(real_media["home/sala"]["video"])}">Guarda il video della sala ↗</a></noscript></figure><div><p class="eyebrow">BENVENUTI DA SORRISO</p><h2>Sorriso Bistrot,<br>in <em>Via Sarnano</em></h2><p>Sorriso Bistrot è una pizzeria in Via Sarnano 4, nel quartiere San Basilio a Roma. Proponiamo pizza classica napoletana, forno a legna e pizze con impasto senza glutine, da mangiare al tavolo o da ordinare per l’asporto e la consegna a domicilio.</p><p>Gli impasti senza glutine vengono preparati nel nostro laboratorio separato. Il menù comprende anche fritti e dolci senza glutine: consulta le proposte e segnala eventuali allergie quando prenoti o ordini.</p><a class="text-link" href="menu.html">Consulta il menù {ico('arrow')}</a></div></section>'''
s+='''<section id="impasti" class="section tinted"><div class="wrap dough-pin"><div class="section-head"><p class="eyebrow">GLI IMPASTI SENZA GLUTINE</p><h2>L’originale di Sorriso,<br> semi di zucca e <em>canapa</em></h2><p>Senza glutine, senza frumento deglutinato, senza lattosio e senza proteine del latte. Le indicazioni si riferiscono agli impasti; verifica gli allergeni dei condimenti nel menù.</p></div><div class="three-grid doughs">'''
for num,name,kind,desc in [('01','L’originale di Sorriso','grain','L’inconfondibile senza glutine di Sorriso, premiato e irreplicabile.'),('02','Semi di zucca','pumpkin','Preparato con semi di zucca tostati, per un gusto tostato e aromatico. I semi apportano proteine vegetali, grassi insaturi, magnesio e zinco.'),('03','Canapa','leaf','Preparato con semi di canapa biologici di produzione italiana. Un impasto di nostra produzione, da abbinare alla pizza che preferisci.')]:
    key = image_aliases["Impasto: "+name.lower()]
    asset = image_assets[key]
    if asset.get('video'):
        video_id = {'01':'originale-video','02':'zucca-video','03':'canapa-video'}[num]
        poster = asset['variants'][-1]
        visual = f'<figure class="placeholder dough-video"><video data-loop-video id="{video_id}" autoplay muted loop playsinline preload="none" data-src="{esc(asset["video"])}" poster="{esc(poster["src"])}" width="{poster["width"]}" height="{poster["height"]}" aria-label="{esc(asset["name"])}"></video><button class="restaurant-video-toggle" type="button" aria-controls="{video_id}" hidden>Metti in pausa</button><noscript><a class="restaurant-video-link" href="{esc(asset["video"])}">Guarda il video dell’impasto ↗</a></noscript></figure>'
    else:
        visual = ph("Impasto: "+name.lower(),kind)
    s+=f'<article class="dough"><div class="dough-picture">{visual}<span class="number">{num}</span></div><div class="dough-copy"><p class="eyebrow">IMPASTO SENZA GLUTINE</p><h3>{name}</h3><p>{desc}</p><p class="dough-diet">Senza frumento deglutinato, senza lattosio e senza proteine del latte.</p><a href="menu.html" class="text-link">Consulta le pizze ↗</a></div></article>'
s+='''</div><div class="dough-progress" aria-label="Scegli impasto"><button type="button" data-dough="0" aria-pressed="true">01 · L’originale di Sorriso</button><button type="button" data-dough="1" aria-pressed="false">02 · Semi di zucca</button><button type="button" data-dough="2" aria-pressed="false">03 · Canapa</button></div><p class="fine center">Le proprietà dei semi non equivalgono ai valori nutrizionali della pizza finita. Indica l’impasto che preferisci quando ordini.</p></div></section>'''
s+='''<section class="section wrap" id="menu"><div class="menu-intro"><div><p class="eyebrow">IL NOSTRO MENÙ</p><h2>Menù e <em>prezzi</em></h2></div><div><p>Consulta pizze, fritti e dolci, con ingredienti, allergeni indicati e prezzi. Tutte le pizze sono disponibili anche senza glutine.</p><a class="button" href="menu.html">Visualizza menù ↗</a></div></div><div class="three-grid menu-teasers">'''
for name,sub,cat in [('Pizze','Ingredienti e prezzi','pizze'),('Fritti','Consulta le proposte','antipasti'),('Dolci','Le proposte senza glutine','dolci')]:s+=f'<a class="teaser" href="menu.html?categoria={cat}#catalogo">{ph(name,"pizza" if cat=="pizze" else "photo")}<div><h3>{name}</h3><span>↗</span><p>{sub}</p></div></a>'
s+='</div></section>'
s+=f'''<section class="section reviews" id="recensioni"><div class="wrap"><div class="section-head"><p class="eyebrow">Le vostre recensioni</p><h2>Chi viene per la pizza,<br>torna con <em>il sorriso</em></h2><p>Estratti di recensioni Google riportati da Restaurant Guru.</p></div><div id="reviews-wall" aria-label="Recensioni di Sorriso Bistrot"></div><div class="center"><button id="reviews-view" class="text-link" type="button" aria-controls="reviews-readable" aria-expanded="true" hidden>Leggi tutte le recensioni</button></div><div id="reviews-readable" class="reviews-readable">'''
# 23 quoted words total from the secondary source.
for name,quote in [('Marcello Passerini','Veramente la migliore pizzeria di Roma e dintorni'),('Silvia La Torre','Personale e proprietario gentilissimi.'),('Carlo Giuseppe Bertinetto','Best gluten free pizza I have had.')]:
    rating=5 if name in ('Marcello Passerini','Silvia La Torre') else None
    stars=f'<div class="review-stars" role="img" aria-label="Valutazione: {rating} su 5 stelle"><span aria-hidden="true">'+('★'*rating)+'</span></div>' if rating else ''
    s+=f'<article class="review">{stars}<span class="quote-mark">“</span><blockquote>{quote}</blockquote><div class="review-author"><span class="avatar">{name[0]}</span><div><b>{name}</b><small>Recensione Google · estratto</small></div></div><a href="{review_source}" target="_blank" rel="noopener">Leggi su Restaurant Guru ↗</a></article>'
s+=f'''</div><p class="fine center">Estratti consultati il 18 settembre 2026.</p><div class="center"><a class="text-link" href="{maps}" target="_blank" rel="noopener">Trova Sorriso su Google Maps ↗</a></div></div></section>'''
s+='''<section class="section wrap compare-section" id="differenza"><div class="section-head"><p class="eyebrow">IL LABORATORIO E IL MENÙ</p><h2>Come prepariamo<br>il nostro <em>senza glutine</em></h2><p>Dalla preparazione degli impasti alla scelta sul menù: ecco cosa trovi da Sorriso.</p></div><div class="comparison comparison-cards"><article class="compare-before"><span class="compare-tag">Quello che cerchi</span><ul class="compare-list">'''
for point in ['Sapere dove viene preparato l’impasto senza glutine','Scegliere un impasto di produzione propria','Un impasto senza frumento deglutinato','Un impasto senza lattosio','Un impasto senza proteine del latte','Poter scegliere l’impasto','Ordinare anche oltre la pizza']:
    s+=f'<li><span class="compare-need" aria-hidden="true">→</span><strong>{point}</strong></li>'
s+='''</ul></article><article class="compare-after"><div class="compare-card-top"><span class="compare-tag">Da Sorriso</span><img src="img/logo-sorriso-web.webp" alt="Sorriso Bistrot" width="64" height="64" loading="lazy"></div><ul class="compare-list">'''
for point in ['Laboratorio gluten free separato','Impasto di nostra produzione','Senza frumento deglutinato','Impasti senza lattosio','Impasti senza proteine del latte','L’originale di Sorriso, semi di zucca e canapa','Fritti e dolci senza glutine']:
    s+=f'<li>{ico("check")}<strong>{point}</strong></li>'
s+='''</ul><a class="text-link" href="menu.html">Visualizza Menù ↗</a></article></div><p class="fine center">Queste indicazioni riguardano gli impasti senza glutine. Condimenti e altri prodotti possono contenere allergeni: consulta il menù e segnala le tue esigenze allo staff. Proponiamo anche pizze con glutine.</p></section>'''
s+=ordering()
s+='''<section id="prenota" class="section booking"><div class="wrap split"><div><p class="eyebrow">PRENOTAZIONI E ASPORTO</p><h2 id="booking-title">Richiedi <em>un tavolo</em></h2><p id="booking-intro">Compila il modulo e invia il messaggio su WhatsApp. Ti risponderemo per confermare la disponibilità.</p><p>La richiesta è confermata solo dopo la risposta dello staff.</p><a class="text-link" href="tel:+393455834226">Preferisci chiamare? 345 583 4226 ↗</a></div><form id="booking-form" class="booking-form"><div class="service-tabs" aria-label="Tipo di prenotazione"><button type="button" data-service="tavolo" aria-pressed="true">Tavolo</button><button type="button" data-service="asporto" aria-pressed="false">Asporto</button></div><input type="hidden" name="servizio" value="tavolo"><div class="form-grid"><label>Il tuo nome<input name="nome" autocomplete="name" required maxlength="80" placeholder="Come ti chiami?"></label><label>Telefono<input name="telefono" type="tel" autocomplete="tel" required pattern="[+0-9 ()-]{7,20}" placeholder="Il tuo numero"></label><label>Data<input name="data" type="date" required></label><label>Orario<select name="ora" required><option value="">Scegli l’orario</option><option>18:00</option><option>18:30</option><option>19:00</option><option>19:30</option><option>20:00</option><option>20:30</option><option>21:00</option><option>21:30</option><option>22:00</option><option>22:30</option></select></label><label id="people-field">Persone<select name="persone"><option>2 persone</option><option>1 persona</option><option>3 persone</option><option>4 persone</option><option>5 persone</option><option>6 persone</option><option>7 persone</option><option>8 persone</option><option>Più di 8 persone</option></select></label><label class="wide"><span id="note-label">Allergie, esigenze alimentari o altre richieste (facoltativo)</span><textarea name="note" rows="3" maxlength="1200" placeholder="Indica eventuali allergie o altre esigenze"></textarea></label></div><p class="fine">I dati del modulo non vengono salvati su questo sito. Il pulsante prepara un messaggio su WhatsApp: sarai tu a inviarlo al locale.</p><button class="button full" type="submit">Prepara richiesta tavolo ↗</button><p id="form-message" role="status"></p><a id="send-request" class="button full" hidden target="_blank" rel="noopener">Continua su WhatsApp ↗</a></form></div></section>'''
s+=f'''<section id="sedi" class="section wrap split"><div><p class="eyebrow">DOVE SIAMO</p><h2>Sorriso Bistrot,<br><em>Roma San Basilio</em></h2><div class="address"><h3>Via Sarnano</h3><p>Via Sarnano 4 · 00156 Roma<br><a href="tel:+393455834226">345 583 4226</a></p><p>Martedì – domenica · 18:00–23:00<br>Lunedì · chiuso</p></div><div class="actions"><a class="button" href="{maps}" target="_blank" rel="noopener"><img class="maps-brand-pin" src="img/maps-sorriso-v2.svg" alt="" width="32" height="40">Indicazioni su Google Maps ↗</a><a class="text-link" href="tel:+393455834226">Chiama</a></div></div><div class="location-map"><div class="map-preview"><iframe title="Anteprima Google Maps — Via Sarnano 4, Roma" src="https://www.google.com/maps?ll=41.9391098%2C12.5781278&amp;z=17&amp;t=m&amp;output=embed" width="600" height="450" loading="lazy" tabindex="-1" aria-hidden="true" referrerpolicy="no-referrer-when-downgrade"></iframe><a class="map-preview-link" href="{maps}" target="_blank" rel="noopener" aria-label="Sorriso Bistrot, Via Sarnano 4: apri la mappa interattiva su Google Maps"><span class="map-marker" aria-hidden="true"><span class="map-marker-shadow"></span><img src="img/maps-sorriso-v2.svg" alt="" width="70" height="90"><span class="map-marker-label">Sorriso Bistrot</span></span><span class="map-open-label">Apri la mappa interattiva ↗</span></a></div><a href="{maps}" target="_blank" rel="noopener">Apri in Google Maps ↗<span>Via Sarnano 4 · Roma</span></a></div></section>'''
# Social video links and optional local posters are configured independently of page copy.
socials=json.loads((P/'social-videos.json').read_text())
s+='<section id="social" class="section social-section"><div class="wrap"><div class="section-head"><p class="eyebrow">TIKTOK · INSTAGRAM · FACEBOOK</p><h2>Seguici sui <em>social</em></h2><p>Guarda i nostri video per scoprire le promozioni, le offerte e le novità di Sorriso.</p></div><div class="social-tabs" aria-label="Scegli un social">'
for social in socials:
    s+=f'<a class="social-tab" href="#social-{social["id"]}">{esc(social["name"])}</a>'
s+='</div>'
for social in socials:
    sid=social['id'];name=esc(social['name'])
    s+=f'<div class="social-panel" id="social-{sid}" aria-labelledby="social-title-{sid}"><div class="social-panel-head"><h3 id="social-title-{sid}">{name}</h3>'
    if social['profile']:
        s+=f'<a class="text-link" href="{esc(social["profile"])}" target="_blank" rel="noopener noreferrer">Seguici su {name} ↗</a>'
    s+=f'</div><div class="social-track" id="social-track-{sid}" tabindex="0" aria-label="Video {name}">'
    for i in range(len(social['videos'])):
        video=social['videos'][i] if i<len(social['videos']) else None
        if video and video.get('embed'):
            s+=f'<article class="social-video"><div class="social-player"><div class="social-player-fallback" aria-hidden="true">{name}<span>Se il video non si carica,<br>aprilo dal link qui sotto.</span></div><iframe src="{esc(video["embed"])}" title="{esc(video["title"])} — {name}" loading="lazy" allow="fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div><div class="social-video-copy"><h4>{esc(video["title"])}</h4><a class="text-link" href="{esc(video["url"])}" target="_blank" rel="noopener noreferrer">Guarda su {name} ↗</a></div></article>'
        elif video:
            poster=f'<img src="{esc(video["poster"])}" alt="" loading="lazy" width="360" height="480">' if video.get('poster') else ico('play')
            s+=f'<a class="social-video" href="{esc(video["url"])}" target="_blank" rel="noopener noreferrer"><div class="social-poster">{poster}<span class="social-platform">{name}</span></div><div class="social-video-copy"><h4>{esc(video["title"])}</h4><span>Guarda su {name} ↗</span></div></a>'
        else:
            cover_key=['pizze/Margherita','antipasti/Supplì di Riso','dolci/Cheesecake'][i%3]
            cover=image_tag(cover_key,sizes='(max-width:700px) 80vw, 370px',decorative=True)
            s+=f'<article class="social-video is-placeholder" aria-label="Spazio per il video {i+1} di {name}"><div class="social-poster illustrated-cover">{cover}<span class="social-platform">{name}</span><span class="social-placeholder-mark" aria-hidden="true">{i+1:02d}</span><span class="social-coming">Video in arrivo</span></div><div class="social-video-copy"><p>I video di Sorriso su {name}</p></div></article>'
    if not social['videos']:
        destination=social['profile']+'reels/' if sid=='instagram' else social['profile']
        s+=f'<a class="social-profile-link" href="{esc(destination)}" target="_blank" rel="noopener noreferrer">{ico("play")}<strong>Guarda i video di Sorriso su {name}</strong><span>Apri {name} ↗</span></a>'
    s+=f'</div><div class="social-carousel-controls"  hidden><button type="button" data-social-step="-1" aria-controls="social-track-{sid}" aria-label="Video precedenti su {name}">←</button><span>Scorri i video</span><button type="button" data-social-step="1" aria-controls="social-track-{sid}" aria-label="Video successivi su {name}">→</button></div></div>'
s+='</div></section>'
s+='''<section class="wrap faq"><p class="eyebrow">PRIMA DI VENIRE A TROVARCI</p><h2>Domande <em>frequenti</em></h2><details><summary>Dove si trova Sorriso Bistrot?</summary><p>Sorriso Bistrot si trova in Via Sarnano 4, nel quartiere San Basilio a Roma. Puoi mangiare al tavolo oppure richiedere un ordine da asporto.</p></details><details><summary>Il locale propone solo prodotti senza glutine?</summary><p>No, proponiamo anche pizze con impasto classico contenente glutine. Gli impasti senza glutine vengono preparati in un laboratorio separato. Segnala celiachia e altre allergie quando prenoti o ordini.</p></details><details><summary>Come prenoto un tavolo o una pizza da asporto?</summary><p>Usa il modulo per preparare la richiesta su WhatsApp o chiama il 345 583 4226. Per l’asporto indica prodotti, quantità e impasti. Attendi sempre la conferma dello staff.</p></details><details><summary>Ci sono anche fritti e dolci senza glutine?</summary><p>Sì, il menù include antipasti e dolci gluten free. Consulta la pagina menù per prodotti, prezzi e allergeni e verifica le disponibilità con lo staff.</p></details><details><summary>Gli impasti senza glutine contengono frumento deglutinato, lattosio o proteine del latte?</summary><p>No. I nostri impasti senza glutine sono anche senza frumento deglutinato, senza lattosio e senza proteine del latte. Queste indicazioni riguardano gli impasti senza glutine. Condimenti e altri prodotti possono contenere allergeni: consulta il menù e segnala le tue esigenze allo staff.</p></details><details><summary>Preparate voi l’impasto senza glutine?</summary><p>Sì. L’impasto è di nostra produzione e viene preparato nel nostro laboratorio gluten free separato.</p></details><details><summary>Come ordino a domicilio?</summary><p>Puoi ordinare su <a href="https://deliveroo.it/it/menu/Roma/roma-san-basilio/giappo-pizza-senza-glutine" target="_blank" rel="noopener">Deliveroo</a> o <a href="https://www.justeat.it/restaurants-sorriso--gluten-free-roma/menu" target="_blank" rel="noopener">Just Eat</a>. Scegli la piattaforma e completa l’ordine sul suo sito o nella sua app.</p></details></section></main>'''
s+=footer()
(P/'index.html').write_text(s)
# Full menu: prerender products so content and prices are available without JavaScript.
s=head('Menù e prezzi | Sorriso Bistrot, pizzeria senza glutine Roma','Pizze classiche e senza glutine, fritti, dolci e bevande: consulta ingredienti, allergeni e prezzi di Sorriso Bistrot in Via Sarnano 4, Roma San Basilio.','menu.html')+nav()
s+='''<main id="contenuto"><section class="wrap menu-page-head"><p class="eyebrow">SORRISO BISTROT · VIA SARNANO, ROMA</p><h1>Il menù di <em>Sorriso Bistrot</em></h1><p>Pizza classica napoletana, forno a legna, fritti, dolci e bevande. Tutte le pizze sono disponibili anche senza glutine.</p><div class="actions"><a class="button" href="./#prenota">Prenota un tavolo ↗</a><a class="button outline" href="./?servizio=asporto#prenota">Ordina d’asporto ↗</a></div></section>'''+ordering()+'''<section class="wrap menu-catalog"><aside class="dough-assurance menu-assurance" aria-label="Composizione degli impasti senza glutine"><p><strong>Tutte le pizze sono disponibili anche senza glutine</strong></p><p>I nostri impasti senza glutine sono anche senza frumento deglutinato, senza lattosio e senza proteine del latte.</p><p class="dough-assurance-note">Queste indicazioni riguardano gli impasti senza glutine. Condimenti e altri prodotti possono contenere allergeni: consulta il menù e segnala le tue esigenze allo staff.</p></aside><p class="fine menu-image-note">Immagini generate con IA a scopo illustrativo. Per scegliere fai riferimento a ingredienti, varianti e prezzi riportati in ogni scheda.</p><div class="catalog-tools" id="catalogo"><div class="catalog-tools-top"><div><h2>Esplora il menù</h2><p class="category-scroll-hint">Scorri le categorie <span aria-hidden="true">→</span></p></div><label>Cerca nel menù<input id="search-menu" type="search" placeholder="Margherita, supplì, pistacchio…"></label></div><div class="category-list" role="group" aria-label="Filtra per categoria">'''
s+=f'<button class="category-chip" type="button" data-category-filter="tutte" aria-pressed="true" aria-controls="menu-results">Tutto il menù <span>{sum(len(c["items"]) for c in data)}</span></button>'
category_labels={'pizze':'Pizze classiche','speciali':'Speciali','gourmet':'Gourmet','primi':'Primi'}
for cat in data:s+=f'<button class="category-chip" type="button" data-category-filter="{cat["id"]}" aria-pressed="false" aria-controls="menu-results">{esc(category_labels.get(cat["id"],cat["t"]))} <span>{len(cat["items"])}</span></button>'
s+='''</div></div><div id="menu-results"><p id="result-count" role="status" aria-live="polite"></p><p id="empty-menu" hidden>Nessun prodotto trovato. Prova un altro ingrediente o seleziona tutte le categorie.</p>'''

for cat in data:
    s+=f'<section class="menu-category" id="categoria-{cat["id"]}" data-category="{cat["id"]}"><div class="category-heading"><h2>{esc(cat["t"])}</h2><span>{len(cat["items"]):02d} proposte</span></div><div class="product-grid">'
    for it in cat['items']:
        n=it['n'];d=it['d'];pc=it['pc'];pg=it['pg']
        if pg and pg!=pc:
            prices=f'<div class="product-price multiple"><div class="price-option"><span>Classica</span><b>{esc(pc)}</b></div><div class="price-option"><span>Senza glutine</span><b>{esc(pg)}</b></div></div>'
        else:
            prices=f'<div class="product-price"><b>{esc(pg or pc)}</b><span>{"Classica e senza glutine" if pg else ""}</span></div>'
        gluten_free_badge = f'<span class="product-gf-badge" lang="en">{ico("check")}Gluten free</span>' if cat["id"] in ("antipasti", "dolci") else ""
        s+=f'<article class="product" id="{item_id(cat["id"],n)}" data-search="{esc((n+" "+d).lower())}">{ph(n,key=cat["id"]+"/"+n)}<div class="product-copy">{gluten_free_badge}<h3>{esc(n)}</h3><p>{esc(d)}</p><p class="allergens">Allergeni: {esc(it["a"]) if it["a"] else "chiedere allo staff"}</p>{prices}</div></article>'
    s+='</div></section>'
s+='''</div></section><section class="wrap menu-notes"><h2>Ingredienti e allergeni</h2><p><strong>Impasti senza glutine:</strong> senza frumento deglutinato, senza lattosio e senza proteine del latte. Le indicazioni si riferiscono agli impasti; per condimenti e altri prodotti consulta gli allergeni di ciascuna proposta.</p><p>1 Glutine · 2 Crostacei · 3 Uova · 4 Pesce · 5 Arachidi · 6 Soia · 7 Latte · 8 Frutta a guscio · 9 Sedano · 10 Senape · 11 Sesamo · 12 Anidride solforosa e solfiti · 13 Lupino · 14 Molluschi.</p><p>L’impasto classico contiene glutine. Le indicazioni sono riprese dal menù fornito; in caso di celiachia o allergie chiedi conferma al personale prima di ordinare. Il menù di origine riporta la possibile presenza di tracce per contaminazione.</p><p>Extra: ingrediente €1 · salsiccia €1,50 · prosciutto €2 · cornicione ricotta €2 · senza lattosio €1,50 · impasto canapa bio €2. Verifica le varianti disponibili con il locale.</p><a class="button" href="./?servizio=asporto#prenota">Ordina d’asporto ↗</a></section></main>'''+footer()
(P/'menu.html').write_text(s)
print('Generated homepage and menu:',sum(len(x['items']) for x in data),'products')

# Keep discovery files aligned with the public domain when rebuilding the pages.
(P/'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{public_url(page)}</loc></url>\n' for page in ('index.html', 'menu.html'))
    + '</urlset>\n'
)
(P/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
