import arcade

UI_Y = 845
HEALTH_BAR_X = 25
SPRITE_SCALING = .7

def draw_health(ui, health):
    next_x = HEALTH_BAR_X
    for x in range (0, health):
        half_heart = None
        if x % 2 == 0:
            half_heart = arcade.Sprite("resources/images/left-heart.png", SPRITE_SCALING)
            half_heart.left = next_x
            next_x += 19
        else:
            half_heart = arcade.Sprite("resources/images/right-heart.png", SPRITE_SCALING)
            half_heart.left = next_x
            next_x += 34
        half_heart.bottom = UI_Y
        ui.health_bar.append(half_heart)
    background = arcade.Sprite("resources/images/health_background.png", .8, image_width=300, image_height=100)
    background.left = 10
    background.bottom = 835
    ui.extras.append(background)
    background2 = arcade.Sprite("resources/images/health_background.png", .8, flipped_horizontally=True, image_width=300, image_height=100)
    background2.left = 65
    background2.bottom = 835
    ui.extras.append(background2)


class playerUI():

    def __init__(self):
        self.health_bar = None
        self.extras = None

    def setup(self):
        self.health_bar = arcade.SpriteList()
        self.extras = arcade.SpriteList()

    def on_draw(self, player_health, player_armor):
        draw_health(self, player_health)
        self.extras.draw()
        self.health_bar.draw()
        self.health_bar = arcade.SpriteList()
        self.extras = arcade.SpriteList()
        