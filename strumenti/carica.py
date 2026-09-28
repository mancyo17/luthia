# -*- coding: utf-8 -*-
"""Carica le tre fonti: dati attuali dell'app, SRD 2024 di poke5e.app, CSV di PokeAPI."""
import json, csv, os, unicodedata, re
S = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(S, 'src/pokeapi/data/v2/csv')
SRD = os.path.join(S, 'src/poke5e/src/lib/srd/data/2024')

def rcsv(n):
    with open(os.path.join(CSV, n), encoding='utf-8') as f:
        return list(csv.DictReader(f))

def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]', '', s)

ORA = json.load(open(os.path.join(S, 'ora.json'), encoding='utf-8'))
SP = json.load(open(os.path.join(SRD, 'pokemon/en.json'), encoding='utf-8'))['values']
SM = json.load(open(os.path.join(SRD, 'moves/en.json'), encoding='utf-8'))['values']
ST = json.load(open(os.path.join(SRD, 'tms/en.json'), encoding='utf-8'))['values']

MOVES_CSV = {r['identifier']: r for r in rcsv('moves.csv')}
MOVE_BY_ID = {r['id']: r['identifier'] for r in rcsv('moves.csv')}
NOMI = {}
for r in rcsv('move_names.csv'):
    if r['local_language_id'] in ('8', '9'):
        NOMI.setdefault(MOVE_BY_ID.get(r['move_id']), {})['it' if r['local_language_id']=='8' else 'en'] = r['name']

# ---- dex P5e inglese (Jerakin) da cui il nostro è stato tradotto ----
JER = {}
_jd = os.path.join(S, 'src/jerakin/data/pokemon')
for fn in os.listdir(_jd):
    JER[fn[:-5]] = json.load(open(os.path.join(_jd, fn), encoding='utf-8'))

def slug(en):
    return re.sub(r'-+', '-', re.sub(r"[^a-z0-9]+", '-', unicodedata.normalize('NFKD', en).encode('ascii','ignore').decode().lower().replace("'", ''))).strip('-')

def rosetta():
    """Italiano -> inglese per le mosse, allineando le liste delle stesse specie."""
    from collections import Counter, defaultdict
    voti = defaultdict(Counter)
    for nome, j in JER.items():
        o = ORA['POKEMON'].get(nome)
        if not o: continue
        a = o['mv'].get('s', []); b = j['Moves'].get('Starting Moves', [])
        if len(a) == len(b):
            for x, y in zip(a, b): voti[x][y] += 1
        for lv, lst in (j['Moves'].get('Level') or {}).items():
            oa = (o['mv'].get('l') or {}).get(lv) or (o['mv'].get('l') or {}).get(int(lv)) or []
            if len(oa) == len(lst):
                for x, y in zip(oa, lst): voti[x][y] += 1
    return {it: c.most_common(1)[0][0] for it, c in voti.items()}, voti

def mappa_mosse():
    """nome italiano dell'app -> slug inglese (id delle mosse di poke5e.app e PokeAPI)."""
    R, _ = rosetta()
    m = {it: slug(en) for it, en in R.items()}
    # stesso numero di MT = stessa mossa
    tm24 = {t['id']: t['move'] for t in ST}
    for n, it in ORA['TM'].items():
        if int(n) in tm24: m.setdefault(it, tm24[int(n)])
    # nome italiano ufficiale (PokeAPI) o nome rimasto in inglese
    it2slug, en2slug = {}, {}
    for s_, n in NOMI.items():
        if not s_: continue
        if n.get('it'): it2slug.setdefault(norm(n['it']), s_)
        if n.get('en'): en2slug.setdefault(norm(n['en']), s_)
    for it in ORA['MOVES']:
        if it in m: continue
        k = norm(it)
        if k in it2slug: m[it] = it2slug[k]
        elif k in en2slug: m[it] = en2slug[k]
    return m

# le mosse di gen 8/9 che avevo nominato io, verificate sul file di gen 8
# (stessa specie, stessa posizione nella lista) e sul tipo
A_MANO = {
 'Acidomela':'apple-acid', 'Alapsichica':'esper-wing', 'Artigliofatale':'dire-claw',
 'Ascia di Pietra':'stone-axe', 'Ascialcio':'axe-kick', 'Blocco Netto':'obstruct',
 'Calcio Tuonante':'thunderous-kick', 'Cannonalmax':'dynamax-cannon', 'Cavallone':'wave-crash',
 'Clororaggio':'chloroblast', 'Coistinto':'entrainment', 'Corteo Infernale':'infernal-parade',
 'Dardidrago':'dragon-darts', 'Elettromagnete':'magnetic-flux', 'Falsa Resa':'false-surrender',
 'Fossa Iperspaziale':'hyperspace-hole', 'Furia Cieca':'raging-fury', 'Gelidomalanimo':'bitter-malice',
 'Gravimela':'grav-apple', 'Iceberg Vagante':'mountain-gale', 'Lamainfinita':'ceaseless-edge',
 'Manimano':'hold-hands', 'Nessunoscampo':'no-retreat', 'Piovralock':'octolock',
 'Raffica Aculei':'barb-barrage', 'Ramoccolpo':'branch-poke', 'Rugiadavita':'life-dew',
 'Ruotaurea':'aura-wheel', 'Scudo Corazza':'shelter', 'Tempesta Amorosa':'springtide-storm',
 'Triplofreccia':'triple-arrows', 'Urtoiperspazio':'hyperspace-fury', 'Vaporstrano':'strange-steam',
 'Vocearcana':'eerie-spell',
}
_mm = mappa_mosse
def mappa_mosse():
    m = _mm()
    for k, v in A_MANO.items(): m.setdefault(k, v)
    return m

