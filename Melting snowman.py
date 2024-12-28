
# Imports pygame, and random
# Initializes pygame
import pygame
import random
#import time
pygame.init()

# Initializes global variables/constants
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED   = (255,0, 0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
LIGHT_BLUE = (102,255,255)

btn_font = pygame.font.SysFont('arial', 20)
guess_font = pygame.font.SysFont('monospace', 24)
clue_font = pygame.font.SysFont('monospace', 16)
extras_font = pygame.font.SysFont('calibri', 70)
again_font = pygame.font.SysFont('monospace', 20)
win = pygame.display.set_mode((700,480))

happy = pygame.image.load('./Pictures/nice.png')
happy = pygame.transform.scale(happy, (50, 50))
sad = pygame.image.load('./Pictures/wrong.png')
sad = pygame.transform.scale(sad, (50, 50))
clock = pygame.time.Clock

yay = pygame.mixer.Sound('./Sounds/ding.ogg')
no = pygame.mixer.Sound('./Sounds/buzzer.ogg')
won = pygame.mixer.Sound('./Sounds/won.ogg')
lost = pygame.mixer.Sound('./Sounds/lost.ogg')

# Creates a list of all the data for each letter button
def createButtons():
    x = 98
    y = 400
    buttons = []
    for btn in range(26):
        buttons.append((x,y))
        x += 42
        if btn == 12:
            x = 98
            y += 42
    print(buttons)
    return buttons

# Draws all the buttons using the data above and changes the colour when moused over or clicked
def drawButtons(buttons):
    mouse = pygame.mouse.get_pos()
    for i,xy in enumerate(buttons):
        if chr(i+65) in usedLtrs:
            ltrToRender = ''
            colour = RED
        else:
            a = mouse[0] - xy[0]
            b = mouse[1] - xy[1]
            c = (a**2 + b**2)**.5
            if c <= 15:
                colour = LIGHT_BLUE
            else:
                colour = WHITE
                
        ltrToRender = chr(i+65)
        pygame.draw.circle (win,colour,xy,15,0)
        pygame.draw.circle (win,BLACK,xy,15,1)
        
        ltrSurface = btn_font.render(ltrToRender,True,BLACK)
        win.blit(ltrSurface,(xy[0]-ltrSurface.get_width()//2,xy[1]-ltrSurface.get_height()//2))
        
# Checks if a button has been clicked
def clickBtn(mp,buttons):
    for i,xy in enumerate(buttons):
        a = mp[0] - xy[0]
        b = mp[1] - xy[1]
        c = (a**2 + b**2)**.5
        if c <= 15:
            return i
    return -1

# Loads the images of the snowman and stores them in a list
def loadSnowmanImages():
    smImages = []
    for imgNum in range(9):
        fileName = 'snowman' + str(imgNum) + '.png'
        smImages.append(pygame.image.load('./Pictures/' + fileName))
    return smImages

# Loads the puzzles created in the text file
def loadPuzzles():
    puzzles = [[],[],[]]
    fi = open('puzzle.txt', 'r')
    for p in fi:
        puz = p.strip().split(',')
        catIndex = int(puz[0]) - 1
        puzzles[catIndex].append(puz[1:])
    fi.close()
    return puzzles

# Chooses a puzzle from the puzzles loaded and makes sure to not pick the same one twice
def getRandomPuzzle(cat, puzzles):
    pIndex = random.randrange(0, len(puzzles[cat]))
    while True:
        if pIndex in chosen: 
            pIndex = random.randrange(0, len(puzzles[cat]))
        else:
            break
    chosen.append(pIndex)
    
    randomPuzz = puzzles[cat][pIndex]
    return randomPuzz
    
# Creates a starting guess by replacing all the letters with underscores
def initializeGuess(puzzle):
    guess = ''
    for c in puzzle:
        if c == ' ':
            guess += ' '
        else:
            guess += '_'
    return guess

# Spaces out the underscores of the guess with spaces to know the amount of letters
def SpacedOut(puzzle):
    new = ''
    for char in puzzle:
        new += char + ' '
    return new[:-1]

# Draws the starting guess on the screen and the clue given
def drawGuess():
    guessSurface = guess_font.render(SpacedOut(guess), True, WHITE)
    x = (win.get_width() - guessSurface.get_width()) //2
    win.blit(guessSurface, (x, 270))
    clueSurface = clue_font.render(clue, True, WHITE)
    x = (win.get_width() - clueSurface.get_width()) //2
    win.blit(clueSurface, (x, 320))

# Updates the guess with letters based on buttons clicked, changing underscores to appropriate letters
def updateGuess(letter, guess, puzzle):
    newGuess = ''
    for i,ltr in enumerate(puzzle):
        if letter == ltr:
            newGuess += ltr
        else:
            newGuess += guess[i]
    print(newGuess)
    return newGuess

# Draws the category buttons and changes colour if they are moused over
def drawCategoryButtons(catButtons):
    cat_mouse = pygame.mouse.get_pos()
    for b in catButtons:
        if pygame.Rect(b[0]).collidepoint(cat_mouse):
            cat_colour = LIGHT_BLUE
        else:
            cat_colour = WHITE
        pygame.draw.rect(win, cat_colour, b[0], 0)
        pygame.draw.rect(win, BLACK, b[0], 3)
        txtSurface = btn_font.render(b[1], True, BLUE)
        x = b[0][0] + (b[0][2] - txtSurface.get_width()) // 2
        y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
        win.blit(txtSurface, (x,y))

# Checks if a catergory button has been clicked
def catBtnClick(mp, buttons):
    for i,b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            return i
    return -1

# Redraws the game window based on which screen it is (category, game, game over), animates the snowman
#   on the game screen appropriately after wrong guesses and wins or losses and updates the display
def redraw_game_window():
    if currentScreen == 1:
        win.fill(BLUE)
        win.blit(title, (110, 60))
        win.blit(hangman, (170, 115))
        drawCategoryButtons(catButtons)
        
    elif currentScreen == 2:
        win.fill(BLUE)
        drawButtons(the_buttons)
        win.blit(smImages[wrongCount], (175, 10))
        drawGuess()
        
        if wrongCount == 8:
            win.blit(wonSurface, (30, 100))
            win.blit(play_again, (20, 150))
            win.blit(play_again_key, (20, 175))
            win.blit(quit_game, (20, 200))
            win.blit(quit_game_key, (20, 225))
                              
        elif puzzle == guess:
            win.blit(wonSurface, (30, 100))
            win.blit(play_again, (20, 150))
            win.blit(play_again_key, (20, 175))
            win.blit(quit_game, (20, 200))
            win.blit(quit_game_key, (20, 225))
        
    elif currentScreen == 3:
        win.fill(BLUE)
        win.blit(over, (100, 100))
        
    pygame.display.update()

# Initializes texts to render and the category buttons (with the category name)
title = extras_font.render('Snowman Game', True, WHITE)
hangman = extras_font.render('(Hangman)', True, WHITE)
over = extras_font.render('GAME OVER :(', True, WHITE)
play_again = again_font.render('PLAY AGAIN??', True, WHITE)
play_again_key = again_font.render('(Press p)', True, WHITE)
quit_game = again_font.render('MENU', True, WHITE)
quit_game_key = again_font.render('(Press m)', True, WHITE)
    
catButtons = [[(56,200,160,80), 'Colours'],
              [(271,200,160,80), 'Exotic Fruits'],
              [(486,200,160,80),'Holiday']]

wonSurface = guess_font.render('YOU WIN!', True, WHITE)
lostSurface = guess_font.render('YOU LOST!', True, WHITE)
 
# Initializes the variable to determine which screen to display
currentScreen = 1
chosen =[]

# Main Loop:
# Initializes variable to control the loop
inPlay = True


while inPlay:
    
    redraw_game_window()                           # constantly redraws display (updates)
    pygame.time.delay(10)                          # pause for 10 miliseconds

    for event in pygame.event.get():               # check for any events
        if event.type == pygame.QUIT:              # if user clicks on the window's 'X' button
            inPlay = False                         # exit from the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:       # if user clicks on the 'escape' button
                inPlay = False                     # exit from the game
            if event.key == pygame.K_p:            # if user clicks on the 'p' button
                the_buttons = createButtons()      # the game restarts in the same category
                smImages = loadSnowmanImages()
                puzzles = loadPuzzles()
                randomPuzz = getRandomPuzzle(cat, puzzles)
                puzzle = randomPuzz[0]
                clue = randomPuzz[1]
                print(puzzle)
                print(clue)
                guess = initializeGuess(puzzle)
                usedLtrs = []
                wrongCount = 0                        
                
            if event.key == pygame.K_m:             # if user clicks on the 'm' button
                chosen.clear()
                currentScreen = 1                   # they go back to the menu (categories)
        if event.type == pygame.MOUSEBUTTONDOWN:    # if user clicks anywhere on win
            clickPos = pygame.mouse.get_pos()       # determines mouse position on the screen when clicked
            
            if currentScreen == 1:                          # if they are on the menu screen
                cat = catBtnClick(clickPos, catButtons)     # determines which category they clicked
                if cat != -1:
                    currentScreen = 2                       # goes to the game screen when looped again
                    the_buttons = createButtons()           # starts up the game
                    smImages = loadSnowmanImages()
                    puzzles = loadPuzzles()
                    randomPuzz = getRandomPuzzle(cat, puzzles)
                    puzzle = randomPuzz[0]
                    clue = randomPuzz[1]
                    print(puzzle)
                    print(clue)
                    guess = initializeGuess(puzzle)
                    usedLtrs = []
                    wrongCount = 0
    
            elif currentScreen == 2:                                    # if they are on the game screen
                if clickBtn(clickPos, the_buttons) != -1:
                    letter = chr(clickBtn(clickPos, the_buttons)+ 65)   # determines what letter button was clicked
                    print('You clicked on the letter', letter)          # prints that letter
                    usedLtrs.append(letter)                             # adds it to a list

                    if letter in puzzle:                                # if the letter is correct
                        yay.play()                                      # sound is played
                        guess = updateGuess(letter,guess,puzzle)        # guess is updated
                        win.blit(happy, (600, 100))                     # image animation shown
                        pygame.display.update()
                        pygame.time.wait(200)
                                              
                    else:                                               # if the letter isn't correct
                        no.play()                                       # sound is played
                        wrongCount += 1                                 # adds another wrong guess
                        win.blit(sad, (600, 100))                       # image animation shown
                        pygame.display.update()
                        pygame.time.wait(200)

                    if wrongCount == 8:                                 # if 8 wrong guesses are made, you lose
                        lost.play()                                     # sound is played
                        if len(chosen) == 6:                            # game over if you run out of puzzles
                            pygame.time.wait(300)
                            currentScreen = 3
                    elif puzzle == guess:                               # if you guess the word, you win
                        won.play()                                      # sound is played
                        if len(chosen) == 6:                            # game over if you run out of puzzles
                            pygame.time.wait(300)
                            currentScreen = 3
                        
        
                
                        
pygame.quit()                                                           # quits pyagame
