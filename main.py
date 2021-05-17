import pygame as g
import random as r
from time import sleep
import math as m


def INIT():
    global screen, IS_FULLSCREEN, size, w, h
    
    TITLE="Aygaran's Quest"
    size = (800, 600)
    w, h = size
    screen = g.display.set_mode(size) #, g.FULLSCREEN)
    IS_FULLSCREEN = 0
    g.display.set_caption(TITLE)

g.init()
INIT()
clock = g.time.Clock()
font = g.font.Font("Assets/fonts/font.ttf", 20)
BIGfont = g.font.Font("Assets/fonts/title.ttf", 64)


###################

class player:
    def __init__(self, x, y, img):
        Mw, Mh = 30, 30
        self.o = g.Rect(x, y, Mw, Mh)
        
        self.img = g.transform.scale(g.image.load(img), (Mw+20, Mh+20))
        self.Pimg = self.img
        self.Patk = g.transform.scale(g.image.load('Assets/skeletob_atk.png'), (Mw+20, Mh+20))
        self.Pstand = self.Pimg
        self.Pruot = 0
        
        self.img_spost = 0
        self.xspid, self.yspid = 0,0
        self.room = 0
        self.Proom = 0
        self.attackrange = (50, 40)
        WI, HE = self.attackrange
        self.attackbox = g.Rect(0,0, WI, HE)
        self.BOXX = self.o.x+50
        self.selected_spell = 0
        
        self.spells = [
            SPELL('heal', 'restores 5 hp', 1, 0, g.image.load('Assets/heal.png')),
            SPELL('shockwave', 'fucks enemies around you', 3, 0, g.transform.scale(g.image.load('Assets/shock.png'), (800, 600))),
            SPELL('Big Blood Magic Thing', 'turns 5 hp to 1 mana', 0, 1, g.transform.scale(g.image.load('Assets/hptmp.png'), (800, 600)))
        ]
        self.lvl = 0
        self.pointz = 0
        self.mana = 0
        self.maxhp = 20
        self.hp = 20
        self.danno = 1
        self.knockback = 10
        self.dif = 0
        
        self.inv = []
    
    def renderbox(self):
        WI, HE = self.attackrange
        if self.xspid > 0: self.BOXX = self.o.x+30
        elif self.xspid < 0: self.BOXX = self.o.x-WI-5
        self.attackbox = g.Rect(self.BOXX, self.o.y, WI, HE)

class SPELL:
    def __init__(self, name, description, cost, required, animation=0):
        self.name = name
        self.description = description
        self.cost = cost
        self.rlvl = required
        self.ani = animation


def GETIMG(arg, self):
    return g.transform.scale(g.image.load(f'Assets/{arg}'), (self.l, self.l))

class nemico:
    def __init__(self, x, y, mytype):

        codex = [
            ('orc', 1, 2, 1, 0, 30, []),
            ('spider', 3, 1, 3, 0, 40, ['tooth']),
            ('troll', 5, 1, 3, 0, 50, ['bat']),
            ('pig', 1, 1, 5, 0, 50, ['porckchop']),
        ]
        
        ##                                                            hitbox
        self.index = mytype
        self.name, self.hp, self.spid, self.danno, self.die_on_hit,  self.l, self.drop = codex[int(mytype)] # ninni type è li
        self.o = g.Rect(x, y, self.l, self.l)
        
        self.anim = [GETIMG(f'{self.name}1.png', self), GETIMG(f'{self.name}2.png', self), GETIMG(f'{self.name}3.png', self), GETIMG(f'{self.name}4.png', self)]
        self.AnimIndex = 0
        self.img = self.anim[self.AnimIndex]
        self.AnimTic = r.randint(1, 12)
        

        self.xspid = 1
        
        self.Pimg = self.img
        self.Pstand = self.Pimg
        self.Pruot = 0
        self.img_spost = 0

    def animate(self):
        self.AnimTic += 1
        if self.AnimTic % 20 == 0:
            self.AnimIndex += 1
            if self.AnimIndex >= len(self.anim): self.AnimIndex = 0
            self.Pimg = self.anim[self.AnimIndex]


class room:
    def __init__(self, up, right, down, left, img, nems, uscita=0):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.nears = [up, right, left, down]
        self.uscita = uscita
        
        #print('Assets/map/'+img+'.png')
        self.img = g.transform.scale(g.image.load('Assets/map/'+img+'.png'), (w, h))         ## w, h = size dello scrin
        self.nems = []
        for i in nems:
            self.nems.append(nemico(r.randint(0,w), r.randint(0,h), i))





##################

