# -*- coding: utf-8 -*-
"""Le 45 mosse ufficiali (SRD 2024 di poke5e.app) che servono alle specie di gen 9
e alle forme aggiunte. Tradotte dal testo inglese; i dadi vengono dalla tabella
delle classi di danno del sistema (src/lib/moves/dice/DiceClass.ts)."""
from nuove19 import CLASSI as _C19

CLASSI = dict(_C19)
CLASSI.update({
 "20": ["1d4", "2d4", "1d12", "4d4"],  "30": ["1d6", "1d10", "2d8", "5d4"],
 "60": ["1d10", "2d8", "5d4", "4d8"],  "110": ["3d6", "3d8", "6d6", "7d8"],
 "130": ["5d4", "3d10", "5d8", "8d8"], "140": ["2d12", "3d10", "7d6", "8d8"],
 "150": ["3d8", "5d6", "4d12", "8d8"], "160": ["4d6", "5d6", "6d8", "6d12"],
 "180": ["3d10", "6d6", "8d6", "7d12"], "200": ["5d6", "4d10", "6d10", "8d12"],
})

def dadi(cl, extra=''):
    t = CLASSI[cl] if isinstance(cl, str) else cl
    mod = '+MOSSA' + extra
    return ({"1": t[0] + mod, "5": t[1] + mod, "10": t[2] + mod, "17": t[3] + mod},
            "Ai livelli superiori: i dadi diventano %s al livello 5, %s al livello 10 e %s al livello 17." % (t[1], t[2], t[3])
            if len(set(t)) > 1 else '')

A, AB, R = '1 azione', '1 azione bonus', '1 reazione'
I, MIN = 'Istantanea', '1 minuto, concentrazione'
VULN = " Se il bersaglio è vulnerabile a questo tipo, i danni aumentano ancora di MOSSA."

