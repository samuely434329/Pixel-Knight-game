import pygame
from character import Character

class Enemy(Character):
    def __init__(self, x, y, width, height, color, player):
        #from game import Player
        super().__init__(x, y, width, height, color)
        # access player
        self.player = player
        # image stuff
        self.image1 = pygame.image.load("images/enemy/ogre_idle_anim_f0.png")
        self.image = pygame.transform.scale(self.image1, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the sprite
        # combat stuff
        self.enemyHealth = 100
        self.attackCooldownInterval = 1000 
        self.firstHit = False
        self.lastAttackTime = 0

    def update(self, delta_time):
        # self.check_on_ground()  # This method doesn't exist, removing it
        self.gravity(delta_time)
        self.chasePlayer(delta_time)
        #self.attackPlayer()

    def chasePlayer(self, delta_time):
        if self.rect.x > self.player.rect.x:
            self.rect.x -= self.speed * delta_time
        elif self.rect.x < self.player.rect.x:
            self.rect.x += self.speed * delta_time
        # jump
        if self.rect.y-50 > self.player.rect.y and self.onGround:
            self.onGround = False
            self.verticalSpeed = self.initialJumpHeight+6
            self.jump_index = 0

    def attackPlayer(self):
        if self.rect.x == self.player.rect.x:
            current_time = pygame.time.get_ticks()
            if not self.firstHit:
                self.player.playerHealth = self.player.playerHealth - 10
                self.firstHit = True
                self.lastAttackTime = current_time

            elif current_time - self.lastAttackTime >= 1000:
                self.player.playerHealth = self.player.playerHealth - 10
                self.firstHit = False
                self.lastAttackTime = 0






