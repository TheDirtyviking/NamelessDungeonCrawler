import arcade

def torch_get_picked_up(slayer):
    slayer.change_sight(1)

def sword_get_picked_up(slayer):
    slayer.change_damage(1)

def shield_get_picked_up(slayer):
    slayer.change_armor(1)

def heal_get_picked_up(slayer):
    slayer.heal(3)