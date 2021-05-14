import pygame as p
from pygame.constants import KEYDOWN, K_ESCAPE, K_KP_ENTER, K_RETURN
import ChessEngine
import chess.pgn
import random

## Initialize pygame.
p.init() 

## Set Global Variables.
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = 64      #Square size (of each tile).
IMAGES = {}
soundObj = p.mixer.Sound('public_sound_standard_Capture.mp3')


## Load Images.
def loadImages():
    pieces = ["wp","wB","wN","wR","wK","wQ","bp","bB","bN","bR","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))       # Scales the images to fit in a square.
    

## Main function.
def test():
    pgn = open("openings/eco.pgn")
    all_games = []
    for i in range(2014):
        all_games.append(chess.pgn.read_game(pgn))

    all_moves = []
    opening_number = random.randint(0,2013)
    for move in all_games[opening_number].mainline_moves():
        all_moves.append(move)

    length = str(len(all_moves))

    gameDisplay = p.display.set_mode((512,575))      # Creates a square of size mentioned in the beginning (512).
    gs = ChessEngine.GameState()
    p.draw.rect(gameDisplay, ((119, 148, 85)), p.Rect(0,512,512,63), 0)
    opening_name_1 = all_games[opening_number].headers["White"]
    opening_name_2 = all_games[opening_number].headers["Black"]

    opening_name_2 = "" if opening_name_2 == "?" else opening_name_2

    myfont = p.font.SysFont("Courier New Bold", 18)
    # apply it to text on a label
    label_1 = myfont.render("Set the Board according to " + opening_name_1 + " " + opening_name_2, 1, (0,0,0))
    label_2 = myfont.render(length + " " + "moves (including both sides)", 1, (0,0,0))
    text_rect_1 = label_1.get_rect(center=(WIDTH/2, 535))
    text_rect_2 = label_2.get_rect(center=(WIDTH/2, 550))
    gameDisplay.blit(label_1, text_rect_1)
    gameDisplay.blit(label_2, text_rect_2)

    gs = ChessEngine.GameState()
    loadImages()
    x = 0; y = 0; startSQ = (0,0); endSQ = (0,0)
    item_selected = False
    move = False
    drawGame(gameDisplay,gs.board,IMAGES, x, y, startSQ, endSQ, item_selected, move)       # Calls the function to draw the board/pieces.

    ## Main Loop.
    running = True      # Set game as running.
    while running:
        pos = p.mouse.get_pos(); x = pos[0]; y = pos[1]

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False         # If the game is quit, then change the game status to False.
            elif event.type == p.MOUSEBUTTONDOWN:
                col_init = x // SQ_SIZE
                row_init = y // SQ_SIZE
                startSQ = (row_init, col_init)
                if gs.board[row_init][col_init] != '--':
                    item_selected = True
            elif event.type == p.MOUSEBUTTONUP:
                col_final = x // SQ_SIZE
                row_final = y // SQ_SIZE
                endSQ = (row_final, col_final)

                if gs.board[row_init][col_init] != '--':
                    item_selected = False
                    move = True

            keys = p.key.get_pressed()
            if keys[p.K_ESCAPE]:
                running = False
                mainMenu()


        if move == True:
            gs.makeMove(startSQ, endSQ)
            drawGame(gameDisplay, gs.board, IMAGES, x, y, startSQ, endSQ, item_selected, move)
            soundObj.play()
            item_selected = False
            move = False
        elif item_selected == True:
            drawGame(gameDisplay, gs.board, IMAGES, x, y, startSQ, endSQ, item_selected, move)
        p.display.flip()

## Draws the Board and the Pieces.
def drawGame(gameDisplay,board,IMAGES, x, y, startSQ, endSQ, item_selected, move):
    ##Draw the Board.
    colors = [(235, 235, 208), (119, 148, 85),(255, 225, 143), (189, 156, 66)]    

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j)%2)]
            p.draw.rect(gameDisplay, color, p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE), 0)
            if item_selected == True:
                if board[j][i] != '--' and startSQ[0] == j and startSQ[1] == i:
                    p.draw.rect(gameDisplay, colors[2], p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE), 0)
            elif move == True:
                if board[j][i] != '--' and endSQ[0] == j and endSQ[1] == i:
                    p.draw.rect(gameDisplay, colors[3], p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE), 0)
    
    #Draw the Pieces.
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if item_selected == False:
                if board[j][i] != '--':
                    gameDisplay.blit(IMAGES[board[j][i]], (i*SQ_SIZE,j*SQ_SIZE))
            elif item_selected == True: 
                if board[j][i] != '--' and startSQ != (j,i):
                    gameDisplay.blit(IMAGES[board[j][i]], (i*SQ_SIZE,j*SQ_SIZE))
                gameDisplay.blit(IMAGES[board[startSQ[0]][startSQ[1]]], (x - SQ_SIZE//2,y-SQ_SIZE//2))
    
def drawOpening():
    pgn = open("openings/eco.pgn")
    all_games = []
    for i in range(2014):
        all_games.append(chess.pgn.read_game(pgn))

    all_moves = []
    opening_number = random.randint(0,2013)
    for move in all_games[opening_number].mainline_moves():
        all_moves.append(move)

    gameDisplay = p.display.set_mode((512,575))      # Creates a square of size mentioned in the beginning (512).
    gs = ChessEngine.GameState()
    p.draw.rect(gameDisplay, ((119, 148, 85)), p.Rect(0,512,512,63), 0)
    opening_name_1 = all_games[opening_number].headers["White"]
    opening_name_2 = all_games[opening_number].headers["Black"]

    opening_name_2 = "" if opening_name_2 == "?" else opening_name_2

    myfont = p.font.SysFont("Courier New Bold", 18)
    # apply it to text on a label
    label_1 = myfont.render(opening_name_1, 1, (0,0,0))
    label_2 = myfont.render(opening_name_2, 1, (0,0,0))
    text_rect_1 = label_1.get_rect(center=(WIDTH/2, 535))
    text_rect_2 = label_2.get_rect(center=(WIDTH/2, 555))
    gameDisplay.blit(label_1, text_rect_1)
    gameDisplay.blit(label_2, text_rect_2)
    
    loadImages()
    x = 0; y = 0; startSQ = (0,0); endSQ = (0,0)
    item_selected = False
    move = False
    drawGame(gameDisplay,gs.board,IMAGES, x, y, startSQ, endSQ, item_selected, move)       # Calls the function to draw the board/pieces.
    press = 0

    print(len(all_moves))

    running = True      # Set game as running.
    while running:
        forward = True
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False         # If the game is quit, then change the game status to False.
            
            keys = p.key.get_pressed()

            if keys[p.K_RIGHT]:
                forward = True
                if press == 0:
                    move = chess.Move.uci(all_moves[0])
                    gs.openingMove(move, forward)
                    soundObj.play()
                    press += 1
                elif press >= 1 and press<len(all_moves):
                    move = chess.Move.uci(all_moves[press])
                    gs.openingMove(move, forward)
                    print(all_moves[press])
                    print(press)
                    press = press + 1
                    soundObj.play()
                elif press >= len(all_moves):
                    drawOpening()
                    running = False
            if keys[p.K_LEFT]:
                forward = False
                if press == 0:
                    move = chess.Move.uci(all_moves[0])
                    gs.openingMove(move, forward)
                    soundObj.play()
                    press = press - 1
                elif press >= 1 and press<=len(all_moves):
                    press = press - 1
                    move = chess.Move.uci(all_moves[press])
                    gs.openingMove(move, forward)
                    soundObj.play()
            if keys[p.K_ESCAPE]:
                running = False
                mainMenu()

        drawGame(gameDisplay, gs.board, IMAGES, x, y, startSQ, endSQ, item_selected, move)
        p.display.flip()
        
def mainMenu():
    background = p.transform.scale(p.image.load("images/peoplePlaying.jpg"), (HEIGHT//2,WIDTH//2))
    cursor = p.transform.scale(p.image.load("images/wp.png"), (SQ_SIZE//2,SQ_SIZE//2))
    gameDisplay = p.display.set_mode((HEIGHT,WIDTH)) 
    gameDisplay.fill((255,255,255))     # Creates a square of size mentioned in the beginning (512).
    gameDisplay.blit(cursor, (35,180))
    gameDisplay.blit(background, (WIDTH//4,0))
    gs = ChessEngine.GameState()
    myfont = p.font.SysFont("Courier New Bold", 55)

    label_1 = myfont.render('Test Your Knowledge', 1, (128,128,128))
    label_2 = myfont.render('Learn Openings', 1, (128,128,128))
    label_3 = myfont.render('Options', 1, (128,128,128))
    label_4 = myfont.render('Credits', 1, (128,128,128))
    text_rect_1 = label_1.get_rect(center=(WIDTH/2, 200))
    text_rect_2 = label_2.get_rect(center=(WIDTH/2, 250))
    text_rect_3 = label_3.get_rect(center=(WIDTH/2, 300))
    text_rect_4 = label_4.get_rect(center=(WIDTH/2, 350))
    gameDisplay.blit(label_1, text_rect_1)
    gameDisplay.blit(label_2, text_rect_2)
    gameDisplay.blit(label_3, text_rect_3)
    gameDisplay.blit(label_4, text_rect_4)

    cursor_pos_1 = 180
    cursor_pos_2 = 35
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            
            keys = p.key.get_pressed()

            if keys[p.K_DOWN]:
                if cursor_pos_1 < 300:
                    cursor_pos_1 +=50
                    if cursor_pos_1 == 230:
                        cursor_pos_2 = 75
                    elif cursor_pos_1 == 280:
                        cursor_pos_2 = 150
                    elif cursor_pos_1 == 330:
                        cursor_pos_2 = 155
                    else:
                        cursor_pos_2 = 35

            if keys[p.K_UP]:
                if cursor_pos_1 > 200:
                    cursor_pos_1 -=50
                    if cursor_pos_1 == 230:
                        cursor_pos_2 = 75
                    elif cursor_pos_1 == 280:
                        cursor_pos_2 = 150
                    elif cursor_pos_1 == 330:
                        cursor_pos_2 = 155
                    else:
                        cursor_pos_2 = 35
            if keys[K_RETURN]:
                if cursor_pos_1 == 180:
                    test()
                    running = False
                elif cursor_pos_1 == 230:
                    drawOpening()
                    running = False

        gameDisplay.fill((255,255,255)) 
        gameDisplay.blit(background, (WIDTH//4,0))
        gameDisplay.blit(cursor, (cursor_pos_2,cursor_pos_1))
        gameDisplay.blit(label_1, text_rect_1)
        gameDisplay.blit(label_2, text_rect_2)
        gameDisplay.blit(label_3, text_rect_3)
        gameDisplay.blit(label_4, text_rect_4)
        p.display.flip()
if __name__ == "__main__":
    mainMenu()
