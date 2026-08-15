# luthia
manuale

## Pokédex di Aethera

`pokedex.html` — compagno digitale per la campagna «Cronache di Allenatori» (Pokémon 5e),
**file unico** con tutto il database incorporato: si apre nel browser, anche da telefono,
senza installare nulla; i salvataggi restano sul dispositivo di ognuno (con
Esporta/Importa per condividerli).

- **Schede Pokémon** (schermata iniziale): una galleria di schede, una per giocatore,
  ognuna indipendente ed esportabile come file a sé. Dentro la scheda: **squadra di sei**
  in stile scheda del personaggio (scegli la specie e si compila da sola dal dex) e
  **Box** con tutti gli altri Pokémon catturati, con scambio in due tocchi. Mosse con
  dettagli e danni scalati al livello, PF/competenza/STAB ricalcolati a ogni livello,
  evoluzioni che aggiornano la scheda.
- **Natura e abilità come nei giochi**: alla cattura escono da sole — natura fra le 21
  ufficiali, abilità sorteggiata fra quelle che quella specie può avere (nascosta compresa).
  Quando il Pokémon evolve l'abilità può cambiare: decide il giocatore (o il GM imposta
  «la tiene» / «si ritira sempre»).
- **Poké Market**: scaffali per categoria con Poké Ball, cure, vitamine, pietre, oggetti
  chiave e **tutte le 256 MT**, ognuno con il suo prezzo. Si compra per il giocatore la cui
  scheda è aperta: i soldi si scalano da soli, la roba finisce nello zaino e si può
  rivendere a metà prezzo. Ogni articolo ha la sua scheda con la descrizione per intero e,
  per le MT, la scheda completa della mossa: tipo, PP, gittata, danni per livello ed effetti.
  Lo zaino è diviso in tasche e le MT si usano direttamente da lì, che le propone solo ai
  Pokémon che possono impararle.
- **Centro Pokémon**: un tocco e tutta la squadra torna a PF pieni, senza stati e con i
  PP ricaricati; si può curare solo una cosa alla volta o includere anche il Box.
- **Stati e PP**: i sette stati (avvelenato, iper-avvelenato, scottato, paralizzato,
  addormentato, congelato, confuso) stanno sulla scheda con il loro effetto, e il pulsante
  «fine turno» tira i danni e i tiri salvezza per liberarsene. Gli effetti sono quelli che
  il sistema P5e descrive nelle proprie abilità e mosse — *Dentistretti* (svantaggio,
  riduzione dei danni, danni a fine turno), *Velencura*, *Tossina* (il doppio), *Gelamento*
  (velocità 0), *Sveglialampo* — mentre i numeri, che il database non riporta, si regolano
  da **Impostazioni → Stati**. Ogni mossa negli slot ha i suoi PP, che si consumano usandola
  e si ricaricano con Etere, Elisir o al Centro; si possono spegnere del tutto.
- **Usare gli oggetti**: dal Pokémon, «🎒 Usa oggetto» mostra cosa c'è nello zaino che serve
  davvero in quel momento — pozioni e Acqua Fresca se è ferito, antidoti se ha uno stato,
  Etere se ha finito i PP — tira la formula di cura scritta sull'oggetto e lo consuma.
- **Natura scegliibile**: come per l'abilità, l'elenco completo delle 21 nature con i loro
  modificatori; alla cattura resta sorteggiata.
- **MT e mosse modificabili**: da Impostazioni → Tabella MT si corregge quale mossa insegna
  ogni MT, si creano **MT nuove** con un numero libero e si apre l'**editor delle mosse** —
  tipo, PP, attivazione, gittata, danni per fascia di livello e descrizione. Serve soprattutto
  per le 91 mosse recenti che il dex P5e non descrive: scritte una volta, compaiono ovunque
  come le altre. Tutto con ripristino.
- **Lealtà**: il valore del sistema P5e usato dalle bacche che riducono le caratteristiche e
  dalla Calmanella, ora tracciato sulla scheda; alcune Poké Ball la assegnano alla cattura.
- **Statistiche del giocatore**: record vittorie/sconfitte con percentuale, Pokémon
  catturati, medaglie, Pokémon più usato, iniziale, mossa preferita, XP guadagnati,
  avversario ricorrente e composizione della squadra per tipo. Si aggiornano da sole
  con le lotte, le catture e l'esperienza.
