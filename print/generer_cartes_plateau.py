# -*- coding: utf-8 -*-
"""
ROYAUME — matériel imprimable : planches de cartes (recto + verso) et plateau A3.
Sortie : cartes-royaume.pdf, plateau-royaume.pdf
Cartes au format poker 63 x 88 mm, 9 par page A4, traits de coupe.
"""
import os
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- polices ----------------
FONTS = r'C:\Windows\Fonts'
def reg(name, file):
    p = os.path.join(FONTS, file)
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont(name, p)); return True
    return False

HAS_G  = reg('Serif', 'georgia.ttf')
HAS_GB = reg('Serif-Bold', 'georgiab.ttf')
HAS_GI = reg('Serif-Italic', 'georgiai.ttf')
HAS_SY = reg('Sym', 'seguisym.ttf')
F  = 'Serif' if HAS_G else 'Times-Roman'
FB = 'Serif-Bold' if HAS_GB else 'Times-Bold'
FI = 'Serif-Italic' if HAS_GI else 'Times-Italic'
SY = 'Sym' if HAS_SY else FB

# ---------------- palette ----------------
PARCH  = HexColor('#f3e9d2')   # parchemin
PARCH2 = HexColor('#e9dcbc')
INK    = HexColor('#2b2118')   # encre brune
GOLD   = HexColor('#b8860b')
CATS = {
    'vote':     ('VOTE',      HexColor('#3f6fae')),
    'argent':   ('ÉCUS',      HexColor('#b8860b')),
    'nuit':     ('NUIT',      HexColor('#6b5b95')),
    'passif':   ('PASSIF',    HexColor('#3e8e6b')),
    'coup':     ('RÉVOLTE',   HexColor('#a63a3a')),
    'event':    ('ÉVÉNEMENT', HexColor('#8a5a2b')),
    'ambition': ('AMBITION',  HexColor('#5b3a6b')),
    'charge':   ('CHARGE',    HexColor('#7a1f1f')),
    'lieu':     ('LIEU',      HexColor('#4a6b3a')),
    'aide':     ('AIDE DE JEU', HexColor('#555555')),
}
PLAYER_COLORS = ['#e0b34e','#d95f5f','#5f8fd9','#8b7fd9','#4eb98f','#d98b44','#d977a5']

