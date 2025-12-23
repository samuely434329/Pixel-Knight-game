import pygame
from character import Character

class Enemy(Character):
    def __init__(self, x, y, width, height):
        #from game import Player
        super().__init__(x, y, width, height)
        # access player
        #self.player = player
        # image stuff
        self.image_1 = pygame.image.load("ogre_idle_anim_f0.png")
        self.image = pygame.transform.scale(self.image_1, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the sprite
        # combat stuff
        self.enemy_health = 100
        self.attack_cooldown_interval = 1000 
        self.first_hit = False
        self.last_attack_time = 0

    def update(self):
        self.check_on_ground()
        self.gravity()
        self.chase_player()
        #self.attack_player()

    def chase_player(self):
        if self.rect.x > self.player.rect.x:
            self.rect.move_ip(-5, 0)
        elif self.rect.x < self.player.rect.x:
            self.rect.move_ip(5, 0)
        # jump
        if self.rect.y-50 > self.player.rect.y and self.on_ground:
            self.on_ground = False
            self.vertical_speed = self.initial_jump_height+6
            self.jump_index = 0

    def attack_player(self):
        if self.rect.x == self.player.rect.x:
            current_time = pygame.time.get_ticks()
            if not self.first_hit:
                self.player.health = self.player.health - 10
                self.first_hit = True
                self.last_attack_time = current_time

            elif current_time - self.last_attack_time >= 1000:
                self.player.health = self.player.health - 10
                self.first_hit = False
                self.last_attack_time = 0






