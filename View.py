import tkinter as tk
import Table
import Vocabulary
from tkinter import filedialog
import re
from tkinter import messagebox
from tkinter import ttk


class View(tk.Tk):
    def __init__(self):
        super(View, self).__init__()
        self.title("Анализ предложения")
        self.geometry("1000x400")
        self.maxsize(1920, 1080)
        self.minsize(1000, 400)
        self.__controller = None

        menu_frame = tk.Frame(self)
        open_button = tk.Button(menu_frame, text="открыть", command=self.__command_open)
        open_button.grid(row=0, column=0)
        save_button = tk.Button(menu_frame, text="сохранить", command=self.__command_save)
        save_button.grid(row=0, column=1)
        create_empty_voc = tk.Button(menu_frame, text="создать пустой", command=self.__command_create_empty)
        create_empty_voc.grid(row=0, column=2)
        create_from_doc = tk.Button(menu_frame, text="создать из docx", command=self.__command_create_from_doc)
        create_from_doc.grid(row=0, column=3)
        add_new_item = tk.Button(menu_frame, text="добавить предложение", command=self.__command_sentence_word_to_voc)
        add_new_item.grid(row=0, column=4)
        edit_word = tk.Button(menu_frame, text="редактировать предложение", command=self.__command_edit_sentence)
        edit_word.grid(row=0, column=5)
        filter_table = tk.Button(menu_frame, text="фильтрация", command=self.__command_filter_table)
        filter_table.grid(row=0, column=6)
        find_by_smth = tk.Button(menu_frame, text="поиск", command=self.__command_find_by)
        find_by_smth.grid(row=0, column=7)
        save_as_doc = tk.Button(menu_frame, text="документирование", command=self.__command_save_as_doc)
        save_as_doc.grid(row=0, column=8)
        user_info = tk.Button(menu_frame, text="информация", command=self.__command_user_info)
        user_info.grid(row=0, column=9)
        menu_frame.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        self.__menu_frame = menu_frame
        self.__content_frame = None
        self.__set_content_table(Vocabulary.Vocabulary())

    def __command_user_info(self):
        user_guid = """
        открыть - выбрав подходящий файл можно загрузить словарь\n
        сохранить - набрав имя файла его можно сохранить\n
        создать пустой - создание пустого словаря\n
        создать из docx - помогает созать словарь по имеющемуся docx файлу\n
        добавить предложение - после ввода предложения ему можно сохранить и оно появится в словаре\n
        редактировать предложение - изначально необходимо выбрать номер предложения из выпадающего спика
        , после нажать на кнопку "Выбрать и оно будет доступно для редактирования и последующего сохранения"\n
        фильтрация - возможность включить и отключить фильтры по необходимым критериям (*)\n
        поиск - поиск по заданным критериям (*)\n
        документирование - сохранения словаря в документированном виде в файле типа docx, также можно применить фильтр (*)\n\n
        (*) фильтры:\n
        NN - существительное в единственном числе (pyramid)\n
        NNS - существительное во множественном числе (lectures)\n
        NNP - имя собственное (Khufu)\n
        VBD - глагол прошедшего времени (claimed)\n
        VBZ - глагол настоящего времени 3-го лица единственного числа (is)\n
        VBP - глагол настоящего времени не 3-го лица единственного числа (have)\n
        VBN - причастие прошедшего времени (found)\n
        PRP - местоимение (they)\n
        PRP$ - притяжательное местоимение (their)\n
        JJ - прилагательное (public)\n
        IN - предлог (in)\n
        DT - определитель (the)\n
        """
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Информация")
        tk.Label(top, text=user_guid).grid(row=0, column=0, padx=10, pady=10)

    def __command_save_as_doc(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.geometry("1000x400")
        top.title("Документировать")
        chb_map = {}
        headers = ["NN", "NNS", "NNP", "VBD", "VBZ", "VBP", "VBN", "PRP", "PRP$", "JJ", "IN", "DT"]

        for i in range(len(headers)):
            head = headers[i]
            var = tk.IntVar()
            chb = tk.Checkbutton(top, text=head, variable=var)
            chb.grid(row=0, column=i, pady=10, padx=10)
            chb_map[head] = var

        top.chb_map = chb_map

        content_frame = tk.Frame(top)
        my_canvas = tk.Canvas(content_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scroll_bar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        my_canvas.configure(yscrollcommand=my_scroll_bar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        top.table = Table.Table(my_canvas, Vocabulary.Vocabulary())
        content_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        top.content_frame = content_frame

        l_filename = tk.Label(top, text="Имя файла")
        l_filename.grid(row=1, column=0, padx=10, pady=10, columnspan=6)
        e_filename = tk.Entry(top)
        e_filename.grid(row=1, column=7, padx=10, pady=10, columnspan=6)
        top.filename = e_filename

        submit = tk.Button(top, text="Сохранить", command=lambda: self.__process_save_as_doc(top))
        submit.grid(row=2, column=0, pady=10, padx=10, columnspan=12)

    def __process_save_as_doc(self, top):
        settings = []
        for item in dict(top.chb_map).items():
            if item[1].get() == 1:
                settings.append(item[0])
        fname = top.filename.get()
        top.destroy()
        self.__controller.set_filter_settings(settings)
        self.__controller.set_filter_enable(True)
        self.__controller.save_as_doc(fname)
        self.__controller.set_filter_enable(False)

    def __command_find_by(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.geometry("1000x700")
        top.title("Поиск")
        chb_map = {}
        headers = ["NN", "NNS", "NNP", "VBD", "VBZ", "VBP", "VBN", "PRP", "PRP$", "JJ", "IN", "DT"]

        for i in range(len(headers)):
            head = headers[i]
            var = tk.IntVar()
            chb = tk.Checkbutton(top, text=head, variable=var)
            chb.grid(row=0, column=i, pady=10, padx=10)
            chb_map[head] = var

        top.chb_map = chb_map

        content_frame = tk.Frame(top)
        my_canvas = tk.Canvas(content_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scroll_bar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        my_canvas.configure(yscrollcommand=my_scroll_bar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        top.table = Table.Table(my_canvas, Vocabulary.Vocabulary())
        content_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        top.content_frame = content_frame

        submit = tk.Button(top, text="Найти", command=lambda: self.__process_find_by(top))
        submit.grid(row=1, column=0, pady=10, padx=10, columnspan=12)

    def __process_find_by(self, top):
        settings = []
        for item in dict(top.chb_map).items():
            if item[1].get() == 1:
                settings.append(item[0])
        self.__controller.set_filter_settings(settings)
        self.__controller.set_filter_enable(True)
        voc = self.__controller.get_voc()
        if top.table and top.content_frame:
            top.content_frame.destroy()
        content_frame = tk.Frame(top)
        content_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
        my_canvas = tk.Canvas(content_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scroll_bar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        my_canvas.configure(yscrollcommand=my_scroll_bar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        top.table = Table.Table(my_canvas, voc)
        top.content_frame = content_frame
        self.__controller.set_filter_enable(False)

    def __command_filter_table(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.geometry("200x650")
        top.title("Фильтр")
        chb_map = {}
        headers = ["NN", "NNS", "NNP", "VBD", "VBZ", "VBP", "VBN", "PRP", "PRP$", "JJ", "IN", "DT"]

        for i in range(len(headers)):
            head = headers[i]
            var = tk.IntVar()
            chb = tk.Checkbutton(top, text=head, variable=var)
            chb.grid(row=i, column=0, pady=10, padx=10)
            chb_map[head] = var

        top.chb_map = chb_map

        submit = tk.Button(top, text="Применить", command=lambda: self.__process_filter_button(top))
        submit.grid(row=len(headers), column=0, pady=10, padx=10)
        reset = tk.Button(top, text="Сбросить изменения", command=lambda: self.__reset_filter(top))
        reset.grid(row=len(headers) + 1, column=0, pady=10, padx=10)

    def __process_filter_button(self, top):
        settings = []
        for item in dict(top.chb_map).items():
            if item[1].get() == 1:
                settings.append(item[0])
        top.destroy()
        self.__controller.set_filter_settings(settings)
        self.__controller.set_filter_enable(True)
        voc = self.__controller.get_voc()
        self.__set_content_table(voc)

    def __reset_filter(self, top):
        top.destroy()
        self.__controller.set_filter_enable(False)
        voc = self.__controller.get_voc()
        self.__set_content_table(voc)

    def __command_edit_sentence(self):
        sentences = self.__controller.get_voc().get_all_sentences()
        if len(sentences) < 1:
            messagebox.showerror("Редактирование", "Нет подходящих предложений для редактирования")
        else:
            top = tk.Toplevel()
            top.resizable(False, False)
            top.geometry("500x300")
            top.title("Редактирование")
            top.sentences = sentences
            menu_choice = tk.StringVar()
            menu_choice.set(str(0))
            top.choice = menu_choice

            drop = tk.OptionMenu(top, menu_choice, *list(dict(sentences).keys()))
            drop.grid(row=0, column=0, padx=10, pady=10)
            set_sentence_b = tk.Button(top, text="Выбрать", command=lambda: self.__set_sentence_for_editing(top))
            set_sentence_b.grid(row=0, column=1, padx=10, pady=10)

            e_input = tk.Entry(top, width=75)
            e_input.configure(state=tk.DISABLED)
            e_input.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
            top.e_input = e_input

            submit = tk.Button(top, text="Изменить", command=lambda: self.__edit_sentence_process(top))
            submit.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    def __set_sentence_for_editing(self, top):
        sent_num = int(top.choice.get())
        sent_str = top.sentences[sent_num].get_string()
        top.e_input.delete(0, tk.END)
        top.e_input.insert(tk.END, sent_str)
        top.e_input.configure(state=tk.NORMAL)
        top.number_of_sen = sent_num

    def __edit_sentence_process(self, top):
        if top.e_input['state'] == 'disabled':
            messagebox.showerror("Редактирование", "Не было выбрано предложение для редактирования")
        else:
            sent_number = top.number_of_sen
            sent_str = top.e_input.get()
            top.destroy()
            voc = self.__controller.edit_word_in_voc(sent_number, sent_str)
            self.__set_content_table(voc)

    def __command_sentence_word_to_voc(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Добавить новое предложение")
        l_sentence = tk.Label(top, text="Предложение")
        e_sentence = tk.Entry(top)

        l_sentence.grid(row=0, column=0, pady=10, padx=10)
        e_sentence.grid(row=1, column=0, pady=10, padx=10)
        top.sentence = e_sentence
        b_add = tk.Button(top, text="Добавить", command=lambda: self.__add_new_sentence_process(top))
        b_add.grid(row=2, column=0, pady=10, padx=10)

    def __add_new_sentence_process(self, top):
        sentence = top.sentence.get()
        top.destroy()
        voc = self.__controller.add_new_sentence_to_voc(sentence)
        self.__set_content_table(voc)

    def __command_open(self):
        filename = filedialog.askopenfilename(title="Выберите файл для открытия", filetypes=[("pkl files", ".pkl")])
        if filename and self.__controller:
            voc = self.__controller.open_vocabulary(filename)
            self.__set_content_table(voc)

    def __command_save(self):
        top = tk.Toplevel()
        top.title("Сохранить как файл")
        label = tk.Label(top, text="Введите имя файла")
        entry = tk.Entry(top)
        button = tk.Button(top, text="Сохранить", command=lambda: self.__prosecc_save_button(top, entry))
        label.grid(row=0, column=0, padx=10, pady=10)
        entry.grid(row=0, column=1, padx=10, pady=10)
        button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def __prosecc_save_button(self, window, entry):
        fname = entry.get()
        window.destroy()
        regex = re.compile('[a-zA-Z]+', re.I)
        match = regex.match(str(fname))
        if bool(match):
            self.__controller.save_vocabulary(fname)
            messagebox.showinfo("Сохранить в файл", "Успешно!")
        else:
            messagebox.showerror("Сохранить в файл", "Некорректное имя файла")

    def __command_create_empty(self):
        if self.__controller:
            voc = self.__controller.create_empty()
            self.__set_content_table(voc)

    def __command_create_from_doc(self):
        filename = filedialog.askopenfilename(title="Выберите файл для открытия",
                                              filetypes=[("docx files", ".docx"), ("doc files", ".doc")])
        if filename and self.__controller:
            voc = self.__controller.create_from_doc(filename)
            self.__set_content_table(voc)

    def __set_content_table(self, voc):
        if self.__content_frame:
            del self.__content_frame
        content_frame = tk.Frame(self)
        content_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        my_canvas = tk.Canvas(content_frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        my_scroll_bar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        my_canvas.configure(yscrollcommand=my_scroll_bar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        self.__table = Table.Table(my_canvas, voc)
        self.__content_frame = content_frame

    def set_controller(self, controller):
        self.__controller = controller