def reset():
    global map, pl, nemici
    
    map = DUNGEON[livello].copy()
    
    nemici = []
    
    pl.room = 0
    pl.Proom = 0

def sposta(gio):
    Proom = gio.room
    if gio.o.x >= w-10:
        gio.room = map[gio.room].right
        if Proom!=gio.room: gio.o.x = 50
        else: gio.o.x = w-10
        
    if gio.o.x <= 0:
        gio.room = map[gio.room].left
        if Proom!=gio.room: gio.o.x = w-50
        else: gio.o.x = 10
        
    if gio.o.y <= 0:
        gio.room = map[gio.room].up
        if Proom!=gio.room: gio.o.y = h-50
        else: gio.o.y = 10
        
    if gio.o.y >= h-10:
        gio.room = map[gio.room].down
        if Proom!=gio.room: gio.o.y = 50
        else: gio.o.y = h-10
    
    return gio


def pl_render(pl):
    
    if pl.xspid > 0:
        pl.Pruot = 1
    elif pl.xspid < 0:
        pl.Pruot = 0
        pl.img_spost = -20
    
    pl.img = g.transform.flip(pl.Pimg, 1, 0) if pl.Pruot else pl.Pimg
        
    screen.blit(pl.img, (pl.o.x+pl.img_spost, pl.o.y))


def GenDungeon(Oposs, lun):
    buff = []
    poss = Oposs.copy()
    
    diffs = len(poss)
    count = m.ceil(lun/diffs)
    
    for i in poss:
        for j in range(count):
            try:
                A = r.choice(poss[i])
                buff.append(A)
                poss.remove(A)
            except: 0

    return buff


def GAMEOVER():
    global run, splash
    splash = 'You died and your corpse was eaten by rats'
    run = 0

def WIN():
    global run, splash
    splash = 'You escaped the dungeon! Ready to start all over again!'
    run = 1




def spell_menu(screen):
    pl.mana = round(pl.mana, 1)
    
    try:
        LVL = str(pl.lvl).split(".")[0]+str(pl.lvl).split(".")[1][0]
    except:
        LVL = str(pl.lvl)
    
    actuel = pl.spells[pl.selected_spell]
    
    menu = g.Surface((w, 70))
    menu.fill((50, 50, 50))
    
    menu.blit(font.render('>  ' + actuel.name + '  <', 0, (0, 200, 0)), (10, 5))
    menu.blit(font.render(actuel.description,0,(0,200,0)), (10, 30))
    menu.blit(font.render(f'requires mp: {actuel.cost}    lvl: {actuel.rlvl}', 0, (0, 200, 0)), (10, 50))
    
    menu.blit(font.render(f' |         you', 0, (0,200,0)), (400, 5))
    menu.blit(font.render(f' |         mp: {pl.mana}    lvl: {LVL}', 0, (0,200,0)), (400, 30))
    menu.blit(font.render(f' |', 0, (0,200,0)), (400, 50))
    
    screen.blit(menu, (0, h-70))

def CAST(spell):    
    actuel = pl.spells[spell]
    #print(actuel.name)
    if pl.lvl >=  actuel.rlvl:
        if pl.mana >= actuel.cost:
            pl.mana -= actuel.cost
            global OnScreenSpell
            OnScreenSpell = actuel.ani
            
            if actuel.name == 'heal':
                pl.hp += 5
                if pl.hp > pl.maxhp:
                    pl.hp = pl.maxhp
        
            if actuel.name == 'shockwave':
                for boi in nemici:
                    boi.hp -= 2
                    if boi.hp <= 0:
                        nemici.remove(boi)
            
            if actuel.name == 'Big Blood Magic Thing':
                pl.mana += 5
                pl.hp -= 1
                if pl.hp <= 0:
                    GAMEOVER()

#######

dial_letter = 0
blecbox = g.Surface((w,60))
blecbox.fill((0,0,0))
dial_text = ''

VOICE = g.mixer.Sound('Assets/voice.wav')

def dialogue(text):
    global dial_letter, dial_text

    if text != dial_text:
        dial_letter = 0
        dial_text = text
        
    screen.blit(blecbox, (0,0))
    screen.blit(font.render(text[:dial_letter], 0, (0,255,0)), (10, 20))
    if dial_letter<len(text) and tic%30:
        dial_letter+=1
        g.mixer.Sound.play(VOICE)
    

##title screen

class button:
    def __init__(self, rect, name):
        self.rect = rect
        self.name = name

def do(ds):
    global jen
    global bigboi
    
    if ds == 'play':
        jen = False
    elif ds == 'controls':
        bigboi = g.image.load('Assets/howtoplay.png')
    elif ds == 'credits':
        bigboi = g.image.load('Assets/credits.png')

            
