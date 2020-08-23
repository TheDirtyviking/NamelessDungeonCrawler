import arcade
import room_setup
import os
import playerUI
import slayer
import menuHandler
import sys

SPRITE_SCALING = .6
PLAYER_SCALING = .9
SPRITE_NATIVE_SIZE = 100
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)
SCREEN_WIDTH = SPRITE_SIZE * 25
SCREEN_HEIGHT = SPRITE_SIZE * 15
SCREEN_TITLE = "Nameless Dungeon Crawler"
PLAYER_DAMAGE = 3
PLAYER_HEALTH = 10
PLAYER_ARMOR = 0
MOVEMENT_SPEED = 5

class NamelessDungeonCrawler(arcade.Window):
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.current_room = 0

        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False

        self.slayer = None

        self.player_ui = None

        self.handler = None

        self.in_menu = False
    
    def setup(self):
        
        self.handler = menuHandler.Menu_Handler(self)
        self.in_menu = True

    def game_setup(self):
        self.player_sprite = arcade.Sprite("resources/images/slayer.png", PLAYER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 100
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.slayer = slayer.Slayer()

        self.rooms = []
        room = room_setup.setup_room_1()
        self.rooms.append(room)
        self.current_room = 0
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

        self.player_ui = playerUI.playerUI()
        self.player_ui.setup()

        self.attack_cooldown = 0


    def on_draw(self):
        arcade.start_render()
        
        if self.in_menu:
            self.handler.draw_menu()
        else:
            self.rooms[self.current_room].floor_list.draw()
            self.rooms[self.current_room].wall_list.draw()
            self.rooms[self.current_room].accent_list.draw()
            self.rooms[self.current_room].item_list.draw()
            self.rooms[self.current_room].enemy_list.draw()
            self.rooms[self.current_room].player_attack_list.draw()
            self.rooms[self.current_room].enemy_attack_list.draw()
            self.rooms[self.current_room].fog_list.draw()
            self.player_ui.on_draw(self.slayer.health, self.slayer.armor)
            self.player_list.draw()

    def on_update(self, delta_time):
        if not self.in_menu and self.slayer.health <= 0:
            self.in_menu = True
            self.handler.set_menu(menuHandler.GAME_OVER)
        if self.in_menu:
            self.handler.draw_menu()
        else:
            self.physics_engine.update()

            if self.rooms[self.current_room].next_room(self.player_sprite.center_x, self.player_sprite.center_y):
                self.win_game()

            item_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.rooms[self.current_room].item_list)

            for hit_item in item_hit_list:
                hit_item.pickup(self.slayer)
                self.rooms[self.current_room].item_list.remove(hit_item)

            if self.player_sprite.change_y == 0 and ((self.w_pressed and not self.s_pressed) or (self.s_pressed and not self.w_pressed)):
                if self.w_pressed:
                    self.player_sprite.change_y = self.slayer.movespeed
                elif self.s_pressed:
                    self.player_sprite.change_y = -self.slayer.movespeed
            
            if self.player_sprite.change_x == 0 and ((self.a_pressed and not self.d_pressed) or (self.d_pressed and not self.a_pressed)):
                if self.a_pressed:
                    self.player_sprite.change_x = -self.slayer.movespeed
                elif self.d_pressed:
                    self.player_sprite.change_x = self.slayer.movespeed

            self.slayer.update_position(self.player_sprite.center_x, self.player_sprite.center_y)
            
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

            room_setup.update_player_attacks(self.rooms[self.current_room])
            room_setup.update_fog(self.rooms[self.current_room], self.player_sprite.position, self.slayer.sight)
            room_setup.update_enemies(self.rooms[self.current_room], self.player_sprite.position)
            room_setup.update_enemy_attacks(self.rooms[self.current_room], self.player_sprite, self.slayer)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = True
            if self.s_pressed:
                self.player_sprite.change_y = 0
            else:
                self.player_sprite.change_y = self.slayer.movespeed
        elif key == arcade.key.S:
            self.s_pressed = True
            if self.w_pressed:
                self.player_sprite.change_y = 0
            else:
                self.player_sprite.change_y = -self.slayer.movespeed
        elif key == arcade.key.D:
            self.d_pressed = True
            if self.a_pressed:
                self.player_sprite.change_x = 0
            else:
                self.player_sprite.change_x = self.slayer.movespeed
        elif key == arcade.key.A:
            self.a_pressed = True
            if self.d_pressed:
                self.player_sprite.change_x = 0
            else:
                self.player_sprite.change_x = -self.slayer.movespeed
        elif key == arcade.key.ESCAPE:
            self.handler.set_menu(menuHandler.PAUSE)
            self.in_menu = not self.in_menu

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.w_pressed = False
            if self.s_pressed:
                self.player_sprite.change_y = -self.slayer.movespeed
            else:
                self.player_sprite.change_y = 0
        elif key == arcade.key.S:
            self.s_pressed = False
            if self.w_pressed:
                self.player_sprite.change_y = self.slayer.movespeed
            else:
                self.player_sprite.change_y = 0
        elif key == arcade.key.D:
            self.d_pressed = False
            if self.a_pressed:
                self.player_sprite.change_x = -self.slayer.movespeed
            else:
                self.player_sprite.change_x = 0
        elif key == arcade.key.A:
            self.a_pressed = False
            if self.d_pressed:
                self.player_sprite.change_x = self.slayer.movespeed
            else:
                self.player_sprite.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.in_menu:
            if self.attack_cooldown == 0:
                spawn_x = self.player_sprite.center_x
                spawn_y = self.player_sprite.center_y
                base_angle = 0
                if x > self.player_sprite.center_x + 25:
                    spawn_x += 40
                    base_angle = 360
                elif x < self.player_sprite.center_x - 25:
                    spawn_x -= 40
                    base_angle = 180
                if y < self.player_sprite.center_y - 25:
                    spawn_y -= 40
                    if base_angle == 180:
                        base_angle += 45
                    elif base_angle == 360:
                        base_angle -= 45
                    else:
                        base_angle = 270
                elif y > self.player_sprite.center_y + 25:
                    spawn_y += 40
                    if base_angle == 180:
                        base_angle -= 45
                    elif base_angle == 360:
                        base_angle += 45
                    else:
                        base_angle = 90
                if spawn_x == self.player_sprite.center_x and spawn_y == self.player_sprite.center_y:
                    spawn_x += 40
                    spawn_y += 40
                spawn_angle = base_angle
                room_setup.add_player_attack(self.rooms[self.current_room], spawn_x, spawn_y, spawn_angle, self.slayer.damage)
                self.attack_cooldown = 15
        else:
            self.check_mouse_press_for_buttons(x, y, self.handler.menu_list[self.handler.menu].buttons)

    def on_mouse_release(self, x, y, button, modifiers):
        self.check_mouse_release_for_buttons(self.handler.menu_list[self.handler.menu].buttons)

    def start_game(self):
        self.in_menu = False
        self.game_setup()

    def resume_game(self):
        self.in_menu = False

    def quit_game(self):
        arcade.close_window()

    def win_game(self):
        self.in_menu = True
        self.handler.set_menu(menuHandler.WIN)

    def check_mouse_press_for_buttons(self, x, y, button_list):
        for button in button_list:
            if x > button.center_x + button.width / 2:
                continue
            if x < button.center_x - button.width / 2:
                continue
            if y > button.center_y + button.height / 2:
                continue
            if y < button.center_y - button.height / 2:
                continue
            button.on_press()

    def check_mouse_release_for_buttons(self, button_list):
        for button in button_list:
            if button.pressed:
                button.on_release()

def main():
    game = NamelessDungeonCrawler(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()