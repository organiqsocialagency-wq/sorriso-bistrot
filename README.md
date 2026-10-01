# Sorriso Bistrot

Sito della pizzeria Sorriso Bistrot, Via Sarnano 4, Roma.

Landing responsive e menù con 89 prodotti, ricerca, categorie a pulsanti e prezzi classica/gluten free visibili nelle schede, senza selettore del listino. Richieste tavolo e asporto tramite messaggio WhatsApp; consegna tramite Deliveroo e Just Eat.

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

Il sito contiene 95 immagini generate con IA a scopo illustrativo: 6 immagini per la home e una per ciascuno degli 89 prodotti del menù. La dicitura è visibile sulle pagine; le immagini non rappresentano fotografie del locale o dei prodotti effettivamente serviti.

Le 196 varianti WebP responsive attive sono in `img/generated/`; `image-assets.json` associa ogni prodotto alle sue immagini. Il caricamento usa `srcset` e `sizes`, dimensioni esplicite e lazy loading, tranne la prima immagine principale.

`prepare_images.py` prepara le varianti dagli originali elencati nel manifest locale `output/imagegen/manifest.json` e salva i prompt in `output/imagegen/prompts.json`. Questa fase richiede Pillow; la cartella `output/` è esclusa da Git. Per ricostruire il sito con le immagini già presenti è sufficiente `python3 build_site.py`.

Il 1 ottobre 2026 sono state rigenerate 34 immagini di pizze e 2 immagini della home usando come riferimento gli scatti di pinse forniti dal locale: forma tonda, piatto bianco, luce chiara e condimenti coerenti con il menù. I file aggiornati hanno suffisso `-v2-` per evitare immagini obsolete in cache. Gli originali, i riferimenti e i prompt della nuova serie sono archiviati localmente in `output/imagegen/reference-v2/`. La Campione del Mondo conserva il dettaglio dell’impasto precedente, in attesa dei sette ingredienti o di una foto identificata dal locale.

Il carosello della home mostra tre immagini di copertina. Per attivare i tre video aggiungere i file MP4 in `videos/` e impostare `videoSources` in `app.js`:

```js
const videoSources = ['videos/impasti.mp4', 'videos/forno.mp4', 'videos/pizzeria.mp4'];
```

Per video con parlato aggiungere sottotitoli WebVTT.

## Prenotazioni

Il modulo prepara una richiesta WhatsApp al locale. Il visitatore deve inviarla e attendere la conferma dello staff. Non è presente un database prenotazioni né una disponibilità dei tavoli in tempo reale.

## Contenuti

Le recensioni sono brevi estratti attribuiti a Google e riportati da Restaurant Guru, con fonte visibile; non sono un feed sincronizzato. Disponibilità, orari, prezzi e allergeni vanno mantenuti aggiornati dal locale. Il sito include anche il listino delle pizze con glutine.

## Animazioni

Movimenti ispirati a Split Text, Scroll Stack, Animated Content, Tilted Card, Carousel e Fade Content di React Bits, riscritti con CSS e Web Animations API per il sito statico. Non richiedono React né librerie esterne. Il titolo entra per parole; gli impasti si sovrappongono durante lo scroll nativo sui desktop con spazio sufficiente; le anteprime della home rispondono al puntatore. Carosello e categorie hanno transizioni brevi; i social mantengono lo scorrimento manuale.

La preferenza di sistema per il movimento ridotto disattiva gli effetti e la rotazione automatica iniziale. Su mobile e schermi bassi gli impasti restano consultabili in sequenza; senza JavaScript testi, foto, prodotti e link rimangono nell’HTML. Il carosello della hero supporta swipe e frecce da tastiera quando ha il focus, e si ferma fuori schermo, durante l’interazione e durante la riproduzione video.
