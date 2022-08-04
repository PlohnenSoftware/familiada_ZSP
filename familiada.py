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

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)