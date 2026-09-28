# -*- coding: utf-8 -*-
"""Le 19 mosse ufficiali (SRD 2024 di poke5e.app) che il nostro dex non aveva.
Tradotte dal testo inglese; i dadi vengono dalla tabella ufficiale delle classi
di danno (src/lib/moves/dice/DiceClass.ts), fasce ai livelli 1/5/10/17."""

CLASSI = {
 "10": ["1d4", "1d6", "1d8", "2d6"],  "40": ["1d6", "1d12", "2d8", "4d6"],
 "50": ["1d8", "2d6", "4d4", "3d10"], "70": ["1d12", "2d8", "2d12", "6d6"],
 "80": ["2d6", "2d8", "4d6", "6d6"],  "90": ["2d8", "2d10", "3d10", "4d12"],
 "100": ["4d4", "2d12", "4d8", "8d6"], "120": ["2d10", "3d8", "4d10", "7d8"],
}

def dadi(cl):
    t = CLASSI[cl] if isinstance(cl, str) else cl
    return ({"1": t[0] + "+MOSSA", "5": t[1] + "+MOSSA", "10": t[2] + "+MOSSA", "17": t[3] + "+MOSSA"},
            "Ai livelli superiori: i dadi diventano %s al livello 5, %s al livello 10 e %s al livello 17." % (t[1], t[2], t[3]))

TEMPESTA = (" Una creatura effettua il TS anche quando entra nell'area o vi termina il turno, "
            "ma non più di una volta per turno. Se piove, le creature tirano con svantaggio.")

