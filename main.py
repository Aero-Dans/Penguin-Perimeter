import pygame as pg
from enemy import Enemy
import constants as con
from tower import Tower
import random

# Initialize Pygame
pg.init()

# Create the game window
screen = pg.display.set_mode((con.SCREEN_WIDTH + 200, con.SCREEN_HEIGHT))
pg.display.set_caption("Penguin Perimeter")

# Create a clock to control the frame rate
clock = pg.time.Clock()

# Load game images
tower_image = pg.image.load('assets/images/towers/penquin_rpg.png').convert_alpha()
bullet_image = pg.image.load('assets/images/towers/rocket.png').convert_alpha()

enemy_image = [
    {"image": pg.image.load('assets/images/enemies/polarbear.png').convert_alpha(), "health": 10, "speed": 0.5},
    {"image": pg.image.load('assets/images/enemies/polarbear_blue.png').convert_alpha(), "health": 15, "speed": 1},
    {"image": pg.image.load('assets/images/enemies/polarbear_green.png').convert_alpha(), "health": 8, "speed": 0.25},
    {"image": pg.image.load('assets/images/enemies/polarbear_orange.png').convert_alpha(), "health": 12, "speed": 0.5},
    {"image": pg.image.load('assets/images/enemies/polarbear_pink.png').convert_alpha(), "health": 18, "speed": 2},
    {"image": pg.image.load('assets/images/enemies/polarbear_purple.png').convert_alpha(), "health": 20, "speed": 3},
    {"image": pg.image.load('assets/images/enemies/polarbear_red.png').convert_alpha(), "health": 25, "speed": 4},
    {"image": pg.image.load('assets/images/enemies/polarbear_turquois.png').convert_alpha(), "health": 30, "speed": 5},
    {"image": pg.image.load('assets/images/enemies/polarbear_yellow.png').convert_alpha(), "health": 35, "speed": 5},
    {"image": pg.image.load('assets/images/enemies/polarbear_grey.png').convert_alpha(), "health": 40, "speed": 6},
]

# Function to create a wave of enemies
def create_wave(waypoints, wave_number):
    enemies = []
    num_enemies = wave_number * 5  # Increase the number of enemies per wave
    for i in range(num_enemies):
        enemy_type = random.choice(enemy_image)
        # Increase enemy health and speed progressively with wave number
        enemy_health = enemy_type["health"] + wave_number * 0.1
        enemy_speed = enemy_type["speed"] + wave_number * 0.05
        enemy = Enemy(waypoints, enemy_type["image"], enemy_health, enemy_speed)
        enemy.health = enemy_health  # set the enemy's health
        enemies.append(enemy)
    return enemies

# Function to draw the game background
def draw_background():
    screen.fill(con.BACKGROUND_COLOR)

# Function to draw the path
def draw_path():
    for (col, row) in con.PATH:
        rect = pg.Rect(col * con.CELL_SIZE, row * con.CELL_SIZE, con.CELL_SIZE, con.CELL_SIZE)
        pg.draw.rect(screen, con.PATH_COLOR, rect)

# Function to select a tower
def select_tower(mouse_pos):
    global selected_tower
    for tower in tower_group:
        tower.selected = False
    for tower in tower_group:
        if tower.rect.collidepoint(mouse_pos):
            tower.selected = True
            selected_tower = tower
            return

# Function to clear the selected tower
def clear_selection():
    for tower in tower_group:
        tower.selected = False

# Function to center the text position
def center_text_position(text_surface):
    # Calculate the center position of the text surface
    x = con.SCREEN_WIDTH // 2 - text_surface.get_width() // 2
    y = con.SCREEN_HEIGHT // 2 - text_surface.get_height() // 2
    return x, y

