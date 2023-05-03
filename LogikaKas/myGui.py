import tkinter as tk

class MyGui:
    def __init__(self, size: int):
        self.root = tk.Tk()
        self.root.title("Symulacja kas w sklepie")
        

        # Kwadraty czerwone - kasy
        self.squares_big = []
        for i in range(size):
            square = tk.Canvas(self.root, width=40, height=40, bg="red", highlightthickness=0)
            square.grid(row=0, column=i, padx=2, pady=2)
            self.squares_big.append(square)

        # Kwadraty białe z ramką czarną - klienci
        self.squares_small = []
        for i in range(8):
            row_squares = []
            for j in range(size):
                square = tk.Canvas(self.root, width=30, height=30, bg="white", highlightthickness=1,
                                   highlightbackground="black")
                square.grid(row=i + 1, column=j, padx=2, pady=2)
                row_squares.append(square)
            self.squares_small.append(row_squares)

        self.status_legend = tk.Label(self.root, text="Legenda kolory kas: ", fg="black")
        self.status_legend.grid(row=4, column=size, pady=10)

        self.status_active = tk.Label(self.root, text="aktywna", fg="green")
        self.status_active.grid(row=5, column=size, pady=10)

        self.status_closed = tk.Label(self.root, text="zamknięta", fg="red")
        self.status_closed.grid(row=6, column=size, pady=10)

        self.status_problem = tk.Label(self.root, text="problem z klientem", fg="orange")
        self.status_problem.grid(row=7, column=size, pady=10)

        self.status_repair = tk.Label(self.root, text="w naprawie", fg="gray")
        self.status_repair.grid(row=8, column=size, pady=10)

        self.status_legend = tk.Label(self.root, text="Kasy sklepowe ", fg="black")
        self.status_legend.grid(row=0, column=size, pady=10)

        self.status_legend = tk.Label(self.root, text="Klienci w kolejce ", fg="black")
        self.status_legend.grid(row=2, column=size, pady=10)

    def klient_change_color(self, row, column, color):
        self.squares_small[row][column].configure(bg=color)
        self.root.update()

    def klienci_change_color(self, column, numberOfClients):
        for i in range(8):
            self.klient_change_color(i, column, "white")

        for i in range(numberOfClients):
            self.klient_change_color(i, column, "black")
        self.root.update()

    def kasa_change_color(self, col, color):
        self.squares_big[col].configure(bg=color)
        self.root.update()

    def run(self):
        self.root.mainloop()