# slug: (nome, tipo, time, rng, dur, pow, classe o tiers o None, save, descrizione con {d} per i dadi)
MOSSE = {
 'aqua-cutter': ('Idrotaglio', 'Acq', '1 azione', 'Mischia', 'Istantanea', ['FOR', 'DES'], '70', None,
   "Espelli acqua ad alta pressione e tagli il bersaglio come con una lama. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acqua. Questo attacco mette a segno un colpo critico con un 19 o un 20 naturale."),
 'aqua-step': ('Idroballetto', 'Acq', '1 azione', 'Mischia', 'Istantanea', ['FOR', 'CAR'], '80', None,
   "Ti lanci sul bersaglio con passi di danza fluidi. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Acqua. Alla fine del tuo turno, che tu abbia colpito o no, la tua velocità di movimento aumenta di 3 m fino alla fine del tuo prossimo turno."),
 'armor-cannon': ('Corazza Cannone', 'Fuo', '1 azione', '18 m', 'Istantanea', ['FOR', 'COS'], '120', None,
   "Spari la tua stessa corazza come una raffica di proiettili infuocati. Effettua un tiro per colpire a distanza contro un bersaglio entro gittata: se colpisci, infliggi {d} + MOSSA danni di tipo Fuoco. Fino alla fine del tuo prossimo turno tutti gli attacchi contro di te hanno vantaggio, e tu hai svantaggio a tutti i TS su COS."),
 'bitter-blade': ('Lama del Rimorso', 'Fuo', '1 azione', 'Mischia', 'Istantanea', ['FOR', 'DES'], '90', None,
   "Concentri in un fendente tutto il rancore che provi verso il mondo dei vivi. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Fuoco e recuperi punti ferita pari alla metà dei danni inflitti."),
 'bleakwind-storm': ('Tempesta Boreale', 'Vol', '1 azione', '30 m', '1 minuto, concentrazione', ['DES'], '100', 'COS',
   "Scateni una tempesta di venti gelidi e feroci, che fanno tremare corpo e spirito, in un cubo di 12 m di lato centrato su un punto entro gittata. Ogni creatura nemica nell'area effettua un TS su COS contro la CD della tua Mossa: se fallisce subisce {d} + MOSSA danni di tipo Volante, la metà se riesce. Per le creature nemiche l'area è terreno difficile." + TEMPESTA),
 'clangorous-soul': ('Dracofonia', 'Dra', '1 azione', 'Se stesso', 'Istantanea', ['CAR'], None, None,
   "Batti fra loro le mani squamose per rafforzarti. Subisci 3d6 danni senza tipo e in cambio ottieni +1 ai tiri per colpire, +1 alla CA e +1 ai tiri per i danni per il resto dello scontro o finché non vieni richiamato. L'effetto si cumula fino a cinque volte, per un bonus massimo di +5 ciascuno."),
 'comeuppance': ('Ritorsione', 'Bui', '1 reazione', 'Mischia', 'Istantanea', ['FOR', 'DES'], '10', None,
   "Quando vieni colpito da un attacco in mischia, puoi usare la reazione per effettuare un attacco in mischia contro la creatura che ti ha colpito: se colpisci, infliggi {d} + MOSSA danni di tipo Buio."),
 'flower-trick': ('Prestigiafiore', 'Erb', '1 azione', '9 m', 'Istantanea', ['DES', 'CAR'], '70', 'DES',
   "Lanci al bersaglio un mazzo di fiori truccato. Il bersaglio effettua un TS su DES contro la CD della tua Mossa: subisce {d} + MOSSA danni di tipo Erba, la metà se riesce. Ai fini di altri effetti, questo attacco conta come un colpo critico."),
 'glaive-rush': ('Spadoncarica', 'Dra', '1 azione', 'Mischia', 'Istantanea', ['FOR'], '120', None,
   "Ti lanci in una carica sconsiderata con tutto il corpo. Effettua un tiro per colpire in mischia con vantaggio: se colpisci, infliggi {d} + MOSSA danni di tipo Drago. Fino all'inizio del tuo prossimo turno i tiri per colpire contro di te hanno vantaggio."),
 'hyper-drill': ('Ipertrapano', 'Nor', '1 azione', 'Mischia', 'Istantanea', ['FOR', 'DES'], '100', None,
   "Ti schianti su una creatura roteando su te stesso come un trapano. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni di tipo Normale. L'attacco trapassa le mosse difensive come Protezione o Individua e ignora i bonus alla CA dati da effetti come Scudo."),
 'lunar-blessing': ('Invocaluna', 'Psi', '1 azione', 'Se stesso', '1 minuto, concentrazione', ['CAR'], ['2d4', '1d12', '2d8', '4d6'], None,
   "Benedici l'area intorno a te con la luce di una falce di luna. Per la durata, quando una creatura alleata (tu compreso) inizia il turno entro 30 m da te, recupera {d} + MOSSA punti ferita ed è curata da ogni stato alterato."),
 'mystical-power': ('Forza Mistica', 'Psi', '1 azione', '18 m', 'Istantanea', ['INT', 'SAG', 'CAR'], '70', None,
   "Attacchi emanando un potere mistico. Effettua un tiro per colpire a distanza: se colpisci, infliggi {d} + MOSSA danni di tipo Psico e ottieni +1 a tutti i tiri per colpire che usano INT, SAG o CAR come potenza, fino alla fine dello scontro o finché non vieni richiamato. Se manchi, ottieni invece +1 alla CA per lo stesso tempo. La somma di questi bonus non supera +5."),
 'rage-fist': ('Pugno Furibondo', 'Spe', '1 azione', 'Mischia', 'Istantanea', ['FOR'], '50', None,
   "Trasformi la rabbia in energia per attaccare. Effettua un tiro per colpire in mischia contro una creatura a portata: se colpisci, infliggi {d} + MOSSA danni di tipo Spettro, più 1 danno aggiuntivo per ogni 10 PF che ti mancano rispetto al massimo."),
 'raging-bull': ('Scatenatoro', 'Nor', '1 azione', 'Mischia', 'Istantanea', ['FOR'], '90', None,
   "Carichi come un toro infuriato. Effettua un tiro per colpire in mischia: se colpisci, infliggi {d} + MOSSA danni. Questa mossa ignora gli effetti che ne ridurrebbero i danni, come Rafforzatore o Riflesso. Il tipo dei danni dipende dalla razza di chi la usa."),
 'sandsear-storm': ('Tempesta Ardente', 'Ter', '1 azione', '30 m', '1 minuto, concentrazione', ['FOR'], '100', 'FOR',
   "Scateni una tempesta di venti feroci e sabbia rovente in un cubo di 12 m di lato centrato su un punto entro gittata. Ogni creatura nemica nell'area effettua un TS su FOR contro la CD della tua Mossa: se fallisce subisce {d} + MOSSA danni di tipo Terra ed è scottata; se riesce subisce la metà e non viene scottata." + TEMPESTA),
 'take-heart': ('Baldimpulso', 'Psi', '1 reazione', 'Se stesso', 'Istantanea', [], None, None,
   "Come reazione quando subisci uno stato alterato o diventi spaventato, ti liberi di quella condizione e fino alla fine del tuo prossimo turno sei immune agli stati alterati e alla paura. Inoltre, fino alla fine del tuo prossimo turno, hai vantaggio ai tiri per colpire che usano SAG o CAR come potenza e a tutti i TS su SAG e CAR."),
 'torch-song': ('Canzone Ardente', 'Fuo', '1 azione', 'Se stesso (raggio di 6 m)', 'Istantanea', ['COS', 'CAR'], '80', 'CAR',
   "Soffi fiamme furiose mentre intoni un canto. Scegli un numero qualsiasi di creature entro 6 m da te: ciascuna effettua un TS su CAR contro la CD della tua Mossa e subisce {d} + MOSSA danni di tipo Fuoco se fallisce, la metà se riesce. La CD di questa mossa aumenta di 1 per ogni turno consecutivo in cui la usi, fino a un massimo di +5, e torna normale dopo un turno in cui non la usi."),
 'twin-beam': ('Doppioraggio', 'Psi', '1 azione', '9 m', 'Istantanea', ['INT', 'SAG'], '40', None,
   "Spari dagli occhi due raggi mistici. Effettua due tiri per colpire a distanza contro un bersaglio: ogni colpo a segno infligge {d} + MOSSA danni di tipo Psico."),
 'wildbolt-storm': ('Tempesta Tonante', 'Ele', '1 azione', '30 m', '1 minuto, concentrazione', ['SAG'], '100', 'DES',
   "Scateni una tempesta fragorosa di fulmini e vento in un cubo di 12 m di lato centrato su un punto entro gittata. Ogni creatura nemica nell'area effettua un TS su DES contro la CD della tua Mossa: se fallisce subisce {d} + MOSSA danni di tipo Elettro ed è paralizzata; se riesce subisce la metà e non viene paralizzata." + TEMPESTA),
}

def schede(pp_giochi, pp_srd):
    out = {}
    for s_, (nome, t, time, rng, dur, pw, cl, save, desc) in MOSSE.items():
        m = {'t': t, 'pp': int(pp_giochi[s_]), 'ppP5e': int(pp_srd[s_]), 'time': time, 'rng': rng, 'dur': dur,
             'pow': pw, 'srd': True}
        if cl is not None:
            dmg, sc = dadi(cl)
            m['dmg'] = dmg; m['sc'] = sc
            m['desc'] = desc.replace('{d}', dmg['1'].replace('+MOSSA', ''))
        else:
            m['desc'] = desc
        if save: m['save'] = save
        out[nome] = m
    return out
