# TODO = сделать reset и wintab

import pygame as pg

# Инициализация pg
pg.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Определение размера окна
WINDOW_SIZE = (300, 300)
win = [0, 0]

player = False
bot = False
# Создание игрового поля
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Инициализация окна
window = pg.display.set_mode(WINDOW_SIZE)
pg.display.set_caption("1488")



# Функция для отрисовки игрового поля
def draw_board():
    window.fill(BLACK)
    
    # Отрисовка вертикальных линий
    pg.draw.line(window, WHITE, (100, 0), (100, 300), 2)
    pg.draw.line(window, WHITE, (200, 0), (200, 300), 2)
    
    # Отрисовка горизонтальных линий
    pg.draw.line(window, WHITE, (0, 100), (300, 100), 2)
    pg.draw.line(window, WHITE, (0, 200), (300, 200), 2)
    
    # Отрисовка крестиков и ноликов
    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                pg.draw.line(window, BLUE, (j * 100 + 15, i * 100 + 15), (j * 100 + 85, i * 100 + 85), 2)
                pg.draw.line(window, BLUE, (j * 100 + 15, i * 100 + 85), (j * 100 + 85, i * 100 + 15), 2)
            elif board[i][j] == -1:
                pg.draw.circle(window, BLUE, (j * 100 + 50, i * 100 + 50), 35, 2)


def check():
    for i in range(3):
        if sum(board[i]) == 3:  
            return 3
        elif sum(board[i]) == -3:
            return -3
        elif sum(board[j][i] for j in range(3)) == 3:
            return 3     
        elif sum(board[j][i] for j in range(3)) == -3:
            return -3
    
    if board[0][0] + board[1][1] + board[2][2] == 3 or board[0][2] + board[1][1] + board[2][0] == 3:
        return 3
    
    if board[0][0] + board[1][1] + board[2][2] == -3 or board[0][2] + board[1][1] + board[2][0] == -3:
        return 3

    # Проверка на ничью
    if all(board[i][j] != 0 for i in range(3) for j in range(3)):
        return True

# Функция для проверки окончания игры
def is_game_over():
    global win, running, bot, player
    if check() == 3:
        win[1] += 0.5
        player = True
        running = False
    elif check() == -3:
        win[0] += 0.5
        bot = True
        running = False
        

    
    return False

# Функция для хода бота
def make_bot_move():
    best_score = float("-inf")
    best_move = None
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                # Имитация хода бота
                board[i][j] = 1
                score = minimax(board, 0, False)
                board[i][j] = 0
                
                # Оценка лучшего хода
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    # Сделать лучший ход
    if best_move:
        board[best_move[0]][best_move[1]] = 1

# Функция для оценки ходов
def evaluate():
    # 10 <=> выгодно, -10 <=> не выгодно, 0 <=> нейтрально 
    # Проверка горизонтальных и вертикальных комбинаций
    for i in range(3):
           if sum(board[i]) == 3: 
               return 10
           if sum(board[j][i] for j in range(3)) == 3: 
               return 10
           if sum(board[i]) == -3: 
               return -10
           if sum(board[j][i] for j in range(3)) == -3: 
               return -10

    # Проверка диагональных комбинаций
    if board[0][0] + board[1][1] + board[2][2] == 3:
        return 10
    if board[0][2] + board[1][1] + board[2][0] == 3:
        return 10
    if board[0][0] + board[1][1] + board[2][2] == -3:
        return -10
    if board[0][2] + board[1][1] + board[2][0] == -3:
        return -10
    
    # Ничья
    return 0

# Функция для рекурсивного поиска лучшего хода с использованием алгоритма минимакс
def minimax(board, depth, is_maximizing):
    score = evaluate() 
    
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if is_game_over():
        return 0
    
    if is_maximizing:
        best_score = float("-inf")
        
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
        
        return best_score
    else:
        best_score = float("inf")
        
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1
                    score = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    best_score = min(score, best_score)
        
        return best_score


def reset(): # бета версия повтора игры
    global board, running, player_turn, bot, player
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    
    running = True
    player_turn = True

    player = False
    bot = False

    pg.display.update()

def winTab():
    global win, bot, player
    
    message = pg.font.Font(None, 20)
    text2 = message.render('Ваш счет: '+str(int(win[0]))+' : '+ str(int(win[1]))+ '. Нажмите ПРОБЕЛ!!!',True, (180, 0, 0))
    window.blit(text2, (10, 10))
    pg.display.update()

    gameContinue=True
    while gameContinue==True:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                pg.quit()
                exit()
            elif i.type == pg.KEYDOWN:
                if i.key==pg.K_ESCAPE:
                    pg.quit()
                    exit()
                elif i.key==pg.K_SPACE:
                    gameContinue=False





# сама игра
def main():
    global running, player_turn, win
    
    while running:
        for event in pg.event.get():

            if event.type == pg.QUIT: # выход 
                exit()

            elif event.type == pg.MOUSEBUTTONDOWN and player_turn and is_game_over() == False: 
                # Ход игрока
                x, y = pg.mouse.get_pos()
                row = y // 100
                col = x // 100

                if board[row][col] == 0:
                    board[row][col] = -1
                    player_turn = False

                if not is_game_over():
                    # Ход бота
                    make_bot_move()
                    player_turn = True 


        
        # Отрисовка игрового поля
        draw_board()

        # Обновление окна
        pg.display.update()


    print(win)



running = True
player_turn = True

while 1:
    main()
    winTab()
    reset()
       
    
pg.quit()