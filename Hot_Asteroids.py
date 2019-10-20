import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Hot Asteroids"
MOVEMENT_SPEED = 5

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ASTEROID = .5
ASTEROID_COUNT = 75
SPRITE_SCALING_LASER = 1
LASER_SPEED = 5


class Character(arcade.Sprite):
    def __init__(self, position_x, position_y, change_x, change_y, radius, color):
        self.name = ""
        self.shipcolor = "Blue"
        self.max_hit_points = 0
        self.current_hit_points = 0
        self.max_speed = 0
        self.armor_amount = 0
        self.position_x = position_x
        self.position_y = position_y
        self.radius = radius
        self.change_x = change_x
        self.change_y = change_y
        self.color = color

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


class Asteroid(arcade.Sprite):

    def update(self):
        self.center_y -= 5

        # make the asteroids reappear once off screen
        if self.center_y < -random.randint(50, 250):
            self.center_y = SCREEN_HEIGHT + 20
            self.center_x = random.randrange(SCREEN_WIDTH)


'''
A pause screen and start up screen are two separate classes. These must be created separately

'''


class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Main Menu", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.FOREST_GREEN, font_size=50, anchor_x="center")
        arcade.draw_text("Press Esc to continue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2)-75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            instructions_view = InstructionView()
            self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.FOREST_GREEN)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Use the arrow keys to move", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Use spacebar to shoot", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press Esc to continue", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            game_view = GameView()
            self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Variables that will hold sprite lists.
        self.player_list = None
        self.asteroid_list = None
        self.laser_one_list = None
        self.laser_two_list = None
        self.all_sprites_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        arcade.set_background_color(arcade.color.BLACK)

        self.laser_sound = arcade.sound.load_sound("sounds/laser3.ogg")
        self.start_up_sound = arcade.sound.load_sound("sounds/lowThreeTone.ogg")
        self.explosion_sound = arcade.sound.load_sound("sounds/explosion.wav")
        arcade.sound.play_sound(self.start_up_sound)

        # Sprite List
        self.player_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.laser_one_list = arcade.SpriteList()
        self.laser_two_list = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the Player
        self.player_sprite = arcade.Sprite("art\ship.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the Asteroids
        for i in range(ASTEROID_COUNT):
            # Create a random float size for the asteroid scale
            asteroid_Scale = (random.randint(35, 100) / 100)

            # Create the asteroid instance
            asteroid = Asteroid("art\meteorBrown.png", asteroid_Scale)

            # Position the asteroid
            asteroid.center_x = random.randrange(SCREEN_WIDTH)
            asteroid.center_y = random.randint(SCREEN_HEIGHT + 50, 1250)

            # Add the asteroid to the lists
            self.asteroid_list.append(asteroid)

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        # Call draw() on all your sprite lists below

        self.asteroid_list.draw()
        self.player_list.draw()
        self.laser_one_list.draw()
        self.laser_two_list.draw()

        # Putting the Score on screen
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, SCREEN_HEIGHT - 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, key_modifiers):
        """
        Calls whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED

        if key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        if key == arcade.key.SPACE:
            laser_one = arcade.Sprite('art\laserGreen13.png', SPRITE_SCALING_LASER)
            laser_two = arcade.Sprite('art\laserGreen13.png', SPRITE_SCALING_LASER)
            arcade.sound.play_sound(self.laser_sound)
            arcade.sound.play_sound(self.laser_sound)

            laser_one.change_y = LASER_SPEED
            laser_two.change_y = LASER_SPEED
            laser_one.center_x = self.player_sprite.center_x + 15
            laser_one.bottom = self.player_sprite.top - 35
            laser_two.center_x = self.player_sprite.center_x - 15
            laser_two.bottom = self.player_sprite.top - 35

            self.laser_one_list.append(laser_one)
            self.laser_two_list.append(laser_two)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()
        self.asteroid_list.update()
        self.laser_one_list.update()
        self.laser_two_list.update()

        # Generate a list of all sprites that collided with the player
        asteroids_crash_list = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)

        # loop through each colliding sprite, remove it, and add it to the score
        for asteroid in asteroids_crash_list:
            asteroid.center_y = random.randint(SCREEN_HEIGHT + 50, 1250)
            asteroid.center_x = random.randrange(SCREEN_WIDTH)
            self.score -= 1

        for laser in self.laser_one_list:

            # call the laser and bullet sprites
            self.laser_one_list.update()

            # check if the laser if a asteroid
            hit_list = arcade.check_for_collision_with_list(laser, self.asteroid_list)

            # If they did hit get rid of the asteroid
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()
                laser.kill()

            # for every asteroid we hit, add to the score and remove it
            for asteroid in hit_list:
                asteroid.remove_from_sprite_lists()
                self.score += 1
                arcade.sound.play_sound(self.explosion_sound)

                for i in range(ASTEROID_COUNT - len(self.asteroid_list)):
                    # Create a random float size for the asteroid scale
                    asteroid_Scale = (random.randint(35, 100) / 100)

                    # Create the asteroid instance
                    asteroid = Asteroid("art\meteorBrown.png", asteroid_Scale)

                    # Position the asteroid
                    asteroid.center_x = random.randrange(SCREEN_WIDTH)
                    asteroid.center_y = random.randint(SCREEN_HEIGHT + 50, 1250)

                    # Add the asteroid to the lists
                    self.asteroid_list.append(asteroid)

            # if the laser flies off screen remove it
            if laser.bottom > SCREEN_HEIGHT + 30:
                laser.remove_from_sprite_lists()
                laser.kill()

        for laser in self.laser_two_list:

            # call the laser and bullet sprites
            self.laser_two_list.update()

            # check if the laser if a asteroid
            hit_list = arcade.check_for_collision_with_list(laser, self.asteroid_list)

            # If they did hit get rid of the asteroid
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()
                laser.kill()

            # for every asteroid we hit, add to the score and remove it
            for asteroid in hit_list:
                asteroid.remove_from_sprite_lists()
                self.score += 1
                arcade.sound.play_sound(self.explosion_sound)

                for i in range(ASTEROID_COUNT - len(self.asteroid_list)):
                    # Create a random float size for the asteroid scale
                    asteroid_Scale = (random.randint(35, 100) / 100)

                    # Create the asteroid instance
                    asteroid = Asteroid("art\meteorBrown.png", asteroid_Scale)

                    # Position the asteroid
                    asteroid.center_x = random.randrange(SCREEN_WIDTH)
                    asteroid.center_y = random.randint(SCREEN_HEIGHT + 50, 1250)

                    # Add the asteroid to the lists
                    self.asteroid_list.append(asteroid)

            # if the laser flies off screen remove it
            if laser.bottom > SCREEN_HEIGHT + 30:
                laser.remove_from_sprite_lists()
                laser.kill()


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

    # game.setup()
    # arcade.run()


if __name__ == "__main__":
    main()
