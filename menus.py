import arcade
import arcade.gui
import menuHandler
import button

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

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.add_button('Start', 750, 500, self.click)
        self.add_text('A Nameless Dungeon Crawler', 750, 800, 500)

    def click(self):
        self.game.start_game()

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
