import pygame

clock = pygame.time.Clock()
#Screen borders should be same as game.py, prevents guy from going out of bounds
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
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

        #initial player image
        self.image = pygame.transform.scale(self.imageRight[0], (width, height))  # Resize if needed
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the sprite

        # movement variables
        self.current_keys = None  # ✅ Store key state
        self.speed = 340
        self.initial_jump_height = -16
        self.vertical_speed = 0
        self.gravity_number = 0.3
        self.is_jumping = False
        self.on_ground = False
        self.jump_index = 0  # Tracks which image is active
        self.jump_counter = 0  # Counts how many times gravity has updated
        # animation variables
        self.animation_timer = 0
        self.frame_index = 0

        self.lastDirection = "right"

        # combat variables
        self.player_health = 100
        self.player_damage = 50

    # x accessor 
    def x(self):
        return self.rect.x
    
    # y accessor
    def y(self):
        return self.rect.y

    def update(self, delta_time):
        # self.current_keys = key  # ✅ Save key state for use in other methods
        self.check_for_move(delta_time)  # ✅ Now no need to pass 'key' explicitly
        self.gravity(delta_time)

    def check_for_move(self, delta_time):
        if self.current_keys[pygame.K_w] and self.on_ground:
            self.on_ground = False
            self.vertical_speed = self.initial_jump_height
            self.jump_index = 0

        elif self.current_keys[pygame.K_a] and self.rect.x > 0:
            self.lastDirection = "left"
            self.rect.x -= self.speed * delta_time

            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                try:
                    self.image = self.imageLeft[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0

        elif self.current_keys[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.lastDirection = "right"
            self.rect.x += self.speed * delta_time
            
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                try:
                    self.image = self.imageRight[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0
        # when not moving and on ground
        elif self.on_ground and self.lastDirection == "right":
            self.animation_timer += 1
            if self.animation_timer % 10 == 0:
                try:
                    self.image = self.imageIdleRight[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0

        elif self.on_ground and self.lastDirection == "left":
            self.animation_timer += 1
            if self.animation_timer % 10 == 0:
                try:
                    self.image = self.imageIdleLeft[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0

    def gravity(self, delta_time):
        # Apply gravity
        self.vertical_speed += self.gravity_number * 75 * delta_time
        self.rect.y += self.vertical_speed

        # Check if player is on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.vertical_speed = 0
            if not self.on_ground:
                self.on_ground = True
                self.jump_counter = 0
                self.jump_index = 0
        else:
            self.on_ground = False

        # Update jump animation
        if not self.on_ground:
            self.jump_counter += 1
            animation_speed = 3 # determines how fast the jump animation plays
            
            # Determine which set of jump images to use
            jump_images = self.imageRightJump if self.lastDirection == "right" else self.imageLeftJump
            
            # Update the jump frame
            if self.jump_counter % animation_speed == 0:
                self.jump_index = min(self.jump_index + 1, len(jump_images) - 1)
                self.image = jump_images[self.jump_index]
