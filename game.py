import pygame

from enemy import Enemy
from character import Character


class Game:
    SCREEN_WIDTH = 1400
    SCREEN_HEIGHT = 700

    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #self.background = pygame.image.load("images/startScreen.jpg")
        #self.screen.blit(self.background,(0,0))
        #enemy stuff
        #self.enemy = Enemy(50,50,50,50)

    # opens startscreen, waits for start button click
    def startScreen(self):
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.background = pygame.image.load("images/startScreen.jpg")
        #self.screen.blit(self.background,(0,0))

        #placeholder just for now
        startButtonRect = pygame.Rect(100, 100, 500, 500)  # x, y, width, height

        run = True
        while run:
            self.screen.blit(self.background,(300,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if startButtonRect.collidepoint(mouse_pos) and event.button == 1:  # Left mouse button
                        #starts game when click on start button
                        self.game_start()
                        run = False
            pygame.display.update()
        pygame.quit()


    #intializes game variables, calls main game loop
    def game_start(self):
        
        self.background = pygame.image.load("images/castle_background.png")
        self.screen.blit(self.background,(0,0))
        self.all_sprites = pygame.sprite.Group()
        self.player = Character(300, 250, 100, 100, (250, 0, 0))
        self.enemy = Enemy(50, 50, 50, 50)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy)
        self.start_time = pygame.time.get_ticks()  # Get initial time

        # put all the stuff in init here so that __init__ wil just be for title screen?
        self.start()
        
    #is the main game loop
    def start(self):
        run = True
        while run:
            #self.screen.fill((0, 0, 0))
            self.screen.blit(self.background,(-20,-220))
            key = pygame.key.get_pressed()  # ✅ Get key state once per frame
            self.player.current_keys = key  # ✅ Store key state in player instance

            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            #updates movement, gravity,check on ground
            self.player.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()


game = Game()
screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