# ---------------- données ----------------
ACTIONS = [  # (nom, cat, icône, description) — chaque carte en 3 exemplaires
    ('Faux sceaux','vote','✉','+2 voix lors d’un vote de la taille.'),
    ('Soutien du Pape','vote','☦','+3 voix. Rome veille sur ses intérêts.'),
    ('Guildes achetées','vote','⚒','+2 voix. Les corporations votent bien.'),
    ('Bénédiction de l’Évêque','vote','☦','+2 voix. Dieu est avec vous (moyennant don).'),
    ('Libelle infamant','vote','✉','Le Roi perd 2 voix sur ce vote.'),
    ('Lettre compromettante','vote','✉','Forcez un baron à voter comme vous.'),
    ('Cousinage','vote','♛','+2 voix. La famille, c’est sacré.'),
    ('Pot-de-vin','argent','⚜','+2 écus dans votre poche, immédiatement.'),
    ('Péage sauvage','argent','⚜','+3 écus dans votre poche. Le marché « participe ».'),
    ('Détournement de la taille','argent','⚜','Prenez 2 écus de la poche du Roi.'),
    ('Courrier templier','argent','✉','La nuit : déposez votre poche au coffre depuis n’importe quelle planque.'),
    ('Coffre scellé','argent','⛓','PASSIF — si vous êtes tué, votre poche n’est pas pillée.'),
    ('Or des Lombards','argent','⚜','+4 écus dans votre poche. Un banquier de Florence vous veut du bien.'),
    ('Chantage','argent','⚜','Le baron le plus riche (poche) vous verse 2 écus.'),
    ('Spadassin','nuit','⚔','Attaque de nuit : désignez une cible et devinez sa planque.'),
    ('Baril de poudre','nuit','☠','Attaque : tue et DÉTRUIT toute la poche de la cible. Très mal vu.'),
    ('Empoisonneuse','nuit','⚗','Attaque : ignore les gardes du corps, mais échoue sur 1-3 (1d6).'),
    ('Espion à la cour','nuit','♞','Attaque : pas besoin de deviner, la planque de la cible est connue (sauf Monastère).'),
    ('Coffret piégé','nuit','☠','Attaque : ne fonctionne que si la cible dort à son Manoir.'),
    ('Embuscade aux Templiers','nuit','⚔','Attaque : ne touche que si la cible va chez les Templiers.'),
    ('Garde du corps','passif','⚕','Annule automatiquement la prochaine attaque contre vous (sauf poison). Défaussez-la ensuite.'),
    ('Sosie','passif','♟','Lors d’une attaque réussie : survivez sur 4-6 (1d6). Défaussez-la ensuite.'),
    ('Sauf-conduit','passif','✉','Échappez au billot (une fois). Défaussez-la ensuite.'),
    ('Routiers','coup','⚔','+3 unités à déployer pendant une révolte.'),
    ('Foule en colère','coup','⚔','+2 unités à déployer pendant une révolte.'),
    ('Garnison retournée','coup','⚔','+3 unités : une garnison change de camp.'),
    ('Or des Anglais','coup','⚜','+4 unités… mais tous sauront qui vous paie (rancunes durables).'),
    ('Barricades','coup','⚔','+2 unités. Le peuple des faubourgs vous couvre.'),
    ('Sabotage des arsenaux','coup','⚒','+2 unités : les armes ennemies s’enrayent mystérieusement.'),
]
EVENTS = [
    ('Famine','La taille du prochain tour est réduite de 3 écus.'),
    ('Crédit lombard','Les banquiers font crédit : +4 écus de taille au prochain tour.'),
    ('Jacquerie','Le climat est insurrectionnel : une révolte devient possible ce tour.'),
    ('Les sergents du Roi','Tout baron qui a dormi à son Manoir cette nuit perd 1 écu de poche.'),
    ('Grande foire','Le peuple oublie tout : aucune révolte possible ce tour.'),
    ('Légat du Pape','Chaque baron avec plus de 6 écus en poche en donne 2 à l’Église.'),
    ('Tribut d’un vassal','Le Roi reçoit 2 écus en poche. Personne ne pose de questions.'),
    ('Brigands','La nuit prochaine, la commanderie des Templiers est fermée (aucun dépôt).'),
    ('Grand tournoi','Chaque baron mise 1 écu de poche (s’il peut). Lancez 1d6 chacun : le plus haut rafle la bourse.'),
    ('Mariage princier','Les deux barons aux plus petits coffres reçoivent 1 écu de dot chacun.'),
    ('Peste','Chaque baron défausse une carte de sa main, au hasard.'),
    ('Comète','Mauvais présage : au prochain vote, le Roi ne compte aucune voix bonus de cartes.'),
    ('Fausse monnaie','Tout baron avec 5 écus ou plus en poche en perd 1 (rogné).'),
    ('Pèlerinage','La nuit prochaine, dormir au Monastère rapporte +1 écu.'),
    ('Moisson généreuse','Chaque baron vivant reçoit 1 écu en poche.'),
    ('Inquisition','Le baron à la plus grosse poche (montrez vos écus !) donne 1 écu à l’Église.'),
    ('Troubadours','Le baron au plus petit total (poche + coffre) reçoit 1 écu de la quête.'),
    ('Brume épaisse','La nuit prochaine, chaque attaque échoue sur 1-3 (1d6), avant toute autre résolution.'),
]
AMBITIONS = [
    ('Le Régicide',4,'Un Roi meurt de votre main (attaque de nuit réussie contre le Roi).'),
    ('La Main sanglante',4,'Réussissez au moins 2 assassinats dans la partie.'),
    ('L’Éminence grise',3,'Ne soyez jamais Roi de toute la partie, et soyez vivant à la fin.'),
    ('Le Croisé',3,'Votre camp tient la Cathédrale à la fin d’une révolte.'),
    ('Le Loyal',3,'Traversez au moins une révolte sans jamais rejoindre les félons.'),
    ('Le Grand Félon',3,'Gagnez une révolte dans le camp des félons.'),
    ('L’Usurpateur',3,'Finissez la partie sur le trône sans l’avoir commencé.'),
    ('L’Insaisissable',3,'Qu’aucune attaque ne soit jamais dirigée contre vous de toute la partie.'),
    ('L’Increvable',2,'Ne mourez jamais, pas même une fois.'),
    ('Le Courtisan',2,'Passez au moins 3 nuits chez la Favorite.'),
    ('Le Pénitent',2,'Passez au moins 2 nuits au Monastère.'),
    ('Le Templier',2,'Finissez avec 0 écu en poche et au moins 6 écus au coffre.'),
]
CHARGES = [
    ('Le Roi','♛','3 unités','Répartit la taille royale (le non-alloué file dans sa poche). Toujours royal pendant une révolte. Garde la couronne.'),
    ('Le Connétable','⚔','4 unités','Le ban royal : la plus grosse armée du royaume. Le plus gradé pour le trône.'),
    ('Maître des Engins','⚒','2 unités','Une fois par révolte : le TRÉBUCHET frappe n’importe quel site occupé par l’ennemi et détruit jusqu’à 2 unités.'),
    ('Maître des Assassins','☠','2 unités','Chaque nuit : une attaque gratuite (comme un Spadassin), sans carte.'),
    ('Le Chancelier','✉','1 unité','+1 voix à chaque vote. Pioche 1 carte de plus à chaque fin de tour.'),
    ('L’Amiral de France','⚓','2 unités','(6+ joueurs) Une fois par révolte : la NEF DE GUERRE frappe n’importe quel site ennemi et détruit jusqu’à 2 unités.'),
    ('Capitaine des Routiers','⚔','3 unités','(7 joueurs) Une compagnie de soudards, fidèle au plus offrant.'),
]
LIEUX = [
    ('Manoir','⌂','Confort du logis : piochez 1 carte de plus en fin de tour. Mais tout le monde connaît l’adresse.'),
    ('Templiers','⚜','Déposez toute votre poche au coffre (imprenable). Très prévisible : les tueurs adorent.'),
    ('La Favorite','☾','Discret. Ses relations vous glissent +1 écu au petit matin.'),
    ('Monastère','☦','Droit d’asile : intouchable cette nuit. Ni dépôt, ni bonus.'),
]
AIDE_TXT = [
    ('TOUR DE JEU', ['1. TAILLE — le Roi lance 2d6+4 en secret et propose une répartition.',
                     '2. VOTE — cartes vote, puis pouces levés/baissés simultanés. Rejet : la taille est perdue et sur 4-6 (1d6) la révolte gronde.',
                     '3. NUIT — chacun pose une carte Planque face cachée ; les attaquants posent cible + Filature. Révélation, résolution.',
                     '4. HÉRAUT — révélez 1 carte Événement.',
                     '5. RÉVOLTE — si elle gronde : camps, déploiement, 3 manches, batailles aux dés.']),
    ('POUVOIRS DES SITES (manches 2-3)', ['Garnison : +1 unité de renfort.',
                     'Cathédrale : 1 unité ennemie déserte.',
                     'Trésor : 1 unité contre 2 écus de poche.',
                     'Port : embarquement vers tout site.',
                     'Château : vaut 2 points (majorité à 4/6).']),
]

