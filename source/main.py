import tkinter as tk
from tkinter import messagebox
import time

# --- CẤU HÌNH ---
BOARD_SIZE = 9
WIN_COUNT = 4

class CaroAdvanced:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro AI - Multi-Level Integration")
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.ai_mode = tk.StringVar(value="Alpha-Beta") # Mặc định Level 2
        self.depth = tk.IntVar(value=3)
        self.state_count = 0
        
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Tạo thanh điều khiển để chọn Level và Độ sâu"""
        frame = tk.Frame(self.root, bg="#34495e", pady=5)
        frame.pack(side="top", fill="x")
        
        tk.Label(frame, text="Thuật toán:", bg="#34495e", fg="white").pack(side="left", padx=5)
        tk.OptionMenu(frame, self.ai_mode, "Minimax", "Alpha-Beta").pack(side="left", padx=5)
        
        tk.Label(frame, text="Độ sâu (Depth):", bg="#34495e", fg="white").pack(side="left", padx=5)
        tk.OptionMenu(frame, self.depth, 1, 2, 3).pack(side="left", padx=5)
        
        tk.Button(frame, text="Chơi mới", command=self.reset_game, bg="#e67e22", fg="white").pack(side="right", padx=10)

    def create_widgets(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.board_frame, text="", font=('Arial', 12, 'bold'), 
                                width=4, height=2, command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

    # --- HÀM ĐÁNH GIÁ (Dùng chung cho cả 2 Level) ---
    def evaluate(self, board):
        def score_window(window):
            s = 0
            mine, opp, empty = window.count('O'), window.count('X'), window.count('.')
            if mine == 4: s += 100000
            elif mine == 3 and empty == 1: s += 5000
            if opp == 3 and empty == 1: s -= 80000 # Chặn chuỗi 3 cực gắt
            elif opp == 2 and empty == 2: s -= 5000 # Chặn chuỗi 2 ngay lập tức
            return s

        score = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - 3):
                score += score_window([board[r][c+i] for i in range(4)])
        for r in range(BOARD_SIZE - 3):
            for c in range(BOARD_SIZE):
                score += score_window([board[r+i][c] for i in range(4)])
        for r in range(BOARD_SIZE - 3):
            for c in range(BOARD_SIZE - 3):
                score += score_window([board[r+i][c+i] for i in range(4)])
        for r in range(BOARD_SIZE - 3):
            for c in range(3, BOARD_SIZE):
                score += score_window([board[r+i][c-i] for i in range(4)])
        return score

    # --- LEVEL 1: MINIMAX THUẦN ---
    def minimax(self, board, depth, is_max):
        self.state_count += 1
        if self.is_win(board, 'O'): return 100000, None
        if self.is_win(board, 'X'): return -100000, None
        if depth == 0: return self.evaluate(board), None

        moves = self.get_valid_moves(board)
        best_m = None
        if is_max:
            val = -float('inf')
            for r, c in moves:
                board[r][c] = 'O'
                res = self.minimax(board, depth - 1, False)[0]
                board[r][c] = '.'
                if res > val: val, best_m = res, (r, c)
            return val, best_m
        else:
            val = float('inf')
            for r, c in moves:
                board[r][c] = 'X'
                res = self.minimax(board, depth - 1, True)[0]
                board[r][c] = '.'
                if res < val: val, best_m = res, (r, c)
            return val, best_m

    # --- LEVEL 2: ALPHA-BETA PRUNING ---
    def alphabeta(self, board, depth, alpha, beta, is_max):
        self.state_count += 1
        if self.is_win(board, 'O'): return 100000, None
        if self.is_win(board, 'X'): return -100000, None
        if depth == 0: return self.evaluate(board), None

        moves = self.get_valid_moves(board)
        best_m = None
        if is_max:
            val = -float('inf')
            for r, c in moves:
                board[r][c] = 'O'
                res = self.alphabeta(board, depth - 1, alpha, beta, False)[0]
                board[r][c] = '.'
                if res > val: val, best_m = res, (r, c)
                alpha = max(alpha, val)
                if beta <= alpha: break # Cắt nhánh
            return val, best_m
        else:
            val = float('inf')
            for r, c in moves:
                board[r][c] = 'X'
                res = self.alphabeta(board, depth - 1, alpha, beta, True)[0]
                board[r][c] = '.'
                if res < val: val, best_m = res, (r, c)
                beta = min(beta, val)
                if beta <= alpha: break # Cắt nhánh
            return val, best_m

    # --- ĐIỀU KHIỂN GAME ---
    def ai_turn(self):
        start = time.time()
        self.state_count = 0
        d = self.depth.get()
        
        if self.ai_mode.get() == "Minimax":
            _, move = self.minimax(self.board, d, True)
        else:
            _, move = self.alphabeta(self.board, d, -float('inf'), float('inf'), True)
            
        if move:
            self.make_move(move[0], move[1], 'O')
            print(f"[{self.ai_mode.get()}] Depth:{d} | States:{self.state_count} | Time:{time.time()-start:.2f}s")
            if not self.check_end('O'): self.current_player = 'X'

    def get_valid_moves(self, board):
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == '.':
                    near = False
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r+dr, c+dc
                            if 0<=nr<BOARD_SIZE and 0<=nc<BOARD_SIZE and board[nr][nc] != '.':
                                near = True; break
                        if near: break
                    if near or (r==BOARD_SIZE//2 and c==BOARD_SIZE//2): moves.append((r, c))
        return moves

    def is_win(self, board, player):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == player:
                    for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
                        cnt = 0
                        for i in range(WIN_COUNT):
                            nr, nc = r+dr*i, c+dc*i
                            if 0<=nr<BOARD_SIZE and 0<=nc<BOARD_SIZE and board[nr][nc]==player: cnt += 1
                            else: break
                        if cnt == WIN_COUNT: return True
        return False

    def on_click(self, r, c):
        if self.board[r][c] == '.' and self.current_player == 'X':
            self.make_move(r, c, 'X')
            if not self.check_end('X'):
                self.current_player = 'O'
                self.root.after(100, self.ai_turn)

    def make_move(self, r, c, player):
        self.board[r][c] = player
        color = "#e74c3c" if player == 'X' else "#2980b9"
        self.buttons[r][c].config(text=player, fg=color, state="disabled", disabledforeground=color)

    def check_end(self, player):
        if self.is_win(self.board, player):
            messagebox.showinfo("Kết thúc", f"{player} thắng!"); self.reset_game(); return True
        if all(cell != '.' for row in self.board for cell in row):
            messagebox.showinfo("Kết thúc", "Hòa!"); self.reset_game(); return True
        return False

    def reset_game(self):
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.buttons[r][c].config(text="", state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    game = CaroAdvanced(root)
    root.mainloop()
