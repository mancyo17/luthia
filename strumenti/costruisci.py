# -*- coding: utf-8 -*-
"""Genera p5e-2024.js: la correzione dei dati del Pokédex.

  1. specie: SR, CA, PF, dado vita, livello minimo, caratteristiche, tipi, taglia,
     mosse iniziali, per livello e MT come nel SRD 2024 di poke5e.app;
  2. le 19 mosse ufficiali che il dex non aveva;
  3. PP come nei videogiochi (moves.csv di PokeAPI), tenendo quelli P5e da parte;
  4. MT 257-351: le mosse che sono state MT nei giochi ma mancano dalla tabella P5e,
     compatibili con chi poteva impararle da MT/MN nei giochi;
  5. le 11 MN, con la stessa compatibilità.
"""
import sys, json, re
sys.path.insert(0, '.')
from carica import *
from nuove19 import schede, MOSSE as N19
import nuove45, abil49, aggiunte

m_sp, _ = mappa_specie()
MM = mappa_mosse()
SLUG2IT = {}
for it, s_ in MM.items():
    # il nome del dex (quello che i giocatori hanno già nelle schede) vince sui doppioni
    if s_ not in SLUG2IT or it in ORA['MOVES'] and not ORA['MOVES'][it].get('casa'):
        SLUG2IT[s_] = it
for s_, v in N19.items(): SLUG2IT[s_] = v[0]
for s_, v in nuove45.MOSSE.items(): SLUG2IT[s_] = v[0]

DIE = {'d6': 6, 'd8': 8, 'd10': 10, 'd12': 12, 'd20': 20}

# ---------------- 1. specie ----------------
def mosse_it(lst):
    out = []
    for s_ in lst:
        it = SLUG2IT.get(s_)
        if not it: raise SystemExit('mossa senza nome italiano: ' + s_)
        out.append(it)
    return out

SPECIE = {}
cambi = {}
for n, d in ORA['POKEMON'].items():
    p = m_sp.get(n)
    if not p: continue
    nuovo = {
        'sr': p['sr'], 'ac': p['ac'], 'hp': p['hp'], 'die': DIE[p['hitDice']], 'min': p['minLevel'],
        'attr': {v: p['attributes'][k] for k, v in ATTR.items()},
        'size': SIZE_IT.get(p['size'], d.get('size')),
    }
    if not re.match(r'(Arceus|Silvally) \(', n):
        nuovo['t'] = [TIPO_EN[t] for t in p['type']]
    mv = {'s': mosse_it(p['moves'].get('start', [])), 'l': {}, 'tm': sorted(p['moves'].get('tm', []))}
    for k, v in p['moves'].items():
        if k.startswith('level'): mv['l'][k[5:]] = mosse_it(v)
    diff = {}
    for k, v in nuovo.items():
        if d.get(k) != v:
            diff[k] = v; cambi[k] = cambi.get(k, 0) + 1
    vecchie_l = {str(k): v for k, v in (d['mv'].get('l') or {}).items()}
    if d['mv'].get('s') != mv['s'] or vecchie_l != mv['l'] or sorted(d['mv'].get('tm', [])) != mv['tm']:
        diff['mv'] = mv
        for k, a, b in (('mosse iniziali', d['mv'].get('s'), mv['s']), ('mosse per livello', vecchie_l, mv['l']),
                        ('MT', sorted(d['mv'].get('tm', [])), mv['tm'])):
            if a != b: cambi[k] = cambi.get(k, 0) + 1
    if diff: SPECIE[n] = diff

# ---------------- 2+3. mosse nuove e PP dei giochi ----------------
pp_g = {s_: r['pp'] for s_, r in MOVES_CSV.items()}
pp_srd = {x['id']: x['pp'] for x in SM}
NUOVE = schede(pp_g, pp_srd)
NUOVE.update(nuove45.schede(pp_g, pp_srd))

# ---------------- 2b. specie nuove: gen 9 e forme ufficiali mancanti ----------------
_ab_id = {r['id']: r['identifier'] for r in rcsv('abilities.csv')}
AB_IT = {}
for r in rcsv('ability_names.csv'):
    if r['local_language_id'] == '8': AB_IT[_ab_id.get(r['ability_id'])] = r['name']
