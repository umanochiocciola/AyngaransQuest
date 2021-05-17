def BOSS(hp):
    from math import ceil
    size = (600, 600)
    w, h = size

    screen = g.display.set_mode(size)

    texts=[
        'Pew! Pew! Pew!',
        'My space army will destroy you!',
        'Surrender now!',
        'Stop ruining my ships!',
        'If you do the good boy, I\'ll crush you more gently',
        'I\'MMA FIRIN\' MA LAZOR... Ah good old times',
        'I have an unlimited army!'
    ]
    
    tec = 0

    class ship:
        def __init__(self, hp, bigganza, x, y):
            self.o = g.Rect(x, y, bigganza, bigganza)
            self.hp = hp

    titl = 1
    mousec = g.Rect(0,0,5,5)
    ple = g.Rect(int(w/2)-40, int(h*(3/4)), 80, 40)
    g.mouse.set_visible(True)

    is_blink = 0
    blinkrate = 5
    blinktic = 0
    
    SCORE = 0
    pl = ship(ceil(hp/5), 30, 200, 500)
    
    
    spari = []
    firerate = 10

    nemici = []
    spawnrate = 70

    #MOUSE CONFIGURATION
    holdin = 0

    run = True
    tic = 0
    g.mouse.set_visible(False)
    while run:
        for ev in g.event.get():
            if ev.type == g.QUIT:
                g.quit()
                exit(0)
                
            if ev.type == g.MOUSEBUTTONDOWN and ev.button == 1:
                holdin = 1
            
            if ev.type == g.MOUSEBUTTONUP and ev.button == 1:
                holdin = 0
        
        #-----------------------------------------------  MECHANICS  & MOVEMENT
        
        if tic%spawnrate==0:
            sas = r.randint(2, 7)
            nemici.append(ship(sas, sas*10, r.randint(0,w-sas*10), 0))
        
        if holdin and tic%firerate==0:
            spari.append(g.Rect(pl.o.x+10, pl.o.y, 5, 5))
        
        pl.o.x, a = g.mouse.get_pos()
        if pl.o.x >= w-pl.o.width: pl.o.x = w-pl.o.width
        
        for i in nemici:
            i.o.y += int(tic/1000)+2
            
            if i.o.y >= h:
                nemici.remove(i)
                pl.hp -= 1
                is_blink = 1
                blinktic = 0
                continue
            
            if i.o.colliderect(pl.o):
                pl.hp-=1
                nemici.remove(i)
                is_blink = 1
                blinktic = 0
                continue
            
            for s in spari:
                if i.o.colliderect(s):
                    spari.remove(s)
                    i.hp-=1
                    if i.hp <= 0:
                        is_blink = 1
                        blinktic = 0
                        nemici.remove(i)
                        SCORE += 1
        
        for i in spari:
            i.y -= 10
        
        if pl.hp <= 0:
            return 0, 0
        
        if SCORE>=20:
            return 1, pl.hp*5
            
        
        #-----------------------------------------------  DRAW
        screen.fill((0,10,0))
        if is_blink:
            screen.fill((255,255,255))
            blinktic += 1
            if blinktic >= blinkrate: is_blink = 0
        
        screen.blit(g.transform.scale(g.image.load('Assets/bosses/core.png'), (pl.o.width, pl.o.height)), (pl.o.x, pl.o.y))
        
        for i in spari:
            g.draw.rect(screen, (0, 255, 0), i)
        
        for i in nemici:
            screen.blit(g.transform.scale(g.image.load('Assets/bosses/nem.png'), (i.o.width, i.o.height)), (i.o.x, i.o.y))
        
        screen.blit(font.render(f'{"<3 "*pl.hp}    score: {SCORE}/20', 0, (0, 255, 0)), (10, 60))
        
        dialogue(texts[tec])
        if tic%300 == 0:
            tec += 1
            if tec >= len(texts):
                tec = 0
        
        g.display.flip()
        clock.tick(60)
        tic += 1