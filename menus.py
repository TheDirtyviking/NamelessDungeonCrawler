import arcade
import arcade.gui
import menuHandler
import button
import game as gm

EASY = 0
MODERATE = 1
HARD = 2

class Menu():
    def __init__(self):
        self.buttons = list()
        self.texts = arcade.SpriteList()
        self.accents = arcade.SpriteList()

    def add_button(self, text, x, y, on_click):
        newbutt = button.TextButton(x, y, 250, 45, text, on_click)
        self.buttons.append(newbutt)

    def add_text(self, text, x, y, width = 250):
        text_box = arcade.gui.UILabel(text, center_x = x, center_y = y, width = width)
        self.texts.append(text_box)
    
    def add_accent(self, x, y, image):
        accent = arcade.Sprite(image)
        accent.center_x = x
        accent.center_y = y
        self.accents.append(accent)
    
    def draw(self):
        for button in self.buttons:
            button.draw()
        self.texts.draw()
        self.accents.draw()

    def remove_button(self, button):
        for b in self.buttons:
            if b.text == button:
                self.buttons.remove(b)

    def remove_text(self, text):
        for t in self.texts:
            if t.text == text:
                self.texts.remove(t)

class MainMenu(Menu):
    def __init__(self, game, handler):
        super().__init__()
        self.game = game
        self.handler = handler
        self.add_button('Start', 750, 500, self.click)
        self.add_text('A Nameless Dungeon Crawler', 750, 800, 500)
        self.add_button('Options', 750, 300, self.option_click)

    def click(self):
        self.game.start_game()
    
    def option_click(self):
        self.handler.set_menu(menuHandler.OPTIONS)

class PauseMenu(Menu):
    def __init__(self, game, handler):
        super().__init__()
        self.game = game
        self.handler = handler
        self.add_button('Resume', 750, 450, self.resume_click)
        self.add_button('Main Menu', 750, 300, self.main_click)
        self.add_button('Quit', 750, 150, self.quit_click)
        self.add_text('A Nameless Dungeon Crawler', 750, 800, 500)
        self.add_text('PAUSED', 750, 650)

    def quit_click(self):
        self.game.quit_game()

    def main_click(self):
        self.handler.set_menu(menuHandler.MAIN)

    def resume_click(self):
        self.game.resume_game()

class GameOverMenu(Menu):
    def __init__(self, game, handler):
        super().__init__()
        self.handler = handler
        self.game = game
        self.add_button('Main Menu', 750, 450, self.main_click)
        self.add_button('Quit', 750, 300, self.quit_click)
        self.add_text('GAME OVER', 750, 600)

    def main_click(self):
        self.handler.set_menu(menuHandler.MAIN)

    def quit_click(self):
        self.game.quit_game()

class WinMenu(Menu):
    def __init__(self, game, handler):
        super().__init__()
        self.game = game
        self.handler = handler
        self.add_button('Main Menu', 750, 250, self.main_click)
        self.add_button('Quit', 750, 450, self.quit_click)
        self.add_text('VICTORY', 750, 600)

    def main_click(self):
        self.handler.set_menu(menuHandler.MAIN)

    def quit_click(self):
        self.game.quit_game()

class OptionMenu(Menu):
    def __init__(self, game, handler):
        super().__init__()
        self.game = game
        self.handler = handler
        self.current_difficulty = MODERATE
        self.add_button('Easy', 400, 500, self.easy_click)
        self.add_text('Moderate', 750, 500)
        self.add_button('Hard', 1100, 500, self.hard_click)
        self.add_button('Main Menu', 750, 300, self.main_click)

    def easy_click(self):
        self.game.set_difficulty(gm.EASY)
        self.add_difficulty_button(EASY)
        self.current_difficulty = EASY

    def moderate_click(self):
        self.game.set_difficulty(gm.MODERATE)
        self.add_difficulty_button(MODERATE)
        self.current_difficulty = MODERATE

    def hard_click(self):
        self.game.set_difficulty(gm.HARD)
        self.add_difficulty_button(HARD)
        self.current_difficulty = HARD

    def main_click(self):
        self.handler.set_menu(menuHandler.MAIN)

    def add_difficulty_button(self, difficulty):
        if self.current_difficulty == EASY:
            self.remove_text('Easy')
            self.add_button('Easy', 400, 500, self.easy_click)
        elif self.current_difficulty == MODERATE:
            self.remove_text('Moderate')
            self.add_button('Moderate', 750, 500, self.moderate_click)
        elif self.current_difficulty == HARD:
            self.remove_text('Hard')
            self.add_button('Hard', 1100, 500, self.hard_click)
        if difficulty == EASY:
            self.remove_button('Easy')
            self.add_text('Easy', 400, 500)
        elif difficulty == MODERATE:
            self.remove_button('Moderate')
            self.add_text('Moderate', 750, 500)
        elif difficulty == HARD:
            self.remove_button('Hard')
            self.add_text('Hard', 1100, 500)

        
    

