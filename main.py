import pygame
import random

pygame.init()

screen_width = 800
screen_height = 450

# A class for generating crowds
# To create multiple crowds at the same time


class Crowd:
    width = 131
    height = 114
    y = screen_height - height - 90
    passed = False

    def __init__(self, x=screen_width, repeating=False):
        self.x = x  # attribute of the class
        self.repeating = repeating
        # checks whether that crowd should be drawn
        # again once it leaves the screen


# screen and image parameters
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('IntroCloud')
image = pygame.image.load('lu.jpeg')
pygame.display.set_icon(image)

cloud_img = [pygame.image.load('run1.png'), pygame.image.load('run2.png'),
             pygame.image.load('run3.png'), pygame.image.load('run4.png'),
             pygame.image.load('run5.png'), pygame.image.load('run6.png'),
             pygame.image.load('run7.png'), pygame.image.load('run8.png'),
             pygame.image.load('run9.png')]

img_counter = 9

crowd_img = pygame.image.load('people.png')

crowd_counter = 3

# Background music
file = 'happy.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)

# Game params
score = 0
crowds = [Crowd(repeating=True)]
difficulty = 400

#  cloud parameters
cloud_width = 90
cloud_height = 100
cloud_x = round(screen_width / 3.8)  # position
cloud_y = round(screen_height - cloud_height * (cloud_width/cloud_height + 1))
# position

clock = pygame.time.Clock()
# The clock will be used to control how fast the screen updates

jump_cloud = False
jump_counter = 20


def menu():
    menu_bgrnd = pygame.image.load('menu.jpg')
    display = True

    screen.blit(menu_bgrnd, (0, 0))
    # start button
    start_x = 250
    start_y = 175
    start_text = text('Start Game', start_x, start_y,
                      font_color=(58, 58, 58), font_size=50)
    # quit button
    quit_x = 340
    quit_y = 250
    quit_text = text('Quit', quit_x, quit_y,
                     font_color=(58, 58, 58), font_size=50)

    while display:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Checking if the the position of the mouseclick
                # is inside either of the buttons
                if start_x <= event.pos[0] <= \
                        start_x + start_text.width and start_y \
                        <= event.pos[1] <= start_y + start_text.height:
                                start_game()
                elif quit_x <= event.pos[0] <= \
                        quit_x + quit_text.width and quit_y \
                        <= event.pos[1] <= quit_y + quit_text.height:
                        quit()

        pygame.display.update()
        clock.tick(60)


def init():
    global score, crowds, difficulty
    score = 0
    crowds = [Crowd(repeating=True)]
    difficulty = 400


def start_game():
    global jump_cloud
    game = True

    land = pygame.image.load('bgrnd.png')

    while game:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jump_cloud = True

        if keys[pygame.K_ESCAPE]:
            pause()

        if jump_cloud:
            jump()

        screen.blit(land, (0, 0))
        text('score: ' + str(score), 625, 10)

        if checkForCollision():
            game = False

        for c in crowds:
            draw_crowd(c)
        draw_cloud()
        pygame.display.update()
        clock.tick(60)
    game_over()


def game_over():
    text('Game over', 300, 150, font_size=40)
    text('PRESS ENTER TO RESTART', 170, 200,
         font_size=40, font_color=(255, 255, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                init()
                start_game()

        pygame.display.update()
        clock.tick(30)


def jump():
    global cloud_y, jump_counter, jump_cloud
    if jump_counter >= -20:
        cloud_y -= jump_counter
        jump_counter -= 1
    else:
        jump_counter = 20
        jump_cloud = False


def draw_crowd(crowd: Crowd):
    global score, difficulty

    screen.blit(crowd_img, (crowd.x, crowd.y))
    if crowd.x < cloud_x and not crowd.passed:
        score += 1
        crowd.passed = True
        if crowd.repeating:
            randi = random.randint(0, 50) // 10
            # random number. 1 in 6 cases
            # a new crowd will appear once passed a crowd
            if randi == 0:
                crowds.append(Crowd(screen_width))

    if crowd.x + crowd.width < 0:
        crowds.remove(crowd)
        if crowd.repeating:
            crowds.append(Crowd(x=(screen_width +
                          random.randint(0, difficulty)), repeating=True))
        if difficulty - 10 >= 0:
            difficulty -= 10
    else:
        crowd_passed = False
    crowd.x -= 10


def draw_cloud():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    screen.blit(cloud_img[img_counter // 5], (cloud_x, cloud_y))
    img_counter += 1


def checkForCollision():
    global crowds
    for c in crowds:
        if (cloud_y - cloud_height) <= c.y <= (cloud_y + cloud_height):
            if (cloud_x - cloud_width) <= c.x <= (cloud_x + cloud_width):
                return True


def text(info, x, y, font_color=(242, 14, 24),
         front_type='18392.otf', font_size=30):
    font_type = pygame.font.Font(front_type, font_size)
    text = font_type.render(info, True, font_color)
    screen.blit(text, (x, y))
    return text.get_rect()


def pause():
    paused = True
    text('Paused. Press enter to continue', 160, 100)
    text('Or press space to quit')
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()

        clock.tick(15)
menu()
init()
start_game()
game_over()