AB_IT.update(mappa_abilita())                       # i nomi già usati dal dex vincono
ABIL_NUOVE = {}
for a, (nome, testo) in abil49.ABIL.items():
    AB_IT[a] = nome
    if nome not in ORA['ABIL']: ABIL_NUOVE[nome] = testo
SPECIE_NUOVE, PID_NUOVE, EVO = aggiunte.costruisci(m_sp, SLUG2IT, AB_IT)
# evoluzioni che puntano a un nome che nel dex non esiste (es. Espurr → «Meowstic ♂»):
# le ricolleghiamo alla scheda giusta passando dal nome inglese del SRD
per_nome_srd = {p['name']: n for n, p in m_sp.items()}
for n, d in ORA['POKEMON'].items():
    ev = d.get('ev') or {}
    into = ev.get('into') or []
    if any(x not in ORA['POKEMON'] and x not in SPECIE_NUOVE for x in into):
        giusti = [x if (x in ORA['POKEMON'] or x in SPECIE_NUOVE) else per_nome_srd.get(x, x) for x in into]
        EVO[n] = dict(EVO.get(n, ev), into=giusti)
PP = {}
for it in ORA['MOVES']:
    s_ = MM[it]
    if pp_g.get(s_):
        g = int(pp_g[s_])
        if g != ORA['MOVES'][it].get('pp'): PP[it] = g

# ---------------- 4+5. MT extra e MN dai videogiochi ----------------
items = {r['id']: r['identifier'] for r in rcsv('items.csv')}
vg_gen = {r['id']: int(r['generation_id']) for r in rcsv('version_groups.csv')}
tm_prima = {}   # slug -> (gen, numero) della prima volta che è stata MT
hm_slugs = set()
for r in rcsv('machines.csv'):
    it = items.get(r['item_id'], '')
    s_ = MOVE_BY_ID[r['move_id']]
    if it.startswith('hm'): hm_slugs.add(s_); continue
    if not (it.startswith('tm') or it.startswith('tr')): continue
    k = (vg_gen[r['version_group_id']], int(r['machine_number']))
    if s_ not in tm_prima or k < tm_prima[s_]: tm_prima[s_] = k
p5e_tm = {t['move'] for t in ST}
extra = sorted((s_ for s_ in tm_prima if s_ not in p5e_tm and s_ not in hm_slugs), key=lambda s_: (tm_prima[s_], s_))
TM_EXTRA = {257 + i: SLUG2IT[s_] for i, s_ in enumerate(extra)}
# ordine delle MN: quello storico dei giochi, poi quelle arrivate dopo
MN_ORDINE = ['cut', 'fly', 'surf', 'strength', 'flash', 'rock-smash', 'waterfall', 'dive', 'whirlpool', 'rock-climb', 'defog']
assert set(MN_ORDINE) == hm_slugs, hm_slugs
MN = {i + 1: SLUG2IT[s_] for i, s_ in enumerate(MN_ORDINE)}

# prezzi delle MT: quelli ufficiali del sistema per le 256; per le altre la mediana
# ufficiale delle MT con la stessa classe di danno (le mosse di stato a parte)
import statistics
_SMd = {x['id']: x for x in SM}
def _classe(slug_):
    m = _SMd.get(slug_, {}); c = (m.get('dice') or {}).get('class')
    return c if c and c.isdigit() else 'stato'
_per_classe = {}
for t in ST: _per_classe.setdefault(_classe(t['move']), []).append(t['cost'])
_med = {k: int(round(statistics.median(v) / 100.0) * 100) for k, v in _per_classe.items()}
def _vicina(c):
    if c in _med: return _med[c]
    ks = sorted(int(k) for k in _med if k.isdigit()); x = int(c)
    return _med[str(min(ks, key=lambda k: abs(k - x)))]
TMCOST = {t['id']: t['cost'] for t in ST}
for n, it in TM_EXTRA.items():
    s_ = MM.get(it) or next(k for k, v in list(N19.items()) + list(nuove45.MOSSE.items()) if v[0] == it)
    TMCOST[n] = _vicina(_classe(s_))

