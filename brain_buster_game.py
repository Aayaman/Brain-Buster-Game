import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class MemoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Brain Buster Game")

        self.size = self.ask_grid_size()
        self.max_tries = self.size * self.size  # trial limit is one try per tile
        self.tries = 0
        self.matches_found = 0

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.values = self.generate_grid()
        self.revealed = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.first_click = None

        self.create_widgets()

    def ask_grid_size(self):
        size = simpledialog.askinteger("Grid Size", "Choose grid size (4, 8, or 16):", minvalue=4, maxvalue=16)
        return size if size in [4, 8, 16] else 4

    def generate_grid(self):
        total_tiles = self.size * self.size
        pairs = list(range(total_tiles // 2)) * 2
        random.shuffle(pairs)
        return [pairs[i * self.size:(i + 1) * self.size] for i in range(self.size)]

    def create_widgets(self):
        for i in range(self.size):
            for j in range(self.size):
                btn = tk.Button(
                    self.master,
                    text=" ",
                    width=4,
                    height=2,
                    bg="lightblue",  
                    activebackground="lightpink",
                    font=("Helvetica", 12, "bold"),
                    command=lambda row=i, col=j: self.reveal_tile(row, col)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = btn

    def reveal_tile(self, row, col):
        if self.revealed[row][col] or (self.first_click and (row, col) == self.first_click):
            return

        self.buttons[row][col]["text"] = str(self.values[row][col])
        self.revealed[row][col] = True

        if not self.first_click:
            self.first_click = (row, col)
        else:
            r1, c1 = self.first_click
            r2, c2 = row, col
            self.tries += 1

            if self.values[r1][c1] == self.values[r2][c2]:
                self.buttons[r1][c1]["bg"] = "lightgreen"
                self.buttons[r2][c2]["bg"] = "lightgreen"
                self.matches_found += 1
                if self.matches_found == (self.size * self.size) // 2:
                    messagebox.showinfo("Youpi!", "🎉 Youpi! You win!")
            else:
                self.master.after(800, self.hide_tiles, r1, c1, r2, c2)

            self.first_click = None

            if self.tries >= self.max_tries and self.matches_found < (self.size * self.size) // 2:
                messagebox.showerror("Game Over", "💀 You have exceeded the number of trials. Loser!")
                self.master.destroy()

    def hide_tiles(self, r1, c1, r2, c2):
        self.buttons[r1][c1]["text"] = " "
        self.buttons[r2][c2]["text"] = " "
        self.revealed[r1][c1] = False
        self.revealed[r2][c2] = False

# --- Run the GAME ---
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()