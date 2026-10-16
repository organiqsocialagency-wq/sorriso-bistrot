# Sorriso Bistrot

Sito della pizzeria Sorriso Bistrot, Via Sarnano 4, Roma.

Landing responsive e menù con 88 prodotti, ricerca, categorie a pulsanti e prezzi classica/gluten free visibili nelle schede, senza selettore del listino. Richieste tavolo e asporto tramite messaggio WhatsApp; consegna tramite Deliveroo e Just Eat.

## Sviluppo locale

```sh
python3 -m http.server 8311 --bind 127.0.0.1
```

Aprire http://127.0.0.1:8311/.

## Aggiornare il sito

- `menu.json`: prodotti, ingredienti, allergeni e prezzi.
- `build_site.py`: contenuti e template delle pagine.
- `styles.css`: stile responsive, palette e font locali.
- `app.js`: carosello, navigazione, filtri e richiesta WhatsApp.

Dopo aver aggiornato i dati o i template:

```sh
python3 build_site.py
```

Il sito è statico: i file HTML generati sono già pronti per GitHub Pages.

## Foto e video

La home combina fotografie e video reali con le immagini illustrative ancora prive di uno scatto identificato. `real-media.json` registra i materiali reali in `img/real/` e `videos/`; `image-assets.json` mantiene il catalogo illustrativo in `img/generated/`. Il template distingue i due tipi nelle didascalie e nei testi alternativi. Le fotografie usano varianti WebP responsive, dimensioni esplicite e caricamento differito, tranne la prima copertina.

`prepare_images.py` prepara le varianti dagli originali elencati nel manifest locale `output/imagegen/manifest.json` e salva i prompt in `output/imagegen/prompts.json`. Questa fase richiede Pillow; la cartella `output/` è esclusa da Git. Per ricostruire il sito con le immagini già presenti è sufficiente `python3 build_site.py`.

Il 1 ottobre 2026 sono state rigenerate 34 immagini di pizze e 2 immagini della home usando come riferimento gli scatti di pinse forniti dal locale: forma tonda, piatto bianco, luce chiara e condimenti coerenti con il menù. I file aggiornati hanno suffisso `-v2-` per evitare immagini obsolete in cache. Gli originali, i riferimenti e i prompt della nuova serie sono archiviati localmente in `output/imagegen/reference-v2/`. La Campione del Mondo conserva il dettaglio dell’impasto precedente, in attesa dei sette ingredienti o di una foto identificata dal locale.

## Prenotazioni

Il modulo prepara una richiesta WhatsApp al locale. Il visitatore deve inviarla e attendere la conferma dello staff. Non è presente un database prenotazioni né una disponibilità dei tavoli in tempo reale.

## Contenuti

Le recensioni sono brevi estratti attribuiti a Google e riportati da Restaurant Guru, con fonte visibile; non sono un feed sincronizzato. Disponibilità, orari, prezzi e allergeni vanno mantenuti aggiornati dal locale. Il sito include anche il listino delle pizze con glutine.

## Animazioni

Movimenti ispirati a Split Text, Scroll Stack, Animated Content, Tilted Card, Carousel e Fade Content di React Bits, riscritti con CSS e Web Animations API per il sito statico. Questi effetti non richiedono librerie esterne; la sezione recensioni usa invece il componente React DriftWall originale, fornito dal cliente e conservato senza modifiche in `components/DriftWall.tsx` e `components/DriftWall.css`. Il titolo entra per parole; gli impasti si sovrappongono durante lo scroll nativo sui desktop con spazio sufficiente; le anteprime della home rispondono al puntatore. Carosello e categorie hanno transizioni brevi; i social mantengono lo scorrimento manuale.

La preferenza di sistema per il movimento ridotto disattiva gli effetti e la rotazione automatica iniziale. Su mobile e schermi bassi gli impasti restano consultabili in sequenza; senza JavaScript testi, foto, prodotti e link rimangono nell’HTML. Il carosello della hero supporta swipe e frecce da tastiera quando ha il focus, e si ferma fuori schermo, durante l’interazione e durante la riproduzione video.

