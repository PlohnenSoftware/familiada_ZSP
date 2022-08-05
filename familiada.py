import pygame, sys, tkinter
class Blackboard:
    def __init__(self,stroke):
        self.letter_matrix = [['' for _ in range(29)] for _ in range(10)]
        self.stroke = stroke

    # write a word horizontally to the matrix
    def write_horizontally(self,word, start_row, start_col,):
        letters = list(word)
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row][start_col+i] = letter

    # write a word vertically to the matrix
    def write_vertically(self,word, start_row, start_col):
        letters = list(word)
        for i, letter in enumerate(letters):
            self.letter_matrix[start_row+i][start_col] = letter   

    # fill whole board with one character        
    def fill(self,char = ''):
        self.letter_matrix = [[char for _ in range(29)] for _ in range(10)]      

# Create the window, saving it to a variable.
pygame.init()
surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Familiada")
programIcon = pygame.image.load("familiada.ico")
pygame.display.set_icon(programIcon)

# Create the second window
window1 = tkinter.Tk()
window1.title("Familiada - reżyserka")
window1.iconbitmap("familiada.ico")
window1.geometry("400x200")
window1.configure(background='#f0f0f0')
window1.protocol("WM_DELETE_WINDOW", lambda:exit_app(window1))
label = tkinter.Label(window1,text="usernane")
inputUser = tkinter.Entry(window1)
labelPassword = tkinter.Label(window1, text="Password")
inputPassword = tkinter.Entry(window1)
button = tkinter.Button(window1,text="Go", command=lambda: pygame.mixer.Sound.play(intro_music))
label.pack() 
inputUser.pack() 
labelPassword.pack() 
inputPassword.pack()
button.pack()

#import pygame SFX
pygame.mixer.init()
correct_sound = pygame.mixer.Sound("sfx/correct.wav")
wrong_sound = pygame.mixer.Sound("sfx/incorrect.wav")
dubel_sound = pygame.mixer.Sound("sfx/dubel.wav")
ending_music = pygame.mixer.Sound("sfx/final_ending.wav")
intro_music = pygame.mixer.Sound("sfx/show_music.wav")

#initalize game matrix object
game1 = Blackboard(20)
# game1.fill("-")

def exit_app(tkwindow):
    tkwindow.destroy()
    pygame.display.quit()
    pygame.quit()
    sys.exit()

running = True
while running:
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
    pygame.draw.rect(surface, (81,81,81), (game1.stroke,game1.stroke, surface.get_width()-game1.stroke*2,surface.get_height()-game1.stroke*2))
    
    letter_hight = round(block_height * 0.75)
    myfont = pygame.font.Font("familiada.ttf", letter_hight)

    # Draw black rectangles & letters on the surface.
    for i in range(10):
        for j in range(29):
            pos_x = block_x + 50 + (block_width+3)*j
            pos_y = block_y + 50 + (block_height+3)*i
            label = myfont.render(game1.letter_matrix[i][j], 1, (255,255,0))
            pygame.draw.rect(surface, (0,0,0), (pos_x, pos_y, block_width, block_height))
            surface.blit(label, (pos_x+block_width*0.146, pos_y+block_height/2-letter_hight/2))

    #refresh windows
    pygame.display.update()
    window1.update() 
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit_app(window1)

            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
    # quit the game if window is closed
    except pygame.error:
        sys.exit()
