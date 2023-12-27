import chess
import chess.svg
import tkinter as tk
from PIL import Image, ImageTk
import io
import cairosvg

# Initialize the board
board = chess.Board()
selected_piece = None  # Initialize the selected_piece variable

def update_board():
    svg_data = chess.svg.board(board=board)
    png_data = cairosvg.svg2png(bytestring=svg_data.encode("utf-8"))
    img = Image.open(io.BytesIO(png_data))
    img = img.resize((400, 400), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img
# Evaluation function (simple material count)
def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King value not used for this evaluation
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            score += piece_values[piece.piece_type] * (1 if piece.color == chess.WHITE else -1)

    return score


# Minimax with alpha-beta pruning (adapted for GUI)
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# Function to make the AI move using minimax with alpha-beta pruning
def play_ai_move():
    best_move = None
    best_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    depth = 3  # Set the search depth (you can adjust this value)

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > best_eval:
            best_eval = eval
            best_move = move

    if best_move is not None:
        board.push(best_move)
        update_board()

# Function to handle user's move
def handle_click(event):
    global selected_piece
    rank = 7 - int(event.y / 50)  # Adjust the division factor according to your board size ------------- modified -------------
    file = int(event.x / 50)  # Adjust the division factor according to your board size
    square = chess.square(file, rank)

    if selected_piece is None:
        piece_at_square = board.piece_at(square)
        if piece_at_square and piece_at_square.color == board.turn:
            selected_piece = square
    else:
        move = chess.Move(selected_piece, square)
        if move in board.legal_moves:
            board.push(move)
            update_board()
            play_ai_move()
        selected_piece = None # ------------- modified -------------

# Create the GUI window
root = tk.Tk()
root.title("Chess Game")

panel = tk.Label(root, image=None)
panel.pack()

# Display the initial board
update_board()

selected_piece = None
panel.bind("<Button-1>", handle_click)

root.mainloop()