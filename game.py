import pygame

from enemy import Enemy
from character import Character


class Game:
    screenWidth = 1400
    screenHeight = 700

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))

    # opens startscreen, waits for start button click
    def startScreen(self):
        self.background = pygame.image.load("images/startScreen.jpg").convert()

        startSoundEffect = pygame.mixer.Sound("sounds/startSoundEffect.wav")

        #placeholder just for now                      #  275, 109     
        startButtonRect = pygame.Rect(0, 0, 275, 109)  # x, y, width, height
        startButtonRect.center = ( self.screenWidth // 2, self.screenWidth // 2 -250) # button slightly offset

        #updates startscreen, x button
        run = True
        while run:
            self.screen.blit(self.background,(300,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if startButtonRect.collidepoint(mouse_pos) and event.button == 1:  # Left mouse button
                        #starts game, plays sound when click on start button
                        startSoundEffect.play()
                        self.gameStart()
                        run = False
            pygame.display.update()
        pygame.quit()


    #intializes game variables, calls main game loop
    def gameStart(self):
        
        self.background = pygame.image.load("images/castle_background.png").convert()
        self.screen.blit(self.background,(0,0))
        self.allSprites = pygame.sprite.Group()
        self.player = Character(300, self.screenHeight - 75, 75, 75, (250, 0, 0))
        self.enemy = Enemy(50, self.screenHeight - 50, 50, 50, (0, 0, 250), self.player)
        self.allSprites.add(self.player)
        self.allSprites.add(self.enemy)
        self.startTime = pygame.time.get_ticks()  # Get initial time

        # put all the stuff in init here so that __init__ wil just be for title screen?
        self.start()
        
    #is the main game loop
    def start(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            delta_time = clock.tick(60) / 1000.0

            #self.screen.fill((0, 0, 0))
            self.screen.blit(self.background,(-20,-220))
            key = pygame.key.get_pressed()  # ✅ Get key state once per frame
            self.player.currentKeys = key  # ✅ Store key state in player instance

            self.allSprites.update(delta_time)
            self.allSprites.draw(self.screen)
            #updates movement, gravity,check on ground
            self.player.update(delta_time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        pygame.quit()


