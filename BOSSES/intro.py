def BOSSINTRO(boss, instructions):
    tic = 1
    
    MSGs = [
        'You encounter '+boss,
         '-- Prepare to fight --',
    ]
    
    for i in instructions.split('\n'):
        MSGs.append(i)
    
    I = 0
    G = 0
    
    while run:
        for ev in g.event.get():
            if ev.type == g.QUIT:
                g.quit()
                exit(0)
        
        if tic%100 == 0:
            I += 1
            if G: return
            if I >= len(MSGs): I -= 1; G = 1
            
        
        
        screen.fill((0, 0, 0))

        screen.blit(font.render(MSGs[I], True, (0, 250, 0)), (10, 150))
        
        g.display.flip()
        clock.tick(60)
        tic+= 1

    return RETURN