# slug: (nome, tipo, time, rng, dur, pow, classe|tiers|None, save, descrizione con {d}, extra_mod)
MOSSE = {
 'astral-barrage': ('Schegge Astrali', 'Spe', A, '18 m', I, ['SAG','CAR'], '120', 'SAG',
   "Scagli una quantità spaventosa di piccoli spettri su un punto entro gittata. Ogni creatura in una sfera di 3 m di raggio centrata lì effettua un TS su SAG contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Spettro se fallisce, la metà se riesce."),
 'behemoth-bash': ('Colpo Maestoso', 'Acc', A, 'Mischia', I, ['COS'], '100', None,
   "Colpisci con il tuo scudo gigantesco. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acciaio. Se il bersaglio era dynamaxizzato, i danni totali raddoppiano."),
 'behemoth-blade': ('Taglio Maestoso', 'Acc', A, 'Mischia', I, ['FOR'], '100', None,
   "Fendi con la tua spada gigantesca. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acciaio. Se il bersaglio era dynamaxizzato, i danni totali raddoppiano."),
 'blood-moon': ('Luna Rossa', 'Nor', A, '9 m', I, ['SAG'], '140', 'DES',
   "Scateni tutta la forza del tuo spirito da una luna piena rossa come il sangue. Una creatura entro gittata effettua un TS su DES contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Normale se fallisce, la metà se riesce. Non puoi usare questa mossa in due turni consecutivi."),
 'burning-bulwark': ('Egida Ignea', 'Fuo', A, 'Se stesso', MIN, ['COS'], ['1d8','2d8','3d8','4d8'], None,
   "La tua pelliccia rovente brucia chi ti tocca. Per la durata le fiamme ti avvolgono, emettendo luce intensa in un raggio di 3 m e luce fioca per altri 3 m. Ogni volta che una creatura ti colpisce con un attacco in mischia, la barriera erutta: l'attaccante subisce {d} + MOSSA danni di tipo Fuoco."),
 'collision-course': ('Turboschianto', 'Lot', A, 'Mischia', I, ['FOR','COS'], '100', 'FOR',
   "Ti schianti al suolo provocando un'esplosione preistorica. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Lotta e il bersaglio effettua un TS su FOR o cade prono." + VULN),
 'doodle': ('Ricalco', 'Nor', A, '9 m', MIN, [], None, None,
   "Catturi in uno schizzo l'essenza stessa del bersaglio. Scegli una creatura entro gittata: tu e ogni alleato entro 1,5 m da te cambiate una delle vostre abilità con un'abilità del bersaglio. Se conosci le sue abilità scegli quale copiare, altrimenti ne ottieni una a caso."),
 'double-shock': ('Doppiolampo', 'Ele', A, 'Mischia', I, ['FOR','DES'], '120', None,
   "Scarichi tutta l'elettricità del tuo corpo in un unico colpo. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Elettro. Perdi il tipo Elettro (se eri solo Elettro diventi senza tipo) a meno che tu non sia teracristallizzato; lo recuperi dopo un riposo breve. Puoi usare questa mossa solo se hai il tipo Elettro."),
 'electro-drift': ('Fulmiscatto', 'Ele', A, 'Mischia', I, ['DES','SAG'], '100', None,
   "Sfrecci a velocità futuristica avvolto dall'elettricità. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Elettro e il bersaglio non può fare attacchi di opportunità contro di te fino alla fine del tuo turno." + VULN),
 'electro-shot': ('Elettroraggio', 'Ele', A, 'Se stesso (linea di 24 m)', '1 round, concentrazione', ['DES','SAG'], '130', 'DES',
   "Assorbi elettricità e ti prepari a scaricarla. Nel tuo turno successivo, se hai mantenuto la concentrazione, con un'azione crei una linea di energia lunga 24 m e larga 1,5 m: ogni creatura nella linea effettua un TS su DES contro la CD della tua Mossa, subendo {d} + MOSSA danni di tipo Elettro se fallisce, la metà se riesce. Sotto la pioggia raddoppi il modificatore MOSSA ai danni e scarichi la mossa subito, senza concentrazione."),
 'fickle-beam': ('Irregolaser', 'Dra', A, '24 m', I, ['DES'], '80', None,
   "Spari un raggio di luce. Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Drago. Questa mossa mette a segno un colpo critico con un 17 naturale o più."),
 'fillet-away': ('Alleggerimento', 'Nor', AB, 'Se stesso', I, [], None, None,
   "Ti alleggerisci di una parte di te per affinare i sensi. Subisci 10 danni senza tipo: il tuo prossimo attacco ha vantaggio e la tua velocità aumenta di 4,5 m fino all'inizio del tuo prossimo turno."),
 'gigaton-hammer': ('Granmartello', 'Acc', A, 'Mischia', I, ['FOR'], '160', None,
   "Fai roteare tutto il corpo e colpisci col tuo enorme martello. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acciaio. Non puoi usare questa mossa in due turni consecutivi."),
 'glacial-lance': ('Lancia Glaciale', 'Ghi', A, '24 m', I, ['FOR','DES'], '120', 'DES',
   "Scagli una lancia di ghiaccio avvolta dalla bufera. Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Ghiaccio. Tutte le altre creature entro 1,5 m dalla linea retta fra te e il bersaglio effettuano un TS su DES contro la CD della tua Mossa, e se falliscono subiscono 2×MOSSA danni di tipo Ghiaccio."),
 'hydro-steam': ('Idrovapore', 'Acq', A, '9 m', I, ['FOR','DES'], '80', None,
   "Investi il bersaglio con acqua bollente. Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Acqua. Sotto il sole intenso i danni non subiscono svantaggio e l'attacco ha vantaggio."),
 'ivy-cudgel': ('Clava di Liane', 'Erb', A, 'Mischia', I, ['FOR','DES'], '100', None,
   "Colpisci con una clava avvolta di edera. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Erba; il critico arriva con 19 o 20. Usata da Ogerpon, il tipo dell'attacco è quello della maschera che indossa: Turchese Erba, Pozzo Acqua, Focolare Fuoco, Fondamenta Roccia."),
 'jet-punch': ('Pugnojet', 'Acq', AB, 'Mischia', I, ['DES'], ['1d4','1d6','1d10','1d12'], None,
   "Raccogli un torrente intorno al pugno e colpisci a velocità accecante. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acqua."),
 'kowtow-cleave': ('Genufendente', 'Bui', A, 'Mischia', I, ['FOR','CAR'], '80', 'CAR',
   "Ti prostri per far abbassare la guardia all'avversario e poi lo colpisci. Il bersaglio effettua un TS su CAR contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Buio se fallisce, la metà se riesce."),
 'last-respects': ('Omaggio ai KO', 'Spe', A, '9 m', I, ['CAR'], ['1d6','1d6','1d6','1d6'], None,
   "Vendichi i tuoi alleati con un attacco potente. Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Spettro, più 2d6 per ogni alleato messo KO in questo scontro, fino a un massimo di 10d6."),
 'lumina-crash': ('Fotocollisione', 'Psi', A, 'Se stesso (cono di 6 m)', I, ['SAG'], '80', 'SAG',
   "Sprigioni una luce singolare che altera la mente. Ogni creatura nel cono effettua un TS su SAG contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Psico se fallisce, la metà se riesce. Chi fallisce ha anche −2 ai TS su SAG fino alla fine del tuo prossimo turno."),
 'make-it-rain': ('Corsa all\'Oro', 'Acc', A, 'Se stesso (cono di 6 m)', I, ['SAG','CAR'], '120', 'DES',
   "Lanci una pioggia di monete. Ogni creatura nel cono effettua un TS su DES contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Acciaio se fallisce, la metà se riesce. Guadagni 1d10 P$ per ogni creatura che fallisce e 2d10 P$ per ognuna che riesce."),
 'malignant-chain': ('Intossicatena', 'Vel', A, '9 m', I, ['DES','CAR'], '100', 'COS',
   "Avvolgi il bersaglio in una catena tossica e corrosiva. Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Veleno e il bersaglio effettua un TS su COS o diventa iper-avvelenato."),
 'matcha-gotcha': ('Spruzzatè', 'Erb', A, 'Se stesso (cono di 6 m)', I, ['DES','CAR'], '80', 'DES',
   "Spruzzi un getto del tè che hai preparato. Le creature nel cono effettuano un TS su DES contro la CD della tua Mossa: subiscono {d} + MOSSA danni di tipo Erba se falliscono, la metà se riescono. Per ogni creatura che fallisce recuperi 1d6 PF."),
 'mighty-cleave': ('Taglio Poderoso', 'Roc', A, 'Mischia', I, ['FOR'], '90', None,
   "Brandisci la luce accumulata sulla tua testa per fendere il bersaglio. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Roccia. Il colpo va a segno anche attraverso mosse e abilità che lo annullerebbero, come Protezione o Agodifesa."),
 'mortal-spin': ('Glitturbine', 'Vel', A, 'Mischia', I, ['FOR','DES'], '30', 'DES',
   "Ruoti su te stesso a velocità incredibile. Tutte le creature a portata di mischia effettuano un TS su DES contro la CD della tua Mossa: subiscono {d} + MOSSA danni di tipo Veleno se falliscono, la metà se riescono, e chi fallisce è anche avvelenato. Prima del tiro ti liberi da Parassiseme e da qualunque cosa ti stia afferrando o trattenendo."),
 'order-up': ('Alta Cucina', 'Dra', A, '4,5 m', I, ['FOR'], '80', None,
   "Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Drago. Se hai un Tatsugiri in bocca, c'è un effetto in più secondo la sua forma: Arcuata (arancione) — danni extra pari al tuo modificatore di FOR; Cascante (rosa) — +3 alla CA fino all'inizio del tuo prossimo turno; Distesa (gialla) — vantaggio ai TS su DES fino all'inizio del tuo prossimo turno."),
 'population-bomb': ('Infestazione', 'Nor', A, 'Mischia', I, ['DES'], ['1','1','1','1'], None,
   "I tuoi simili accorrono in massa per un attacco combinato. Effettua 10 tiri per colpire in mischia contro un bersaglio: ogni colpo a segno infligge {d} + MOSSA danni di tipo Normale."),
 'psyblade': ('Psicolama', 'Psi', A, 'Mischia', I, ['FOR','SAG'], '80', None,
   "Squarci il bersaglio con una lama eterea. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Psico. Su un Campo Elettrico l'attacco ha vantaggio."),
 'revival-blessing': ('Preghiera Vitale', 'Nor', A, 'Mischia', I, [], None, None,
   "Doni una benedizione amorevole a un Pokémon esausto a portata: recupera metà dei suoi punti ferita."),
 'rising-voltage': ('Elettroimpennata', 'Ele', A, '18 m', I, ['DES','SAG'], '70', 'DES',
   "Attacchi con una tensione elettrica che sale dal terreno. Il bersaglio effettua un TS su DES contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Elettro se fallisce, la metà se riesce. Se sei su un Campo Elettrico, diventano bersagli anche tutte le altre creature sullo stesso campo entro 18 m da te."),
 'ruination': ('Catastrofe', 'Bui', A, '18 m', I, ['CAR'], None, 'COS',
   "Evochi un disastro rovinoso su una creatura che vedi entro gittata. Il bersaglio effettua un TS su COS contro la CD della tua Mossa: se fallisce perde metà dei suoi PF attuali, e i suoi PF massimi si riducono della stessa quantità."),
 'salt-cure': ('Sotto Sale', 'Roc', A, '9 m', I, ['FOR'], '40', 'DES',
   "Metti il bersaglio sotto sale, danneggiandolo nel tempo. Il bersaglio effettua un TS su DES contro la CD della tua Mossa: se fallisce subisce {d} + MOSSA danni di tipo Roccia, e 1d6 danni di tipo Roccia all'inizio di ogni suo turno finché non torna nella Poké Ball o non viene curato. I Pokémon di tipo Acqua e Acciaio sono vulnerabili a questi danni."),
 'shed-tail': ('Tagliacoda', 'Nor', R, 'Se stesso', I, [], None, None,
   "Quando vieni colpito da un attacco, puoi usare la reazione per subire 2d6 danni senza tipo e annullare danni ed effetti dell'attacco. Se lo fai, esci dalla lotta con un'azione gratuita."),
 'silk-trap': ('Telatrappola', 'Col', R, 'Se stesso', I, ['DES'], None, 'DES',
   "Tessi una trappola di seta per l'avversario. Quando una mossa in mischia ti colpirebbe con danni o effetti, li eviti automaticamente; l'attaccante effettua un TS su DES contro la CD della tua Mossa e se fallisce è trattenuto fino alla fine del suo prossimo turno. Non funziona contro un 20 naturale."),
 'spicy-extract': ('Essenza Piccante', 'Erb', A, 'Se stesso (raggio di 6 m)', '1 minuto', ['SAG','CAR'], None, 'CAR',
   "Emetti un estratto piccantissimo. Tutte le creature entro 6 m effettuano un TS su CAR contro la CD della tua Mossa: per la durata, chi fallisce attacca con vantaggio e viene attaccato con vantaggio."),
 'spin-out': ('Slittaruote', 'Acc', A, 'Mischia', I, ['DES'], '100', None,
   "Giri vorticosamente sforzando le gambe. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acciaio. Fino all'inizio del tuo prossimo turno hai svantaggio ai TS su DES e la tua velocità è dimezzata."),
 'steel-roller': ('Ferrorullo', 'Acc', A, 'Se stesso', I, ['DES'], '130', 'DES',
   "Attacchi distruggendo il terreno. Puoi usarla solo se c'è un campo attivo (Elettrico, Psichico…). Usi 9 m del tuo movimento: ogni creatura che ti si trova entro 1,5 m durante il percorso effettua un TS su DES contro la CD della tua Mossa, subendo {d} + MOSSA danni di tipo Acciaio se fallisce, la metà se riesce. Il campo attivo viene cancellato."),
 'syrup-bomb': ('Bomba Sciroppata', 'Erb', A, '18 m', '3 round', ['DES'], '60', 'DES',
   "Fai esplodere sciroppo appiccicoso in un punto entro gittata. Ogni creatura entro 1,5 m da quel punto effettua un TS su DES contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Erba se fallisce, la metà se riesce, e se fallisce cade prona. Per la durata lo sciroppo copre il terreno entro 1,5 m dal punto: chi vi entra o vi termina il turno ripete il TS o cade prono."),
 'tachyon-cutter': ('Tachiontaglio', 'Acc', A, '9 m', I, ['DES'], '20', None,
   "Lanci due lame di particelle una dopo l'altra. Colpiscono entrambe in automatico, ognuna per {d} + MOSSA danni di tipo Acciaio, a meno che il bersaglio non sia nella fase invulnerabile di Volo, Fossa, Rimbalzo, Sub o simili."),
 'tera-starstorm': ('Teracluster', 'Nor', A, '72 m', I, ['FOR','CAR'], '140', 'DES',
   "Con il potere dei tuoi cristalli bombardi il bersaglio. Scegli un punto che vedi entro gittata: ogni creatura in una sfera di 6 m di raggio effettua un TS su DES contro la CD della tua Mossa, subendo {d} + MOSSA danni di tipo Astrale se fallisce, la metà se riesce. Solo Terapagos può usarla; nella Forma Astrale sceglie quattro punti invece di uno (chi sta in più sfere è colpito una volta sola). I Pokémon teracristallizzati sono vulnerabili ai danni Astrali, tutti gli altri li subiscono normali."),
 'terrain-pulse': ('Campopulsar', 'Nor', A, 'Varia', I, ['SAG','CAR'], '50', 'SAG',
   "Usi l'energia del campo per attaccare. Se sei sotto l'effetto di un campo speciale puoi bersagliare qualsiasi numero di creature sullo stesso campo, fino a 36 m: ognuna effettua un TS su SAG contro la CD della tua Mossa e subisce {d} + MOSSA danni se fallisce, la metà se riesce. Il tipo dei danni è quello del campo: nessun campo Normale, Elettrico Elettro, Erboso Erba, Nebbioso Folletto, Psichico Psico. Senza campo, la gittata è Se stesso (raggio di 9 m)."),
 'thunderclap': ('Saetta', 'Ele', R, '36 m', I, ['DES'], '40', None,
   "Come reazione a un attacco a distanza di una creatura che vedi entro gittata, colpisci per primo con una scossa. Effettua un tiro per colpire a distanza contro l'attaccante: se colpisci, infliggi {d} + MOSSA danni di tipo Elettro. Il tuo tiro avviene prima del suo."),
 'tidy-up': ('Pulizie', 'Nor', A, 'Se stesso', '1 minuto', ['DES','CAR'], None, 'COS',
   "Fai di tutto per tenere pulito. Fino alla fine del tuo prossimo turno il tuo prossimo tiro per colpire ha vantaggio. Le creature a tua scelta entro 24 m sotto l'effetto di Sostituto effettuano un TS su COS contro la CD della tua Mossa: se falliscono, Sostituto finisce. Per il minuto successivo, quando una creatura che vedi entro 24 m usa Punte, Levitoroccia, Rete Vischiosa, Fielepunte o Sostituto, puoi usare la reazione per farle fare lo stesso TS: se fallisce la mossa svanisce senza effetto (i PP sono spesi comunque). L'effetto su di te resta anche se vieni richiamato."),
 'triple-dive': ('Triplo Tuffo', 'Acq', A, 'Mischia', I, ['FOR','DES'], '30', None,
   "Esegui un triplo tuffo perfettamente sincronizzato. Effettua tre tiri per colpire in mischia contro un bersaglio: ogni colpo a segno infligge {d} + MOSSA danni di tipo Acqua."),
 'wicked-blow': ('Pugnotenebra', 'Bui', A, 'Mischia', I, ['FOR'], '70', None,
   "Colpisci il bersaglio con un unico colpo feroce. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA + 10 danni di tipo Buio.", '+10'),
}

def schede(pp_giochi, pp_srd):
    out = {}
    for s_, v in MOSSE.items():
        nome, t, time, rng, dur, pw, cl, save, desc = v[:9]
        extra = v[9] if len(v) > 9 else ''
        m = {'t': t, 'pp': int(pp_giochi.get(s_) or pp_srd[s_]), 'ppP5e': int(pp_srd[s_]), 'time': time,
             'rng': rng, 'dur': dur, 'pow': pw, 'srd': True}
        if cl is not None:
            dmg, sc = dadi(cl, extra)
            m['dmg'] = dmg
            if sc: m['sc'] = sc
            m['desc'] = desc.replace('{d}', dmg['1'].replace('+MOSSA' + extra, ''))
        else:
            m['desc'] = desc
        if save: m['save'] = save
        out[nome] = m
    return out
