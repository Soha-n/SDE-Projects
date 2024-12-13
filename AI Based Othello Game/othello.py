import pygame
import sys
import copy

# Initialize constants for the game
ROWS = 8
COLUMNS = 8
CELL_SIZE = 80
BOARD_SIZE = CELL_SIZE * ROWS
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 188, 140)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
pygame.display.set_caption('Othello Game with Minimax AI')
font = pygame.font.Font(None, 36)

# Function to create the board
def create_board():
    board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    board[3][3] = PLAYER_X
    board[3][4] = PLAYER_O
    board[4][3] = PLAYER_O
    board[4][4] = PLAYER_X
    return board

# Function to draw the board
def draw_board(board):
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLUMNS):
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if board[row][col] == PLAYER_X:
                pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, WHITE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
    pygame.display.flip()

# Function to display scores and winner
def display_scores(board):
    x_count = count_pieces(board, PLAYER_X)
    o_count = count_pieces(board, PLAYER_O)
    text = f"Score - Human (Black): {x_count} | AI (White): {o_count}"

    if x_count > o_count:
        winners = "Human Wins!!!"
    elif o_count > x_count:
        winners = "AI Wins!!!"
    else:
        winners = "It's a Draw!!!"

    score_surface = font.render(text, True, WHITE)
    screen.fill(BLACK, (0, BOARD_SIZE, BOARD_SIZE, 100))
    screen.blit(score_surface, (10, BOARD_SIZE + 10))

    winner_surface = font.render(winners, True, WHITE)
    screen.blit(winner_surface, (10, BOARD_SIZE + 50))

    pygame.display.flip()

    return x_count, o_count

# Function to check if a move is valid
def is_valid_move(board, row, col, player):
    if board[row][col] != EMPTY:
        return False
    opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        has_opponent_between = False

        while 0 <= r < ROWS and 0 <= c < COLUMNS:
            if board[r][c] == opponent:
                has_opponent_between = True
            elif board[r][c] == player:
                if has_opponent_between:
                    return True
                else:
                    break
            else:
                break
            r, c = r + dr, c + dc
    return False

# Function to make a move and flip the pieces
def make_move(board, row, col, player):
    board[row][col] = player
    opponent = PLAYER_O if player == PLAYER_X else PLAYER_X
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        to_flip = []

        while 0 <= r < ROWS and 0 <= c < COLUMNS:
            if board[r][c] == opponent:
                to_flip.append((r, c))
            elif board[r][c] == player:
                for rr, cc in to_flip:
                    board[rr][cc] = player
                break
            else:
                break
            r, c = r + dr, c + dc

# Function to get the valid moves for a player
def get_valid_moves(board, player):
    valid_moves = []
    for row in range(ROWS):
        for col in range(COLUMNS):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves

# Function to count the pieces for a player
def count_pieces(board, player):
    return sum(row.count(player) for row in board)

# Minimax algorithm with depth-limited search
def minimax(board, depth, maximizing_player):
    if depth == 0 or not get_valid_moves(board, PLAYER_X) and not get_valid_moves(board, PLAYER_O):
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_valid_moves(board, PLAYER_O):
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], PLAYER_O)
            eval_score, _ = minimax(new_board, depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_valid_moves(board, PLAYER_X):
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], PLAYER_X)
            eval_score, _ = minimax(new_board, depth - 1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

# Simple evaluation function for the board
def evaluate_board(board):
    return count_pieces(board, PLAYER_O) - count_pieces(board, PLAYER_X)

# Main function to run the game
def play_othello():
    board = create_board()
    game_over = False
    turn = 0

    draw_board(board)
    display_scores(board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn % 2 == 0:
                x, y = pygame.mouse.get_pos()
                if y < BOARD_SIZE:
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if is_valid_move(board, row, col, PLAYER_X):
                        make_move(board, row, col, PLAYER_X)
                        turn += 1
                        draw_board(board)
                        display_scores(board)

        if turn % 2 == 1:
            pygame.time.wait(1000)
            valid_moves = get_valid_moves(board, PLAYER_O)
            if valid_moves:
                _, move = minimax(board, 3, True)  # AI searches 3 moves deep
                if move:
                    make_move(board, move[0], move[1], PLAYER_O)
                    turn += 1
                    draw_board(board)
                    display_scores(board)
            else:
                print("AI has no valid moves.")
                turn += 1

        if not get_valid_moves(board, PLAYER_X) and not get_valid_moves(board, PLAYER_O):
            game_over = True
            x_count, o_count = display_scores(board)
            print("Game Over! No more valid moves.")
            if x_count > o_count:
                print("Player X (Black) wins!")
            elif o_count > x_count:
                print("Player O (White) wins!")
            else:
                print("It's a draw!")

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        pygame.quit()
                        sys.exit()

# Run the Othello game
play_othello()
