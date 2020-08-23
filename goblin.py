import arcade
import room_setup

class Goblin():

    def __init__(self,  health = 4, damage = 2, armor = 0, center_x = 0, center_y = 0):
        self.health = health
        self.damage = damage
        self.armor = armor
        self.x = center_x
        self.y = center_y
        self.movespeed = 3
        self.attack_cooldown = 0
        

    def die(self, room, left, bottom):
        blood_splatter = arcade.Sprite("resources/images/blood.png", .7)
        blood_splatter.left = left
        blood_splatter.bottom = bottom
        room.accent_list.append(blood_splatter)
        #play a sound effect

    def take_damage(self, damage):
        pain = damage - self.armor
        if pain > 0:
            self.health -= pain
            #play a sound effect

    def update(self, slayer_position, room, sprite):
        self.x = sprite.center_x
        self.y = sprite.center_y
        self.attack_cooldown -= 1
        if arcade.has_line_of_sight(slayer_position, (self.x, self.y), room.wall_list) and not arcade.has_line_of_sight(slayer_position, (self.x, self.y), room.wall_list, 50):
            if slayer_position[0] - (self.x, self.y)[0] <= -6:
                sprite.change_x = -self.movespeed
            elif slayer_position[0] - (self.x, self.y)[0] >= 6:
                sprite.change_x = self.movespeed
            else:
                sprite.change_x = 0
            if slayer_position[1] - (self.x, self.y)[1] <= -6:
                sprite.change_y = -self.movespeed
            elif slayer_position[1] - (self.x, self.y)[1] >= 6:
                sprite.change_y = self.movespeed
            else:
                sprite.change_y = 0
        if arcade.has_line_of_sight(slayer_position, (self.x, self.y), room.wall_list, 50):
            if self.attack_cooldown <= 0:
                spawn_x = self.x
                spawn_y = self.y
                base_angle = 0
                if slayer_position[0] > self.x + 25:
                    spawn_x += 40
                    base_angle = 360
                elif slayer_position[0] < self.x - 25:
                    spawn_x -= 40
                    base_angle = 180
                if slayer_position[1] < self.y - 25:
                    spawn_y -= 40
                    if base_angle == 180:
                        base_angle += 45
                    elif base_angle == 360:
                        base_angle -= 45
                    else:
                        base_angle = 270
                elif slayer_position[1] > self.y + 25:
                    spawn_y += 40
                    if base_angle == 180:
                        base_angle -= 45
                    elif base_angle == 360:
                        base_angle += 45
                    else:
                        base_angle = 90
                if spawn_x == self.x and spawn_y == self.y:
                    spawn_x += 40
                spawn_angle = base_angle
                room_setup.add_enemy_attack(room, spawn_x, spawn_y, spawn_angle, self.damage)
                self.attack_cooldown = 20
        