import pygame, sys

pygame.init()
# Create the window, saving it to a variable.
surface = pygame.display.set_mode((750, 500), pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")
stroke = 20

while True:
    surface.fill((0,0,255))
    # jak po szerokosci:
    # szerokosc_czernego = (surface.get_width()-100-(27*2))/28
    # dlugosc_czernego = szerokosc_czernego*3/2
    # jak po wysokosci:
    # dlugosc_czernego = (surface.get_height()-100-(9*2))/10
    # wysokosc_czernego = dlugosc_czernego*2/3

    # min(surface.get_width(), surface.get_height())

    # height = width * 1.5

    if surface.get_width() < surface.get_height()*(192/108):
        block_width = (surface.get_width()-100-(28*2))/29
        block_height = block_width*3/2
    else:
        block_height = (surface.get_height()-100-(9*2))/10
        block_width = block_height*2/3

    # Draw a red rectangle that resizes with the window.
    pygame.draw.rect(surface, (81,81,81), (stroke,stroke, surface.get_width()-stroke*2,surface.get_height()-stroke*2))

    for i in range(0,10):
        for j in range(0,29):
            pygame.draw.rect(surface, (0,0,0), (50 +(block_width+3)*j, 50 + (block_height+3)*i, block_width, block_height))


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