# -*- coding: utf-8 -*-
"""ROYAUME — livret de règles imprimable (A4). Sortie : livret-regles-royaume.pdf"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak)
from reportlab.lib.styles import ParagraphStyle

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = r'C:\Windows\Fonts'
def reg(name, file):
    p = os.path.join(FONTS, file)
    if os.path.exists(p):
        pdfmetrics.registerFont(TTFont(name, p)); return True
    return False
HAS_G  = reg('Serif', 'georgia.ttf'); HAS_GB = reg('Serif-Bold', 'georgiab.ttf')
HAS_GI = reg('Serif-Italic', 'georgiai.ttf'); HAS_SY = reg('Sym', 'seguisym.ttf')
F  = 'Serif' if HAS_G else 'Times-Roman'
FB = 'Serif-Bold' if HAS_GB else 'Times-Bold'
FI = 'Serif-Italic' if HAS_GI else 'Times-Italic'
SY = 'Sym' if HAS_SY else FB

INK   = HexColor('#2b2118'); GOLD = HexColor('#b8860b'); DARK = HexColor('#241b12')
PARCH = HexColor('#f3e9d2'); RED  = HexColor('#a63a3a')

S_BODY = ParagraphStyle('body', fontName=F, fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle('h1', fontName=FB, fontSize=15, leading=19, textColor=HexColor('#7a1f1f'),
                      spaceBefore=13, spaceAfter=6)
S_H2 = ParagraphStyle('h2', fontName=FB, fontSize=11.5, leading=15, textColor=HexColor('#5b3a2b'),
                      spaceBefore=9, spaceAfter=4)
S_LI = ParagraphStyle('li', parent=S_BODY, leftIndent=7*mm, bulletIndent=2*mm, spaceAfter=3)
S_NOTE = ParagraphStyle('note', parent=S_BODY, fontName=FI, textColor=HexColor('#6b5b3a'),
                        backColor=HexColor('#efe4c8'), borderPadding=5, leftIndent=3*mm, rightIndent=3*mm)
S_EX = ParagraphStyle('ex', parent=S_BODY, fontName=FI, fontSize=8.8, textColor=HexColor('#555555'),
                      leftIndent=6*mm)

GLYPHS = '⚜☠◉♛☾☦⚔⚑⚒⚓†✠★①②③④⑤'
def sym_wrap(t):
    for g in GLYPHS:
        t = t.replace(g, '<font name="'+SY+'">'+g+'</font>')
    return t
def P(t, s=S_BODY): return Paragraph(sym_wrap(t), s)
def LI(t): return Paragraph(sym_wrap('⚜ ' + t), S_LI)

def cover(c, doc):
    W, H = A4
    c.saveState()
    c.setFillColor(DARK); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.rect(12*mm, 12*mm, W-24*mm, H-24*mm, stroke=1, fill=0)
    c.setLineWidth(0.7); c.rect(15*mm, 15*mm, W-30*mm, H-30*mm, stroke=1, fill=0)
    c.setFillColor(GOLD)
    c.setFont(SY, 54); c.drawCentredString(W/2, H-72*mm, '⚜')
    c.setFont(FB, 44); c.drawCentredString(W/2, H-95*mm, 'R O Y A U M E')
    c.setFillColor(HexColor('#c9b78a')); c.setFont(FI, 14)
    c.drawCentredString(W/2, H-107*mm, 'Couronne, trahisons & révoltes')
    c.setFont(F, 11)
    for i, ln in enumerate(['5 à 7 barons félons  ·  45 à 60 minutes  ·  dès 12 ans',
                            '', 'La taille royale arrive à la cour. Le Roi la partage,',
                            'le Conseil vote, la nuit les dagues sortent…',
                            'et quand la Couronne vacille, les bannières se lèvent.',
                            '', 'Seul l’or à l’abri chez les Templiers fera de vous le vainqueur.']):
        c.drawCentredString(W/2, H-130*mm - i*7*mm, ln)
    c.setFont(SY, 22)
    c.drawCentredString(W/2-30*mm, 45*mm, '⚔'); c.drawCentredString(W/2, 45*mm, '♛'); c.drawCentredString(W/2+30*mm, 45*mm, '☠')
    c.setFillColor(HexColor('#8a7a5a')); c.setFont(F, 9)
    c.drawCentredString(W/2, 25*mm, 'LIVRET DE RÈGLES')
    c.restoreState()

def normal_page(c, doc):
    W, H = A4
    c.saveState()
    c.setFillColor(HexColor('#faf5e8')); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(16*mm, H-14*mm, W-16*mm, H-14*mm)
    c.setFillColor(HexColor('#8a7a5a')); c.setFont(FB, 8)
    c.drawString(16*mm, H-12*mm, 'ROYAUME — livret de règles')
    c.line(16*mm, 13*mm, W-16*mm, 13*mm)
    c.setFont(F, 8); c.drawCentredString(W/2, 8*mm, '— ' + str(doc.page) + ' —')
    c.restoreState()

def build():
    path = os.path.join(HERE, 'livret-regles-royaume.pdf')
    doc = BaseDocTemplate(path, pagesize=A4, title='ROYAUME — Livret de règles')
    fr = Frame(18*mm, 18*mm, A4[0]-36*mm, A4[1]-36*mm, id='f')
    doc.addPageTemplates([PageTemplate(id='cover', frames=[fr], onPage=cover),
                          PageTemplate(id='page', frames=[fr], onPage=normal_page)])
    st = []
    from reportlab.platypus import NextPageTemplate
    st.append(NextPageTemplate('page'))
    st.append(PageBreak())

    # ---------- 1. BUT & MATÉRIEL ----------
    st.append(P('1. Le but du jeu', S_H1))
    st.append(P('Vous êtes un baron du royaume. Pendant <b>8 tours</b> (les huit levées de la taille royale), '
                'vous allez voter, comploter, dormir d’un œil et, quand il le faudra, sortir les bannières. '
                'À la fin, seul compte <b>l’or déposé à votre coffre chez les Templiers</b> : le baron le plus riche '
                'au coffre l’emporte. L’or en poche ne vaut rien tant qu’il n’est pas déposé — et il se vole '
                'sur les cadavres. Chacun poursuit de plus une <b>ambition secrète</b> qui rapportera de l’or '
                'au décompte final.'))
    st.append(P('2. Le matériel', S_H1))
    mat = [
        ['1', 'plateau (île du royaume, 5 sites, piste des tours)'],
        ['87', 'cartes ACTION (29 différentes × 3 exemplaires)'],
        ['18', 'cartes ÉVÉNEMENT'],
        ['12', 'cartes AMBITION secrète'],
        ['7',  'cartes CHARGE (Roi, Connétable, Maître des Engins, Maître des Assassins, Chancelier, Amiral de France, Capitaine des Routiers)'],
        ['18', 'cartes TAILLE (le revenu royal — valeurs 7 à 15)'],
        ['56', 'cartes LIEU : pour chaque joueur, 4 cartes PLANQUE + 4 cartes FILATURE'],
        ['7',  'cartes AIDE DE JEU'],
        ['52', 'écus (40 × « 1 », 12 × « 5 »)'],
        ['40', 'unités (20 cubes rouges félons, 20 cubes bleus royaux)'],
        ['112', 'jetons de TRACE (☠ assassinat, ◉ ciblé, ☾ favorite, ☦ monastère, ♛ règne, † mort, ⚔/⚑ camps, ★ victoires, ✠ cathédrale)'],
        ['10', 'marqueurs de contrôle (5 rouges, 5 bleus)'],
        ['2',  'jetons de frappe (trébuchet, nef de guerre) + 1 marqueur de tour'],
        ['2',  'dés à six faces (1 rouge félon, 1 bleu royal)'],
        ['7',  'pions barons (une couleur par joueur)'],
    ]
    t = Table([[Paragraph('<b>'+a+'</b>', S_BODY), Paragraph(b, S_BODY)] for a, b in mat],
              colWidths=[14*mm, 158*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('ROWBACKGROUNDS',(0,0),(-1,-1),[HexColor('#f3e9d2'), HexColor('#ece0c4')]),
                           ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
    st.append(t)
    st.append(P('Chaque joueur cache ses <b>écus de poche</b> dans sa main ou derrière un paravent. '
                'Son <b>coffre</b> (écus déposés chez les Templiers) reste visible de tous, posé sur sa carte Charge.', S_NOTE))

    # ---------- 3. MISE EN PLACE ----------
    st.append(P('3. Mise en place', S_H1))
    for tx in [
        'Placez le plateau au centre. Mélangez séparément la pioche ACTION, la pile ÉVÉNEMENT et la pioche TAILLE, toutes face cachée. Marqueur de tour sur la case 1.',
        'À 5 joueurs, retirez l’Amiral de France et le Capitaine des Routiers ; à 6, retirez seulement le Capitaine. Mélangez les cartes CHARGE et distribuez-en une à chacun, face visible. Celui qui reçoit <b>Le Roi</b> prend la couronne.',
        'Chacun reçoit ses 8 cartes LIEU (4 Planque, 4 Filature), une aide de jeu, et pioche <b>2 cartes ACTION</b> (3 pour le Chancelier).',
        'Mélangez les AMBITIONS et distribuez-en une à chacun, <b>face cachée</b>. Regardez-la, ne la montrez à personne.',
        'Le Maître des Engins prend le jeton trébuchet, l’Amiral le jeton nef.',
    ]:
        st.append(LI(tx))

    # ---------- 4. TOUR DE JEU ----------
    st.append(P('4. Le tour de jeu — cinq phases', S_H1))
    st.append(P('① La taille royale', S_H2))
    st.append(P('Le Roi <b>pioche une carte TAILLE</b> et la regarde sans la montrer : c’est le revenu du royaume '
                'ce tour (un nombre entre 7 et 15). Il la garde <b>face cachée</b> devant lui et propose à voix '
                'haute une répartition : « tant pour untel, tant pour untel… ». Il n’annonce pas le total — '
                'les barons votent sans savoir combien le Roi garde pour lui. <i>Ce qui n’est pas donné file dans '
                'sa poche.</i>'))
    st.append(P('② Le vote du Conseil', S_H2))
    st.append(P('Chacun peut d’abord jouer des cartes VOTE ou ÉCUS de sa main (elles se défaussent). '
                'Puis tous votent <b>simultanément</b> au compte de trois : pouce levé (pour) ou baissé (contre). '
                'Chaque baron vivant = 1 voix, le Chancelier = 2, plus les bonus de cartes. Le Roi vote aussi.'))
    st.append(P('<b>Adopté</b> : chacun prend les écus promis (en poche), le Roi prend discrètement le reste '
                '(valeur de la carte moins les dons) et <b>glisse la carte TAILLE face cachée devant lui</b>, '
                'dans sa réserve royale — <i>sans la montrer</i>. Le total reste secret : nul ne sait vraiment '
                'combien le Roi s’est engraissé. <b>Rejeté</b> : toute la taille retourne à la réserve (le Roi ne '
                'garde rien), la carte va à la défausse, et il lance 1d6 — sur <b>4-6</b>, la révolte gronde '
                '(voir phase ⑤).'))
    st.append(P('Pourquoi une carte plutôt qu’un dé ? Parce qu’un dé secret ne laisse aucune trace : le Roi '
                'pourrait annoncer n’importe quel total. La carte, elle, est un <b>engagement matériel</b> — un '
                'objet unique, choisi avant la proposition, posé face cachée et impossible à changer après coup. '
                'Le total reste caché (le bluff est intact), mais la table garde un recours : à tout moment, un '
                '<b>vote à la majorité exige l’audit</b> — le Roi retourne sa carte, et l’on vérifie au moins qu’il '
                'n’a pas promis plus d’écus que la carte n’en contenait. Un Roi pris en flagrant délit rend le '
                'surplus et récolte les rancunes. Simple garde-fou de confiance entre amis, pas un contrôle '
                'fiscal : à vous de vous surveiller.', S_NOTE))
    st.append(P('③ La nuit', S_H2))
    st.append(P('Voir le chapitre 5 — c’est le cœur du jeu : planques, dagues et coffres.'))
    st.append(P('④ Le héraut', S_H2))
    st.append(P('Révélez la première carte ÉVÉNEMENT et appliquez-la immédiatement. '
                '(« Jacquerie » fait gronder la révolte ; « Grande foire » l’annule pour ce tour.)'))
    st.append(P('⑤ La révolte (si elle gronde)', S_H2))
    st.append(P('Si la révolte a été déclenchée ce tour — vote rejeté malheureux, Roi assassiné cette nuit, '
                'ou Jacquerie — et qu’aucune Grande foire ne l’annule : jouez la révolte (chapitre 6). '
                'Sinon, passez.'))
    st.append(P('Fin de tour', S_H2))
    st.append(P('Chacun pioche <b>1 carte ACTION</b> (2 pour le Chancelier, +1 pour qui a dormi à son Manoir). '
                'Main limitée à 7 cartes (défaussez l’excédent). Les barons morts ce tour <b>reviennent</b> : '
                '« un cousin reprend le fief » — même charge, poche vide, et ils posent un jeton † devant eux. '
                'Avancez le marqueur de tour.'))

    # ---------- 5. LA NUIT ----------
    st.append(P('5. La nuit', S_H1))
    st.append(P('A. Choix simultanés', S_H2))
    st.append(P('Chaque baron pose devant lui une carte <b>PLANQUE face cachée</b> : Manoir, Templiers, '
                'Favorite ou Monastère. Ceux qui veulent attaquer posent EN MÊME TEMPS, face cachée sur leur cible : '
                'une carte d’attaque de leur main (Spadassin, Baril de poudre…) et une carte <b>FILATURE</b> '
                '(le lieu où ils pensent trouver la cible). Le Maître des Assassins peut attaquer sans carte '
                'd’attaque (son privilège, une fois par nuit) — il pose seulement sa Filature.'))
    st.append(P('B. Révélation', S_H2))
    st.append(P('Toutes les planques se révèlent en même temps. Puis chaque attaque se résout, dans le sens '
                'horaire en partant du Roi :'))
    for tx in [
        '<b>Filature ratée</b> (le lieu deviné n’est pas la planque de la cible) : rien ne se passe. L’Espion à la cour ignore la Filature : il touche toujours (sauf Monastère).',
        '<b>Monastère</b> : intouchable, l’attaque échoue toujours.',
        '<b>Empoisonneuse</b> : lancez 1d6, échec sur 1-3.',
        '<b>Garde du corps</b> de la cible : l’attaque échoue (sauf poison), la carte est défaussée.',
        '<b>Sosie</b> : la cible lance 1d6, elle survit sur 4-6 ; la carte est défaussée dans tous les cas.',
        '<b>Sinon la cible meurt</b> : couchez son pion. Elle pose un jeton †, l’attaquant prend un jeton ☠ (et c’est public : tout le monde a vu qui a joué la carte). Le tueur prend la poche de la cible — sauf Coffre scellé. Baril de poudre et Coffret piégé détruisent la poche au lieu de la voler.',
        'Toute cible d’une attaque (réussie ou non) prend un jeton ◉ « ciblé ».',
        'Si le <b>Roi</b> meurt : la révolte gronde pour ce tour.',
    ]:
        st.append(LI(tx))
    st.append(P('C. Dépôts et petits matins', S_H2))
    for tx in [
        '<b>Templiers</b> : déposez toute votre poche sur votre coffre (visible, définitif, imprenable).',
        '<b>Favorite</b> : prenez 1 écu de la réserve et un jeton ☾.',
        '<b>Monastère</b> : prenez un jeton ☦ (et l’écu du Pèlerinage si l’événement est actif).',
        '<b>Manoir</b> : vous piocherez 1 carte de plus en fin de tour.',
    ]:
        st.append(LI(tx))
    st.append(P('Exemple — Isabeau pose sa Planque « Favorite ». Montfort l’attaque au Spadassin avec une Filature '
                '« Templiers » : raté, elle n’y était pas. Isabeau prend quand même son jeton ◉… et saura qu’on lui en veut.', S_EX))

    # ---------- 6. LA RÉVOLTE ----------
    st.append(P('6. La révolte des barons', S_H1))
    st.append(P('A. Les camps', S_H2))
    st.append(P('Le Roi est toujours <b>royal</b>. En partant de sa gauche, chacun annonce son camp : '
                '<b>félon</b> (rouge) ou <b>royal</b> (bleu) — et prend aussitôt le <b>jeton de camp</b> '
                'correspondant (⚔ félon ou ⚑ royal), qui restera devant lui. Chacun peut alors jouer des '
                'cartes RÉVOLTE de sa main : elles ajoutent des unités à déployer. Si personne n’est félon, '
                'le calme revient. Si personne ne défend, la Couronne tombe sans combat (voir E).'))
    st.append(P('B. Manche 1 — le déploiement', S_H2))
    st.append(P('Chaque baron dispose d’unités égales à sa <b>charge</b> (Connétable 4, Routiers 3, Roi 3, '
                'Engins / Assassins / Amiral 2, Chancelier 1) plus ses cartes RÉVOLTE jouées. En commençant par '
                'le Roi puis dans le sens horaire, chacun pose TOUTES ses unités (cubes de la couleur de son camp) '
                'sur les sites de son choix. <b>Le Château est interdit au déploiement félon</b> — il faudra le '
                'prendre d’assaut. Posez un marqueur de contrôle bleu sur chaque site au début (le royaume tient la ville).'))
    st.append(P('C. Manches 2 et 3', S_H2))
    st.append(P('Dans l’ordre : <b>pouvoirs des sites</b>, puis <b>mouvements</b>, puis <b>frappes</b>, puis <b>batailles</b>.'))
    for tx in [
        '<b>Pouvoirs</b> — un site est « tenu » si un seul camp y a des unités : Garnison = +1 unité de renfort sur place · Cathédrale = retirez 1 unité ennemie du plus gros groupe adverse · Trésor Royal = un baron du camp peut payer 2 écus de poche pour poser 1 unité sur le Trésor · Port = pendant les mouvements, les unités partant du Port peuvent aller sur N’IMPORTE QUEL site.',
        '<b>Mouvements</b> — félons d’abord : chaque unité peut se déplacer vers un site adjacent (routes du plateau). Une unité arrivée ne rebouge plus cette manche.',
        '<b>Frappes</b> — une fois par révolte : le Maître des Engins (trébuchet) et/ou l’Amiral (nef) peuvent frapper n’importe quel site occupé par l’ennemi et y détruire jusqu’à 2 unités. Rendez le jeton une fois utilisé.',
        '<b>Batailles</b> — sur chaque site où les deux camps sont présents : dé rouge + unités félonnes contre dé bleu + unités royales. Égalité : le camp qui contrôlait le site tient. Le perdant détruit la moitié de ses unités (arrondi supérieur), les survivants reculent vers un site adjacent ami (sinon anéantis). Le vainqueur perd un quart (arrondi inférieur). Mettez à jour les marqueurs de contrôle.',
    ]:
        st.append(LI(tx))
    st.append(P('D. Le décompte', S_H2))
    st.append(P('Après la manche 3 : chaque site contrôlé vaut 1 point, <b>le Château 2</b> (6 points en tout). '
                'Les félons l’emportent avec <b>4 points ou plus</b>. Distribuez alors les traces de la révolte : '
                'chaque membre du <b>camp vainqueur</b> prend un jeton ★ de sa couleur, et chaque membre du camp '
                'qui <b>tient la Cathédrale</b> prend un jeton ✠.'))
    st.append(P('E. Couronnement et billot', S_H2))
    st.append(P('<b>Félons vainqueurs</b> : le félon à la plus grosse armée de charge (Connétable 4 > Routiers 3 > '
                'Engins / Assassins / Amiral 2 > Chancelier 1 ; égalité : le plus riche au coffre) prend la couronne, '
                'pose un jeton ♛, échange sa carte Charge contre Le Roi et <b>redistribue les charges libérées</b> '
                'comme il l’entend. Le nouveau Roi peut envoyer un vaincu au <b>billot</b> : le condamné pose un '
                'jeton †, sa poche revient au Roi — sauf s’il joue un Sauf-conduit. <b>Royaux vainqueurs</b> : '
                'le Roi garde sa couronne et peut envoyer un félon au billot, mêmes règles. Les exécutés et morts '
                'reviennent au tour suivant (le cousin).'))

    # ---------- 7. AMBITIONS SANS MAÎTRE DU JEU ----------
    st.append(P('7. Ambitions secrètes — jouer sans maître du jeu', S_H1))
    st.append(P('Comment prouver qu’une ambition est accomplie alors que personne n’arbitre ? '
                'Par trois garde-fous, conçus pour que la table s’arbitre elle-même :', S_BODY))
    st.append(P('1. Tout est public', S_H2))
    st.append(P('Aucune ambition ne dépend d’une information restée cachée : les planques sont révélées '
                'chaque nuit, les attaques et leurs auteurs se voient sur la table, les couronnements, morts '
                'et camps de révolte se jouent devant tout le monde. La seule exception, « Le Templier », '
                'se vérifie au moment du décompte final, quand toutes les poches sont montrées.'))
    st.append(P('2. Les jetons de trace', S_H2))
    st.append(P('<b>Chaque événement laisse une trace matérielle, prise au moment où il se produit, devant '
                'tout le monde</b> — c’est un réflexe systématique de TOUS les joueurs, pas un choix :'))
    for tx in [
        '☠ à chaque assassinat que vous réussissez ;',
        '◉ à chaque fois qu’une attaque vous vise (même ratée) ;',
        '† à chaque fois que vous mourez (dague ou billot) ;',
        '♛ à chaque fois que vous prenez la couronne ;',
        '☾ chaque nuit passée chez la Favorite (avec votre écu) ;',
        '☦ chaque nuit passée au Monastère ;',
        '⚔ ou ⚑ à chaque révolte, en annonçant votre camp ;',
        '★ (rouge ou bleue) si votre camp gagne la révolte ; ✠ si votre camp tient la Cathédrale à la fin.',
    ]:
        st.append(LI(tx))
    st.append(P('Prendre un jeton ne trahit PAS votre ambition : tout le monde prend toujours tous ses jetons — '
                'c’est la chronique publique de la partie, pas un aveu. Au décompte, vos jetons font preuve : '
                '« 3 jetons ☾, mon ambition était Le Courtisan, +2 écus. » Personne n’a rien à retenir de tête.', S_NOTE))
    st.append(P('3. La vérification collective', S_H2))
    st.append(P('À la révélation finale, chacun lit son ambition à voix haute et montre ses preuves — chaque '
                'ambition a la sienne, aucune ne repose sur la mémoire seule. Tricher exigerait de prendre un '
                'jeton au vu de tous pour un événement qui n’a pas eu lieu : impossible discrètement. Et les '
                'jetons se recoupent entre eux (chaque ☠ correspond au † de quelqu’un, chaque ★ à une révolte '
                'que toute la table a jouée). En cas de litige, la table tranche à la majorité.'))
    tab_amb = [
        ['Ambition', 'Sa preuve au décompte'],
        ['Le Régicide (+4)', 'un jeton ☠ pris lors d’une nuit où le Roi est mort — l’attaque et sa carte étaient visibles de tous'],
        ['La Main sanglante (+4)', 'au moins 2 jetons ☠'],
        ['L’Éminence grise (+3)', 'AUCUN jeton ♛, pas la couronne de départ, et votre pion debout'],
        ['Le Croisé (+3)', 'un jeton ✠'],
        ['Le Loyal (+3)', 'au moins un jeton ⚑ et AUCUN jeton ⚔'],
        ['Le Grand Félon (+3)', 'une ★ rouge (victoire dans le camp félon)'],
        ['L’Usurpateur (+3)', 'la couronne devant vous à la fin, un jeton ♛, sans être le Roi de départ (la carte Charge initiale fait foi)'],
        ['L’Insaisissable (+3)', 'AUCUN jeton ◉'],
        ['L’Increvable (+2)', 'AUCUN jeton †'],
        ['Le Courtisan (+2)', 'au moins 3 jetons ☾'],
        ['Le Pénitent (+2)', 'au moins 2 jetons ☦'],
        ['Le Templier (+2)', 'montrez votre poche : 0 écu — et 6+ écus sur votre coffre (visible depuis toujours)'],
    ]
    t2 = Table([[Paragraph(sym_wrap('<b>'+a+'</b>'), S_BODY), Paragraph(sym_wrap(b), S_BODY)] for a, b in tab_amb],
               colWidths=[46*mm, 126*mm])
    t2.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('BACKGROUND',(0,0),(-1,0),HexColor('#5b3a6b')),
                            ('TEXTCOLOR',(0,0),(-1,0),HexColor('#f3e9d2')),
                            ('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#f3e9d2'), HexColor('#ece0c4')]),
                            ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
    st.append(t2)

    # ---------- 8. FIN DE PARTIE ----------
    st.append(P('8. Fin de partie et décompte', S_H1))
    for tx in [
        'Après le 8e tour, chacun révèle son ambition et la prouve : si elle est accomplie, il ajoute son bonus À SON COFFRE.',
        'Titres d’honneur (+1 écu au coffre chacun, record strict — en cas d’égalité, personne) : ⚔ le Sanguinaire (le plus de ☠) · ⚑ le Vétéran (le plus de jetons ⚔ et ⚑ cumulés) · ☾ le Noctambule (le plus de ☾) · ⚜ le Grippe-sou (la plus grosse poche finale).',
        'Le baron au coffre le plus garni l’emporte. Égalité : la plus grosse poche départage.',
    ]:
        st.append(LI(tx))
    st.append(P('« On n’a jamais vu un royaume si bien géré », dira le chroniqueur. Il était payé pour.', S_EX))

    doc.build(st)
    print('OK', path)

if __name__ == '__main__':
    build()
