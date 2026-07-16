# -*- coding: utf-8 -*-
"""ROUAGES & COMPLOTS — livret de règles imprimable (A4). Sortie : livret-regles-royaume.pdf"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, Flowable)
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
    c.setFont(FB, 30); c.drawCentredString(W/2, H-95*mm, 'ROUAGES & COMPLOTS')
    c.setFillColor(HexColor('#c9b78a')); c.setFont(FI, 14)
    c.drawCentredString(W/2, H-107*mm, 'Vapeur, corruption & insurrections')
    c.setFont(F, 11)
    for i, ln in enumerate(['4 à 7 notables ambitieux  ·  45 à 60 minutes  ·  dès 12 ans',
                            '', 'La cassette impériale arrive à la cour. L’Empereur la partage,',
                            'le Conseil vote, la nuit les dagues sortent…',
                            'et quand l’Empire vacille, les bannières se lèvent.',
                            '', 'Seul l’or à l’abri chez la Banque fera de vous le vainqueur.']):
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
    c.drawString(16*mm, H-12*mm, 'ROUAGES & COMPLOTS — livret de règles')
    c.line(16*mm, 13*mm, W-16*mm, 13*mm)
    c.setFont(F, 8); c.drawCentredString(W/2, 8*mm, '— ' + str(doc.page) + ' —')
    c.restoreState()

# =====================================================================
# SCHÉMAS (dessin vectoriel dans le PDF)
# =====================================================================
BACK = HexColor('#241b12')

class Diagram(Flowable):
    def __init__(self, w, h, fn, caption=''):
        super().__init__()
        self.width, self.height, self.fn, self.caption = w, h, fn, caption
    def draw(self):
        c = self.canv
        c.saveState()
        self.fn(c)
        if self.caption:
            c.setFillColor(HexColor('#8a7a5a')); c.setFont(FI if HAS_GI else F, 7.5)
            c.drawCentredString(self.width/2, 1*mm, self.caption)
        c.restoreState()

def _wrapc(c, x, y, w, txt, font, size, color, lead=None):
    lead = lead or size*1.25
    c.setFillColor(color); c.setFont(font, size)
    words, line = txt.split(' '), ''
    lines = []
    for wd in words:
        t = (line+' '+wd).strip()
        if c.stringWidth(t, font, size) <= w: line = t
        else: lines.append(line); line = wd
    if line: lines.append(line)
    for i, ln in enumerate(lines):
        c.drawCentredString(x, y-i*lead, ln)
    return len(lines)

def _pile(c, x, y, w, h, label, col, n=3, face='down'):
    for i in range(n):     # effet de pile
        ox = i*0.7*mm
        c.setFillColor(BACK if face=='down' else PARCH)
        c.setStrokeColor(col); c.setLineWidth(0.8)
        c.roundRect(x+ox, y+ox, w, h, 1.2*mm, stroke=1, fill=1)
    cx, cy = x+(n-1)*0.7*mm+w/2, y+(n-1)*0.7*mm+h/2
    if face=='down':
        c.setFillColor(GOLD); c.setFont(SY, 8); c.drawCentredString(cx, cy+1*mm, '⚜')
    _wrapc(c, cx, y-2.5*mm, w+8*mm, label, FB, 5.6, INK)

def _card(c, x, y, w, h, label, col=INK, face='up', icon=''):
    c.setFillColor(BACK if face=='down' else PARCH)
    c.setStrokeColor(GOLD if face=='down' else col); c.setLineWidth(0.9)
    c.roundRect(x, y, w, h, 1.2*mm, stroke=1, fill=1)
    if face=='down':
        c.setFillColor(GOLD); c.setFont(SY, 8); c.drawCentredString(x+w/2, y+h/2-1*mm, '⚜')
    else:
        if icon:
            c.setFillColor(col); c.setFont(SY, 9); c.drawCentredString(x+w/2, y+h/2+1*mm, icon)
        _wrapc(c, x+w/2, y+h-3.2*mm, w+4*mm, label, FB, 5.4, col)

def _coin(c, x, y, r=2.4*mm):
    c.setFillColor(HexColor('#e8c25a')); c.setStrokeColor(HexColor('#8a6a1a')); c.setLineWidth(0.6)
    c.circle(x, y, r, stroke=1, fill=1)

def _token(c, x, y, glyph, ring, r=2.6*mm):
    c.setFillColor(BACK); c.setStrokeColor(ring); c.setLineWidth(0.8)
    c.circle(x, y, r, stroke=1, fill=1)
    c.setFillColor(HexColor('#e8dcc0')); c.setFont(SY, 6); c.drawCentredString(x, y-2, glyph)

def _label(c, x, y, txt, size=6.5, color=HexColor('#7a1f1f'), font=None):
    c.setFillColor(color); c.setFont(font or FB, size); c.drawString(x, y, txt)

# ---- Schéma 1 : mise en place (vue de table) ----
def diagram_setup(c):
    W, H = 174*mm, 92*mm
    # table
    c.setFillColor(HexColor('#efe4c8')); c.setStrokeColor(HexColor('#d8c9a5')); c.setLineWidth(1)
    c.roundRect(2*mm, 6*mm, W-4*mm, H-8*mm, 3*mm, stroke=1, fill=1)
    # plateau au centre
    cx, cy = W/2, 46*mm
    c.setFillColor(HexColor('#7ba05b')); c.setStrokeColor(HexColor('#5f7d43')); c.setLineWidth(1.2)
    c.roundRect(cx-30*mm, cy-19*mm, 60*mm, 38*mm, 3*mm, stroke=1, fill=1)
    c.setFillColor(HexColor('#255')); c.setFillColor(HexColor('#1f5f7a'))
    for (dx,dy,nm) in [(-19,10,'Notre-Dame'),(19,10,'Banque de France'),(-19,-10,'Caserne'),(19,-10,'La Gare')]:
        c.setFillColor(HexColor('#efe4c8')); c.setStrokeColor(INK); c.setLineWidth(0.5)
        c.circle(cx+dx*mm, cy+dy*mm, 5*mm, stroke=1, fill=1)
        c.setFillColor(INK); c.setFont(F, 4.2); c.drawCentredString(cx+dx*mm, cy+dy*mm-1, nm)
    c.setFillColor(HexColor('#7a1f1f')); c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.circle(cx, cy, 6.5*mm, stroke=1, fill=1)
    c.setFillColor(GOLD); c.setFont(SY, 8); c.drawCentredString(cx, cy+1.5*mm, '♛')
    c.setFillColor(HexColor('#f3e9d2')); c.setFont(FB, 4.6); c.drawCentredString(cx, cy-3.5*mm, 'TUILERIES')
    c.setFillColor(HexColor('#1a3a1a')); c.setFont(FB, 6); c.drawCentredString(cx, cy+15*mm, 'PLATEAU')
    # pioches en haut
    cw, ch = 13*mm, 18*mm
    _pile(c, 20*mm, 68*mm, cw, ch, 'Pioche CASSETTE', CATS_taille := HexColor('#8a6a1a'))
    _pile(c, 44*mm, 68*mm, cw, ch, 'Pioche ACTION', GOLD)
    _pile(c, 110*mm, 68*mm, cw, ch, 'Pioche ÉVÉNEMENT', HexColor('#8a5a2b'))
    # réserve de francs
    c.setFillColor(HexColor('#f6eed2')); c.setStrokeColor(HexColor('#8a6a1a')); c.setLineWidth(0.9)
    c.roundRect(134*mm, 68*mm, 20*mm, 18*mm, 2*mm, stroke=1, fill=1)
    for (dx,dy) in [(6,12),(11,12),(8,8),(13,8),(6,5),(11,5)]:
        _coin(c, 134*mm+dx*mm, 68*mm+dy*mm)
    _wrapc(c, 144*mm, 66*mm, 26*mm, 'Réserve de francs + unités', FB, 5.4, INK)
    # 5 zones joueurs autour
    def notable(x, y, n, king=False):
        c.setFillColor(HexColor('#f6eed2')); c.setStrokeColor(HexColor('#b9a97e')); c.setLineWidth(0.8)
        c.roundRect(x, y, 30*mm, 15*mm, 2*mm, stroke=1, fill=1)
        _card(c, x+1.5*mm, y+2*mm, 7*mm, 10*mm, 'Charge', col=HexColor('#7a1f1f'), icon='♛' if king else '')
        # coffre (francs sur la charge)
        _coin(c, x+3*mm, y+13.5*mm); _coin(c, x+6*mm, y+13.5*mm)
        _card(c, x+10*mm, y+2*mm, 7*mm, 10*mm, '', face='down')   # ambition
        _card(c, x+18.5*mm, y+3.5*mm, 9*mm, 7*mm, 'main', col=INK)
        c.setFillColor(HexColor('#7a1f1f') if king else INK); c.setFont(FB, 5)
        c.drawString(x+1.5*mm, y+16*mm, ('L’EMPEREUR' if king else 'Notable '+str(n)))
    notable(8*mm,   40*mm, 1, king=True)
    notable(8*mm,   16*mm, 2)
    notable(72*mm,  9*mm, 3)
    notable(136*mm, 40*mm, 4)
    notable(136*mm, 16*mm, 5)
    c.setFillColor(HexColor('#8a7a5a')); c.setFont(F, 5); c.drawCentredString(W/2, 11*mm, '(6-7 joueurs : deux notables de plus autour de la table)')

# ---- Schéma 2 : la zone de jeu d’un notable ----
def diagram_player(c):
    W, H = 174*mm, 62*mm
    c.setFillColor(HexColor('#f6eed6')); c.setStrokeColor(HexColor('#d8c9a5')); c.setLineWidth(1)
    c.roundRect(2*mm, 5*mm, W-4*mm, H-7*mm, 3*mm, stroke=1, fill=1)
    y0 = 30*mm
    # 1 Charge + coffre
    _card(c, 8*mm, y0, 16*mm, 23*mm, 'CHARGE (face visible)', col=HexColor('#7a1f1f'), icon='♛')
    for (dx,dy) in [(3,3),(7,3),(11,3),(5,7),(9,7)]:
        _coin(c, 8*mm+dx*mm, y0+dy*mm)
    _label(c, 8*mm, y0+25*mm, 'Charge + COFFRE', 6)
    _label(c, 8*mm, y0-4*mm, 'francs déposés = visibles', 5.2, HexColor('#3e8e6b'), F)
    # 2 Ambition face down
    _card(c, 30*mm, y0, 15*mm, 21*mm, '', face='down')
    _label(c, 30*mm, y0+23*mm, 'AMBITION', 6)
    _label(c, 30*mm, y0-4*mm, 'secrète, face cachée', 5.2, HexColor('#5b3a6b'), F)
    # 3 Planque (nuit)
    _card(c, 51*mm, y0, 15*mm, 21*mm, '', face='down')
    _label(c, 51*mm, y0+23*mm, 'PLANQUE', 6)
    _label(c, 51*mm, y0-4*mm, 'la nuit, face cachée', 5.2, HexColor('#4a6b3a'), F)
    # 4 main
    for i in range(4):
        _card(c, 72*mm+i*7*mm, y0+i*0.0, 14*mm, 20*mm, '' , col=INK, face='down')
    _label(c, 72*mm, y0+23*mm, 'MAIN (cartes Action)', 6)
    _label(c, 72*mm, y0-4*mm, 'cachée des autres', 5.2, INK, F)
    # 5 francs de poche (derrière paravent)
    c.setFillColor(HexColor('#e9dcbc')); c.setStrokeColor(INK); c.setLineWidth(0.8); c.setDash(2,2)
    c.roundRect(112*mm, y0, 24*mm, 21*mm, 2*mm, stroke=1, fill=1); c.setDash()
    for (dx,dy) in [(5,5),(10,5),(15,5),(19,5),(7,11),(13,11)]:
        _coin(c, 112*mm+dx*mm, y0+dy*mm)
    _label(c, 112*mm, y0+23*mm, 'POCHE (cachée)', 6)
    _label(c, 112*mm, y0-4*mm, 'derrière le paravent', 5.2, HexColor('#8a6a1a'), F)
    # 2 cartes de vote (POUR / CONTRE)
    _card(c, 143*mm, y0, 13*mm, 19*mm, 'POUR', col=HexColor('#3e8e6b'), icon='✓')
    _card(c, 158*mm, y0, 13*mm, 19*mm, 'CONTRE', col=HexColor('#a63a3a'), icon='✗')
    _label(c, 143*mm, y0+23*mm, 'CARTES DE VOTE', 6)
    _label(c, 143*mm, y0-4*mm, 'jouées face cachée', 5.2, INK, F)

# ---- Schéma 3 : la nuit — poser une attaque ----
def diagram_night(c):
    W, H = 174*mm, 46*mm
    c.setFillColor(HexColor('#171b25')); c.setStrokeColor(HexColor('#3a4358')); c.setLineWidth(1)
    c.roundRect(2*mm, 5*mm, W-4*mm, H-7*mm, 3*mm, stroke=1, fill=1)
    # attaquant à gauche
    _label(c, 10*mm, 34*mm, 'VOUS (l’attaquant)', 6.5, HexColor('#ffd166'))
    _card(c, 10*mm, 12*mm, 15*mm, 20*mm, 'Carte d’ATTAQUE', col=HexColor('#6b5b95'), icon='☠')
    _card(c, 28*mm, 12*mm, 15*mm, 20*mm, 'FILATURE (le lieu deviné)', col=HexColor('#4a6b3a'), icon='☾')
    # flèche
    c.setStrokeColor(HexColor('#ffd166')); c.setLineWidth(1.4)
    c.line(46*mm, 22*mm, 96*mm, 22*mm)
    c.setFillColor(HexColor('#ffd166'))
    p = c.beginPath(); p.moveTo(96*mm,22*mm); p.lineTo(92*mm,24.5*mm); p.lineTo(92*mm,19.5*mm); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(HexColor('#ffd166')); c.setFont(FI if HAS_GI else F, 6)
    c.drawCentredString(71*mm, 24*mm, 'posées FACE CACHÉE sur la cible')
    # cible à droite
    _label(c, 104*mm, 34*mm, 'LA CIBLE', 6.5, HexColor('#ff9b9b'))
    _card(c, 104*mm, 12*mm, 15*mm, 20*mm, 'sa CHARGE', col=HexColor('#7a1f1f'), icon='♛')
    _card(c, 122*mm, 12*mm, 15*mm, 20*mm, 'sa PLANQUE', face='down')
    _card(c, 140*mm, 12*mm, 15*mm, 20*mm, "votre attaque\n+ filature", face='down')
    c.setFillColor(HexColor('#8fa3c7')); c.setFont(F, 5.4)
    c.drawCentredString(147*mm, 9*mm, 'révélées ensemble')

def _cube(c, x, y, col, s=2.6*mm):
    c.setFillColor(col); c.setStrokeColor(HexColor('#2b2118')); c.setLineWidth(0.4)
    c.rect(x-s/2, y-s/2, s, s, stroke=1, fill=1)

def _die(c, x, y, pips, s=8*mm):
    c.setFillColor(HexColor('#f4efe2')); c.setStrokeColor(INK); c.setLineWidth(0.8)
    c.roundRect(x-s/2, y-s/2, s, s, 1.4*mm, stroke=1, fill=1)
    P = {1:[(0,0)], 2:[(-1,1),(1,-1)], 3:[(-1,1),(0,0),(1,-1)],
         4:[(-1,1),(1,1),(-1,-1),(1,-1)], 5:[(-1,1),(1,1),(0,0),(-1,-1),(1,-1)],
         6:[(-1,1),(1,1),(-1,0),(1,0),(-1,-1),(1,-1)]}
    c.setFillColor(INK)
    for (dx,dy) in P[pips]:
        c.circle(x+dx*s*0.26, y+dy*s*0.26, s*0.07, stroke=0, fill=1)

RED = HexColor('#c0392b'); BLUE = HexColor('#2f6fbe')

# ---- Schéma 4 : l’insurrection — déploiement, routes, mouvements ----
def diagram_revolt(c):
    W, H = 174*mm, 84*mm
    c.setFillColor(HexColor('#eef3e6')); c.setStrokeColor(HexColor('#c9d6b8')); c.setLineWidth(1)
    c.roundRect(2*mm, 5*mm, W-4*mm, H-7*mm, 3*mm, stroke=1, fill=1)
    S = {'chateau':(52,45,'Palais','♛','#7a1f1f',True),
         'cathedrale':(24,66,'Notre-Dame','☦','#5b3a6b',False),
         'tresor':(80,66,'Banque de France','⚜','#8a6a1a',False),
         'garnison':(24,23,'Caserne','⚔','#3e6b3e',False),
         'port':(80,23,'La Gare','⚓','#3f6fae',False)}
    def pos(k): return (S[k][0]*mm, S[k][1]*mm)
    routes = [('chateau','cathedrale'),('chateau','tresor'),('chateau','garnison'),('chateau','port'),
              ('cathedrale','tresor'),('tresor','port'),('port','garnison'),('garnison','cathedrale')]
    c.setStrokeColor(HexColor('#b9a97e')); c.setLineWidth(2.4); c.setLineCap(1)
    for a,b in routes:
        (x1,y1),(x2,y2) = pos(a), pos(b); c.line(x1,y1,x2,y2)
    def cubes(k, nred, nblue):
        x,y = pos(k); xs = x-4.2*mm
        for i in range(nred):  _cube(c, xs+i*3.2*mm, y-1.5*mm, RED)
        for i in range(nblue): _cube(c, xs+i*3.2*mm, y-5.0*mm, BLUE)
    for k,(fx,fy,nm,ic,col,big) in S.items():
        x,y = fx*mm,fy*mm; r = (11.5 if big else 9.5)*mm
        c.setFillColor(HexColor('#efe4c8')); c.setStrokeColor(HexColor(col)); c.setLineWidth(1.4)
        c.circle(x,y,r,stroke=1,fill=1)
        c.setFillColor(HexColor(col)); c.setFont(SY,8); c.drawCentredString(x,y+r-4*mm,ic)
        c.setFont(FB,5.2); c.drawCentredString(x,y+r-8.3*mm,nm+(' ×2 pts' if big else ''))
    cubes('chateau',0,3); cubes('cathedrale',2,0); cubes('garnison',2,0); cubes('tresor',0,1); cubes('port',1,0)
    # flèche de mouvement Caserne -> Palais (assaut insurgé)
    (gx,gy),(cx,cy) = pos('garnison'), pos('chateau')
    import math
    ang = math.atan2(cy-gy, cx-gx); sx,sy = gx+11*mm*math.cos(ang), gy+11*mm*math.sin(ang)
    ex,ey = cx-13*mm*math.cos(ang), cy-13*mm*math.sin(ang)
    c.setStrokeColor(RED); c.setLineWidth(1.6); c.setDash(3,2); c.line(sx,sy,ex,ey); c.setDash()
    c.setFillColor(RED)
    p=c.beginPath(); p.moveTo(ex,ey)
    p.lineTo(ex-3.4*mm*math.cos(ang-0.4), ey-3.4*mm*math.sin(ang-0.4))
    p.lineTo(ex-3.4*mm*math.cos(ang+0.4), ey-3.4*mm*math.sin(ang+0.4)); p.close(); c.drawPath(p,fill=1,stroke=0)
    c.setFillColor(RED); c.setFont(FI if HAS_GI else F,5.4); c.drawString(30*mm,36*mm,'assaut')
    # légende à droite
    lx = 100*mm
    c.setFillColor(HexColor('#7a1f1f')); c.setFont(FB,7); c.drawString(lx,74*mm,'LÉGENDE')
    _cube(c, lx+2*mm, 67*mm, RED); c.setFillColor(INK); c.setFont(F,6.4); c.drawString(lx+6*mm,65.6*mm,'unité insurgée (rouge)')
    _cube(c, lx+2*mm, 60*mm, BLUE); c.setFillColor(INK); c.drawString(lx+6*mm,58.6*mm,'unité impériale (bleu)')
    c.setStrokeColor(RED); c.setLineWidth(1.6); c.setDash(3,2); c.line(lx,52*mm,lx+4*mm,52*mm); c.setDash()
    c.setFillColor(INK); c.drawString(lx+6*mm,50.6*mm,'mouvement vers un site adjacent')
    c.setFillColor(HexColor('#7a1f1f')); c.setFont(FB,7); c.drawString(lx,42*mm,'DÉCOMPTE')
    c.setFillColor(INK); c.setFont(F,6.4)
    for i,t in enumerate(['Chaque site tenu = 1 point.','Le Palais = 2 points.',
                          'Total : 6 points.','Félons vainqueurs à 4 points ou +.']):
        c.drawString(lx,36*mm-i*4.4*mm,'• '+t)
    c.setFillColor(HexColor('#7a1f1f')); c.setFont(FB,7); c.drawString(lx,15.5*mm,'ORDRE D’UNE MANCHE')
    c.setFillColor(INK); c.setFont(F,6.2); c.drawString(lx,11*mm,'pouvoirs · mouvements · frappes · batailles')

# ---- Schéma 5 : un exemple de bataille chiffré ----
def diagram_battle(c):
    W, H = 174*mm, 40*mm
    c.setFillColor(HexColor('#f6eed6')); c.setStrokeColor(HexColor('#d8c9a5')); c.setLineWidth(1)
    c.roundRect(2*mm, 4*mm, W-4*mm, H-6*mm, 3*mm, stroke=1, fill=1)
    # AVANT
    c.setFillColor(HexColor('#7a1f1f')); c.setFont(FB,6.5); c.drawString(8*mm,31*mm,'GARNISON contestée')
    for i in range(4): _cube(c, 9*mm+i*3.2*mm, 24*mm, RED)
    c.setFillColor(RED); c.setFont(FB,6); c.drawString(9*mm,19*mm,'4 insurgés')
    for i in range(3): _cube(c, 9*mm+i*3.2*mm, 13*mm, BLUE)
    c.setFillColor(BLUE); c.setFont(FB,6); c.drawString(9*mm,8*mm,'3 royaux')
    # DÉS
    _die(c, 52*mm, 25*mm, 5); c.setFillColor(RED); c.setFont(FB,6.5); c.drawString(60*mm,23.5*mm,'4 + 5 = 9')
    _die(c, 52*mm, 12*mm, 4); c.setFillColor(BLUE); c.setFont(FB,6.5); c.drawString(60*mm,10.5*mm,'3 + 4 = 7')
    c.setFillColor(INK); c.setFont(FI if HAS_GI else F,6); c.drawString(46*mm,32*mm,'chacun lance 1d6')
    # flèche
    c.setStrokeColor(GOLD); c.setLineWidth(1.6); c.line(88*mm,20*mm,102*mm,20*mm)
    c.setFillColor(GOLD); p=c.beginPath(); p.moveTo(102*mm,20*mm); p.lineTo(98*mm,22.5*mm); p.lineTo(98*mm,17.5*mm); p.close(); c.drawPath(p,fill=1,stroke=0)
    # APRÈS
    c.setFillColor(HexColor('#3e8e6b')); c.setFont(FB,6.5); c.drawString(106*mm,31*mm,'INSURGÉS l’emportent (9 > 7)')
    c.setFillColor(INK); c.setFont(F,6)
    for i,t in enumerate(['Écart 9 - 7 = 2 : le perdant (royaux)',
                          'retire 2 cubes. Il en reste 1, qui recule',
                          'sur un site voisin ami. Félons : 0 perte.',
                          'La Caserne passe aux insurgés (4 unités).']):
        c.drawString(106*mm,25.5*mm-i*4.4*mm,t)

def build():
    path = os.path.join(HERE, 'livret-regles-royaume.pdf')
    doc = BaseDocTemplate(path, pagesize=A4, title='ROUAGES & COMPLOTS — Livret de règles')
    fr = Frame(18*mm, 18*mm, A4[0]-36*mm, A4[1]-36*mm, id='f')
    doc.addPageTemplates([PageTemplate(id='cover', frames=[fr], onPage=cover),
                          PageTemplate(id='page', frames=[fr], onPage=normal_page)])
    st = []
    from reportlab.platypus import NextPageTemplate
    st.append(NextPageTemplate('page'))
    st.append(PageBreak())

    # ---------- 1. BUT & MATÉRIEL ----------
    st.append(P('1. Le but du jeu', S_H1))
    st.append(P('Vous êtes un notable du régime. Pendant <b>8 tours</b> (les huit levées de la cassette impériale), '
                'vous allez voter, comploter, dormir d’un œil et, quand il le faudra, sortir les bannières. '
                'À la fin, seul compte <b>l’or déposé à votre coffre chez la Banque</b> : le notable le plus riche '
                'au coffre l’emporte. L’or en poche ne vaut rien tant qu’il n’est pas déposé — et il se vole '
                'sur les cadavres. Chacun poursuit de plus une <b>ambition secrète</b> qui rapportera de l’or '
                'au décompte final.'))
    st.append(P('2. Le matériel', S_H1))
    mat = [
        ['1', 'plateau (plan de la capitale, 5 sites, piste des tours)'],
        ['87', 'cartes ACTION (29 différentes × 3 exemplaires)'],
        ['18', 'cartes ÉVÉNEMENT'],
        ['12', 'cartes AMBITION secrète'],
        ['7',  'cartes CHARGE (Empereur, Maréchal, L’Ingénieur, Le Préfet de Police, Ministre d’État, Amiral, Colonel de la Garde)'],
        ['18', 'cartes CASSETTE (le revenu impérial — valeurs 7 à 15)'],
        ['56', 'cartes LIEU : pour chaque joueur, 4 cartes PLANQUE + 4 cartes FILATURE'],
        ['7',  'cartes AIDE DE JEU'],
        ['52', 'francs (40 × « 1 », 12 × « 5 »)'],
        ['40', 'unités (20 cubes rouges insurgés, 20 cubes bleus royaux)'],
        ['14', 'cartes de VOTE : pour chaque joueur, 1 carte POUR + 1 carte CONTRE'],
        ['10', 'marqueurs de contrôle (5 rouges, 5 bleus)'],
        ['2',  'jetons de frappe (canon à vapeur, cuirassé) + 1 marqueur de tour'],
        ['2',  'dés à six faces (1 rouge insurgé, 1 bleu impérial)'],
        ['7',  'pions notables (une couleur par joueur)'],
    ]
    t = Table([[Paragraph('<b>'+a+'</b>', S_BODY), Paragraph(sym_wrap(b), S_BODY)] for a, b in mat],
              colWidths=[14*mm, 158*mm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
                           ('ROWBACKGROUNDS',(0,0),(-1,-1),[HexColor('#f3e9d2'), HexColor('#ece0c4')]),
                           ('TOPPADDING',(0,0),(-1,-1),2.5),('BOTTOMPADDING',(0,0),(-1,-1),2.5)]))
    st.append(t)
    st.append(P('Chaque joueur cache ses <b>francs de poche</b> dans sa main ou derrière un paravent. '
                'Son <b>coffre</b> (francs déposés chez la Banque) reste visible de tous, posé sur sa carte Charge.', S_NOTE))

    # ---------- 3. MISE EN PLACE ----------
    st.append(P('3. Mise en place', S_H1))
    for tx in [
        'Placez le plateau au centre. Mélangez séparément la pioche ACTION, la pile ÉVÉNEMENT et la pioche CASSETTE, toutes face cachée. Marqueur de tour sur la case 1.',
        'Gardez autant de cartes CHARGE que de joueurs : <b>à 4</b>, retirez le Ministre d’État, l’Amiral et le Colonel de la Garde ; <b>à 5</b>, retirez l’Amiral et le Colonel ; <b>à 6</b>, retirez seulement le Colonel ; <b>à 7</b>, gardez tout. Distribuez-en une à chacun, face visible. Celui qui reçoit <b>L’Empereur</b> monte sur le trône.',
        'Chacun reçoit ses 8 cartes LIEU (4 Planque, 4 Filature), ses <b>2 cartes de vote</b> (POUR / CONTRE), une aide de jeu, et pioche <b>2 cartes ACTION</b> (3 pour le Ministre d’État).',
        'Mélangez les AMBITIONS et distribuez-en une à chacun, <b>face cachée</b>. Regardez-la, ne la montrez à personne.',
        'L’Ingénieur prend le jeton canon à vapeur, l’Amiral le jeton cuirassé.',
    ]:
        st.append(LI(tx))
    st.append(Spacer(1, 3*mm))
    st.append(Diagram(174*mm, 96*mm, diagram_setup,
        'Schéma 1 — La table en début de partie (exemple à 5 notables).'))
    st.append(Spacer(1, 2*mm))
    st.append(P('Votre zone de jeu — où poser chaque carte :', S_H2))
    st.append(Diagram(174*mm, 66*mm, diagram_player,
        'Schéma 2 — Devant vous : Charge (avec le coffre visible), Ambition et Planque face cachées, main d’Action, poche cachée.'))

    # ---------- 4. TOUR DE JEU ----------
    st.append(P('4. Le tour de jeu — cinq phases', S_H1))
    st.append(P('① La cassette impériale', S_H2))
    st.append(P('L’Empereur <b>pioche une carte CASSETTE</b> et la regarde sans la montrer : c’est le revenu du régime '
                'ce tour (un nombre entre 7 et 15). Il la garde <b>face cachée</b> devant lui et propose à voix '
                'haute une répartition : « tant pour untel, tant pour untel… ». Il n’annonce pas le total — '
                'les notables votent sans savoir combien l’Empereur garde pour lui. <i>Ce qui n’est pas donné file dans '
                'sa poche.</i>'))
    st.append(P('② Le vote du Conseil', S_H2))
    st.append(P('Chacun peut d’abord jouer, face visible, ses <b>cartes bonus</b> de la main (VOTE ou FRANCS ; '
                'elles se défaussent) — Faux en écriture, Appui du Sénat, etc. ajoutent des voix. Puis chaque notable prend '
                'sa carte <b>POUR</b> ou sa carte <b>CONTRE</b> et la pose <b>face cachée</b> devant lui.'))
    st.append(P('Quand tout le monde est prêt, on <b>retourne toutes les cartes en même temps</b>. Les votes sont '
                '<b>visibles de tous</b> — mais comme chacun s’est engagé en aveugle, impossible de suivre le '
                'mouvement à la dernière seconde. Voix : 1 par notable vivant, <b>2 pour le Ministre d’État</b>, plus les '
                'cartes bonus. L’Empereur vote aussi. Plus de POUR que de CONTRE = <b>adopté</b>.', S_NOTE))
    st.append(P('<b>Adopté</b> : chacun prend les francs promis (en poche), l’Empereur prend discrètement le reste '
                '(valeur de la carte moins les dons) et <b>glisse la carte CASSETTE face cachée devant lui</b>, '
                'dans sa réserve impériale — <i>sans la montrer</i>. Le total reste secret : nul ne sait vraiment '
                'combien l’Empereur s’est engraissé. <b>Rejeté</b> : toute la cassette retourne à la réserve (l’Empereur ne '
                'garde rien), la carte va à la défausse, et il lance 1d6 — sur <b>4-6</b>, l’insurrection gronde '
                '(voir phase ⑤).'))
    st.append(P('Pourquoi une carte plutôt qu’un dé ? Parce qu’un dé secret ne laisse aucune trace : l’Empereur '
                'pourrait annoncer n’importe quel total. La carte, elle, est un <b>engagement matériel</b> — un '
                'objet unique, choisi avant la proposition, posé face cachée et impossible à changer après coup. '
                'Le total reste caché (le bluff est intact), mais la table garde un recours : à tout moment, un '
                '<b>vote à la majorité exige l’audit</b> — l’Empereur retourne sa carte, et l’on vérifie au moins qu’il '
                'n’a pas promis plus de francs que la carte n’en contenait. Un Empereur pris en flagrant délit rend le '
                'surplus et récolte les rancunes. Simple garde-fou de confiance entre amis, pas un contrôle '
                'fiscal : à vous de vous surveiller.', S_NOTE))
    st.append(P('③ La nuit', S_H2))
    st.append(P('Voir le chapitre 5 — c’est le cœur du jeu : planques, dagues et coffres.'))
    st.append(P('④ Le crieur', S_H2))
    st.append(P('Révélez la première carte ÉVÉNEMENT et appliquez-la immédiatement. '
                '(« Jacquerie » fait gronder l’insurrection ; « Grande foire » l’annule pour ce tour.)'))
    st.append(P('⑤ L’insurrection (si elle gronde)', S_H2))
    st.append(P('Si l’insurrection a été déclenchée ce tour — vote rejeté malheureux, Roi assassiné cette nuit, '
                'ou Jacquerie — et qu’aucune Grande foire ne l’annule : jouez l’insurrection (chapitre 6). '
                'Sinon, passez.'))
    st.append(P('Fin de tour', S_H2))
    st.append(P('Chacun pioche <b>1 carte ACTION</b> (2 pour le Ministre d’État, +1 pour qui a dormi à son Hôtel particulier). '
                'Main limitée à 7 cartes (défaussez l’excédent). Les notables morts ce tour <b>reviennent</b> : '
                '« un cousin reprend le fief » — même charge, poche vide. '
                'Avancez le marqueur de tour.'))

    # ---------- 5. LA NUIT ----------
    st.append(P('5. La nuit', S_H1))
    st.append(P('A. Choix simultanés', S_H2))
    st.append(P('Chaque notable pose devant lui une carte <b>PLANQUE face cachée</b> : Hôtel particulier, Banque, '
                'Cocotte ou Ambassade. Ceux qui veulent attaquer posent EN MÊME TEMPS, face cachée sur leur cible : '
                'une carte d’attaque de leur main (Spadassin, Baril de poudre…) et une carte <b>FILATURE</b> '
                '(le lieu où ils pensent trouver la cible). Le Préfet de Police peut attaquer sans carte '
                'd’attaque (son privilège, une fois par nuit) — il pose seulement sa Filature.'))
    st.append(Spacer(1, 2*mm))
    st.append(Diagram(174*mm, 48*mm, diagram_night,
        'Schéma 3 — Une attaque : posez votre carte d’attaque + votre Filature, face cachée, sur la zone de la cible. Tout se révèle ensuite en même temps.'))
    st.append(Spacer(1, 2*mm))
    st.append(P('B. Révélation', S_H2))
    st.append(P('Toutes les planques se révèlent en même temps. Puis chaque attaque se résout, dans le sens '
                'horaire en partant de l’Empereur :'))
    for tx in [
        '<b>Filature ratée</b> (le lieu deviné n’est pas la planque de la cible) : rien ne se passe. L’Espion à la cour ignore la Filature : il touche toujours (sauf Ambassade).',
        '<b>Ambassade</b> : intouchable, l’attaque échoue toujours.',
        '<b>Empoisonneuse</b> : lancez 1d6, échec sur 1-3.',
        '<b>Garde du corps</b> de la cible : l’attaque échoue (sauf poison), la carte est défaussée.',
        '<b>Sosie</b> : la cible lance 1d6, elle survit sur 4-6 ; la carte est défaussée dans tous les cas.',
        '<b>Sinon la cible meurt</b> : couchez son pion. L’attaque est publique (tout le monde a vu la carte jouée). Le tueur prend la poche de la cible — sauf Coffre scellé. Baril de poudre et Coffret piégé détruisent la poche au lieu de la voler.',
        'Une cible peut se protéger (Garde du corps, Sosie) — voir ci-dessus.',
        'Si le <b>Roi</b> meurt : l’insurrection gronde pour ce tour.',
    ]:
        st.append(LI(tx))
    st.append(P('C. Dépôts et petits matins', S_H2))
    for tx in [
        '<b>Banque</b> : déposez toute votre poche sur votre coffre (visible, définitif, imprenable).',
        '<b>Cocotte</b> : prenez 1 franc de la réserve et un jeton ☾.',
        '<b>Ambassade</b> : prenez un jeton ☦ (et l’écu du Pèlerinage si l’événement est actif).',
        '<b>Hôtel particulier</b> : vous piocherez 1 carte de plus en fin de tour.',
    ]:
        st.append(LI(tx))
    st.append(P('Exemple — la Castiglione pose sa Planque « Cocotte ». Morny l’attaque avec un Homme de main et une '
                'Filature « Banque » : raté, elle n’y était pas. Mais elle a bien vu qu’on la visait… et saura qu’on lui en veut.', S_EX))

    # ---------- 6. LA RÉVOLTE ----------
    st.append(P('6. L’insurrection des notables', S_H1))
    st.append(P('A. Les camps', S_H2))
    st.append(P('L’Empereur est toujours <b>impérial</b>. En partant de sa gauche, chacun annonce son camp : '
                '<b>insurgé</b> (rouge) ou <b>impérial</b> (bleu). Chacun peut alors jouer des '
                'cartes RÉVOLTE de sa main : elles ajoutent des unités à déployer. Si personne n’est insurgé, '
                'le calme revient. Si personne ne défend, l’Empire tombe sans combat (voir E).'))
    st.append(P('B. Manche 1 — le déploiement', S_H2))
    st.append(P('Chaque notable dispose d’unités égales à sa <b>charge</b> (Maréchal 4, Garde 3, Roi 3, '
                'Engins / Assassins / Amiral 2, Ministre d’État 1) plus ses cartes RÉVOLTE jouées. En commençant par '
                'l’Empereur puis dans le sens horaire, chacun pose TOUTES ses unités (cubes de la couleur de son camp) '
                'sur les sites de son choix. <b>Le Palais est interdit au déploiement insurgé</b> — il faudra le '
                'prendre d’assaut. Posez un marqueur de contrôle bleu sur chaque site au début (le régime tient la ville).'))
    st.append(Spacer(1, 2*mm))
    st.append(Diagram(174*mm, 86*mm, diagram_revolt,
        'Schéma 4 — Une insurrection en cours : cubes déployés, routes et mouvements (assaut insurgé sur le Palais).'))
    st.append(P('C. Manches 2 et 3', S_H2))
    st.append(P('Dans l’ordre : <b>pouvoirs des sites</b>, puis <b>mouvements</b>, puis <b>frappes</b>, puis <b>batailles</b>.'))
    for tx in [
        '<b>Pouvoirs</b> — un site est « tenu » si un seul camp y a des unités : Caserne = +1 unité de renfort sur place · Notre-Dame = retirez 1 unité ennemie du plus gros groupe adverse · Banque de France = un notable du camp peut payer 2 francs de poche pour poser 1 unité sur la Banque de France · Gare = pendant les mouvements, les unités partant de la Gare peuvent aller sur N’IMPORTE QUEL site.',
        '<b>Mouvements</b> — insurgés d’abord : chaque unité peut se déplacer vers un site adjacent (routes du plateau). Une unité arrivée ne rebouge plus cette manche.',
        '<b>Frappes</b> — une fois par insurrection : l’Ingénieur (canon à vapeur) et/ou l’Amiral (cuirassé) peuvent frapper n’importe quel site occupé par l’ennemi et y détruire jusqu’à 2 unités. Rendez le jeton une fois utilisé.',
        '<b>Batailles</b> — sur chaque site où les deux camps sont présents : chaque camp fait <b>ses unités + 1 dé</b> (dé rouge insurgé, dé bleu impérial). Le plus grand total gagne (égalité : le camp qui contrôlait le site tient). <b>Le perdant retire autant de cubes que l’ÉCART entre les deux totaux</b> (au maximum tous ses cubes) ; le vainqueur ne perd rien. Les cubes qui restent au perdant reculent vers un site adjacent ami (sinon anéantis). Mettez à jour les marqueurs de contrôle.',
    ]:
        st.append(LI(tx))
    st.append(Spacer(1, 2*mm))
    st.append(Diagram(174*mm, 42*mm, diagram_battle,
        'Schéma 5 — Exemple de bataille résolue aux dés (chaque camp : ses unités + 1d6, insurgés d’abord).'))
    st.append(P('D. Le décompte', S_H2))
    st.append(P('Après la manche 3 : chaque site contrôlé vaut 1 point, <b>les Tuileries 2</b> (6 points en tout). '
                'Les insurgés l’emportent avec <b>4 points ou plus</b>.'))
    st.append(P('E. Accession au trône et peloton', S_H2))
    st.append(P('<b>Félons vainqueurs</b> : le insurgé à la plus grosse armée de charge (Maréchal 4 > Garde 3 > '
                'Engins / Assassins / Amiral 2 > Ministre d’État 1 ; égalité : le plus riche au coffre) prend la couronne, '
                'pose un jeton ♛, échange sa carte Charge contre L’Empereur et <b>redistribue les charges libérées</b> '
                'comme il l’entend. Le nouvel Empereur peut envoyer un vaincu au <b>peloton</b> : le condamné pose un '
                'jeton †, sa poche revient à l’Empereur — sauf s’il joue un Sauf-conduit. <b>Royaux vainqueurs</b> : '
                'l’Empereur garde sa couronne et peut envoyer un insurgé au peloton, mêmes règles. Les exécutés et morts '
                'reviennent au tour suivant (le cousin).'))

    # ---------- 7. AMBITIONS SANS MAÎTRE DU JEU ----------
    st.append(P('7. Objectifs secrets — vérifiés sans arbitre', S_H1))
    st.append(P('Chacun a tiré un objectif secret en début de partie. Comment le prouver à la fin, sans '
                'maître du jeu ? Parce que chaque objectif se vérifie de deux façons seulement — <b>sans jamais '
                'rien noter ni distribuer de jetons pendant la partie</b> :', S_BODY))
    st.append(P('1. D’un coup d’œil, à la fin', S_H2))
    st.append(P('La plupart se lisent directement sur la table au décompte : <b>qui est sur le trône</b>, '
                'l’<b>argent</b> (poche et banque, montrés à ce moment), les <b>pions encore debout</b>. Rien à suivre.'))
    st.append(P('2. Un seul fait marquant', S_H2))
    st.append(P('Les autres tiennent à un <b>événement rare et spectaculaire que toute la table a vu</b> — un '
                'Empereur assassiné, une insurrection gagnée. Ça ne s’oublie pas ; en cas de doute, la table '
                'tranche à la majorité. Fini les jetons de trace : on regarde, on se souvient, on tranche.', S_NOTE))
    tab_amb = [
        ['Objectif secret', 'Comment on vérifie, à la fin'],
        ['L’Empereur (+4)', 'vous êtes sur le trône'],
        ['Le Régicide (+4)', 'vous avez tué un Empereur (une nuit que tout le monde a vue)'],
        ['L’Insurgé (+3)', 'vous avez gagné une insurrection dans le camp insurgé'],
        ['Le Pilier du régime (+3)', 'vous avez gagné une insurrection dans le camp impérial'],
        ['Le Rentier (+3)', 'poche à 0, et 6 francs ou plus en banque (montrés au décompte)'],
        ['Le Magot (+3)', 'la plus grosse poche de la table (montrée au décompte)'],
        ['L’Opposant (+3)', 'votre pion est debout, mais vous n’êtes pas sur le trône'],
        ['L’Immortel (+3)', 'vous n’êtes jamais mort ni déporté'],
        ['Le Discret (+2)', 'vous n’avez jamais été Empereur'],
        ['L’Assassin (+2)', 'vous avez tué au moins un notable'],
        ['Le Magnat (+2)', '10 francs ou plus en banque'],
        ['Le Revenant (+2)', 'mort au moins une fois, mais debout à la fin'],
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
        'Titre d’honneur (facultatif, +1 franc) : ⚜ le Grippe-sou — la plus grosse poche à la fin (record strict ; égalité : personne). Un seul, visible au décompte, rien à suivre.',
        'Le notable au coffre le plus garni l’emporte. Égalité : la plus grosse poche départage.',
    ]:
        st.append(LI(tx))
    st.append(P('« On n’a jamais vu un régime si bien géré », dira le chroniqueur. Il était payé pour.', S_EX))

    doc.build(st)
    print('OK', path)

if __name__ == '__main__':
    build()
