# Generatori dei dati del Pokédex

Servono solo a chi vuole rigenerare `p5e-2024.js`; l'app non li usa.

1. Clona in una cartella `src/` accanto a questi script (bastano i file indicati):
   - `https://github.com/Auroratide/poke5e` → `src/lib/srd/data/2024/{pokemon,moves,tms}/en.json`
   - `https://github.com/PokeAPI/pokeapi` → `data/v2/csv/` (moves, move_names, machines, items,
     pokemon, pokemon_moves, version_groups)
   - `https://github.com/Jerakin/p5e-data` (branch `no-variants`) → `data/pokemon/`
2. Esporta i dati attuali dell'app in `ora.json` (P5E dopo `p5e-data.js` e `p5e-gen8.js`).
3. `python3 costruisci.py` scrive `p5e-2024.js`; `python3 fuori_nuove.py` aggiunge a
   `p5e-fuori.js` il testo «fuori dalla lotta» delle mosse nuove.

La mappa dei nomi (italiano dell'app ↔ identificativi inglesi) usa le liste di mosse
delle stesse specie in inglese e in italiano, la tabella MT, i nomi ufficiali di PokéAPI
e, per le poche mosse di gen 8 rimaste, il file `dati-gen8-poke5e.txt`.
