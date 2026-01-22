# Pygame final
# Author: Lu Ethan
# Date: Jan 20, 2025

import pygame
import random

# COLOURS - (R, G, B)
# CONSTANTS ALL HAVE CAPS FOR THEIR NAMES
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GREY  = (128, 128, 128)

# Coin, base collectable
class Coin(pygame.sprite.Sprite):
    def __init__(self, colour: pygame.Color, width: int, height: int):
        """Coin"""
        super().__init__()

        # Visual representation of our image
        self.image = pygame.image.load("assets/mariocoin.png")
        self.image = pygame.transform.scale_by(self.image, 0.05)

        # A Rect tells you two things:
        #   - how big the hitbox is (width, height)
        #   - where it is (x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100

        self.point_value = 1

    def level_up(self, val: int):
        """Incr point value"""
        self.point_value *= val

# New block that gives 3 times more points but moves around like an enemy at variable speeds
class Star(pygame.sprite.Sprite):
    def __init__(self, colour: pygame.Color, width: int, height: int):
        """Star"""
        super().__init__()

        # Visual representation of star
        self.image = pygame.image.load("assets/mariostar.png")
        self.image = pygame.transform.scale_by(self.image, 0.05)

        self.vel_x = 0
        self.vel_y = 0

        # A Rect tells you two things:
        #   - how big the hitbox is (width, height)
        #   - where it is (x, y)
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100

        # 3 times as valuable as a coin
        self.point_value = 3

    def level_up(self, val: int):
        """Incr point value"""
        self.point_value *= val

    def update(self):
        # movement in the x- and y-axis
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

class Mario(pygame.sprite.Sprite):
    def __init__(self):
        """The player"""
        super().__init__()

        # Right version of Mario and Left version
        self.image_right =  pygame.image.load("assets/mario-snes.png")
        self.image_right = pygame.transform.scale_by(self.image_right, 0.5)
        self.image_left = pygame.transform.flip(self.image_right, True, False)

        self.image = self.image_right
        self.rect = self.image.get_rect()

        self.previous_x = 0               # help with direction
        self.health = 100
        self.points = 0

    def calc_damage(self, amt: int) -> int:
        """Decrease player health by amt
        Returns:
            Remaining health"""
        self.health -= amt
        return self.health

    def incr_score(self, amt: int) -> int:
        """Increases player score by amt
        Returns:
            Score"""
        self.points += amt
        return self.points

    def get_damage_percentage(self) -> float:
        return self.health / 100

    def update(self):
        """Update Mario's location based on the mouse pos
        Update Mario's image based on where he's going"""
        self.rect.center = pygame.mouse.get_pos()

        # If Mario's previous x less than current x
        #   Then Mario is facing Right
        # If Mario's previous x is greater than current x
        #   Then Mario is facing Left
        if self.previous_x < self.rect.x:
            self.image = self.image_right
        elif self.previous_x > self.rect.x:
            self.image = self.image_left

        self.previous_x = self.rect.x

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/goomba-nes.png")
        self.rect = self.image.get_rect()

        self.vel_x = 0
        self.vel_y = 0

        self.damage = 1

    def update(self):
        # movement in the x- and y-axis
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def level_up(self):
        # increase damage
        self.damage *= 2

class HealthBar(pygame.Surface):
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        super().__init__((width, height))

        self.fill(RED)

    def update_info(self, percentage: float):
        """Updates the healthbar with the given percentage"""
        self.fill(RED)
        pygame.draw.rect(self, GREEN, (0, 0, percentage * self._width, self._height))

