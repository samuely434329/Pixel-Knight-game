import pygame
from character import Character

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # image stuff
        self.image_1 = pygame.image.load("images/ogre_idle_anim_f0.png")
        self.image = pygame.transform.scale(self.image_1, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the sprite

        # combat stuff
        self.enemy_health = 100
        self.speed = 1
    
    def chase(self, character):
        #move right 
        if character.rect.x > self.rect.x:
            self.rect.x += self.speed
        #move left
        elif character.rect.x < self.rect.x:
            self.rect.x -= self.speed