# chi può imparare cosa da macchina, in qualunque gioco
pk = rcsv('pokemon.csv')
pk_by_ident = {r['identifier']: r for r in pk}
pk_default = {int(r['species_id']): r for r in pk if r['is_default'] == '1'}
REG = {'Alola': 'alola', 'Galar': 'galar', 'Hisui': 'hisui', 'Paldea': 'paldea'}
def pokeapi_id(n, d):
    p = m_sp.get(n)
    cand = []
    r = re.search(r'^(.*) di (Alola|Galar|Hisui|Paldea)$', n)
    if r: cand.append(slug(r.group(1)) + '-' + REG[r.group(2)])
    if p: cand += [p['id'], p['id'].replace('-form', ''), p['id'].replace('-forme', '')]
    for c in cand:
        if c in pk_by_ident: return pk_by_ident[c]['id']
    if n in PID_NUOVE and PID_NUOVE[n] in pk_by_ident: return pk_by_ident[PID_NUOVE[n]]['id']
    base = pk_default.get(d.get('n'))
    return base['id'] if base else None

interessanti = {int(MOVES_CSV[s_]['id']): s_ for s_ in list(extra) + MN_ORDINE + [t['move'] for t in ST]}
imparano = {}
with open(os.path.join(CSV, 'pokemon_moves.csv'), encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['pokemon_move_method_id'] != '4': continue
        mid = int(r['move_id'])
        if mid in interessanti: imparano.setdefault(r['pokemon_id'], set()).add(interessanti[mid])

num_extra = {s_: n for n, it in TM_EXTRA.items() for s_ in [MM.get(it) or [k for k, v in N19.items() if v[0] == it][0]]}
num_mn = {s_: i + 1 for i, s_ in enumerate(MN_ORDINE)}
num_extra.update({t['move']: t['id'] for t in ST})   # le 256 del sistema: chi le impara nei giochi
COMPAT = {}
senza_id = []
TUTTE = dict(ORA['POKEMON']); TUTTE.update(SPECIE_NUOVE)
for n, d in TUTTE.items():
    pid = pokeapi_id(n, d)
    if not pid: senza_id.append(n); continue
    s = imparano.get(pid, set())
    tm = sorted(num_extra[x] for x in s if x in num_extra)
    mn = sorted(num_mn[x] for x in s if x in num_mn)
    if tm or mn: COMPAT[n] = [tm, mn]

# ---------------- immagini: l'identificativo giusto per le forme ----------------
# Gli sprite di PokeAPI sono per id del Pokémon, non per numero del dex: le forme
# regionali e alternative hanno id 10000+. Lo mettiamo solo se l'immagine esiste.
esistono = set(l.strip() for l in open(os.path.join(S, 'sprite_files.txt')))
def ha(pid, dove):
    return ('sprites/pokemon/%s%s.png' % (dove, pid)) in esistono
IMG = {}
for n, d in TUTTE.items():
    pid = pokeapi_id(n, d)
    if not pid or str(pid) == str(d.get('n')): continue
    if ha(pid, 'other/home/') or ha(pid, '') or ha(pid, 'other/official-artwork/'):
        IMG[n] = int(pid)
out_img = IMG

# ---------------- scrittura ----------------
# le MT di ogni specie, finali (manuale P5e + giochi), come maschera di bit in base64:
# 351 MT = 44 byte a specie invece di centinaia di numeri
import base64
def maschera(nums):
    bits = bytearray((max(TM_EXTRA) + 8) // 8)
    for n in nums: bits[(n - 1) // 8] |= 1 << ((n - 1) % 8)
    return base64.b64encode(bytes(bits)).decode().rstrip('=')
TMB, MNL = {}, {}
for n, d in TUTTE.items():
    if n in SPECIE_NUOVE: base = SPECIE_NUOVE[n]['mv']['tm']
    elif n in SPECIE and 'mv' in SPECIE[n]: base = SPECIE[n]['mv']['tm']
    else: base = d['mv'].get('tm', [])
    tot = set(base) | set(COMPAT.get(n, [[], []])[0])
    TMB[n] = maschera(tot)
    if COMPAT.get(n, [[], []])[1]: MNL[n] = COMPAT[n][1]
for d in list(SPECIE.values()) + list(SPECIE_NUOVE.values()):
    if 'mv' in d: d['mv'].pop('tm', None)
COMPAT = None
out = {'SPECIE': SPECIE, 'NUOVE': NUOVE, 'PP': PP, 'TM': TM_EXTRA, 'MN': MN, 'TMB': TMB, 'MNL': MNL, 'IMG': IMG,
       'SPECIE_NUOVE': SPECIE_NUOVE, 'ABIL': ABIL_NUOVE, 'EVO': EVO, 'TMCOST': TMCOST}
APPLICA = r"""
function dallaMaschera(b64){
  var bin = atob(b64 + '==='.slice((b64.length + 3) % 4)), out = [];
  for(var i = 0; i < bin.length; i++){ var c = bin.charCodeAt(i); for(var k = 0; k < 8; k++) if(c & (1 << k)) out.push(i * 8 + k + 1); }
  return out;
}
window.P5E_2024 = D;
var P = window.P5E;
if(!P || !P.POKEMON || !P.MOVES) return;
/* 1. le 19 mosse ufficiali che mancavano */
for(var n in D.NUOVE) if(!P.MOVES[n] || P.MOVES[n].nodata) P.MOVES[n] = D.NUOVE[n];
/* 2. PP dei videogiochi: quelli del manuale P5e restano in ppP5e */
for(var n in P.MOVES){
  var m = P.MOVES[n];
  if(m.ppP5e == null) m.ppP5e = m.pp;
  if(D.PP[n] != null) m.pp = D.PP[n];
}
/* 3. specie come nel SRD 2024 */
for(var n in D.SPECIE){
  var s = P.POKEMON[n]; if(!s) continue;
  var c = D.SPECIE[n];
  for(var k in c) if(k !== 'mv') s[k] = c[k];
  if(c.mv) s.mv = {s: c.mv.s, l: c.mv.l, tm: s.mv.tm || []};
}
/* 3b. gen 9 e forme ufficiali che mancavano, con le loro abilità; chi evolve in loro lo sa */
P.ABIL = P.ABIL || {};
for(var n in D.ABIL) if(!P.ABIL[n]) P.ABIL[n] = D.ABIL[n];
for(var n in D.SPECIE_NUOVE) if(!P.POKEMON[n]) P.POKEMON[n] = D.SPECIE_NUOVE[n];
for(var n in D.EVO) if(P.POKEMON[n]) P.POKEMON[n].ev = D.EVO[n];
/* 4. MT 257+ dei videogiochi e MN; per tutte le MT, anche chi le impara nei giochi */
P.TM = P.TM || {};
for(var k in D.TM) if(!P.TM[k]) P.TM[k] = D.TM[k];
P.MN = D.MN;
P.TM_COSTO = D.TMCOST;   /* prezzo di ogni MT */
for(var n in D.TMB){
  var s = P.POKEMON[n]; if(!s) continue;
  s.mv.tm = dallaMaschera(D.TMB[n]);
  s.mv.mn = (D.MNL[n] || []).slice();
}
/* 5. l'id dell'immagine giusta per le forme (regionali comprese) */
for(var n in D.IMG) if(P.POKEMON[n]) P.POKEMON[n].pid = D.IMG[n];
P.VERSIONE_DATI = '2024';
"""
js = ("/* Correzione del Pokédex — generato da costruisci.py, non modificare a mano.\n"
      "   Specie e mosse: SRD 2024 di poke5e.app (github.com/Auroratide/poke5e).\n"
      "   PP, MT dei giochi e MN: archivio PokeAPI (github.com/PokeAPI/pokeapi).\n"
      "   Si carica dopo p5e-data.js e p5e-gen8.js e li corregge sul posto. */\n"
      "(function(){\nvar D=" + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ";\n"
      + APPLICA + "})();\n")
open('/home/user/luthia/p5e-2024.js', 'w', encoding='utf-8').write(js)
print('specie corrette:', len(SPECIE), cambi)
print('mosse nuove:', len(NUOVE), '| PP cambiati:', len(PP), '| MT extra:', len(TM_EXTRA), min(TM_EXTRA), '-', max(TM_EXTRA), '| MN:', MN)
print('specie con MT:', len(TMB), '| senza id PokeAPI:', senza_id)
print('forme con immagine propria:', len(IMG), sorted(IMG)[:12])
print('specie nuove:', len(SPECIE_NUOVE), '| abilità nuove:', len(ABIL_NUOVE), '| evoluzioni aggiornate:', sorted(EVO))
print('prezzi MT: Tuono', TMCOST[25], '| Iperraggio', TMCOST[15], '| MT257', TM_EXTRA[257], TMCOST[257], '| fascia', min(TMCOST.values()), '-', max(TMCOST.values()))
print('dimensione:', len(js.encode()) // 1024, 'KB')
