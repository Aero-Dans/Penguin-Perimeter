import pygame as pg
from pygame.math import Vector2


class Enemy(pg.sprite.Sprite):
    def __init__(self,waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()

    def move(self):
        # define target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()


        # calculate distance to target
        dist = self.movement.length()
        # check if remaining dist is greater than enemy speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1


        self.rect.center = self.pos
            
