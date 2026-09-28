# -*- coding: utf-8 -*-
"""Aggiunge a p5e-fuori.js le 19 mosse nuove, riusando il testo di mosse simili."""
import json, re, sys
from collections import Counter
sys.path.insert(0, '.')
from carica import ORA
from nuove19 import MOSSE
F = '/home/user/luthia/p5e-fuori.js'
s = open(F, encoding='utf-8').read()
T = json.loads(s[s.index('var T=') + 6: s.index(';\nvar M=')])
i0 = s.index('var M=') + 6; i1 = s.index(';\n', i0)
M = json.loads(s[i0:i1])

def variante(rng):
    if re.search(r'raggio|cono|linea|cubo', rng): return 2
    if rng in ('Mischia', 'Se stesso', ''): return 0
    return 1
# a mano: quelle che non sono un attacco del proprio tipo
A_MANO = {'Dracofonia': 'Cuordileone', 'Baldimpulso': 'Calmamente', 'Invocaluna': 'Desiderio'}
TEMPESTE = {'Tempesta Boreale', 'Tempesta Ardente', 'Tempesta Tonante'}
for slug, (nome, t, time, rng, *_ ) in MOSSE.items():
    if nome in M: continue
    if nome in A_MANO: M[nome] = M[A_MANO[nome]]; continue
    v = 2 if nome in TEMPESTE else variante(rng)
    simili = Counter(M[n] for n, m in ORA['MOVES'].items()
                     if n in M and m.get('t') == t and variante(m.get('rng', '')) == v and m.get('dmg'))
    M[nome] = simili.most_common(1)[0][0]
    print(f'{nome:18} ← {T[M[nome]][:70]}…')
s = s[:i0] + json.dumps(M, ensure_ascii=False, sort_keys=True) + s[i1:]
open(F, 'w', encoding='utf-8').write(s)