# ---------------- utilitaires dessin ----------------
CW, CH = 63*mm, 88*mm
COLS, ROWS = 3, 3
PAGE_W, PAGE_H = A4
GRID_W, GRID_H = COLS*CW, ROWS*CH
OX, OY = (PAGE_W-GRID_W)/2, (PAGE_H-GRID_H)/2

def wrap(c, text, font, size, maxw):
    words, lines, cur = text.split(' '), [], ''
    for w in words:
        t = (cur+' '+w).strip()
        if c.stringWidth(t, font, size) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_card(c, x, y, cat, name, icon, desc, corner='', edge=None, big_bonus=None):
    label, col = CATS[cat]
    # fond parchemin + cadre
    c.setFillColor(PARCH); c.setStrokeColor(INK); c.setLineWidth(1.2)
    c.roundRect(x+1.5*mm, y+1.5*mm, CW-3*mm, CH-3*mm, 3*mm, stroke=1, fill=1)
    if edge:  # liseré couleur joueur (cartes Lieu)
        c.setStrokeColor(HexColor(edge)); c.setLineWidth(2.2)
        c.roundRect(x+2.6*mm, y+2.6*mm, CW-5.2*mm, CH-5.2*mm, 2.4*mm, stroke=1, fill=0)
    # bandeau de catégorie
    c.setFillColor(col)
    c.roundRect(x+4*mm, y+CH-12*mm, CW-8*mm, 7*mm, 2*mm, stroke=0, fill=1)
    c.setFillColor(HexColor('#f8f2e2')); c.setFont(FB, 8)
    c.drawCentredString(x+CW/2, y+CH-9.6*mm, label)
    # nom (réduit si trop long)
    size = 10.5
    while c.stringWidth(name, FB, size) > CW-10*mm and size > 6.5: size -= 0.5
    c.setFillColor(INK); c.setFont(FB, size)
    c.drawCentredString(x+CW/2, y+CH-19*mm, name)
    # icône
    c.setFillColor(col); c.setFont(SY, 26)
    c.drawCentredString(x+CW/2, y+CH-33*mm, icon)
    # filet
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(x+10*mm, y+CH-38*mm, x+CW-10*mm, y+CH-38*mm)
    # description
    c.setFillColor(INK); c.setFont(F, 8)
    lines = wrap(c, desc, F, 8, CW-12*mm)
    ty = y+CH-44*mm
    for ln in lines[:8]:
        c.drawCentredString(x+CW/2, ty, ln); ty -= 3.8*mm
    # bonus (ambitions)
    if big_bonus:
        c.setFillColor(HexColor('#5b3a6b')); c.setFont(FB, 13)
        c.drawCentredString(x+CW/2, y+8*mm, '+'+str(big_bonus)+' écus au coffre')
    # coin (numéro d'exemplaire / joueur)
    if corner:
        c.setFillColor(HexColor('#8a7a5a')); c.setFont(F, 6)
        c.drawString(x+4.5*mm, y+4*mm, corner)