# Function to show the victory menu
def show_victory_menu():
    screen.fill((0, 0, 0))
    font = pg.font.Font(None, 74)
    text = font.render("Victory!", True, (255, 255, 255))
    text_rect = text.get_rect(center=((con.SCREEN_WIDTH + 200) // 2, con.SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.wait(3000)

# Function to show the game over menu
def show_game_over_menu():
    screen.fill((0, 0, 0))
    font = pg.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=((con.SCREEN_WIDTH + 200) // 2, con.SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pg.display.flip()
    pg.time.wait(3000)

# Create game groups
enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

# Find path waypoints
waypoints = [(x * con.CELL_SIZE + con.CELL_SIZE // 2, y * con.CELL_SIZE + con.CELL_SIZE // 2) for x, y in con.PATH]

# Create menu buttons
menu_buttons = [
    pg.Rect(con.SCREEN_WIDTH, 10, 190, 30),
    pg.Rect(con.SCREEN_WIDTH, 50, 190, 30),
    pg.Rect(con.SCREEN_WIDTH, 90, 190, 30),
    pg.Rect(con.SCREEN_WIDTH, 130, 190, 30),
]

# Game variables
place_tower = False
selected_tower = None
tower_pos = None
delete_mode = False
next_wave = False
health = 200
wave_number = 1
tower_cost = 100  # cost of placing a tower

# Game loop
run = True
while run:
    clock.tick(con.FPS)

    # Draw the game background and path
    draw_background()
    draw_path()

    # Update the enemy and tower groups
    enemy_group.update()
    tower_group.update(enemy_group)

    # Update the selected tower
    if selected_tower:
        selected_tower.selected = True

    # Update the bullets
    for tower in tower_group:
        tower.bullets.update()

    # Draw the enemy and tower groups
    enemy_group.draw(screen)
    for tower in tower_group:
        tower.draw(screen)
        for bullet in tower.bullets:
            screen.blit(bullet.image, bullet.rect)

    # Draw the menu background and buttons
    pg.draw.rect(screen, (255, 255, 255), (con.SCREEN_WIDTH, 0, 200, con.SCREEN_HEIGHT))  # white background

    for tower in tower_group:
        if tower.selected:
            for i, button in enumerate(tower.upgrade_buttons):
                pg.draw.rect(screen, (255, 255, 255), button, 2)  # draw white outline
                if i == 0:
                    font = pg.font.Font(None, 24)
                    text = font.render("Upgrade Damage", True, (0, 0, 0))
                    screen.blit(text, (button.x + 10, button.y + 5))
                elif i == 1:
                    font = pg.font.Font(None, 24)
                    text = font.render("Upgrade Cooldown:", True, (0, 0, 0))
                    screen.blit(text, (button.x + 10, button.y + 5))
                else:
                    font = pg.font.Font(None, 24)
                    text = font.render("Upgrade Range", True, (0, 0, 0))
                    screen.blit(text, (button.x + 10, button.y + 5))

    for button in menu_buttons:
        font = pg.font.Font(None, 24)
        if button == menu_buttons[0]:
            text = font.render("Place Tower", True, (0, 0, 0))
        elif button == menu_buttons[1]:
            text = font.render("Delete Tower", True, (0, 0, 0))
        elif button == menu_buttons[2]:
            text = font.render("Exit", True, (0, 0, 0))
        else:
            text = font.render("Next Wave", True, (0, 0, 0))
        screen.blit(text, (button.x + 10, button.y + 5))

    # Draw money text
    font = pg.font.Font(None, 24)
    money_text = font.render(f"Money: ${Tower.money}", True, (0, 0, 0))
    screen.blit(money_text, (con.SCREEN_WIDTH + 10, 180))

    # Draw wave number text
    wave_text = font.render(f"Wave: {wave_number}", True, (0, 0, 0))
    screen.blit(wave_text, (con.SCREEN_WIDTH + 10, 900))

    # Check if the player is placing a tower
    if place_tower:
        mouse_pos = pg.mouse.get_pos()
        if 0 < mouse_pos[0] < con.SCREEN_WIDTH and 0 < mouse_pos[1] < con.SCREEN_HEIGHT:
            tower_preview = Tower(mouse_pos, tower_image, bullet_image)
            tower_preview.draw(screen)
            # draw range circle
            surf = pg.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT))
            surf.set_alpha(50)  # set alpha value for translucency
            pg.draw.circle(surf, (245, 245, 245), mouse_pos, tower_preview.range)
            screen.blit(surf, (0, 0))

    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            for button in menu_buttons:
                if button.collidepoint(event.pos):
                    if button == menu_buttons[0]:
                        place_tower = True
                    elif button == menu_buttons[1]:
                        delete_mode = True
                    elif button == menu_buttons[2]:
                        run = False
                    else:
                        next_wave = True
            else:
                mouse_pos = pg.mouse.get_pos()
                if selected_tower:
                    selected_tower.handle_upgrade(event.pos)
                    if not selected_tower.rect.collidepoint(mouse_pos):
                        clear_selection()
                        selected_tower = None
                select_tower(mouse_pos)
                if place_tower:
                    if 0 < event.pos[0] < con.SCREEN_WIDTH and 0 < event.pos[1] < con.SCREEN_HEIGHT:
                        # Check if the clicked position is on the path
                        on_path = False
                        for (col, row) in con.PATH:
                            if col * con.CELL_SIZE - 30 <= event.pos[0] < (col + 1) * con.CELL_SIZE + 30 and row * con.CELL_SIZE - 30 <= event.pos[1] < (row + 1) *con.CELL_SIZE + 30:
                                on_path = True
                                break
                        if not on_path:
                            # Check if the clicked position is not occupied by another tower
                            tower_collision = False
                            for tower in tower_group:
                                if tower.rect.inflate(50, 50).collidepoint(event.pos):
                                    tower_collision = True
                                    break
                            if not tower_collision and Tower.money >= tower_cost:
                                tower = Tower(event.pos, tower_image, bullet_image)
                                tower_group.add(tower)
                                Tower.money -= tower_cost  # subtract the cost of the tower from the money
                                place_tower = False
                if delete_mode:
                    for tower in tower_group:
                        if tower.rect.collidepoint(event.pos):
                            tower_group.remove(tower)
                            delete_mode = False
                            break

    # Check if the next wave button is clicked
    if next_wave:
        if not enemy_group:  # Check if all enemies are killed
            next_wave = False
            enemy_wave = create_wave(waypoints, wave_number)
            for enemy in enemy_wave:
                enemy_group.add(enemy)
            wave_number += 1
        else:
            next_wave = False  # Reset the next wave flag if enemies are still alive

    # Check for enemy reaching the end of the path
    for enemy in enemy_group:
        if enemy.pos.y < 0:
            health -= enemy.health
            enemy.kill()
            break

    # Check if health is 0
    if health <= 0:
        show_game_over_menu()
        run = False

    # Check if wave number exceeds 20
    if wave_number > 5:
        show_victory_menu()
        run = False

    # Draw health bar
    pg.draw.rect(screen, (0, 0, 0), (con.SCREEN_WIDTH, con.SCREEN_HEIGHT - 50, 204, 54), 2)  # draw black outline
    pg.draw.rect(screen, (255, 0, 0), (con.SCREEN_WIDTH, con.SCREEN_HEIGHT - 50, 200, 50))  # draw red background
    health_width = int((health / 200) * 200)  # calculate the width of the green health bar
    pg.draw.rect(screen, (0, 255, 0), (con.SCREEN_WIDTH, con.SCREEN_HEIGHT - 50, health_width, 50))  # draw green health bar

    pg.draw.rect(screen, (0, 0, 0), (con.SCREEN_WIDTH, 0, 200, con.SCREEN_HEIGHT), 2)  # black outline

    # Update the game window
    pg.display.flip()

# Ensure Pygame quits properly
pg.quit()