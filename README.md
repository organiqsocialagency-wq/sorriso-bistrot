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

La preferenza di sistema per il movimento ridotto disattiva gli effetti e la rotazione automatica iniziale. Su mobile e schermi bassi gli impasti restano consultabili in sequenza; senza JavaScript testi, foto, prodotti e link rimangono nell’HTML. La hero usa AccordionGallery con espansione al passaggio del mouse, al tocco e tramite tastiera; la preferenza di movimento ridotto elimina transizioni, inclinazione e parallasse.

## Materiali reali della home — ottobre 2026

I nuovi scatti e filmati forniti dal locale si trovano nella cartella sorella `Immagini:Video/`. `prepare_real_media.py` conserva gli originali e prepara WebP responsive e MP4 H.264/SDR con fast start. `real-media.json` registra file sorgente e intervalli selezionati; il template unisce questi dati al catalogo delle immagini illustrative.

La hero mostra tre fotografie rielaborate con pizze tonde; i precedenti filmati della hero rimangono archiviati nel repository, ma non vengono caricati in pagina. La sezione pizzeria riproduce il filmato reale della sala IMG_6202; L’Originale di Sorriso usa i secondi 15–30 di IMG_8359 (15 secondi totali, senza traccia audio), i semi di zucca usano i secondi 17–27 di IMG_8327 (10 secondi totali, senza traccia audio); la canapa usa un estratto di 5 secondi (da 00:02 a 00:07) di IMG_8326. I quattro video sono silenziati, in loop e si fermano fuori schermo; è disponibile la pausa manuale. La card Pizze è tornata alla Margherita illustrativa, mentre Fritti conserva lo scatto reale del supplì. I dolci mantengono immagini illustrative. Tutti e tre gli impasti mostrano ora filmati reali.

Per aggiornare i materiali reali: `python3 prepare_real_media.py`, poi `python3 build_site.py`. Non caricare gli originali HEIC/MOV nel repository.

## Recensioni DriftWall e promozioni

Dopo modifiche al componente o al suo adattatore:

```sh
npm ci
npm run build:reviews
python3 build_site.py
```

`assets/reviews.js` e `assets/reviews.css` sono bundle locali già pronti per Pages. `components/reviews.tsx` configura il componente fornito, senza modificarlo; le schede SVG contengono gli stessi tre estratti già pubblicati. La vista testuale è disponibile con “Leggi tutte le recensioni”, senza JavaScript e con movimento ridotto. Le stelle compaiono solo dove la valutazione è documentata.

Il popup condiviso è in `components/promotions.html`: Promo Famiglia, martedì/mercoledì/giovedì, sconto 15% per tavoli di almeno 4 persone, da comunicare alla prenotazione. La CTA chiama +39 345 583 4226. Il pulsante “Aggiornami sulle nuove promo” passa alla seconda schermata dello stesso dialog (2/2), con un pulsante per tornare alla promo. La riapertura parte sempre dalla promo, senza numerazione; il passaggio fra schermate conserva i campi compilati. Il modulo aggiornamenti raccoglie nome, cognome e una scelta fra email e telefono, con consenso esplicito; prepara un messaggio WhatsApp che l’utente deve inviare. Non esiste un database iscritti e nessun dato è salvato dal sito.

L’ultima serie illustrativa dei fritti comprende 11 immagini, generate con il tool imagegen integrato dalla foto autentica `img/real/fritti-1280.webp`. Originali e prompt sono in `output/imagegen/fritti-reference-v3/`; le varianti ottimizzate hanno suffisso `-v3-` e sono registrate in `image-assets.json`. Non rigenerare questo catalogo dal vecchio manifest di `prepare_images.py`, che contiene le immagini precedenti.

I sette video usano la serie `*-sdr-v3.mp4`, riesportata dagli originali iPhone HLG. La conversione percettiva in un solo passaggio (FFmpeg 9 `scale`, intent `perceptual`) conserva i dettagli delle alte luci che la precedente catena di conversione appiattiva; una curva moderata abbassa l’esposizione e porta il bianco massimo all’86%. La correzione è nei file, incluse le copertine estratte dagli MP4: il filtro CSS di luminosità è stato rimosso. Le esportazioni sono H.264/BT.709 a intervallo limitato, senza metadati HDR residui e con percorsi versionati per evitare la cache. `prepare_real_media.py` prepara anche la sala e tutti e tre gli impasti. I ritagli e l’assenza di audio nei quattro video in loop sono conservati.