TIPO_EN = {'normal':'Nor','fighting':'Lot','flying':'Vol','poison':'Vel','ground':'Ter','rock':'Roc','bug':'Col',
  'ghost':'Spe','steel':'Acc','fire':'Fuo','water':'Acq','grass':'Erb','electric':'Ele','psychic':'Psi',
  'ice':'Ghi','dragon':'Dra','dark':'Bui','fairy':'Fol'}
ATTR = {'str':'FOR','dex':'DES','con':'COS','int':'INT','wis':'SAG','cha':'CAR'}

def mappa_specie():
    """nome dell'app -> scheda SRD 2024. Prima il nome, poi numero + tipi + statistiche."""
    by_name = {p['name']: p for p in SP}
    by_num = {}
    for p in SP: by_num.setdefault(p['number'], []).append(p)
    out, dubbi = {}, []
    usati = set()
    for n, d in ORA['POKEMON'].items():
        if n in by_name: out[n] = by_name[n]; usati.add(by_name[n]['id'])
    for n, d in ORA['POKEMON'].items():
        if n in out: continue
        cand = [p for p in by_num.get(d.get('n'), []) if p['id'] not in usati]
        def punti(p):
            s = 0
            if sorted(TIPO_EN[t] for t in p['type']) == sorted(d.get('t', [])): s += 100
            reg = re.search(r' di (Alola|Galar|Hisui|Paldea)\b', n)
            if reg and reg.group(1).lower() in p['id']: s += 60
            if not reg and re.search(r'alola|galar|hisui|paldea', p['id']): s -= 60
            s -= abs(p['hp'] - d.get('hp', 0)) + 3 * abs(p['ac'] - d.get('ac', 0))
            s -= sum(abs(p['attributes'][k] - d.get('attr', {}).get(v, 0)) for k, v in ATTR.items())
            return s
        cand.sort(key=punti, reverse=True)
        if cand:
            out[n] = cand[0]; usati.add(cand[0]['id'])
            if len(cand) > 1 and punti(cand[0]) - punti(cand[1]) < 15: dubbi.append((n, cand[0]['name'], cand[1]['name']))
    return out, dubbi

FORZATE = {
 'Lycanroc Forma Giorno':'Lycanroc Midday Form', 'Lycanroc Forma Crepuscolo':'Lycanroc Dusk Form',
 'Lycanroc Forma Notte':'Lycanroc Midnight Form', 'Meowstic-m':'Meowstic ♂', 'Meowstic-f':'Meowstic ♀',
}
_ms = mappa_specie
def mappa_specie():
    m, dubbi = _ms()
    by_name = {p['name']: p for p in SP}
    for a, b in FORZATE.items(): m[a] = by_name[b]
    # le forme di tipo di Arceus e Silvally hanno le statistiche della forma base
    for n in ORA['POKEMON']:
        if re.match(r'(Arceus|Silvally) \(', n): m[n] = by_name[n.split(' (')[0]]
    return m, dubbi

TS_IT = {'str':'Forza','dex':'Destrezza','con':'Costituzione','int':'Intelligenza','wis':'Saggezza','cha':'Carisma'}
SK_IT = {'survival':'Sopravvivenza','sleight-of-hand':'Rapidità di Mano','insight':'Intuizione','acrobatics':'Acrobazia',
 'athletics':'Atletica','intimidation':'Intimidire','perception':'Percezione','nature':'Natura','arcana':'Arcano',
 'medicine':'Medicina','stealth':'Furtività','deception':'Inganno','persuasion':'Persuasione','performance':'Intrattenere',
 'history':'Storia','investigation':'Indagare','religion':'Religione','animal-handling':'Addestrare Animali','all':'Tutte'}
SIZE_IT = {'tiny':'Minuscolo','small':'Piccolo','medium':'Medio','large':'Grande','huge':'Enorme','gargantuan':'Mastodontico'}
SPD_IT = {'walking':'','swimming':'nuoto','flying':'volo','climbing':'scalata','burrowing':'scavo','hover':'volo (fluttua)'}

def mappa_abilita():
    """slug inglese -> nome italiano dell'app, dalle stesse specie in inglese e in italiano."""
    from collections import defaultdict, Counter
    v = defaultdict(Counter)
    for n, j in JER.items():
        o = ORA['POKEMON'].get(n)
        if not o: continue
        if len(o.get('ab', [])) == len(j.get('Abilities', [])):
            for x, y in zip(o['ab'], j['Abilities']): v[slug(y)][x] += 1
        if o.get('hab') and j.get('Hidden Ability'): v[slug(j['Hidden Ability'])][o['hab']] += 1
    return {k: c.most_common(1)[0][0] for k, c in v.items()}
