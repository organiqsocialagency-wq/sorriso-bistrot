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

Movimenti ispirati a Split Text, Scroll Stack, Animated Content, Tilted Card, Carousel e Fade Content di React Bits, riscritti con CSS e Web Animations API per il sito statico. Non richiedono React né librerie esterne. Il titolo entra per parole; gli impasti si sovrappongono durante lo scroll nativo sui desktop con spazio sufficiente; le anteprime della home rispondono al puntatore. Carosello e categorie hanno transizioni brevi; i social mantengono lo scorrimento manuale.

La preferenza di sistema per il movimento ridotto disattiva gli effetti e la rotazione automatica iniziale. Su mobile e schermi bassi gli impasti restano consultabili in sequenza; senza JavaScript testi, foto, prodotti e link rimangono nell’HTML. Il carosello della hero supporta swipe e frecce da tastiera quando ha il focus, e si ferma fuori schermo, durante l’interazione e durante la riproduzione video.

## Materiali reali della home — ottobre 2026

I nuovi scatti e filmati forniti dal locale si trovano nella cartella sorella `Immagini:Video/`. `prepare_real_media.py` conserva gli originali e prepara WebP responsive e MP4 H.264/SDR con fast start. `real-media.json` registra file sorgente e intervalli selezionati; il template unisce questi dati al catalogo delle immagini illustrative.

La hero mostra tre filmati: stesura (IMG_8359), condimento (IMG_8361) e cottura (IMG_8364). I video si caricano al clic, partono silenziati con controlli nativi e si fermano cambiando slide, uscendo dalla hero o nascondendo la scheda. Le anteprime pizze e fritti e la foto della sezione pizzeria usano materiali reali. Le foto delle tre ricette d’impasto restano illustrative in attesa dell’identificazione degli scatti; manca una foto reale dei dolci.

Per aggiornare i materiali reali: `python3 prepare_real_media.py`, poi `python3 build_site.py`. Non caricare gli originali HEIC/MOV nel repository.