def game():
    pygame.init()

    # CONSTANTS
    WIDTH = 800
    HEIGHT = 600
    SIZE = (WIDTH, HEIGHT)

    # Creating the Screen
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Collect Blocks")

    # Variables
    done = False
    clock = pygame.time.Clock()
    num_enemies = 5
    num_stars = 5
    num_coins = 100
    health_bar = HealthBar(200, 10)
    level = 1

    # Create a Sprite Group
    all_sprites_group = pygame.sprite.Group()
    coin_sprites_group = pygame.sprite.Group()
    enemy_sprites_group = pygame.sprite.Group()
    star_sprites_group = pygame.sprite.Group()

    # Create Enemies
    for _ in range(num_enemies):
        # Create an enemy
        enemy = Enemy()
        # Randomize movement
        random_x = random.choice([-5, -3, -1, 1, 3, 5])
        random_y = random.choice([-5, -3, -1, 1, 3, 5])
        enemy.vel_x, enemy.vel_y = random_x, random_y
        # Start them in the middle
        enemy.rect.center = (WIDTH/2, HEIGHT/2)

        all_sprites_group.add(enemy)
        enemy_sprites_group.add(enemy)

    # Create stars
    for _ in range(num_stars):
        # Create an enemy
        star = Star("255, 255, 0", 20, 10)
        # Randomize movement
        random_x = random.choice([-5, -3, -1, 1, 3, 5])
        random_y = random.choice([-5, -3, -1, 1, 3, 5])
        star.vel_x, star.vel_y = random_x, random_y
        # Start them in the middle
        star.rect.center = (WIDTH/2, HEIGHT/2)

        all_sprites_group.add(star)
        star_sprites_group.add(star)

    # Create 100 blocks
    # Randomly place them throughout the screen
    for _ in range(num_coins):
        coin = Coin(BLUE, 20, 10)
        # Choose a random position for it
        coin.rect.centerx = random.randrange(0, WIDTH)
        coin.rect.centery = random.randrange(0, HEIGHT)

        all_sprites_group.add(coin)
        coin_sprites_group.add(coin)

    # Create a player
    player = Mario()
    player.rect.center = (WIDTH / 2, HEIGHT / 2)
    # Add the player to the sprite group
    all_sprites_group.add(player)

    # ------------ MAIN GAME LOOP
    while not done:
        # ------ MAIN EVENT LISTENER
        # when the user does something
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ------ GAME LOGIC
        all_sprites_group.update()

        # Keep enemies in screen
        for enemy in enemy_sprites_group:
            if enemy.rect.left < 0 or enemy.rect.right > WIDTH:
                enemy.vel_x = -enemy.vel_x
            if enemy.rect.top < 0 or enemy.rect.bottom > HEIGHT:
                enemy.vel_y = -enemy.vel_y

        for star in star_sprites_group:
            if star.rect.left < 0 or star.rect.right > WIDTH:
                star.vel_x = -star.vel_x
            if star.rect.top < 0 or star.rect.bottom > HEIGHT:
                star.vel_y = -star.vel_y

        # Collision between Player and Blocks
        coins_collided = pygame.sprite.spritecollide(player, coin_sprites_group, True)
        stars_collided = pygame.sprite.spritecollide(player, star_sprites_group, True)
        # if the blocks_collided list has something in it
        # print Mario has collided with a block!
        for coin in coins_collided:
            if type(coin) is Coin:
                print("Player score: ", player.incr_score(coin.point_value))

        for star in stars_collided:
            if type(star) is Star:
                print("Player score: ", player.incr_score(star.point_value))

        # Fill blocks if block list is empty
        # Add more blocks and add one enemy
        if not coin_sprites_group and not star_sprites_group:
            level += 1

            for _ in range(num_coins):
                coin = Coin(BLUE, 20, 10)
                # Choose a random position for it
                coin.rect.centerx = random.randrange(0, WIDTH)
                coin.rect.centery = random.randrange(0, HEIGHT)

                coin.level_up(level)

                all_sprites_group.add(coin)
                coin_sprites_group.add(coin)

            for _ in range(num_stars):
                star = Star("255, 255, 0", 20, 10)
                star.rect.centerx = random.randrange(0, WIDTH)
                star.rect.centery = random.randrange(0, HEIGHT)
                random_x = random.choice([-5, -3, -1, 1, 3, 5])
                random_y = random.choice([-5, -3, -1, 1, 3, 5])
                star.vel_x, star.vel_y = random_x, random_y

                star.level_up(level)

                all_sprites_group.add(star)
                star_sprites_group.add(star)


            enemy = Enemy()
            random_x = random.choice([-5, -3, -1, 1, 3, 5])
            random_y = random.choice([-5, -3, -1, 1, 3, 5])
            enemy.vel_x, enemy.vel_y = random_x, random_y
            # Start them in the middle
            enemy.rect.center = (WIDTH/2, HEIGHT/2)
            all_sprites_group.add(enemy)
            enemy_sprites_group.add(enemy)

            for enemy in enemy_sprites_group:
                enemy.level_up()

        # Collision between Player and Enemies
        enemies_collided = pygame.sprite.spritecollide(player, enemy_sprites_group, False)
        for enemy in enemies_collided:
            # decrease mario's life
            player.calc_damage(enemy.damage)

        health_bar.update_info(player.get_damage_percentage())

        # Game ends when Player's health is zero or less
        if player.health <= 0:
            done = True

        # ------ DRAWING TO SCREEN
        screen.fill(WHITE)
        all_sprites_group.draw(screen)
        screen.blit(health_bar, (10, 10))

        # Update screen
        pygame.display.flip()

        # ------ CLOCK TICK
        clock.tick(60) # 60 fps

    # Display final score:
    print("Thanks for playing!")
    print("Final score is:", player.points)

    pygame.quit()

if __name__ == "__main__":
    game()