def cut_marks(c):
    c.setStrokeColor(HexColor('#999999')); c.setLineWidth(0.3)
    for i in range(COLS+1):
        x = OX+i*CW
        c.line(x, OY-4*mm, x, OY); c.line(x, OY+GRID_H, x, OY+GRID_H+4*mm)
    for j in range(ROWS+1):
        y = OY+j*CH
        c.line(OX-4*mm, y, OX, y); c.line(OX+GRID_W, y, OX+GRID_W+4*mm, y)

def draw_back(c, x, y, deck, col):
    c.setFillColor(HexColor('#241b12')); c.setStrokeColor(GOLD); c.setLineWidth(1.2)
    c.roundRect(x+1.5*mm, y+1.5*mm, CW-3*mm, CH-3*mm, 3*mm, stroke=1, fill=1)
    c.setStrokeColor(col); c.setLineWidth(1)
    c.roundRect(x+4*mm, y+4*mm, CW-8*mm, CH-8*mm, 2.5*mm, stroke=1, fill=0)
    c.setFillColor(GOLD); c.setFont(SY, 34)
    c.drawCentredString(x+CW/2, y+CH/2+2*mm, '⚜')
    c.setFont(FB, 11); c.drawCentredString(x+CW/2, y+CH/2-9*mm, 'ROYAUME')
    c.setFillColor(col); c.setFont(FB, 7.5)
    c.drawCentredString(x+CW/2, y+9*mm, deck)

