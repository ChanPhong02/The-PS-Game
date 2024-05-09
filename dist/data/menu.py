import pygame, sys

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = game.screen_width / 2, game.screen_height / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 100, 100)
        self.offset = - 160

    def draw_cursor(self):
        self.game.draw_text('>', 50, self.cursor_rect.x + 80, self.cursor_rect.y + 160, 'red')


    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
    
    def background(self):
        self.game.background = pygame.image.load('data/graphics/background.png')
        self.game.background = pygame.transform.scale(self.game.background, (1280, 720))
        self.game.display.blit(self.game.background, (0,0))

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h - 50
        self.quitx, self.quity = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 10)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.background()
            self.title_font = pygame.font.Font('data/font/Pixeltype.ttf', 200)
            self.text_font = pygame.font.Font('data/font/Pixeltype.ttf', 50)
            #self.game.draw_text(('The PS Game'), 100, self.game.screen_width / 2, self.game.screen_height / 2 - 200, 'white')
            self.title = self.title_font.render('PS Platformer', False,'White')
            self.game.display.blit(self.title,(self.game.screen_width / 2 - 350, self.game.screen_height / 2 - 250))
            #self.game.draw_text("Start Game", 50, self.startx, self.starty, 'white')
            self.text = self.text_font.render('Start Game', False,'White')
            self.game.display.blit(self.text,(self.startx - 90, self.starty + 150))
            #self.game.draw_text("Quit Game", 50, self.quitx, self.quity, 'white')
            self.text = self.text_font.render('Quit Game', False,'White')
            self.game.display.blit(self.text,(self.quitx - 78, self.quity + 120))
            self.game.draw_text('Made by The PS Team', 20, self.game.screen_width / 2, self.game.screen_height / 2 + 300, 'cyan')
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity - 30)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 5)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity - 25)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty - 10)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.run_display = False
                self.game.playing = True
            elif self.state == 'Quit':
                self.game.curr_menu = self.game.quit
            self.run_display = False

class QuitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        pygame.quit()
        sys.exit()

