import pygame
import random
clock = pygame.time.Clock()
#Screen borders should be same as game.py, prevents guy from going out of bounds
screenWidth = 1400
screenHeight = 700


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        # setups jump sound effects
        self.jumpSoundEffects = []
        for i in range(5):  
            sfx = pygame.mixer.Sound(f"sounds/jump{i}.wav")
            self.jumpSoundEffects.append(sfx)
        # setups right images
        self.imageRight = []
        for i in range(7):
            img = pygame.transform.scale(pygame.image.load(f"images/right/Right{i}.png"), (width, height))
            self.imageRight.append(img)
        # setups left images
        self.imageLeft = []
        for i in range(7):
            img = pygame.transform.scale(pygame.image.load(f"images/left/Left{i}.png"), (width, height))
            self.imageLeft.append(img)
        # setups up right jumping images
        self.imageRightJump = []
        for i in range(1,16):
            img = pygame.transform.scale(pygame.image.load(f"images/right/jumpingRight{i}.png"), (width, height))
            self.imageRightJump.append(img)
        # setups up left jumping images
        self.imageLeftJump = []
        for i in range(1,16):
            img = pygame.transform.scale(pygame.image.load(f"images/left/jumpingLeft{i}.png"), (width, height))
            self.imageLeftJump.append(img)

        # setups right side idle images
        self.imageIdleRight = []
        for i in range(1,7):
            img = pygame.transform.scale(pygame.image.load(f"images/right/idleRight{i}.png"), (width, height))
            self.imageIdleRight.append(img)
        #setups left side idle images
        self.imageIdleLeft = []
        for i in range(1,7):
            img = pygame.transform.scale(pygame.image.load(f"images/left/idleLeft{i}.png"), (width, height))
            self.imageIdleLeft.append(img)

        # attack images
        self.imageRightAttack = []
        self.imageLeftAttack = []
        for i in range(10):
            rightImage = pygame.transform.scale(pygame.image.load(f"images/right/rightAttack{i}.png"), (width, height))
            leftImage = pygame.transform.scale(pygame.image.load(f"images/left/leftAttack{i}.png"), (width, height))

            self.imageRightAttack.append(rightImage)
            self.imageLeftAttack.append(leftImage)
        
        #initial player image
        self.image = pygame.transform.scale(self.imageRight[0], (width, height))  # Resize if needed
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the sprite

        # movement variables
        self.currentKeys = None  # ✅ Store key state
        self.speed = 320
        self.initialJumpHeight = -16
        self.verticalSpeed = 0
        self.gravityNumber = 0.29 #0.3 initially
        self.isJumping = False
        self.onGround = False
        self.jumpIndex = 0  # Tracks which image is active
        self.jumpCounter = 0  # Counts how many times gravity has updated
        # animation variables
        self.animationTimer = 0
        self.frameIndex = 0
        self.lastDirection = "right"

        # combat variables
        self.playerHealth = 100
        self.playerDamage = 50

    # x accessor 
    def x(self):
        return self.rect.x
    
    # y accessor
    def y(self):
        return self.rect.y

    def update(self, delta_time):
        # self.current_keys = key  # ✅ Save key state for use in other methods
        self.checkForKeys(delta_time)  # ✅ Now no need to pass 'key' explicitly
        self.gravity(delta_time)

    def checkForKeys(self, delta_time):
        #jump
        if self.currentKeys[pygame.K_w] and self.onGround:
            random.choice(self.jumpSoundEffects).play()
            self.onGround = False
            self.verticalSpeed = self.initialJumpHeight
            self.jump_index = 0

        # move left
        elif self.currentKeys[pygame.K_a] and self.rect.x > 0:
            self.lastDirection = "left"
            self.rect.x -= self.speed * delta_time

            self.animationTimer += 1
            if self.animationTimer % 5 == 0:
                try:
                    self.image = self.imageLeft[self.frameIndex]
                    self.frameIndex += 1
                except IndexError:
                    self.frameIndex = 0
        # move right
        elif self.currentKeys[pygame.K_d] and self.rect.x < screenWidth - self.rect.width:
            self.lastDirection = "right"
            self.rect.x += self.speed * delta_time
            
            self.animationTimer += 1
            if self.animationTimer % 5 == 0:
                try:
                    self.image = self.imageRight[self.frameIndex]
                    self.frameIndex += 1
                except IndexError:
                    self.frameIndex = 0

        # when facing right
        elif self.lastDirection == "right":
            # when press attack key
            if self.currentKeys[pygame.K_f]:
                self.animationTimer += 1
                #cooldown for animation
                # loop through it slowly (timer)       
                try:
                    self.image = self.imageRightAttack[self.frameIndex]
                    self.frameIndex += 1
                except IndexError:
                    self.frameIndex = 0
            # when idle play right idle animation
            elif self.onGround:
                self.animationTimer += 1
                if self.animationTimer % 10 == 0:
                    try:
                        self.image = self.imageIdleRight[self.frameIndex]
                        self.frameIndex += 1
                    except IndexError:
                        self.frameIndex = 0
           


        # when facing left
        elif self.lastDirection == "left":
            # when press attack key
            if self.currentKeys[pygame.K_f]:
                self.animationTimer += 1
                if self.animationTimer % 5 == 0:          
                    try:
                        self.image = self.imageLeftAttack[self.frameIndex]
                        self.frameIndex += 1
                    except IndexError:
                        self.frameIndex = 0
            #if idle play left idle animation
            elif self.onGround:
                self.animationTimer += 1
                if self.animationTimer % 10 == 0:
                    try:
                        self.image = self.imageIdleLeft[self.frameIndex]
                        self.frameIndex += 1
                    except IndexError:
                        self.frameIndex = 0
    

    def gravity(self, delta_time):
        # Apply gravity
        self.verticalSpeed += self.gravityNumber * 75 * delta_time
        self.rect.y += self.verticalSpeed

        # Check if player is on the ground
        if self.rect.y >= screenHeight - self.rect.height:
            self.rect.y = screenHeight - self.rect.height
            self.verticalSpeed = 0
            if not self.onGround:
                self.onGround = True
                self.jumpCounter = 0
                self.jumpIndex = 0
        else:
            self.onGround = False

        # Update jump animation
        if not self.onGround:
            self.jumpCounter += 1
            animation_speed = 3 # determines how fast the jump animation plays
            
            # Determine which set of jump images to use
            jump_images = self.imageRightJump if self.lastDirection == "right" else self.imageLeftJump
            
            # Update the jump frame
            if self.jumpCounter % animation_speed == 0:
                self.jumpIndex = min(self.jumpIndex + 1, len(jump_images) - 1)
                self.image = jump_images[self.jumpIndex]

    def attack(self, enemy):
        #play animation first
        
        #if facing left
        if self.lastDirection == "left":
            self.image = self.imageAttackLeft
        else:
            self.image = self.imageAttackRight

        enemy.enemyHealth -= self.playerDamage
