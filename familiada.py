import pygame, sys, tkinter, threading
pygame.init()
# Create the window, saving it to a variable.
surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Familiada")
stroke = 20
letter_matrix = [['' for _ in range(29)] for _ in range(10)]

def write_obj(type,napis,row,col):
    match type:
        case 1:
            letter_matrix[row][col] = napis
        case 2:
            letters = list(napis)
            for i in range(len(letters)):
                letter_matrix[row][col+i] = letters[i]
        case 3:
            letters = list(napis)
            for i in range(len(letters)):
                letter_matrix[row+i][col] = letters[i]
        # case 4:
        #     letter_matrix = [['' for _ in range(29)] for _ in range(10)]


window = tkinter.Tk()
window.title("Familiada - reżyserka")
window.geometry("400x200")
label = tkinter.Label(window,text="usernane")
inputUser = tkinter.Entry(window)
labelPassword = tkinter.Label(window, text="Password")
inputPassword = tkinter.Entry(window)

button = tkinter.Button(window,text="Go")
label.pack() 
inputUser.pack() 
labelPassword.pack() 
inputPassword.pack()
button.pack()


write_obj(2,"faper",2,5)
write_obj(3,"faper",4,8)

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
    
    letter_hight = round(block_height * 0.75)
    myfont = pygame.font.Font("familiada.ttf", letter_hight)

    # Draw black rectangles & letters on the surface.
    for i in range(10):
        for j in range(29):
            pos_x = block_x + 50 + (block_width+3)*j
            pos_y = block_y + 50 + (block_height+3)*i
            label = myfont.render(letter_matrix[i][j], 1, (255,255,0))
            pygame.draw.rect(surface, (0,0,0), (pos_x, pos_y, block_width, block_height))
            surface.blit(label, (pos_x+block_width*0.146, pos_y+block_height/2-letter_hight/2))

    pygame.display.update()
    window.update() 
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



