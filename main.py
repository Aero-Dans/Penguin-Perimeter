import pygame as pg
from enemy import Enemy
import constants as con

# pygame setup
pg.init()

# create window
screen = pg.display.set_mode((con.SCREEN_WIDTH, con.SCREEN_HEIGHT))
pg.display.set_caption("Penguin Perimeter")

# create clock
clock = pg.time.Clock()

waypoints = [(100, 200), (300,400), (200,600), (600,700), (50, 70)]

# load images
eimage_ppcat = pg.image.load('assets/images/enemies/ppcat.png').convert_alpha()

# create groups
enemy_group = pg.sprite.Group()

enemy = Enemy(waypoints, eimage_ppcat)
enemy_group.add(enemy)


# game loop
run = True
while run:

    clock.tick(con.FPS)  

    screen.fill('grey100')

    pg.draw.lines(screen, "grey0", False, waypoints)

    # update groups
    enemy_group.update()

    # draw groups
    enemy_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    
    

    # RENDER YOUR GAME HERE

    


    # update window
    pg.display.flip()



pg.quit()