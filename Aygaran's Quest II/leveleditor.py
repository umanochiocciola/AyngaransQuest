import pygame as g

TITLE="Aygaran's Quest -- Level Editor"
size = (800, 600)
w, h = size

g.init()
screen = g.display.set_mode(size)
g.display.set_caption(TITLE)
clock = g.time.Clock()
font = g.font.SysFont("cambria", 20)

codex = ['orc', 'spider', 'troll', 'pig']

rooms = []
enemies = []
Arooms = []

mousebop = g.Rect(0,0,5,5)
run = 1
selected = Exit = -1
addEnem = 0
TileExit = 0
while run:
    mousebop.x, mousebop.y = g.mouse.get_pos()
    for ev in g.event.get():
        if ev.type == g.QUIT:
            print(Arooms)
            g.quit()
            exit(0)
        
        if ev.type == g.MOUSEBUTTONDOWN:
            if ev.button==1:
                if TileExit == 1:
                    Exit = len(rooms)
                    TileExit = 0
                x, y = g.mouse.get_pos()
                rooms.append(g.Rect(int(x/50)*50, int(y/50)*50, 50, 50))
                Arooms.append((int(x/50), int(y/50)))
                enemies.append([])
            
            if ev.button==3:
                for i in range(len(rooms)):
                    if mousebop.colliderect(rooms[i]):
                        if Exit == i:
                            Exit = -1
                        rooms.remove(rooms[i])
                        enemies.remove(enemies[i])
                        Arooms.remove((int(mousebop.x/50), int(mousebop.y/50)))
                        selected = -1
                        break
                        
             
            if ev.button == 2:
                enemies[selected].append(addEnem)
                    
                    
        if ev.type == g.KEYDOWN:
            if ev.key == g.K_e:
                TileExit = 1
            
            if ev.key == g.K_SPACE:
                run = 0
                break
            
            if ev.key == g.K_UP:
                addEnem += 1
                if addEnem > 3: addEnem = 0
            
            if ev.key == g.K_DOWN:
                addEnem -= 1
                if addEnem < 0: addEnem = 3
    
    
    for i in range(len(rooms)):
        if mousebop.colliderect(rooms[i]):
            selected = i
            
    
            
    screen.fill((0,0,0))
    
    for i in range(len(rooms)):
        SANDRO = ' (exit)' if i==Exit else ''
        g.draw.rect(screen, (100, 100, 100), rooms[i])
        screen.blit(font.render(str(i)+SANDRO, 0, (0,255,0)), (rooms[i].x+20, rooms[i].y+20))
    
    if selected != -1:
        screen.blit(font.render(f'room {selected}    enemies: {enemies[selected]}', 0, (255, 0, 0)), (0,0))
        screen.blit(font.render(f'press M2 to add {codex[addEnem]}', 0, (255, 0,0)), (0, 30))
    
    g.display.flip()
    clock.tick(60)
g.quit()


print('computing')
sx=sy=999
for i in Arooms:
    x, y = i
    if x < sx: sx = x
    if y < sy: sy = y

rooms = []
for i in Arooms:
    x, y = i
    rooms.append((x-sx, y-sy))
###


selexit = 1
LEVEL = '[\n\t'
for j in range(len(rooms)):
    i = rooms[j]
    bop = 'room('
    x, y = i
    
    right=left=up=down=0
    
    if (x, y-1) in rooms:
        bop += f'{rooms.index((x, y-1))}, '
        up = 1
    else: bop += f'{j}, '
        
    if (x+1, y) in rooms:
        bop += f'{rooms.index((x+1, y))}, '
        right = 1
    else: bop += f'{j}, '
    
    if (x, y+1) in rooms:
        bop += f'{rooms.index((x, y+1))}, '
        down = 1
    else: bop += f'{j}, '

    if (x-1, y) in rooms:
        bop += f'{rooms.index((x-1, y))}, '
        left = 1
    else: bop += f'{j}, '
    
    
    img = 'STONE/'
    if right and left and up and down:
        img += 'cross'
    elif right and left and up:
        img += 'horizontal-up'
    elif right and left and down:
        img += 'horizontal-down'
    elif right and left:
        img += 'horizontal'
    elif up and down and right:
        img += 'vertical-right'
    elif up and down and left:
        img += 'vertical-left'
    elif up and down:
        img += 'vertical'
    elif up and right:
        img += 'up-right'
    elif up and left:
        img += 'up-left'
    elif down and right:
        img += 'down-right'
    elif down and left:
        img += 'down-left'
    elif right:
        img += 'right'
    elif left:
        img += 'left'
    elif up:
        img += 'up'
    elif down:
        img += 'down'
    
    bop += f"'{img}', {enemies[j]}, "
    if Exit == j: bop += 'EXIT'; selexit = 0
    bop += '),'
    LEVEL += bop+'\n\t'

LEVEL += '],'

print(LEVEL)
if selexit: print('NO EXIT TILE SELECTED!')