def cards_pdf():
    path = os.path.join(HERE, 'cartes-royaume.pdf')
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle('ROYAUME — planches de cartes')

    def emit(deck_label, deck_col, cards):
        """cards = liste de fonctions de dessin ; pages recto puis verso par page (duplex bord long)."""
        for start in range(0, len(cards), COLS*ROWS):
            batch = cards[start:start+COLS*ROWS]
            # recto
            for k, fn in enumerate(batch):
                col_i, row_i = k % COLS, k // COLS
                x = OX + col_i*CW
                y = OY + (ROWS-1-row_i)*CH
                fn(c, x, y)
            cut_marks(c)
            c.setFillColor(HexColor('#888888')); c.setFont(F, 7)
            c.drawCentredString(PAGE_W/2, 6*mm, 'ROYAUME — planche recto (' + deck_label + ') — impression recto/verso bord long')
            c.showPage()
            # verso (miroir horizontal des positions pour tomber en face au duplex)
            for k in range(len(batch)):
                col_i, row_i = k % COLS, k // COLS
                mx = COLS-1-col_i
                x = OX + mx*CW
                y = OY + (ROWS-1-row_i)*CH
                draw_back(c, x, y, deck_label, deck_col)
            cut_marks(c)
            c.setFillColor(HexColor('#888888')); c.setFont(F, 7)
            c.drawCentredString(PAGE_W/2, 6*mm, 'ROYAUME — planche verso (' + deck_label + ')')
            c.showPage()

    # ---- 87 cartes Action (29 x 3) ----
    fns = []
    for (name, cat, icon, desc) in ACTIONS:
        for n in range(3):
            fns.append(lambda c,x,y,name=name,cat=cat,icon=icon,desc=desc,n=n:
                draw_card(c, x, y, cat, name, icon, desc, corner=str(n+1)+'/3'))
    emit('ACTION', GOLD, fns)

    # ---- 18 Événements ----
    fns = [lambda c,x,y,n=n,d=d: draw_card(c, x, y, 'event', n, '⚕', d) for (n,d) in EVENTS]
    fns = []
    for (n, d) in EVENTS:
        fns.append(lambda c,x,y,n=n,d=d: draw_card(c, x, y, 'event', n, '⚠', d))
    emit('ÉVÉNEMENT', CATS['event'][1], fns)

    # ---- 12 Ambitions ----
    fns = []
    for (n, b, d) in AMBITIONS:
        fns.append(lambda c,x,y,n=n,b=b,d=d: draw_card(c, x, y, 'ambition', n, '♛', d, big_bonus=b))
    emit('AMBITION', CATS['ambition'][1], fns)

    # ---- 7 Charges ----
    fns = []
    for (n, ic, u, d) in CHARGES:
        fns.append(lambda c,x,y,n=n,ic=ic,u=u,d=d: draw_card(c, x, y, 'charge', n, ic, u+' — '+d))
    emit('CHARGE', CATS['charge'][1], fns)

    # ---- 56 cartes Lieu : par joueur, 4 Planque + 4 Filature ----
    fns = []
    for pi, pc in enumerate(PLAYER_COLORS):
        for (n, ic, d) in LIEUX:
            fns.append(lambda c,x,y,n=n,ic=ic,d=d,pc=pc,pi=pi:
                draw_card(c, x, y, 'lieu', n, ic, d, corner='PLANQUE — joueur '+str(pi+1), edge=pc))
        for (n, ic, d) in LIEUX:
            fns.append(lambda c,x,y,n=n,ic=ic,pc=pc,pi=pi:
                draw_card(c, x, y, 'lieu', n, ic, 'FILATURE : posez cette carte face cachée sur votre cible pour deviner sa planque.',
                          corner='FILATURE — joueur '+str(pi+1), edge=pc))
    emit('LIEU', CATS['lieu'][1], fns)

    # ---- 7 Aides de jeu ----
    def draw_aide(c, x, y):
        label, col = CATS['aide']
        c.setFillColor(PARCH); c.setStrokeColor(INK); c.setLineWidth(1.2)
        c.roundRect(x+1.5*mm, y+1.5*mm, CW-3*mm, CH-3*mm, 3*mm, stroke=1, fill=1)
        ty = y+CH-8*mm
        for (title, lines) in AIDE_TXT:
            c.setFillColor(HexColor('#7a1f1f')); c.setFont(FB, 7)
            c.drawString(x+4*mm, ty, title); ty -= 3.4*mm
            c.setFillColor(INK); c.setFont(F, 5.6)
            for ln in lines:
                for sub in wrap(c, ln, F, 5.6, CW-9*mm):
                    c.drawString(x+4.5*mm, ty, sub); ty -= 2.6*mm
                ty -= 0.4*mm
            ty -= 1.6*mm
    emit('AIDE DE JEU', CATS['aide'][1], [draw_aide]*7)

    c.save()
    print('OK', path)

