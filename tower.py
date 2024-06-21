import pygame as pg
import constants as con
from pygame.math import Vector2
import math


class Tower(pg.sprite.Sprite):

    money = 1000  # Initial tower money

    def __init__(self, pos, image, bullet_image):
        pg.sprite.Sprite.__init__(self)
        self.pos = Vector2(pos)  # Tower position
        self.original_image = image  # Original tower image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.bullet_image = bullet_image  # Bullet image
        self.bullets = pg.sprite.Group()  # Group for bullets
        self.target = None  # Target enemy
        self.range = 300  # Tower range
        self.damage = 20  # Tower damage
        self.base_cooldown = 300  # Base cooldown value
        self.cooldown = self.base_cooldown  # Initial cooldown
        self.level = 1  # Tower level
        self.upgrade_cost = 100  # Upgrade cost
        self.selected = False  # Is the tower selected?
        self.tile_x = pos[0] // con.GRID_SIZE  # Tower tile x position
        self.tile_y = pos[1] // con.GRID_SIZE  # Tower tile y position
        self.upgrade_buttons = [
            pg.Rect(con.SCREEN_WIDTH + 10, 220, 180, 30),  # damage upgrade button
            pg.Rect(con.SCREEN_WIDTH + 10, 260, 180, 30),  # cooldown upgrade button
            pg.Rect(con.SCREEN_WIDTH + 10, 300, 180, 30),  # range upgrade button
        ]

        # Create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
        self.range_image.fill((0, 0, 0, 0))
        pg.draw.circle(self.range_image, (255, 255, 255, 100), (self.range, self.range), self.range)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1  # Decrease cooldown
        else:
            self.target = self.find_target(enemies)  # Find the closest enemy
            if self.target:
                distance = (self.target.pos - self.pos).length()
                if distance <= self.range:
                    self.direction = (self.target.pos - self.pos).normalize()
                    self.rotate()  # Rotate the tower to face the enemy
                    self.shoot()  # Shoot a bullet
                else:
                    self.target = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            self.range_rect.center = self.rect.center
            surface.blit(self.range_image, self.range_rect)  # Draw the range circle

    def handle_upgrade(self, mouse_pos):
        if self.selected:
            for i, button in enumerate(self.upgrade_buttons):
                if button.collidepoint(mouse_pos):
                    if Tower.money >= self.upgrade_cost:
                        if i == 0:
                            self.damage += 5  # Upgrade damage
                        elif i == 1:
                            self.base_cooldown = max(50, self.base_cooldown - 20)  # Upgrade cooldown
                        else:
                            self.range += 50  # Upgrade range
                            self.update_range_image()  # Update range circle
                        self.level += 1
                        Tower.money -= self.upgrade_cost
                        self.upgrade_cost += 100
                        break

    def update_range_image(self):
        # Update the range circle image
        self.range_image = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA)
        self.range_image.fill((0, 0, 0, 0))
        pg.draw.circle(self.range_image, (255, 255, 255, 100), (self.range, self.range), self.range)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def find_target(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in enemies:
            distance = (enemy.pos - self.pos).length()
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
        return closest_enemy

    def rotate(self):
        if self.direction.length() > 0:
            self.angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def shoot(self):
        bullet = Bullet(self.pos, self.bullet_image, self.target, self.damage)
        self.bullets.add(bullet)
        self.cooldown = self.base_cooldown  # Set cooldown to the current base cooldown value


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, image, target, damage):
        super().__init__()
        self.pos = Vector2(pos)
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.target = target
        self.speed = 40
        self.damage = damage
        self.angle = 0

    def update(self):
        # Check if the target is still alive
        if not self.target.alive():
            self.kill()
            return

        direction = (self.target.pos - self.pos).normalize()
        self.angle = math.degrees(math.atan2(-direction[1], direction[0]))
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += direction * self.speed

        # Check if the bullet has reached the enemy's position
        if (self.target.pos - self.pos).length() < 15:
            self.target.take_damage(self.damage)
            Tower.money += self.damage  # Add the damage dealt to the tower's money
            self.kill()  # Remove the bullet