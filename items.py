import arcade
import sound_manager

def torch_get_picked_up(slayer):
    slayer.change_sight(.5)
    sound_manager.play_sound(sound_manager.TORCH_PICKUP, .15)

def sword_get_picked_up(slayer):
    slayer.change_damage(1)
    sound_manager.play_sound(sound_manager.SWORD_PICKUP, .15)

def shield_get_picked_up(slayer):
    slayer.change_armor(1)
    sound_manager.play_sound(sound_manager.SHIELD_PICKUP, .15)

def heal_get_picked_up(slayer):
    slayer.heal(3)
    sound_manager.play_sound(sound_manager.HEAL, .15)