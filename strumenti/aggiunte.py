# -*- coding: utf-8 -*-
"""Specie nuove dal SRD 2024 di poke5e.app: la nona generazione e le forme ufficiali
che il dex non aveva. Le creature inventate dal sito (numero 0) restano fuori."""
import json, os, re
from carica import SP, SRD, TIPO_EN, ATTR, TS_IT, SK_IT, SIZE_IT, ORA, slug, rcsv

# nomi italiani delle forme (le specie base di gen 9 si chiamano come in inglese)
NOMI_FORME = {
 'kyogre-primal': 'Kyogre Archeo', 'groudon-primal': 'Groudon Archeo',
 'dialga-origin': 'Dialga Forma Origine', 'palkia-origin': 'Palkia Forma Origine',
 'basculin-blue-striped': 'Basculin Linea Blu', 'basculin-white-striped': 'Basculin Linea Bianca',
 'tornadus-therian': 'Tornadus Forma Totem', 'thundurus-therian': 'Thundurus Forma Totem',
 'landorus-therian': 'Landorus Forma Totem', 'enamorus-therian': 'Enamorus Forma Totem',
 'floette-eternal': 'Floette Fiore Eterno', 'indeedee-m': 'Indeedee ♂', 'basculegion-f': 'Basculegion ♀',
 'zacian-crowned': 'Zacian Re delle Spade', 'zamazenta-crowned': 'Zamazenta Re degli Scudi',
 'eternatus-eternamax': 'Eternatus Dynamax Infinito', 'urshifu-single': 'Urshifu Stile Singolo',
 'calyrex-ice': 'Calyrex Cavaliere Glaciale', 'calyrex-shadow': 'Calyrex Cavaliere Spettrale',
 'ursaluna-bloodmoon': 'Ursaluna Luna Cremisi',
 'tauros-paldea-combat-breed': 'Tauros di Paldea (Razza Combattiva)',
 'tauros-paldea-blaze-breed': 'Tauros di Paldea (Razza Infuocata)',
 'tauros-paldea-aqua-breed': 'Tauros di Paldea (Razza Acquatica)', 'wooper-paldea': 'Wooper di Paldea',
 'gimmighoul': 'Gimmighoul (Forma Scrigno)', 'gimmighoul-roaming': 'Gimmighoul (Forma Ambulante)',
 'ogerpon': 'Ogerpon (Maschera Turchese)', 'ogerpon-wellspring-mask': 'Ogerpon (Maschera Pozzo)',
 'ogerpon-heartflame-mask': 'Ogerpon (Maschera Focolare)', 'ogerpon-cornerstone-mask': 'Ogerpon (Maschera Fondamenta)',
 'terapagos-terastal-form': 'Terapagos (Forma Teracristal)', 'terapagos-stellar-form': 'Terapagos (Forma Astrale)',
}
# identificativi PokéAPI dove il sito ne usa uno diverso (immagini e compatibilità dai giochi)
POKEAPI = {
 'indeedee-m': 'indeedee-male', 'urshifu-single': 'urshifu-single-strike', 'basculegion-f': 'basculegion-female',
 'maushold': 'maushold-family-of-four', 'squawkabilly': 'squawkabilly-green-plumage', 'palafin': 'palafin-zero',
 'tatsugiri': 'tatsugiri-curly', 'dudunsparce': 'dudunsparce-two-segment',
 'ogerpon-heartflame-mask': 'ogerpon-hearthflame-mask', 'terapagos-terastal-form': 'terapagos-terastal',
 'terapagos-stellar-form': 'terapagos-stellar',
}
SENSI = {'darkvision': 'Vista al Buio', 'truesight': 'Vista Pura', 'tremorsense': 'Percezione Tellurica', 'blindsight': 'Vista Cieca'}
VEL = {'walking': '', 'swimming': 'nuoto', 'flying': 'volo', 'climbing': 'scalata', 'burrowing': 'scavo', 'hover': 'librarsi'}
DIE = {'d6': 6, 'd8': 8, 'd10': 10, 'd12': 12, 'd20': 20}

def metri(ft):
    m = round(ft * 0.3, 1)
    return (str(int(m)) if m == int(m) else str(m).replace('.', ',')) + ' m'

