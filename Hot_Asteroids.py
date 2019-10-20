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
        self.player_name = ""
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
        arcade.draw_text("Press Esc to continue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 75,
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
        arcade.draw_text("Use space bar to shoot", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press Esc to continue", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Also press ESC to pause the game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            game_view = GameView()
            self.window.show_view(game_view)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        arcade.set_background_color(arcade.color.FOREST_GREEN)

    def on_draw(self):
        arcade.start_render()

        # Draw player so they will know their current placement if they unpause
        player_sprite = self.game_view.player_sprite
        player_sprite.draw()

        # draw an green filter over him
        arcade.draw_lrtb_rectangle_filled(left=player_sprite.left, right=player_sprite.right,
                                          top=player_sprite.top, bottom=player_sprite.bottom,
                                          color=arcade.color.FOREST_GREEN + (200,))

        arcade.draw_text("PAUSED", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         SCREEN_WIDTH/2, SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        # Resume the game
        if key == arcade.key.ESCAPE:
            arcade.set_background_color(arcade.color.BLACK)
            self.window.show_view(self.game_view)
        # Restart the game (level)
        elif key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)


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
        self.player_start_health = 9
        self.survival_time = 0

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

        # Put player health on the screen
        player_health = f"Health: {self.player_start_health}"
        arcade.draw_text(player_health, 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 14)

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


        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this views state?
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        self.survival_time += delta_time
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()
        self.asteroid_list.update()
        self.laser_one_list.update()
        self.laser_two_list.update()

        # prevent player from going out of bounds
        if self.player_sprite.left < 0 or self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.change_x = 0
        if self.player_sprite.bottom < 0 or self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.change_y = 0

        # Generate a list of all sprites that collided with the player
        asteroids_crash_list = arcade.check_for_collision_with_list(self.player_sprite, self.asteroid_list)

        # loop through each colliding sprite, remove it, and subtract from player health
        for asteroid in asteroids_crash_list:
            asteroid.center_y = random.randint(SCREEN_HEIGHT + 50, 1250)
            asteroid.center_x = random.randrange(SCREEN_WIDTH)
            self.score -= 3
            self.player_start_health -= 1

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

        if self.player_start_health == 0:
            game_over_view = GameOver()
            game_over_view.survival_time = self.survival_time
            game_over_view.score = self.score
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)

class GameOver(arcade.View):
    def __init__(self):
        super().__init__()
        self.survival_time = 0
        self.score = 0

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        # Put game over across the screen
        arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2.75, SCREEN_HEIGHT - 300, arcade.color.WHITE, font_size = 36)
        arcade.draw_text("Press enter to restart", SCREEN_WIDTH / 2.85, SCREEN_HEIGHT - 350, arcade.color.WHITE,
                         font_size = 24)

        time_taken_formatted = f"{round(self.survival_time, 2)} seconds"
        arcade.draw_text(f"Time Survived: {time_taken_formatted}",
                         SCREEN_WIDTH/2, SCREEN_HEIGHT - 400,
                         arcade.color.BLUE_BELL,font_size=15, anchor_x="center")

        output_total = f"Total Score: {self.score}"
        arcade.draw_text(output_total,
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT - 450,
                         arcade.color.BLUE_BELL, font_size=15, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        # Resume the game
        if key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)

def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
