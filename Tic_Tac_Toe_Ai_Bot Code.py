import sys
import pygame
import numpy as np
import random 

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Game constants
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
DIFFICULTY_EASY = "easy"
DIFFICULTY_HARD = "hard"
difficulty = None

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))



font = pygame.font.Font(None, 36)

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

def draw_start_screen():
    screen.fill(BLACK)
    title = font.render("Tic Tac Toe AI", True, WHITE)
    title2 = font.render("Choose difficulty level", True, WHITE)
    easy_text = font.render("Easy", True, GREEN)
    hard_text = font.render("Hard", True, RED)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
    screen.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 60))
    
    line_y = 120
    line_height = 50
    pygame.draw.line(screen, WHITE, (50, line_y), (WIDTH - 50, line_y), 2)
    easy_rect = screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, line_y + 10))
    
    pygame.draw.line(screen, WHITE, (50, line_y + line_height), (WIDTH - 50, line_y + line_height), 2)
    hard_rect = screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, line_y + line_height + 10))
    
    pygame.draw.line(screen, WHITE, (50, line_y + 2 * line_height), (WIDTH - 50, line_y + 2 * line_height), 2) 

    pygame.display.update()
    return easy_rect, hard_rect

def select_difficulty():
    global difficulty
    easy_rect, hard_rect = draw_start_screen()
    selecting_difficulty = True
    while selecting_difficulty:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mouse_pos):
                    difficulty = DIFFICULTY_EASY
                    selecting_difficulty = False
                elif hard_rect.collidepoint(mouse_pos):
                    difficulty = DIFFICULTY_HARD
                    selecting_difficulty = False

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    global difficulty

    empty_squares = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == 0]
    if not empty_squares:
        return False
    if difficulty == DIFFICULTY_EASY:
        move = random.choice(empty_squares)
        mark_square(move[0], move[1], 2)
        return True

    elif difficulty == DIFFICULTY_HARD:
        best_score = -float('inf')
        move = (-1, -1)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, 0, False)
                    board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        if move != (-1, -1):
            mark_square(move[0], move[1], 2)
            return True

    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0



select_difficulty()
restart_game()

player = 1
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                # Player's move
                mark_square(mouseY, mouseX, player)
                draw_figures()
                pygame.display.update()

                if check_win(player):
                    game_over = True
                else:
                    player = player % 2 + 1

                    if not game_over:
                        if best_move():
                            if check_win(2):
                                game_over = True
                            player = player % 2 + 1
                        draw_figures()
                        pygame.display.update()

                    if not game_over:
                        if is_board_full():
                            game_over = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                select_difficulty()
                restart_game()
                game_over = False
                player = 1
    
    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(GRAY)
            draw_lines(GRAY)

    pygame.display.update()