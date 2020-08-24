#This file will hold all the player information
import arcade
import math

class Slayer():

    def __init__(self):
        self.health = 10
        self.damage = 3
        self.armor = 0
        self.sight = 2
        self.movespeed = 5
        self.position = [100, 100]
        self.attack_range = 50

    def take_damage(self, damage):
        self.health -= (damage - self.armor)

    def heal(self, health):
        self.health += health
        if self.health > 10:
            self.health = 10
    
    def change_sight(self, vision):
        self.sight += vision

    def change_armor(self, armor):
        self.armor += armor

    def change_damage(self, damage):
        self.damage += damage

    def attack(self):
        pass #Add combat logic here

    def update_position(self, x, y):
        self.position = [x, y]

