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



# load images
eimage_ppcat = pg.image.load('assets/images/enemies/ppcat.png').convert_alpha()

def draw_background():
    screen.fill(con.BACKGROUND_COLOR)


# draws path on screen
def draw_path():
    for (col, row) in con.PATH:
        rect = pg.Rect(col * con.CELL_SIZE, row * con.CELL_SIZE, con.CELL_SIZE, con.CELL_SIZE)
        pg.draw.rect(screen, con.PATH_COLOR, rect)
    
    # Draw connecting rectangles
    for i in range(len(con.PATH) - 1):
        col1, row1 = con.PATH[i]
        col2, row2 = con.PATH[i + 1]
        if col1 == col2:  # Vertical movement
            rect = pg.Rect(col1 * con.CELL_SIZE, min(row1, row2) * con.CELL_SIZE, con.CELL_SIZE, abs(row1 - row2) * con.CELL_SIZE + con.CELL_SIZE)
        else:  # Horizontal movement
            rect = pg.Rect(min(col1, col2) * con.CELL_SIZE, row1 * con.CELL_SIZE, abs(col1 - col2) * con.CELL_SIZE + con.CELL_SIZE, con.CELL_SIZE)
        pg.draw.rect(screen, con.PATH_COLOR, rect)

# create groups
enemy_group = pg.sprite.Group()

# find path waypoints
waypoints = [(x * con.CELL_SIZE + con.CELL_SIZE // 2, y * con.CELL_SIZE + con.CELL_SIZE // 2) for x, y in con.PATH]

enemy = Enemy(waypoints, eimage_ppcat)
enemy_group.add(enemy)

# game loop
run = True
while run:

    clock.tick(con.FPS)  

    screen.fill('grey100')
    

    draw_background()
    draw_path()

    pg.draw.lines(screen, 'grey0', False, waypoints)

    # update groups
    enemy_group.update()

    # draw groups
    enemy_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # update window
    pg.display.flip()

pg.quit()