# ---------------- plateau A3 ----------------
def plateau_pdf():
    path = os.path.join(HERE, 'plateau-royaume.pdf')
    W, H = landscape(A3)
    c = canvas.Canvas(path, pagesize=landscape(A3))
    c.setTitle('ROYAUME — plateau')
    # mer
    c.setFillColor(HexColor('#2a6ea0')); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(HexColor('#35799e'))
    for i in range(40):
        import math, random
        random.seed(i*7)
        c.circle(random.uniform(0,W), random.uniform(0,H), 2.2*mm, stroke=0, fill=1)
    # île (décagone)
    import math
    cx, cy, R = W*0.42, H*0.52, H*0.40
    pts = [(cx+R*1.18*math.cos(a), cy+R*0.95*math.sin(a)) for a in [math.pi*2*i/10+0.31 for i in range(10)]]
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close()
    c.setFillColor(HexColor('#d9c98f')); c.setStrokeColor(HexColor('#b9a97e')); c.setLineWidth(3)
    c.drawPath(p, stroke=1, fill=1)
    pts2 = [(cx+(R*1.18-9*mm)*math.cos(a), cy+(R*0.95-9*mm)*math.sin(a)) for a in [math.pi*2*i/10+0.31 for i in range(10)]]
    p2 = c.beginPath(); p2.moveTo(*pts2[0])
    for q in pts2[1:]: p2.lineTo(*q)
    p2.close()
    c.setFillColor(HexColor('#7ba05b')); c.drawPath(p2, stroke=0, fill=1)

    # sites (fractions reprises du jeu vidéo)
    S = {
        'chateau':   (0.50, 0.50, 'CHÂTEAU ROYAL', '♛', 'Vaut 2 points — interdit au déploiement félon', '#7a1f1f'),
        'cathedrale':(0.26, 0.72, 'CATHÉDRALE', '☦', 'Manches 2-3 : 1 unité ennemie déserte', '#5b3a6b'),
        'tresor':    (0.74, 0.72, 'TRÉSOR ROYAL', '⚜', 'Manches 2-3 : 1 unité contre 2 écus', '#b8860b'),
        'garnison':  (0.26, 0.28, 'GARNISON', '⚔', 'Manches 2-3 : +1 renfort', '#3e6b3e'),
        'port':      (0.74, 0.28, 'PORT', '⚓', 'Manches 2-3 : embarquement vers tout site', '#3f6fae'),
    }
    def sp(k):
        fx, fy, *_ = S[k]
        return (cx + (fx-0.5)*R*2.05, cy + (fy-0.5)*R*1.62)
    # routes (adjacences)
    c.setStrokeColor(HexColor('#a98c5f')); c.setLineWidth(7); c.setLineCap(1)
    adj = [('chateau','cathedrale'),('chateau','tresor'),('chateau','garnison'),('chateau','port'),
           ('cathedrale','tresor'),('cathedrale','garnison'),('tresor','port'),('garnison','port')]
    for a,b in adj:
        (x1,y1),(x2,y2) = sp(a), sp(b)
        c.line(x1,y1,x2,y2)
    # cercles de sites
    for k,(fx,fy,nm,ic,pw,col) in S.items():
        x,y = sp(k)
        rr = 33*mm if k=='chateau' else 27*mm
        c.setFillColor(HexColor('#efe4c8')); c.setStrokeColor(HexColor(col)); c.setLineWidth(2.6)
        c.circle(x, y, rr, stroke=1, fill=1)
        c.setFillColor(HexColor(col)); c.setFont(SY, 24); c.drawCentredString(x, y+rr-14*mm, ic)
        c.setFont(FB, 12.5); c.drawCentredString(x, y+rr-21*mm, nm)
        c.setFillColor(INK); c.setFont(F, 8)
        for i, ln in enumerate(wrap(c, pw, F, 8, rr*1.8)):
            c.drawCentredString(x, y+rr-27*mm-i*3.6*mm, ln)
        c.setFillColor(HexColor('#8a7a5a')); c.setFont(FI if HAS_GI else F, 7)
        c.drawCentredString(x, y-rr+5*mm, 'zone des unités')

    # bandeau titre
    c.setFillColor(HexColor('#241b12')); c.roundRect(W-118*mm, H-30*mm, 110*mm, 22*mm, 4*mm, stroke=0, fill=1)
    c.setFillColor(GOLD); c.setFont(SY, 16); c.drawString(W-113*mm, H-22*mm, '⚜')
    c.setFont(FB, 20); c.drawString(W-104*mm, H-22*mm, 'R O Y A U M E')
    c.setFillColor(HexColor('#c9b78a')); c.setFont(FI if HAS_GI else F, 9)
    c.drawString(W-104*mm, H-27.5*mm, 'Couronne, trahisons & révoltes')

    # piste des tours
    c.setFillColor(HexColor('#241b12')); c.roundRect(W-118*mm, H-72*mm, 110*mm, 34*mm, 4*mm, stroke=0, fill=1)
    c.setFillColor(HexColor('#c9b78a')); c.setFont(FB, 9); c.drawString(W-113*mm, H-46*mm, 'PISTE DES TOURS — 8 levées de la taille')
    for i in range(8):
        x = W-113*mm + i*13*mm
        c.setFillColor(PARCH); c.setStrokeColor(GOLD); c.setLineWidth(1)
        c.roundRect(x, H-66*mm, 11*mm, 14*mm, 2*mm, stroke=1, fill=1)
        c.setFillColor(INK); c.setFont(FB, 10); c.drawCentredString(x+5.5*mm, H-61*mm, str(i+1))

    # zones de pioche
    for (label, yoff) in [('PIOCHE ACTION', 82), ('DÉFAUSSE', 82+50)]:
        pass
    zones = [('PIOCHE ACTION', W-118*mm, H-125*mm), ('DÉFAUSSE', W-88*mm, H-125*mm), ('ÉVÉNEMENTS', W-58*mm, H-125*mm)]
    for (label, zx, zy) in zones:
        c.setFillColor(HexColor('#00000055')) if False else None
        c.setStrokeColor(HexColor('#f3e9d2')); c.setLineWidth(1.4); c.setDash(4,3)
        c.roundRect(zx, zy, 26*mm, 37*mm, 3*mm, stroke=1, fill=0)
        c.setDash()
        c.setFillColor(HexColor('#f3e9d2')); c.setFont(FB, 7)
        c.drawCentredString(zx+13*mm, zy-4*mm, label)

    # légende bataille
    c.setFillColor(HexColor('#241b12')); c.roundRect(W-118*mm, 12*mm, 110*mm, 42*mm, 4*mm, stroke=0, fill=1)
    c.setFillColor(GOLD); c.setFont(FB, 10); c.drawString(W-113*mm, 46*mm, 'BATAILLE (site contesté)')
    c.setFillColor(HexColor('#e8dcc0')); c.setFont(F, 8.5)
    for i, ln in enumerate(['Chaque camp : unités présentes + 1d6 (félons d’abord).',
                            'Égalité : le défenseur tient. Perdant : moitié des unités',
                            'détruites (arrondi sup.), survivants en retraite adjacente.',
                            'Vainqueur : un quart de pertes (arrondi inf.).',
                            'Décompte final : majorité à 4 points sur 6 pour les félons.']):
        c.drawString(W-113*mm, 40*mm-i*5.2*mm, ln)

    c.save()
    print('OK', path)

