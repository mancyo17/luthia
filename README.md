# luthia
manuale

## Pokédex di Aethera

`pokedex.html` — compagno digitale per la campagna «Cronache di Allenatori» (Pokémon 5e),
**file unico** con tutto il database incorporato: si apre nel browser, anche da telefono,
senza installare nulla; i salvataggi restano sul dispositivo di ognuno (con
Esporta/Importa per condividerli).

- **Schede Pokémon** (schermata iniziale): una galleria di schede, una per giocatore,
  ognuna indipendente ed esportabile come file a sé. Dentro la scheda: squadra in stile
  scheda del personaggio (scegli la specie e si compila da sola dal dex), nature ufficiali
  P5e applicate in automatico, mosse con dettagli e danni scalati al livello,
  PF/competenza/STAB ricalcolati a ogni livello, evoluzioni che aggiornano la scheda.
- **Statistiche del giocatore**: record vittorie/sconfitte con percentuale, Pokémon
  catturati, medaglie, Pokémon più usato, iniziale, mossa preferita, XP guadagnati,
  avversario ricorrente e composizione della squadra per tipo. Si aggiornano da sole
  con le lotte, le catture e l'esperienza.
- **Pokédex**: 1043 specie con scheda completa (CA, PF, statistiche, tiri salvezza,
  abilità, mosse per livello, evoluzioni, MT con numero e nome) — senza indicazioni su
  dove trovarle in Aethera, per non fare spoiler ai giocatori. Comprende le 896 specie
  del dex P5e standard più le **132 schede ufficiali di Spada/Scudo, Leggende Arceus e
  delle forme di Galar e di Hisui**, convertite dalle pagine di poke5e.app.
- **Console del GM**: i giocatori mandano la propria scheda con un codice da incollare in
  chat (o il file .json) e il GM vede squadre, livelli, PF, mosse e zaino di tutti.
  Nessun server: i salvataggi restano sui dispositivi.
- **Lotte**: tavolo del GM per più scontri in contemporanea — PF auto-calcolati, stati,
  prova di cattura in stile PHB (CD = base + livello + PF rimasti) con tutte le Poké Ball.
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

`p5e-data.js` è generato dal dataset open source del dex P5e standard
(Jerakin/p5e-data, branch no-variants) più i datafiles di Jerakin/Pokedex5E.
