
import random,os,pygame,sys,time,copy
from pygame.locals import *

# game window size
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 700


# pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
FONT  = pygame.font.SysFont('Comic Sans MS', 35)
FONT2 = pygame.font.SysFont('Comic Sans MS', 20)
FONT3 = pygame.font.SysFont('Comic Sans MS', 50)
pygame.display.set_caption('CONNECT 4')



# color for terminal game 
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# nut's images
RED = pygame.image.load('images/RED.png')
RED = pygame.transform.smoothscale(RED,(60,60))
BLUE = pygame.image.load('images/BLUE.png')
BLUE = pygame.transform.smoothscale(BLUE,(60,60))

# background images
BACKGROUND =  pygame.image.load('images/flippybackground.png')
BACKGROUND = pygame.transform.smoothscale(BACKGROUND,(540,700))
BOARD_BACKGROUND = pygame.image.load('images/green.png')
BOARD_BACKGROUND = pygame.transform.smoothscale(BOARD_BACKGROUND,(420,360))
CIRCLE = pygame.image.load('images/circle.png')
CIRCLE = pygame.transform.smoothscale(CIRCLE,(60,60))

# Menu picture image
RED_MENU = pygame.image.load('images/menu.png')
RED_MENU = pygame.transform.smoothscale(RED_MENU,(240,70))

# depth of minmax tree with alpha-beta
DEPTH = 5
# depth of minmax tree without alpha-beta
DEPTH2 = 4


HEIGHT = 6 #board height
WIDTH = 7 #board width  

#player's symbol for terminal
X = 'X' # player
O = 'O' # AI

# player's name  
AI = 'AI'
PLAYER = 'player'


#player won image
PLAYERWON = pygame.image.load('images/WON.png')
# player lost image
AIWON = pygame.image.load('images/LOSER.png') 
# game tied image
GAMETIED = pygame.image.load('images/TIED.png')

# smooth scale of images
PLAYERWON = pygame.transform.smoothscale(PLAYERWON,(240,240))
AIWON = pygame.transform.smoothscale(AIWON,(240,240))
GAMETIED = pygame.transform.smoothscale(GAMETIED,(240,240))

def main():
    # alpha-beta flag
    global FLAG 
    FLAG = None

    while True:
        if FLAG == False or FLAG :
            break
        window.fill((200,200,200))
        value = FONT3.render('CONNECT 4',True,(136,8,8))
        window.blit(value,(120,130))
        window.blit(RED_MENU,(150,200))
        window.blit(RED_MENU,(150,280))
        window.blit(RED_MENU,(150,360))
        value = FONT.render('1-  alpha-beta',True,(0,0,0))
        window.blit(value,(152,210))
        value = FONT.render('2-  MINIMAX',True,(0,0,0))
        window.blit(value,(152,290))
        value = FONT.render('3-  QUIT',True,(0,0,0))
        window.blit(value,(152,370))
        value = FONT2.render('PRESS NUMBERS ON KEYBOARD',True,(0,0,0))
        window.blit(value,(110,430))
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_1:
                    FLAG = True
                    break
                if event.key == K_2:
                    FLAG = False
                    break
                if event.key == K_3:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    RunGame()

def RunGame():
    # Random choice of turn
    if random.randint(0, 1) == 0:
        turn = AI
    else:
        turn = PLAYER
    # create board for game
    BOARD = NewBoard()
    # game loop 
    while True :
        #drawing board at each level
        DrawBoard(BOARD)
        pygame.display.update()
        # turn's
        if turn == PLAYER :
            PlayerMove(BOARD)
            if Winning(BOARD, X):
                win_img = PLAYERWON
                break
            # switch turn 
            turn = AI 
        # AI turn
        elif turn == AI :
            while True:
                if FLAG:
                    column = ComputerDecision_AlphaBeta(BOARD,DEPTH,True)
                    if Valid_Move(BOARD,column):
                        break
                else :
                    column = ComputerDecision(BOARD,DEPTH2,True)
                    if Valid_Move(BOARD,column):
                        break
            make_move(BOARD,O,column)
            if Winning(BOARD,O):
                win_img = AIWON
                break
            # switch turn 
            turn = PLAYER

        if Board_Is_Full(BOARD): # nobody could win 
            win_img = GAMETIED
            break
    while True:
        DrawBoard(BOARD)
        window.blit(win_img,((540/2)-120,380))
        value = FONT2.render('-click ENTER if you want to continue',True,(136,8,8))
        value2 = FONT2.render('-click ESC if you want to quit',True,(136,8,8))
        window.blit(value,(100,620))
        window.blit(value2,(100,640))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP:
                if event.key == K_RETURN:
                    main()

