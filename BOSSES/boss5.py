def BOSS(hp):
    
    for i in range(100):
        for ev in g.event.get():
            if ev.type==g.QUIT:
                g.quit()
                exit(0)
            
        screen.fill((0,0,0))
        screen.blit(font.render('Work in progress, no boss for now :P', 0, (0,255,0)), (10,150))
        clock.tick(10)
    
    return 1,hp
