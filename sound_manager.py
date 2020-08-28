import arcade
import time
import random

PLAYER_ATTACK = 0
GOBLIN_ATTACK = 1
PLAYER_DEATH = 2
GOBLIN_DEATH = 3
HEAL = 4
SWORD_PICKUP = 5
SHIELD_PICKUP = 6
TORCH_PICKUP = 7
ROOM_CLEAR = 8
GAME_WIN = 9
BACKGROUND_MUSIC = 0
SOUND_LIBRARY = [
    ["resources/sounds/player_attack_1.mp3", "resources/sounds/player_attack_2.mp3", "resources/sounds/player_attack_3.mp3"],
    ["resources/sounds/goblin_attack_1.mp3", "resources/sounds/goblin_attack_2.mp3", "resources/sounds/goblin_attack_3.mp3"],
    ["resources/sounds/player_death.mp3"],
    ["resources/sounds/goblin_death_1.mp3", "resources/sounds/goblin_death_2.mp3", "resources/sounds/goblin_death_3.mp3"],
    ["resources/sounds/heal.wav"],
    ["resources/sounds/sword_1.mp3", "resources/sounds/sword_2.mp3"],
    ["resources/sounds/shield.mp3"],
    ["resources/sounds/torch.mp3"],
    ["resources/sounds/room_clear.mp3"],
    ["resources/sounds/game_win.mp3"],
    ["resources/sounds/background_music.mp3"]
]
MUSIC_LIBRARY = [
    ["resources/sounds/background_music.mp3"]
]

def play_sound(sound_type, vol):
    sound_options = SOUND_LIBRARY[sound_type]
    selected = random.randrange(0, len(sound_options))
    sound = arcade.Sound(sound_options[selected], True)
    sound.play(volume=vol)

class MusicManager():

    def __init__(self):
        self.music = None

    def play_music(self, music_type):
        music_options = MUSIC_LIBRARY[music_type]
        selected = random.randrange(0, len(music_options))
        music = arcade.Sound(music_options[selected], True)
        music.play(.05)
        self.music = music