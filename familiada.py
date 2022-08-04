import pygame, sys

pygame.init()
# Create the window, saving it to a variable.
surface = pygame.display.set_mode((750, 500), pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")
stroke = 20
letter_matrix = [['A' for _ in range(29)] for _ in range(10)]

while True:
    surface.fill((0,0,255))

    

    # determine responsive width and height of the rectangles
    if surface.get_width() < surface.get_height()*(192/108):
        block_width = (surface.get_width()-125-(28*2))/29
        block_height = block_width*3/2

        # move blocks to the center of the screen
        block_x = 0
        block_y = (surface.get_height() - (block_height*10) - (9*2) - 100)/2
    else:
        block_height = (surface.get_height()-100-(9*2))/10
        block_width = block_height*2/3

        # move blocks to the center of the screen
        block_x = (surface.get_width() - (block_width*29) - (28*2) - 125)/2
        block_y = 0

    # Draw a grey rectangle around the game board
    pygame.draw.rect(surface, (81,81,81), (stroke,stroke, surface.get_width()-stroke*2,surface.get_height()-stroke*2))
    
    myfont = pygame.font.Font("familiada.ttf", round(block_height * 0.75))
    letter_hight = round(block_height * 0.8)
    myfont = pygame.font.Font("familiada.ttf", letter_hight)

    # Draw black rectangles on the surface.
    for i in range(10):
        for j in range(29):
            pos_x = block_x + 50 + (block_width+3)*j
            pos_y = block_y + 50 + (block_height+3)*i
            label = myfont.render(letter_matrix[i][j], 1, (255,255,0))
            pygame.draw.rect(surface, (41,41,41), (pos_x, pos_y, block_width, block_height))
            surface.blit(label, (pos_x+block_width*0.1, pos_y+block_height/2-letter_hight/2))

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
            