import tkinter as tk


class Table:
    def __init__(self, parent, voc):
        second_frame = tk.Frame(parent)
        parent.create_window((0, 0), window=second_frame, anchor="nw")

        for item in dict(voc.get_all_sentences()).items():
            i = item[0]
            sent = item[1]
            number = tk.Label(second_frame, text=i, width=20, fg='black',
                              font=('Arial', 10, 'bold'), borderwidth=1)
            number.grid(row=i, column=0, padx=10, pady=10)
            sentence = tk.Label(second_frame, text=sent.get_string(), width=50, fg='black',
                                font=('Arial', 10, 'bold'), borderwidth=1)
            sentence.grid(row=i, column=1, padx=10, pady=10)
            self.__init_button_to_draw_tree(second_frame, i, sent)

    def __init_button_to_draw_tree(self, frame, i, s):
        b = tk.Button(frame, text="показать дерево", command=lambda: s.get_tree().draw())
        b.grid(row=i, column=2, padx=10, pady=10)