BACKIMG = g.transform.scale(g.image.load('Assets/beckimg.jpg'), (800, 600))
def TitleScreen():
    global bigboi
    global jen
    global game
    
    buttonz = [
        button(g.Rect(100, 150, 130, 30), 'play'),
        button(g.Rect(100, 240, 130, 30), 'controls'),
        button(g.Rect(100, 280, 130, 30), 'credits'),
    ]

    mousebop = g.Rect(12, 12, 12, 12)
    while jen:
        mousebop.x, mousebop.y = g.mouse.get_pos()
        for ev in g.event.get():
            if ev.type == g.QUIT:
                if bigboi: bigboi = ''
                else:
                    g.quit()
                    exit(0)
            
            if ev.type == g.KEYDOWN and ev.key == g.K_x: bigboi = ''
            
            if ev.type == g.KEYDOWN and ev.key == g.K_ESCAPE: do('start') 
                
            if ev.type == g.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for boi in buttonz:
                        if boi.rect.colliderect(mousebop):
                            do(boi.name)
                            
                    
        
        screen.fill((50, 50, 50))
        screen.blit(BACKIMG, (0,0))
        
        for boi in buttonz:
            gu = font.render(boi.name, True, (50, 255, 50))
            g.draw.rect(screen, (100, 100, 100), boi.rect)
            screen.blit(gu, (boi.rect.x, boi.rect.y))
        
        try: screen.blit(bigboi, (0, 0))
        except: 0
        
        screen.blit(BIGfont.render('Ayngaran\'s Quest', 0, (0, 255, 0)), (100, 0))
        screen.blit(font.render(splash, 0, (0, 255, 0)), (100, 70))
        
        g.display.flip()
        clock.tick(60)



###

BOSSES = {
    'PeaNut': 'use arrows to dodge bas spikes, collect green stuff',
    'Fancy Space Boi': 'your ship will follow your mouse, click to fire.\nStop all opponent\'s ship by destroing them.',
    'an empty room': 'just wait a bit :|',
    'an empty room': 'just wait a bit :|',
    'an empty room': 'just wait a bit :|',
}

BOSSNAMES = []
for i in BOSSES: BOSSNAMES.append(i)
        
jen = True
bigboi = ''
game = True
splash = 'Return to Nadesan\'s Mine!'


MUSI=1

music = g.mixer.Sound('Assets/main.wav')
g.mixer.Sound.play(music, -1)


