# Sorriso Bistrot

Sito della pizzeria Sorriso Bistrot, Via Sarnano 4, Roma.

Landing responsive e menù con 89 prodotti, ricerca, categorie e prezzi classica/gluten free. Richieste tavolo e asporto tramite messaggio WhatsApp; consegna tramite Deliveroo e Just Eat.

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

Foto della pizzeria, farine e prodotti sono segnaposto. Per attivare i tre video aggiungere i file MP4 in `videos/` e impostare `videoSources` in `app.js`:

```js
const videoSources = ['videos/impasti.mp4', 'videos/forno.mp4', 'videos/pizzeria.mp4'];
```

Per video con parlato aggiungere sottotitoli WebVTT.

## Prenotazioni

Il modulo prepara una richiesta WhatsApp al locale. Il visitatore deve inviarla e attendere la conferma dello staff. Non è presente un database prenotazioni né una disponibilità dei tavoli in tempo reale.

## Contenuti

Le recensioni sono brevi estratti attribuiti a Google e riportati da Restaurant Guru, con fonte visibile; non sono un feed sincronizzato. Disponibilità, orari, prezzi e allergeni vanno mantenuti aggiornati dal locale. Il sito include anche il listino delle pizze con glutine.
