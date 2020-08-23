import arcade
import menus
MAIN = 0
PAUSE = 1
GAME_OVER = 2
WIN = 3

class Menu_Handler():
    def __init__(self, game):
        self.menu = 0
        self.menu_list = list()
        self.menu_list.append(menus.MainMenu(game))
        self.menu_list.append(menus.PauseMenu(game, self))
        self.menu_list.append(menus.GameOverMenu(game, self))
        self.menu_list.append(menus.WinMenu(game, self))
    
    def set_menu(self, menu):
        self.menu = menu

    def draw_menu(self):
        self.menu_list[self.menu].draw()