def make_move(board,nut,column):
   empty = Empty_In_Column(board,column)
   if empty != -1 :
       board[empty][column] = nut

def Valid_Move(board,column):
    if Empty_In_Column(board,column) == -1 :
        return False
    return True

def Empty_In_Column(board,column):
    for row in range(6):
        if board[row][column] == X or board[row][column] == O :
            return row-1
    return 5

def PlayerMove(board):
    # check if the choosen column is valid or not
    while True:
        column = PlayerChoose()
        if Valid_Move(board,column):
            break
    board[Empty_In_Column(board,column)][column] = X

def PlayerChoose():
    # player choose a column with keyboard
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                    if event.key == K_1:
                       return 0
                    if event.key == K_2:
                        return 1
                    if event.key == K_3:
                        return 2
                    if event.key == K_4:
                        return 3
                    if event.key == K_5:
                        return 4
                    if event.key == K_6:
                        return 5
                    if event.key == K_7:
                        return 6

def DrawBoard(board):
    window.blit(BACKGROUND,(0,0))
    window.blit(BOARD_BACKGROUND,(60,60))
    for i in range(60,480,60):
        for j in range(60,420,60):
            window.blit(CIRCLE,(i,j))
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if board[j][i] == 'X':
                window.blit(RED,((i+1)*60,(j+1)*60))
            elif board[j][i] == 'O':
                window.blit(BLUE,((i+1)*60,(j+1)*60))

    for i in range(90,510,60):
        for j in range(90,450,60):
            pygame.draw.circle(window, (124,240,0), (i, j), 30, 2)
    
    for i in range(2*60,420,60):
        pygame.draw.line(window,(0,0,0),(60,i),(480,i))
    for i in range(60,540,60):
        pygame.draw.line(window,(0,0,0),(i,60),(i,420))
    pygame.draw.line(window,(0,0,0),(60,60),(60,420),6)
    pygame.draw.line(window,(0,0,0),(480,60),(480,420),6)
    pygame.draw.line(window,(0,0,0),(60,420),(480,420),6)
    col = 1
    for x in range(77,463,60):
        value = FONT.render(str(col), True, (0,0,0))
        window.blit(value, (x,415))
        col = col + 1
    value = FONT.render('YOU ARE RED',True,(136,8,8))
    window.blit(value,(61,500))
    window.blit(RED,(0,492))
    value = FONT.render('AI IS BLUE',True,(0,0,0))
    window.blit(value,(61,560))
    window.blit(BLUE,(0,552))
    value = FONT2.render('PRESS NUMBERS ON KEYBOARD TO MOVE',True,(0,0,0))
    window.blit(value,(50,0))
    
def Board_Is_Full(board):
    # checking the board is full or not
    for i in range(7):
        if board[0][i] == 0:
            return False
    return True    

def NewBoard():
    # get a new board
    board = []
    for i in range(HEIGHT):
        board.append([0]*WIDTH)
    return board    

def Winning(board,nut): # check winner or not
    # horizontal
    for i in range(HEIGHT-1,-1,-1):
        for j in range(WIDTH-3):
            if board[i][j] == nut and board[i][j+1] == nut and board[i][j+2] == nut and board[i][j+3] == nut:
                return True
    # vertical
    for i in range(WIDTH):
        for j in range(HEIGHT-1,2,-1):
            if board[j][i] == nut and board[j-1][i] == nut and board[j-2][i] == nut and board[j-3][i] == nut:
                return True
    # diagonal \\
    for i in range(WIDTH-3):
        for j in range(HEIGHT-3):
            if board[j][i] == nut and board[j+1][i+1] == nut and board[j+2][i+2] == nut and board[j+3][i+3] == nut:
                return True
    # diagonal //
    for i in range(WIDTH-3):
        for j in range(HEIGHT-1,2,-1):
            if board[j][i] == nut and board[j-1][i+1] == nut and board[j-2][i+2] == nut and board[j-3][i+3] == nut:
                return True
    return False

def Make_move2(board,column,player):
    copy_board = copy.deepcopy(board)
    if player :
        make_move(copy_board,O,column)
    else :
        make_move(copy_board,X,column)
    return copy_board

