import pygame as pg
from pygame.math import Vector2
import math


class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image, health, speed):
        pg.sprite.Sprite.__init__(self)
        # Initialize waypoints, position, and target waypoint
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = speed
        self.angle = 0
        # Store original image and rotated image
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # Store direction vector
        self.direction = Vector2(0, 0)  
        self.health = health


    def update(self):
        # Update enemy movement and rotation
        self.move()
        self.rotate()


    def move(self):
        # Define target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            # Calculate direction vector to target waypoint
            self.direction = (self.target - self.pos).normalize()
        # Move enemy towards target waypoint
        self.pos += self.direction * self.speed
        # Check if enemy has reached target waypoint
        if (self.target - self.pos).length() < self.speed:
            self.pos = self.target
            # Move to next waypoint
            self.target_waypoint += 1


    def rotate(self):
        # Calculate direction angle
        if self.direction.length() > 0:
            self.angle = math.degrees(math.atan2(-self.direction[1], self.direction[0]))
            # Rotate image and update rectangle
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos


    def take_damage(self, damage):
        # Reduce enemy health by damage amount
        self.health -= damage
        if self.health <= 0:
            # Kill enemy if health reaches 0
            self.kill()

