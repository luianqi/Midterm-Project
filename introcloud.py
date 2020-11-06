import pygame

pygame.init()

screen_width = 800
screen_height = 450

#screen and image parameters
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('IntroCloud')
image = pygame.image.load('lu.jpeg')
pygame.display.set_icon(image)

cloud_img = [pygame.image.load('run1.png'), pygame.image.load('run2.png'), pygame.image.load('run3.png'),
           pygame.image.load('run4.png'), pygame.image.load('run5.png'), pygame.image.load('run6.png'),
           pygame.image.load('run7.png'), pygame.image.load('run8.png'), pygame.image.load('run9.png')]

img_counter = 9

crowd_img = [pygame.image.load('people.png'), pygame.image.load('people.png'), pygame.image.load('people.png')]

stone_counter = 3

bird_img = [pygame.image.load('b1.png'), pygame.image.load('b2.png'), pygame.image.load('b3.png'),
            pygame.image.load('b4.png'), pygame.image.load('b5.png'), pygame.image.load('b6.png'),
            pygame.image.load('b7.png'), pygame.image.load('b8.png'), pygame.image.load('b9.png')]

bird_counter = 9

#cloud parameters
cloud_width = 90
cloud_height = 100
cloud_x = round(screen_width / 3.8) #position
cloud_y = round(screen_height - cloud_height * (cloud_width/cloud_height + 1)) #position

#crowd parameters
crowd_width = 131
crowd_height = 114
crowd_x = screen_width
crowd_y = screen_height - crowd_height - 90
crowd_passed = False


clock = pygame.time.Clock()  # The clock will be used to control how fast the screen updates

button_sound = pygame.mixer.Sound('button.wav')
jump_cloud = False
jump_counter = 30
scores = 0

class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (255, 255, 255)
        self.active_color = (0, 0, 0)

    def draw(self, x, y, text, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[1] < y + self.width:
            if y < mouse[0] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

                if click[0] == 1 and action is not None:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(300)
                    action()



        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        text(text, x + 10, y + 10)

def start_game():
    global jump_cloud
    button = Button
    game=True

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
        text('scores: ' + str(scores), 625, 10)
        draw_crowd()
        draw_cloud()
        button.draw()
        pygame.display.update()

        if checkForCollision():
            game = False
        clock.tick(60)

def jump():
   global cloud_y, jump_counter, jump_cloud
   if jump_counter >= -30:
       cloud_y -= jump_counter
       jump_counter -= 2
   else:
        jump_counter = 30
        jump_cloud = False

def draw_crowd():
    global crowd_x, crowd_y, crowd_width, crowd_height, scores, crowd_passed

    if crowd_x < cloud_x and not crowd_passed:
        scores += 1
        crowd_passed = True

    if crowd_x >= crowd_width:
        screen.blit(crowd_img[stone_counter // 9], (crowd_x, crowd_y))
        crowd_x -= 9
    else:
        crowd_passed = False
        crowd_x = screen_width - 9

def draw_cloud():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    screen.blit(cloud_img[img_counter // 5], (cloud_x, cloud_y))
    img_counter += 1


def checkForCollision():
    if crowd_y >= (cloud_y - cloud_height) and crowd_y <= (cloud_y + cloud_height):
        if crowd_x >= cloud_x and crowd_x <= (cloud_x + cloud_width):
            return True

def text(info, x, y, font_color = (246, 240, 37), front_type = '18392.otf', font_size = 30):
    font_type = pygame.font.Font(front_type, font_size)
    text = font_type.render(info, True, font_color)
    screen.blit(text, (x, y))

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        text('Paused. Press enter to continue', 160, 100)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()

        clock.tick(15)

start_game()