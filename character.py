import pygame

clock = pygame.time.Clock()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        # setups right images
        self.image_right = []
        for i in range(7):
            img = pygame.transform.scale(pygame.image.load(f"images/Right{i}.png"), (width, height))
            self.image_right.append(img)
        # setups left images
        self.image_left = []
        for i in range(7):
            img = pygame.transform.scale(pygame.image.load(f"images/Left{i}.png"), (width, height))
            self.image_left.append(img)
        # setups up images
        self.image_up = []
        for i in range(15):
            img = pygame.transform.scale(pygame.image.load(f"images/Jumping{i}.png"), (width, height))
            self.image_up.append(img)
        self.image_idle = []
        for i in range(6):
            img = pygame.transform.scale(pygame.image.load(f"images/Idle{i}.png"), (width, height))
            self.image_idle.append(img)

        self.image = pygame.transform.scale(self.image_right[0], (width, height))  # Resize if needed
        self.rect = self.image.get_rect(topleft=(x, y))  # Position the sprite
        # movement variables
        self.current_keys = None  # ✅ Store key state
        self.speed = 1
        self.initial_jump_height = -12
        self.vertical_speed = 0
        self.gravity_number = 0.3
        self.is_jumping = False
        self.on_ground = False
        self.jump_index = 0  # Tracks which image is active
        self.jump_counter = 0  # Counts how many times gravity has updated
        # animation variables
        self.animation_timer = 0
        self.frame_index = 0
        # combat variables
        self.player_health = 100
        self.player_damage = 50

    def update(self):
        # self.current_keys = key  # ✅ Save key state for use in other methods
        self.check_on_ground()
        self.check_for_move()  # ✅ Now no need to pass 'key' explicitly
        self.gravity()

    def check_for_move(self):
        if self.current_keys[pygame.K_w] and self.on_ground:
            self.on_ground = False
            self.vertical_speed = self.initial_jump_height
            self.jump_index = 0

        elif self.current_keys[pygame.K_a] and self.rect.x > 0:
            self.rect.move_ip(-10, 0)

            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                try:
                    self.image = self.image_left[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0

        elif self.current_keys[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.move_ip(10, 0)

            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                try:
                    self.image = self.image_right[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0
        # when not moving
        else:
            self.animation_timer += 1
            if self.animation_timer % 5 == 0:
                try:
                    self.image = self.image_idle[self.frame_index]
                    self.frame_index += 1
                except IndexError:
                    self.frame_index = 0

    def gravity(self):
        # checks for time here, longer time = higher speed
        delta_time = clock.tick(60) / 10
        self.vertical_speed += self.gravity_number * delta_time
        self.rect.y += self.vertical_speed * delta_time
        # 49 ticks not on ground
        if not self.on_ground and not self.current_keys[pygame.K_a] and not self.current_keys[pygame.K_d]:
            self.jump_counter += 1
            if self.jump_counter % (49 // 15) == 0:  # Change frame at intervals
                self.jump_index = min(self.jump_index + 1, 14)  # Prevent going out of range
                self.image = self.image_up[self.jump_index]  # Update sprite image

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.vertical_speed = 0
            self.on_ground = True

    def check_on_ground(self):
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.on_ground = True

        elif self.rect.y < SCREEN_HEIGHT:
            self.on_ground = False