def velocita(lst):
    a = [x for x in lst if x['type'] == 'walking']
    b = [x for x in lst if x['type'] != 'walking']
    pezzi = [metri(x['value']) for x in a] + [VEL[x['type']] + ' ' + metri(x['value']) for x in b]
    return ', '.join(pezzi) or '0 m'

def nome_it(p):
    return NOMI_FORME.get(p['id'], p['name'])

def costruisci(m_sp, slug2it, ab_it):
    """-> (specie nuove {nome: scheda}, mappa id SRD -> nome per tutte le specie, id pokeapi per le nuove)"""
    usati = {p['id'] for p in m_sp.values()}
    nuove = [p for p in SP if p['id'] not in usati and p['number'] > 0]
    nome_di = {p['id']: n for n, p in m_sp.items()}
    for p in nuove: nome_di[p['id']] = nome_it(p)
    # evoluzioni: grafo completo del SRD, per stadio e totale
    E = json.load(open(os.path.join(SRD, 'evolutions/en.json'), encoding='utf-8'))['values']
    da = {}
    for e in E: da.setdefault(e['from'], []).append(e)
    padre = {e['to']: e['from'] for e in E}
    def stadio(i):
        s = 1
        while i in padre: i = padre[i]; s += 1
        return s
    def profondita(i):
        return 1 + max([profondita(e['to']) for e in da.get(i, [])] or [0])
    def radice(i):
        while i in padre: i = padre[i]
        return i
    def ev(i):
        figli = [e for e in da.get(i, []) if e['to'] in nome_di]
        lv = next((c['value'] for e in figli for c in e['conditions'] if c['type'] == 'level'), 0)
        pts = next((x['value'] for e in figli for x in e.get('effects', []) if x['type'] == 'asi'), 0)
        return {'into': [nome_di[e['to']] for e in figli], 'lv': lv, 'pts': pts,
                'st': stadio(i), 'tot': profondita(radice(i)) + 0}
    out, pid = {}, {}
    for p in nuove:
        n = nome_it(p)
        d = {
          'n': p['number'], 't': [TIPO_EN[t] for t in p['type']], 'sr': p['sr'], 'ac': p['ac'], 'hp': p['hp'],
          'die': DIE[p['hitDice']], 'min': p['minLevel'],
          'attr': {v: p['attributes'][k] for k, v in ATTR.items()},
          'ts': [TS_IT[x] for x in p['savingThrows']],
          'sk': [SK_IT.get(x.replace(' ', '-'), x) for x in p['skills']],
          'spd': velocita(p['speed']), 'size': SIZE_IT[p['size']],
          'ab': [ab_it[a['id']] for a in p['abilities'] if not a['hidden']],
          'hab': next((ab_it[a['id']] for a in p['abilities'] if a['hidden']), ''),
          'mv': {'s': [slug2it[x] for x in p['moves'].get('start', [])],
                 'l': {k[5:]: [slug2it[x] for x in v] for k, v in p['moves'].items() if k.startswith('level')},
                 'tm': sorted(p['moves'].get('tm', []))},
          'ev': ev(p['id']), 'srd': True,
        }
        if p['senses']:
            d['sen'] = ', '.join(SENSI[s['type']] + ' ' + metri(s['value']) for s in p['senses'])
        out[n] = d
        pid[n] = POKEAPI.get(p['id'], p['id'])
    # le specie che c'erano già ma che ora evolvono in una specie nuova
    evo_vecchie = {}
    for n, p in m_sp.items():
        e = ev(p['id'])
        vecchie = (ORA['POKEMON'][n].get('ev') or {}).get('into') or []
        nuovi = [x for x in e['into'] if x not in vecchie and x in out]
        if nuovi:
            base = dict(ORA['POKEMON'][n].get('ev') or e)
            base['into'] = vecchie + nuovi
            if not base.get('lv'): base['lv'] = e['lv']
            if not base.get('pts'): base['pts'] = e['pts']
            base['tot'] = max(base.get('tot', 1), e['tot'])
            evo_vecchie[n] = base
    return out, pid, evo_vecchie