while game:
    jen = True
    
    TitleScreen()

    ############ dungeon generation

    screen.fill((0,0,0))
    screen.blit(font.render('loading...',0,(0,255,0)),(350,300))
    g.display.flip()

    EXIT = 1

    with open('levels.py', 'r') as f:
        exec(f.read())

    DUNGEON = GenDungeon(PossibleLevels, 5)


    #########
    
    pl = player(int(w/2), int(h/2), 'Assets/skeletob.png')

    livello = 0
    reset()

    exitrect = g.Rect(int(w/2)-15, int(h/2)-15, 50, 50)

    nemici = []
    ATKING = 0
    ATKED = 0
    ATKCOOL = 40
    SpellMenu = 0
    OnScreenSpell = 0
    SHOWTIME = 50 # ticks


    tic = 1
    run = True
    while run:
        for ev in g.event.get():
            if ev.type == g.QUIT:
                exit(0)
                MUSIC.duit=0
        
            ################################################  COMMANDS
            if ev.type == g.KEYDOWN:
                if ev.key == g.K_ESCAPE:
                    screen = g.display.set_mode(size)
            
                if ev.key == g.K_f:
                    if IS_FULLSCREEN:
                        screen = g.display.set_mode(size)
                        IS_FULLSCREEN = 0
                    else:
                        g.display.set_mode(size, g.FULLSCREEN)
                        IS_FULLSCREEN = 1
            
                if ev.key == g.K_w:
                    pl.yspid -= 5
                if ev.key == g.K_s:
                    pl.yspid += 5
                if ev.key == g.K_a:
                    pl.xspid -= 5
                if ev.key == g.K_d:
                    pl.xspid += 5
                    
                if ev.key == g.K_SPACE:
                    ATKING = 1
                    pl.Pimg = pl.Patk
                
                
                if ev.key == g.K_e:
                    CAST(pl.selected_spell)
                
                if ev.key == g.K_q:
                    SpellMenu = not SpellMenu
                
                if SpellMenu:
                    if ev.key == g.K_UP:
                       pl.selected_spell += 1
                       if pl.selected_spell == len(pl.spells):
                           pl.selected_spell = 0
                    
                    if ev.key == g.K_DOWN:
                       pl.selected_spell -= 1
                       if pl.selected_spell == -1:
                           pl.selected_spell = len(pl.spells)-1
            
            if ev.type == g.KEYUP:
            
                if ev.key == g.K_w:
                    pl.yspid += 5
                if ev.key == g.K_s:
                    pl.yspid -= 5
                if ev.key == g.K_a:
                    pl.xspid += 5
                if ev.key == g.K_d:
                    pl.xspid -= 5
                
                #if ev.key == g.K_SPACE:
                #    ATKING = 0
        
        #######################################################  MECHANICS
        
        
        
        pl.o.x += pl.xspid
        pl.o.y += pl.yspid
        
        pl = sposta(pl)
        if pl.room != pl.Proom:
            map[pl.Proom].nems = nemici
            pl.Proom = pl.room
            nemici = []
            for i in map[pl.room].nems:
                nemici.append(i)
        
        for i in nemici:
            
            i.animate()
            
            if i.o.x >= pl.o.x:
                i.o.x -= i.spid
                i.xspid = -1
            if i.o.x <= pl.o.x:
                i.o.x += i.spid
                i.xspid = 1
            if i.o.y >= pl.o.y:
                i.o.y -= i.spid
            if i.o.y <= pl.o.y:
                i.o.y += i.spid
            
            
            if ATKING:
                if i.o.colliderect(pl.attackbox):
                    ATKED = 1
                    i.hp -= pl.danno
                    if i.hp <= 0:
                        nemici.remove(i)
                        pl.mana += 0.1
                        if i.drop != []:
                            pl.inv.append(r.choice(i.drop))
                        pl.lvl += 0.1*i.index
            if i.o.colliderect(pl.o) and not ATKED:
                    i.o.x-=(40+pl.knockback)*r.choice([0,1])
                    i.o.x-=(40+pl.knockback)*r.choice([0,1])
                    pl.hp -= i.danno
                    if pl.hp <= 0: GAMEOVER(); break
        
        
        if ATKED or (ATKING and tic%ATKCOOL==0):
            ATKED = 0
            ATKING = 0
            pl.Pimg = pl.Pstand
        
        if map[pl.room].uscita and pl.o.colliderect(exitrect) and ATKING:
            
            g.mixer.pause()
            with open(f'BOSSES/intro.py', 'r') as f:
                exec(f.read())
                
            BOSSINTRO(BOSSNAMES[livello], BOSSES[BOSSNAMES[livello]])
            
            music = g.mixer.Sound(f'Assets/bosses/boss{livello}-theme.wav')
            VOICE = g.mixer.Sound(f'Assets/bosses/voice{livello}.wav')
            
            g.mixer.Sound.play(music, -1)
            screen.fill((0,0,0))
            with open(f'BOSSES/boss{livello}.py', 'r') as f:
                exec(f.read())
            
            pl.xspid = pl.yspid = 0
            OUT, pl.hp = BOSS(pl.hp)
            if not OUT:
                GAMEOVER()
            INIT()
            VOICE = g.mixer.Sound('Assets/voice.wav')
            
            g.mixer.pause()
            music = g.mixer.Sound(f'Assets/main.wav')
            g.mixer.Sound.play(music, -1)
            
            livello += 1
            if len(DUNGEON) > livello:
                reset()
            else:
                WIN()
                break
        
        
        
        ####################################################### GRAPHICS
        screen.fill((50, 50, 50))
        screen.blit(map[pl.room].img, (0,0))
        
        if map[pl.room].uscita:
            screen.blit(g.transform.scale(g.image.load('Assets/exit.png'), (exitrect.width, exitrect.height)), (exitrect.x, exitrect.y))
        
        for i in nemici:
            pl_render(i)
        
        if OnScreenSpell:
            if tic%SHOWTIME:
                screen.blit(OnScreenSpell, (0,0))
            else:
                OnScreenSpell = 0
        
        pl_render(pl)
        #g.draw.rect(screen, (0, 255, 0), pl.o)
        
        pl.renderbox()
        #g.draw.rect(screen, (255, 0, 0), pl.attackbox)
        
        if SpellMenu:
            spell_menu(screen)
            
        if tic < 200: dialogue('(?): Welcome to the dungeon!')
        screen.blit(font.render(f'room: {pl.room}    hp: {pl.hp}', 0, (0,255,0)), (10, 60))
        
        g.display.flip()
        clock.tick(60)
        tic += 1