def heuristic(board):
    score = 0
    # rows
    for row in range(6):
        for col in range(4):
            Range_4 = board[row][col:col+4]
            score += Score(Range_4)
    # columns
    for col in range(7):
        for row in range(3):
            Range_4 = [board[row+i][col] for i in range(4)]
            score += Score(Range_4)

    # diagonals    
    for row in range(3):
        for col in range(4):
            Range_4 = [board[row+i][col+i] for i in range(4)]
            score += Score(Range_4)

        for col in range(4):
            Range_4 = [board[row+3-i][col+i] for i in range(4)]
            score += Score(Range_4)
    return score

def Score(Range_4):
    score = 0
    if Range_4.count("O") == 4:
        score += 1000
    elif Range_4.count("O") == 3 and Range_4.count(0) == 1:
        score += 500
    elif Range_4.count("O") == 2 and Range_4.count(0) == 2:
        score += 20
    elif Range_4.count("O") == 1 and Range_4.count(0) == 3:
        score += 10

    if Range_4.count('X') == 4:
        score -= 1000
    if Range_4.count("X") == 3 and Range_4.count(0) == 1:
        score -= 500
    return score

# minimax with alpha-beta
def minimax1(board, depth, alpha, beta, maxmin):
    if depth == 0 or Board_Is_Full(board):
        return heuristic(board)

    if maxmin:
        v = float('-inf')
        for move in Actions(board):
            new_board = Make_move2(board, move, maxmin)
            if Winning(new_board,O):
                return 1000
            eval = minimax1(new_board, depth - 1, alpha, beta, False)
            v = max(v, eval)
            if beta <= v:
                return v
            alpha = max(alpha, eval)
        return v
    else:
        v2 = float('inf')
        for move in Actions(board):
            new_board = Make_move2(board, move, maxmin)
            if Winning(new_board,X):
                return -1000
            eval = minimax1(new_board, depth - 1, alpha, beta, True)
            v2 = min(v2, eval)
            if v2 <= alpha:
                return v2
            beta = min(beta, eval)
        return v2
# decision function with alpha-beta
def ComputerDecision_AlphaBeta(board, depth, maxmin):
    column = None
    best_score = float('-inf')

    for action in Actions(board):
        new_board = Make_move2(board, action, maxmin)
        score = minimax1(new_board, depth - 1, float('-inf'), float('inf'), not maxmin)
        if Winning(new_board,O):
            return action 
        if score > best_score:
            best_score = score
            column = action 

    return column


# minimax without alpha-beta
def minimax(board, depth, maxmin):
    if depth == 0 or Board_Is_Full(board):
        return heuristic(board)

    if maxmin:
        v = float('-inf')
        for move in Actions(board):
            new_board = Make_move2(board, move, maxmin)
            if Winning(new_board,O):
                return 1000
            eval = minimax(new_board, depth - 1, False)
            v = max(v, eval)
        return v
    else:
        v2 = float('inf')
        for move in Actions(board):
            new_board = Make_move2(board, move, maxmin)
            if Winning(new_board,X):
                return -1000
            eval = minimax(new_board, depth - 1, True)
            v2 = min(v2, eval)
        return v2
# decision function without alpha-beta
def  ComputerDecision(board, depth, maxmin):
    column = None
    best_score = float('-inf')

    for action in Actions(board):
        new_board = Make_move2(board, action, maxmin)
        score = minimax(new_board, depth - 1, not maxmin)
        if Winning(new_board,O):
            return action 
        if score > best_score:
            best_score = score
            column = action 

    return column


def Actions(board):
    moves = []
    for i in range(WIDTH):
       if Valid_Move(board,i):
           moves.append(i)
    return moves

if __name__ == '__main__' :
    main()


# def DrawBoard(board):
#     # drawing the board
#     os.system('clear')
#     for i in range(6):
#         for j in range(7):
#             if board[i][j] == 0:
#                 print(style.BLUE+str(board[i][j]),end="")
#             if board[i][j] == X :
#                 print(style.GREEN+board[i][j],end="")
#             if board[i][j] == O :
#                 print(style.RED+board[i][j],end="")
#             print(style.WHITE+"  |  ",end="")
#         print()
#         print(style.WHITE+'----------------------------------------')
#     print(style.YELLOW+"1  |  2  |  3  |  4  |  5  |  6  |  7  |")