Dettagli delle opzioni di conversione: [documentazione FFmpeg](https://ffmpeg.org/ffmpeg-filters.html#scale).

La Promo Famiglia include un’immagine illustrativa generata con il tool imagegen integrato: una famiglia a tavola e il testo dell’offerta incorporato nella grafica. Originale e prompt sono in `output/imagegen/promo-famiglia-v2/`; le varianti WebP da 480 e 960 px in `img/generated/`. Subito sotto, un esempio di conto per quattro persone mostra 90,00 € barrati, totale scontato 76,50 € e risparmio 13,50 € (15%). Il popup chiarisce che ogni mese c’è una nuova promozione e che questa offerta è valida solo martedì, mercoledì e giovedì per un tavolo di almeno quattro persone.


Il popup promozioni usa due colonne sui desktop (massimo 1040 px) e una colonna sui dispositivi più stretti. La CTA telefonica “Prenota ora” è arricchita dal componente React Bits StarBorder originale fornito dal cliente, conservato in `components/StarBorder.tsx` e `components/StarBorder.css`. `components/promo.tsx` applica la palette Sorriso; il modulo viene caricato solo alla prima apertura del popup. Il link telefonico statico resta utilizzabile se il modulo dell’animazione non si carica; con movimento ridotto richiesto resta privo di animazione. Compilare con `npm run build:promo` prima di `python3 build_site.py`.


## Hero AccordionGallery

`components/AccordionGallery.tsx` e `.css` contengono il componente React Bits fornito dal cliente, con l’animazione GSAP originale. Le integrazioni riguardano pulsanti accessibili, spostamento del focus con le frecce, testi italiani e immagini responsive. `components/hero.tsx` configura la palette Sorriso, conserva i colori delle foto e passa a una colonna espandibile su schermi stretti. Il CSS del sito corregge l’altezza automatica della demo mobile per consentire l’espansione effettiva dei pannelli.

La galleria sostituisce solo i tre video della hero, mantenendo titolo, pulsanti, sala e impasti. Le immagini WebP in `img/hero/` derivano dai tre ritocchi approvati nella conversazione: la pinsa è stata trasformata in pizza tonda. Originali di generazione e prompt sono archiviati localmente in `output/imagegen/pizze-tonde-originali-v1/`. Una galleria HTML statica resta visibile senza JavaScript o se il modulo non si carica. Il movimento ridotto è rispettato anche quando cambia a pagina aperta.

Ricompilare con `npm run build:hero`, quindi `python3 build_site.py`. Il modulo e il suo CSS vengono inclusi solo nella homepage; i relativi URL sono versionati con hash.


## Dominio sorrisobistrot.it

La configurazione per il dominio è nel file `CNAME`. `SITE_URL` in `build_site.py` determina canonical, Open Graph, URL strutturati, sitemap e robots. Dopo una modifica al dominio eseguire `python3 build_site.py`.

La pubblicazione GitHub Pages usa il ramo `main`, cartella `/`. La configurazione DNS rimane presso Register.it. Per attivare il dominio, configurare prima `sorrisobistrot.it` su GitHub Pages e poi applicare questi record in **Dominio & DNS → Configurazione DNS → Modifica zone DNS**:

| Tipo | Nome | Valore |
| --- | --- | --- |
| A | sorrisobistrot.it | 185.199.108.153 |
| A | sorrisobistrot.it | 185.199.109.153 |
| A | sorrisobistrot.it | 185.199.110.153 |
| A | sorrisobistrot.it | 185.199.111.153 |
| CNAME | www.sorrisobistrot.it | organiqsocialagency-wq.github.io |

I quattro record A sostituiscono il puntamento precedente a `195.110.124.133`. Il CNAME `www` sostituisce quello che puntava a `sorrisobistrot.it`. Conservare nameserver e record email esistenti: il record MX rilevato il 26 ottobre 2026 è `10 mail.register.it`. Al momento della verifica non erano presenti record AAAA o CAA.

Dopo il cambio DNS verificare homepage, menù, media, redirect da `www` e dal precedente indirizzo GitHub Pages. Abilitare **Enforce HTTPS** appena GitHub ha emesso il certificato. La presenza del file CNAME da sola non conferma che il dominio sia operativo.

Riferimenti: [GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [gestione DNS Register.it](https://www.register.it/assistenza/cambiare-dns/).