# ---------------- jetons (écus, unités, traces d'ambition…) ----------------
def tokens_pdf():
    """Chaque événement public laisse une TRACE : le jeton se prend devant tout le
    monde au moment où il se produit. À la révélation des ambitions, les jetons
    posés devant soi font preuve — pas besoin de maître du jeu."""
    path = os.path.join(HERE, 'jetons-royaume.pdf')
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle('ROYAUME — jetons à découper')
    D = 17*mm            # diamètre jeton
    GAP = 2.5*mm
    per_row = int((PAGE_W-24*mm)//(D+GAP))
    x0, y0 = 14*mm, PAGE_H-26*mm
    state = {'i': 0, 'page_titled': False}

    def title_page():
        c.setFillColor(INK); c.setFont(FB, 13)
        c.drawString(14*mm, PAGE_H-14*mm, 'ROYAUME — planche de jetons (à coller sur carton avant découpe)')
        c.setFillColor(HexColor('#666666')); c.setFont(F, 8)
        c.drawString(14*mm, PAGE_H-19*mm, 'Jetons de TRACE : à prendre publiquement au moment de l’événement — ils prouvent vos ambitions au décompte.')

    def next_pos():
        i = state['i']
        col_i, row_i = i % per_row, i // per_row
        y = y0 - row_i*(D+GAP) - D
        if y < 14*mm:
            c.showPage(); state['i'] = 0; state['page_titled'] = False
            return next_pos()
        if not state['page_titled']:
            title_page(); state['page_titled'] = True
        state['i'] += 1
        return (x0 + col_i*(D+GAP), y)

    def circle_token(fill, ring, glyph, gfont, gsize, gcolor, sub=''):
        x, y = next_pos()
        cxx, cyy = x+D/2, y+D/2
        c.setFillColor(fill); c.setStrokeColor(ring); c.setLineWidth(1.3)
        c.circle(cxx, cyy, D/2, stroke=1, fill=1)
        c.setFillColor(gcolor); c.setFont(gfont, gsize)
        c.drawCentredString(cxx, cyy - gsize*0.36, glyph)
        if sub:
            c.setFont(FB, 4.6); c.drawCentredString(cxx, y+1.6*mm, sub)

    def square_token(fill):
        x, y = next_pos()
        c.setFillColor(fill); c.setStrokeColor(INK); c.setLineWidth(1)
        c.rect(x+1.5*mm, y+1.5*mm, D-3*mm, D-3*mm, stroke=1, fill=1)

    dark = HexColor('#241b12')
    # écus
    for _ in range(40): circle_token(HexColor('#e8c25a'), HexColor('#8a6a1a'), '1', FB, 10, dark, 'ÉCU')
    for _ in range(12): circle_token(HexColor('#c9962b'), HexColor('#6b4f12'), '5', FB, 10, dark, 'ÉCUS')
    # unités (cubes imprimables si pas de cubes en bois)
    for _ in range(20): square_token(HexColor('#c0392b'))
    for _ in range(20): square_token(HexColor('#2f6fbe'))
    # marqueurs de contrôle des sites
    for _ in range(5):  circle_token(HexColor('#f3d5d5'), HexColor('#a63a3a'), '⚑', SY, 10, HexColor('#a63a3a'), 'FÉLONS')
    for _ in range(5):  circle_token(HexColor('#d5e2f3'), HexColor('#3f6fae'), '⚑', SY, 10, HexColor('#3f6fae'), 'ROYAUX')
    # frappes uniques & tour
    circle_token(PARCH, INK, '⚒', SY, 11, INK, 'TRÉBUCHET')
    circle_token(PARCH, INK, '⚓', SY, 11, INK, 'NEF')
    circle_token(PARCH, GOLD, '♛', SY, 11, GOLD, 'TOUR')
    # jetons de TRACE (preuves d'ambition)
    for _ in range(10): circle_token(dark, HexColor('#a63a3a'), '☠', SY, 11, HexColor('#e8dcc0'), 'ASSASSINAT')
    for _ in range(12): circle_token(dark, HexColor('#c9962b'), '◉', SY, 11, HexColor('#e8c25a'), 'CIBLÉ')
    for _ in range(16): circle_token(dark, HexColor('#8b7fd9'), '☾', SY, 11, HexColor('#cfc4f3'), 'FAVORITE')
    for _ in range(12): circle_token(dark, HexColor('#4eb98f'), '☦', SY, 11, HexColor('#c8ead9'), 'MONASTÈRE')
    for _ in range(8):  circle_token(dark, GOLD, '♛', SY, 11, HexColor('#e8c25a'), 'RÈGNE')
    for _ in range(10): circle_token(dark, HexColor('#888888'), '†', FB, 12, HexColor('#dddddd'), 'MORT')
    c.showPage()
    c.save()
    print('OK', path)

if __name__ == '__main__':
    cards_pdf()
    plateau_pdf()
    tokens_pdf()
