import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SQUARE_SIZE = WIDTH // 8

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Define the chess board (initial configuration)
chess_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

# Load images for chess pieces (replace these with your own images)
black_pawn_img = pygame.image.load("black_pawn_image.png")  # Replace with actual path or filename
white_pawn_img = pygame.image.load("white_pawn_image.png")  # Replace with actual path or filename

# Helper function to get the board coordinates from mouse position
def get_board_coordinates(pos):
    return pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE

# Game loop
running = True
dragging = False
selected_piece = None
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Get the selected piece
                x, y = get_board_coordinates(pygame.mouse.get_pos())
                selected_piece = chess_board[y][x]
                if selected_piece:
                    dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if dragging:
                    # Handle piece movement
                    x, y = get_board_coordinates(pygame.mouse.get_pos())
                    # Implement piece movement validation here
                    chess_board[y][x] = selected_piece
                    selected_piece = None
                    dragging = False

    # Draw the chess board and pieces
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, BLACK, pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, pygame.Rect(i * SQUARE_SIZE, j * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = chess_board[j][i]
            if piece == "p":
                screen.blit(black_pawn_img, (i * SQUARE_SIZE, j * SQUARE_SIZE))
            elif piece == "P":
                screen.blit(white_pawn_img, (i * SQUARE_SIZE, j * SQUARE_SIZE))
            # Add similar blit logic for other chess pieces...

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
sys.exit()