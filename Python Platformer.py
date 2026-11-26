
                #----------PYTHON-PLATFORMER----------#
                #                                     #
                # Copyright (c) Henrique Oliveira 2015#
                #                                     #
                #---------------CREDITS---------------#
                # Marc Wahab - Debugging - Insperation#
                # iD Tech - Debugging                 #
                # Geometry Dash - Insperation         #
                #-------------------------------------#


##Run this game: python3 "Python Platformer.py"
##Install pygame if you don't have it: pip install pygame


import pygame

# Colors
# Global constants

PURPLE = (160, 32, 240)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 45
        height = 45
        self.image = pygame.Surface([width, height])
        self.image.fill(PURPLE)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        self.update_level = False

        # List of sprites we can bump against
        self.level = None

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x

        # hits lava level 1
        if isinstance(self.level, Level_01) and self.rect.bottom == 690 and self.rect.left > 400:
            self.rect.x = 20
            self.rect.y = 680

        # hits portal level 1
        elif isinstance(self.level, Level_01) and self.rect.left >= 0 and self.rect.right <= 150 and self.rect.bottom == 375:
            self.rect.x = 20
            self.rect.y = 680
            self.update_level = True

# hits lava level 2
        if isinstance(self.level, Level_02) and self.rect.bottom == 690 and self.rect.left > 400:
            self.rect.x = 20
            self.rect.y = 680

        # hits portal level 2
        elif isinstance(self.level, Level_02) and self.rect.right >= 1300 and self.rect.bottom >= 290:
            self.rect.x = 20
            self.rect.y = 680
            self.update_level = True

# hits lava level 3
        if isinstance(self.level, Level_03) and self.rect.bottom == 690 and self.rect.left > 400:
            self.rect.x = 20
            self.rect.y = 680

        # hits portal level 3
        elif isinstance(self.level, Level_03) and self.rect.right >= 1000 and self.rect.bottom >= 410:
            self.rect.x = 20
            self.rect.y = 680
            self.update_level = True

        else:
            # See if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:


                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right

            # Move up/down
            self.rect.y += self.change_y

            # Check and see if we hit anything
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:

                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom

                # Stop our vertical movement
                self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .30

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()



class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLACK)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

#----------LEVEL-I------------#
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[160, 30, 250, 500],
                 [160, 30, 500, 400],
                 [160, 30, 700, 300],
                 [160, 30, 100, 600],
                 [400, 10, 0, 690],
                 [160, 30, 1000, 400],
                 [160, 30, 1200, 250],
                 [160, 30, 990, 160],
                 [160, 30, 530, 120],
                 [160, 30, 250, 200],
                 [30, 200, 150, 280],
                 [160, 30, 0, 450],
                 [160, 30, 760, 100]
                 ]

        # Go through the array above and add platforms
        for platform in level:
                block = Platform(platform[0], platform[1])
                block.rect.x = platform[2]
                block.rect.y = platform[3]
                block.player = self.player
                self.platform_list.add(block)

        restart = Platform(1000, 10)
        restart.rect.x = 400
        restart.rect.y = 690
        restart.image = pygame.Surface([1000, 10])
        restart.image.fill(RED)
        self.platform_list.add(restart)

        portal = Platform(150, 80)
        portal.rect.x = 0
        portal.rect.y = 375
        portal.image = pygame.Surface([150, 80])
        portal.image.fill(PURPLE)
        self.platform_list.add(portal)


#---------LEVEL-II-----------#
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 2. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[400, 10, 0, 690],
        [160, 30, 200, 650],
        [160, 30, 350, 550],
        [160, 30, 500, 450],
        [30, 30, 600, 450],
        [30, 30, 950, 550],
        [130, 30, 1270, 450],
        [30, 30, 1270, 370],
        [130, 30, 1270, 340]
        ]

        # Go through the array above and add platforms
        for platform in level:
                block = Platform(platform[0], platform[1])
                block.rect.x = platform[2]
                block.rect.y = platform[3]
                block.player = self.player
                self.platform_list.add(block)

        restart = Platform(1000, 10)
        restart.rect.x = 400
        restart.rect.y = 690
        restart.image = pygame.Surface([1000, 10])
        restart.image.fill(RED)
        self.platform_list.add(restart)

        portal = Platform(100, 80)
        portal.rect.x = 1300
        portal.rect.y = 370
        portal.image = pygame.Surface([100, 80])
        portal.image.fill(PURPLE)
        self.platform_list.add(portal)



#----------LEVEL-III----------#
# Create platforms for the level
class Level_03(Level):
    """ Definition for level 3. """

    def __init__(self, player):
        """ Create level 3. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[400, 10, 0, 690],
        [160, 30, 400, 600],
        [30, 30, 300, 500],
        [30, 30, 150, 400],
        [30, 30, 0, 300],
        [160, 30, 150, 200],
        [30, 30, 400, 300],
        [30, 30, 550, 450],
        [30, 30, 700, 300],
        ]


        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        restart = Platform(1000, 10)
        restart.rect.x = 400
        restart.rect.y = 690
        restart.image = pygame.Surface([1000, 10])
        restart.image.fill(RED)
        self.platform_list.add(restart)

        portal = Platform(160, 80)
        portal.rect.x = 1000
        portal.rect.y = 410
        portal.image = pygame.Surface([160, 80])
        portal.image.fill(PURPLE)
        self.platform_list.add(portal)




def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Python Platformer")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )
    level_list.append( Level_02(player) )
    level_list.append( Level_03(player) )


    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:

        clock.tick(60)

        if player.update_level and current_level_no < len(level_list) - 1:
            current_level_no += 1
            current_level = level_list[current_level_no]
            player.level = current_level
            player.update_level = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT





        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()







