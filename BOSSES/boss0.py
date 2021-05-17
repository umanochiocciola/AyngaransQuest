def BOSS(hp):
    #import pygame as g
    #import random as r
    
    texts=[
        'PeaNut, king of every dried fruit!',
        'Get salty!',
        'Wanna some cashews?',
        'Almonds are sexy...',
        'Hazelnuts are great too...',
        'but nothing\'s like peanuts!',        
    ]
    
    tec = 0
    
    
    font = g.font.Font("Assets/fonts/font.ttf", 32)

    size = (600, 600)
    w = 600

    screen = g.display.set_mode(size)

    g.display.set_caption('BOSSFIGHT!')

    clock = g.time.Clock()
    tic = 1

    player = g.Rect(300, 500, 20, 20)

    star = g.image.load('Assets/bosses/star.png')
    bad = g.image.load('Assets/bosses/bad.png')


    s = 0

    score = 0

    pic = []
    pitic = 100
    pirate = 50

    bon = []
    botic = 100
    borate = 10

    RETURN = 0
    run = True
    while run:
        if tic >= pitic:
            pitic += pirate
            pic.append(g.Rect(r.randint(0, w), 0, 10, 10))
        
        if tic >= botic:
            botic += borate
            bon.append(g.Rect(r.randint(0, w), 0, 10, 10))
        
        for ev in g.event.get():
            if ev.type == g.QUIT:
                run = False
                g.quit()
                exit(0)
        
            if ev.type == g.KEYDOWN:
                if ev.key == g.K_RIGHT:
                    s += 5
                if ev.key == g.K_LEFT:
                    s -= 5
                    
            if ev.type == g.KEYUP:
                if ev.key == g.K_RIGHT:
                    s -= 5
                if ev.key == g.K_LEFT:
                    s += 5
        
        player.x += s
        
        if player.x <= 0:
            player.x = 0
        if player.right >= 600:
            player.right = 600
        
        for boi in pic:
            boi.y += 5
            if boi.colliderect(player):
                score += 1
                pic.remove(boi)
        
        for boi in bon:
            boi.y += 5
            if boi.colliderect(player):
                hp -= 1
                bon.remove(boi)
                if hp<=0:
                    run=False
                    break
        
        if score >= 15:
            RETURN = 1
            run = False
        
        screen.fill((50, 50, 50))
        g.draw.rect(screen, (255, 0, 0), player)
        
        for boi in pic:
            screen.blit(star, (boi.x, boi.y))
        
        for boi in bon:
            screen.blit(bad, (boi.x, boi.y))
        
        screen.blit(font.render(f'{score} / 15', True, (0, 250, 0)), (50, 60))
        screen.blit(font.render(f'HP: {hp}', True, (0, 250, 0)), (50, 100))
        
        dialogue(texts[tec])
        if tic%300 == 0:
            tec += 1
            if tec >= len(texts):
                tec = 0
        
        g.display.flip()
        clock.tick(60)
        tic+= 1

    return RETURN, hp