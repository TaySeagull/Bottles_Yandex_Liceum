import pygame

size = width, height = 501, 501
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.font.init()
pygame.display.set_caption('К щелчку')
running = True
circle_color = pygame.Color('red')
x = x1 = 501 // 2 + 1
y = y1 = 501 // 2 + 1
circle_pos = (x, y)
circle_radius = 20

while running:
    screen.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos
    if x1 > x:
        x += 1
    elif x1 < x:
        x -= 1

    if y1 > y:
        y += 1
    elif y1 < y:
        y -= 1

    circle_pos = (x, y)
    pygame.draw.circle(screen, circle_color, circle_pos, circle_radius, 0)

    pygame.display.flip()
    clock.tick(50)
pygame.quit()
