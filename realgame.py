import pygame
import sys
from pygame.locals import *
import random

pygame.init()

game_over = False
score = 0
win_width, win_height = 800, 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird Clone")

bg_image = pygame.image.load('desert.jpg')
bg_width = bg_image.get_width()
bg = pygame.transform.scale(bg_image, (bg_width, win_height))

character_image = pygame.image.load("planeBlue1.png")
character_rect = character_image.get_rect()
character_rect.topleft = (win_width // 2, win_height // 2)
character_speed = 5
rock_gap = 200
scrolling_speed = 5
rock_frequency = 1500  # milliseconds
last_rock = pygame.time.get_ticks()  # thời gian để tạo ra rock 1 cách đồng đều


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("rockSnow.png")
        self.rect = self.image.get_rect()
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(rock_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(rock_gap / 2)]

    def update(self):
        self.rect.x -= scrolling_speed  # tốc độ di chuyển của khối đá
        if self.rect.right < 0:
            self.kill()
            self.rect.x = 800
            if self.rect.top < 0:
                self.rect.bottomleft = (win_width, 0 - int(rock_gap / 2))
            else:
                self.rect.topleft = (win_width, win_height + int(rock_gap / 2))
        if self.rect.x < 0:
            global score
            score += 1


rock_group = pygame.sprite.Group()

# Create instance of Rock and add it to the sprite group
btm_rock = Rock(300, int(win_height / 1.5), -1)
top_rock = Rock(300, int(win_height / 2), 1)
rock_group.add(btm_rock, top_rock)

x = 250
y = 250
radius = 15
vel_x = 10
vel_y = 10
jump = False
run = True
i = 0
clock = pygame.time.Clock()

font = pygame.font.SysFont('Bauhaus 93 ', 60)
black = (0, 0, 0)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    character_rect.y += character_speed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_rect.x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_rect.x += character_speed
    if keys[pygame.K_UP]:
        character_rect.y -= character_speed * 5
    if keys[pygame.K_DOWN]:
        character_rect.y += character_speed

    if character_rect.y < 0:
        character_rect.y = 0
    if character_rect.x < 0:
        character_rect.x = 0
    if character_rect.y >= 430:
        character_rect.y = 430
    if character_rect.x > 750:
        character_rect.x = 750

  
    # Di chuyển và vẽ nền
    win.blit(bg, (i, 0))
    win.blit(bg, (bg_width + i, 0))
    i -= 5  # Điều chỉnh tốc độ di chuyển của background
    if i <= -bg_width:
        i = 0

    # Vẽ nhân vật lên màn hình
    win.blit(character_image, character_rect)

    # Vẽ rock lên màn hình và cập nhật vị trí
    rock_group.update()
    rock_group.draw(win)

    # generate new rocks
    time_now = pygame.time.get_ticks()
    if time_now - last_rock > rock_frequency:
        rock_height = random.randint(-100, 100)
        btm_rock = Rock(win_width, int(win_height / 2) + rock_height, -1)
        top_rock = Rock(win_width, int(win_height / 2) + rock_height, 1)
        rock_group.add(btm_rock, top_rock)
        last_rock = time_now

    # check if plane has hit the ground
    if character_rect.y > win_height:
        game_over = True

    if game_over:
        character_speed = 0

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()