- **Pokédex ordinabile**: per numero, nome, sfida (SR), tipo, PF, CA o livello minimo.
- **Immagini**: sprite accanto a ogni specie nell'elenco, nelle carte della squadra e del Box,
  e l'artwork grande nella scheda. Arrivano dall'archivio pubblico PokéAPI in base al numero
  del dex — non sono nel repository, quindi la prima volta serve connessione e poi restano
  nella cache del browser. Le forme regionali hanno il numero della specie base: lì compare
  un segnaposto invece di un'immagine sbagliata, e nell'editor della specie c'è un campo per
  incollare l'indirizzo giusto.
- **Schede modificabili da chiunque**: ogni specie del dex si può correggere — utile
  soprattutto per le MT, visto che il dex P5e standard si ferma alla MT 100 e le 156 più
  recenti non sono assegnate alle specie vecchie. Dalla schermata «Usa una MT» c'è
  «Ne manca una?»: si cerca, si aggiunge alla specie una volta sola e vale per sempre.
  Ogni modifica si annulla con **Ripristina** e resta sul proprio dispositivo.
- **Pokédex**: 1043 specie con scheda completa (CA, PF, statistiche, tiri salvezza,
  abilità, mosse per livello, evoluzioni, MT con numero e nome) — senza indicazioni su
  dove trovarle in Aethera, per non fare spoiler ai giocatori. Comprende le 896 specie
  del dex P5e standard più le **132 schede ufficiali di Spada/Scudo, Leggende Arceus e
  delle forme di Galar e di Hisui**, convertite dalle pagine di poke5e.app.
- **Console del GM**: i giocatori mandano la propria scheda con un codice da incollare in
  chat (o il file .json) e il GM vede squadre, livelli, PF, mosse e zaino di tutti.
  Nessun server: i salvataggi restano sui dispositivi.
- **Lotte**: tavolo del GM per più scontri in contemporanea — PF auto-calcolati, stati,
  prova di cattura in stile PHB (CD = base + livello + PF rimasti). Le Poké Ball non
  aiutano il tiro: **abbassano la CD** (Mega Ball −5, Ultra Ball −10, quelle specialistiche
  −8 quando ricorre la loro condizione), e la Master Ball cattura senza tirare.
- **PNG**: capipalestra, rivali del torneo, Superquattro e Campione della guida di Aethera
  già pronti (squadra, formato, regola speciale), modificabili e creabili da zero, con
  apertura rapida della lotta.
- **Oggetti**: catalogo con Poké Ball, cure, vitamine, pietre evolutive e oggetti chiave
  (mappa città, canna da pesca, flauto Poké…), più gli strumenti tenuti del dex; ogni
  giocatore ha zaino con quantità e soldi.
- **Specie personalizzate**: editor per creare o modificare qualsiasi Pokémon. Le linee di
  Scarlatto/Violetto (iniziali di Paldea, Charcadet→Armarouge/Ceruledge, Frigibax→Baxcalibur)
  restano schede di casa, riconoscibili e modificabili; tutto il resto di gen 8 usa i numeri
  ufficiali.
- **Tabella MT completa**: 256 macchine tecniche con numero e nome italiano, usate sia dalle
  schede del dex sia dal sistema dei 4 slot mosse.
- **Calcoli** e **Tipi**: formule P5e e tabella di efficacia in due direzioni.

### Installazione e aggiornamenti

L'app è una PWA: aperta da un indirizzo `https://` si installa sulla schermata Home
(iPhone/iPad da Safari con «Aggiungi a Home», Android da Chrome con «Installa app») e da lì
funziona anche senza connessione.

Gli aggiornamenti **non cancellano nulla**: i salvataggi vivono in `localStorage` e hanno un
numero di schema. Quando l'app cambia struttura, all'avvio converte i dati vecchi da sola
(e prima mette da parte una copia di sicurezza, ripristinabile da *Copie di sicurezza*).
Quando esce una versione nuova compare in basso una barra **Aggiorna**: si applica quando
lo decide il giocatore, mai a metà di una lotta.

`p5e-data.js` è generato dal dataset open source del dex P5e standard
(Jerakin/p5e-data, branch no-variants) più i datafiles di Jerakin/Pokedex5E.