## Materiali reali della home — ottobre 2026

I nuovi scatti e filmati forniti dal locale si trovano nella cartella sorella `Immagini:Video/`. `prepare_real_media.py` conserva gli originali e prepara WebP responsive e MP4 H.264/SDR con fast start. `real-media.json` registra file sorgente e intervalli selezionati; il template unisce questi dati al catalogo delle immagini illustrative.

La hero mostra tre filmati: stesura (IMG_8359), condimento (IMG_8361) e cottura (IMG_8364). I video si caricano al clic, partono silenziati con controlli nativi e si fermano cambiando slide, uscendo dalla hero o nascondendo la scheda. La sezione pizzeria riproduce il filmato reale della sala IMG_6202; la canapa usa un estratto di 5 secondi (da 00:02 a 00:07) di IMG_8326. Entrambi sono silenziati, in loop e si fermano fuori schermo; è disponibile la pausa manuale. La card Pizze è tornata alla Margherita illustrativa, mentre Fritti conserva lo scatto reale del supplì. Originale, zucca e dolci mantengono immagini illustrative.

Per aggiornare i materiali reali: `python3 prepare_real_media.py`, poi `python3 build_site.py`. Non caricare gli originali HEIC/MOV nel repository.

## Recensioni DriftWall e promozioni

Dopo modifiche al componente o al suo adattatore:

```sh
npm ci
npm run build:reviews
python3 build_site.py
```

`assets/reviews.js` e `assets/reviews.css` sono bundle locali già pronti per Pages. `components/reviews.tsx` configura il componente fornito, senza modificarlo; le schede SVG contengono gli stessi tre estratti già pubblicati. La vista testuale è disponibile con “Leggi tutte le recensioni”, senza JavaScript e con movimento ridotto. Le stelle compaiono solo dove la valutazione è documentata.

Il popup condiviso è in `components/promotions.html`: Promo Famiglia, martedì/mercoledì/giovedì, sconto 15% per tavoli di almeno 4 persone, da comunicare alla prenotazione. La CTA chiama +39 345 583 4226. Il modulo aggiornamenti raccoglie nome, cognome e una scelta fra email e telefono, con consenso esplicito; prepara un messaggio WhatsApp che l’utente deve inviare. Non esiste un database iscritti e nessun dato è salvato dal sito.

L’ultima serie illustrativa dei fritti comprende 11 immagini, generate con il tool imagegen integrato dalla foto autentica `img/real/fritti-1280.webp`. Originali e prompt sono in `output/imagegen/fritti-reference-v3/`; le varianti ottimizzate hanno suffisso `-v3-` e sono registrate in `image-assets.json`. Non rigenerare questo catalogo dal vecchio manifest di `prepare_images.py`, che contiene le immagini precedenti.

Il 16 ottobre è stata corretta l’esportazione HDR → SDR dei cinque video: la precedente normalizzazione delle alte luci produceva bianchi troppo chiari. I nuovi file `*-sdr-v2.mp4` e le relative copertine provengono dagli originali, con mappatura Hable rivista, segnalazione BT.709 e rimozione dei metadati HDR residui. I percorsi versionati evitano il riutilizzo dei video precedenti in cache. `prepare_real_media.py` ora prepara anche sala e canapa.

La Promo Famiglia include un’immagine illustrativa generata con il tool imagegen integrato: una famiglia a tavola e il testo dell’offerta incorporato nella grafica. Originale e prompt sono in `output/imagegen/promo-famiglia-v2/`; le varianti WebP da 480 e 960 px in `img/generated/`. Subito sotto, un esempio di conto per quattro persone mostra 90,00 € barrati, totale scontato 76,50 € e risparmio 13,50 € (15%). Il popup chiarisce che ogni mese c’è una nuova promozione e che questa offerta è valida solo martedì, mercoledì e giovedì per un tavolo di almeno quattro persone.
