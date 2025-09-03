import pygame
import sys
import time

# 🎮 Game Setup
pygame.init()
N = 8  # Board size (can change to 4, 6, 10...)
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = WIDTH // N
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("👑 Crown Conquest - N Queens")

# Colors
WHITE = (255, 255, 255)
BLACK = (60, 60, 60)
QUEEN_COLOR = (255, 215, 0)  # Gold
BLOCKED = (255, 99, 71)  # Red highlight for conflicts

# Load Queen Icon
queen_img = pygame.transform.scale(pygame.image.load("queen.png"), (SQUARE_SIZE, SQUARE_SIZE))

# Draw Chessboard
def draw_board(board, highlights=set()):
    for row in range(N):
        for col in range(N):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(WIN, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if (row, col) in highlights:
                pygame.draw.rect(WIN, BLOCKED, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
            if board[row][col] == 1:
                WIN.blit(queen_img, (col*SQUARE_SIZE, row*SQUARE_SIZE))
    pygame.display.update()

# Check if safe
def is_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row, N, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    return True

# Backtracking Algorithm
def solve_backtracking(board, col=0):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if col >= N:
        return True

    for i in range(N):
        if is_safe(board, i, col):
            board[i][col] = 1
            draw_board(board)
            time.sleep(0.3)

            if solve_backtracking(board, col + 1):
                return True

            board[i][col] = 0
            draw_board(board)
            time.sleep(0.3)
    return False

# Branch and Bound Algorithm
def solve_branch_and_bound(board, col=0, leftRow=None, upperDiag=None, lowerDiag=None):
    if leftRow is None:
        leftRow = [0]*N
        upperDiag = [0]*(2*N-1)
        lowerDiag = [0]*(2*N-1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if col >= N:
        return True

    for i in range(N):
        if leftRow[i] == 0 and lowerDiag[i+col] == 0 and upperDiag[N-1+col-i] == 0:
            board[i][col] = 1
            leftRow[i] = 1
            lowerDiag[i+col] = 1
            upperDiag[N-1+col-i] = 1

            draw_board(board)
            time.sleep(0.3)

            if solve_branch_and_bound(board, col+1, leftRow, upperDiag, lowerDiag):
                return True

            board[i][col] = 0
            leftRow[i] = 0
            lowerDiag[i+col] = 0
            upperDiag[N-1+col-i] = 0

            draw_board(board)
            time.sleep(0.3)
    return False

# Game Menu
def main():
    font = pygame.font.SysFont("comicsans", 30)
    run = True
    while run:
        WIN.fill((30, 30, 30))
        text = font.render("👑 Crown Conquest: N Queens", True, (255, 215, 0))
        text2 = font.render("Press B for Backtracking | Press N for Branch & Bound", True, (200, 200, 200))
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, 200))
        WIN.blit(text2, (WIDTH//2 - text2.get_width()//2, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                board = [[0]*N for _ in range(N)]
                if event.key == pygame.K_b:
                    solve_backtracking(board)
                if event.key == pygame.K_n:
                    solve_branch_and_bound(board)
    pygame.quit()

main()
