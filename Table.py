import tkinter as tk
from tkinter import ttk


class Table:
    def __init__(self, parent, voc):

        second_frame = tk.Frame(parent)
        parent.create_window((0, 0), window=second_frame, anchor="nw")
        for i in range(50):
            for j in range(3):
                self.e = tk.Entry(second_frame, width=20, fg='blue',
                                  font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, "hello")
            b = tk.Button(second_frame, text="show")
            b.grid(row=i, column=4)
