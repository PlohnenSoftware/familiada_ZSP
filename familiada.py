import pygame, sys

pygame.init()
# Create the window, saving it to a variable.
surface = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")

stroke = 20

while True:
    surface.fill((0,0,255))

    # Draw a red rectangle that resizes with the window.
    pygame.draw.rect(surface, (81,81,81), (stroke,stroke, surface.get_width()-stroke*2,surface.get_height()-stroke*2))

    for i in range(0,10):
        for j in range(0,28):
            pygame.draw.rect(surface, (0,0,0), (50 +((surface.get_height()/12.3)/1.45+5)*j, 50 + (surface.get_height()/12.3+5)*i, (surface.get_height()/12.3)/1.45, surface.get_height()/12.3))


    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)