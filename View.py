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
        create_from_doc = tk.Button(menu_frame, text="создать из doc", command=self.__command_create_from_doc)
        create_from_doc.grid(row=0, column=3)
        add_new_item = tk.Button(menu_frame, text="добавить предложение", command=self.__command_new_word_to_voc)
        add_new_item.grid(row=0, column=4)
        edit_word = tk.Button(menu_frame, text="редактировать предложение", command=self.__command_edit_word)
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
        создать из doc - помогает созать словарь по имеющемуся doc файлу\n
        добавить словоформу - введя все необходимые параметры можно создать новую словоформу в словаре\n
        редактировать словоформу - необходимо выбрать нужную форму и отредактировать интересующие поля\n
        фильтрация - возможность включить и отключить фильтры по необходимым критериям\n
        поиск - поиск по заданным критериям\n
        документирование - сохранения словаря в документированном виде в файле типа doc\n
        """
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Информация")
        tk.Label(top, text=user_guid).grid(row=0, column=0, padx=10, pady=10)

    def __command_save_as_doc(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Задокументировать")
        l_count = tk.Label(top, text="Кол-во")
        e_count = tk.Entry(top)
        l_count.grid(row=0, column=0, pady=10, padx=10)
        e_count.grid(row=0, column=1, pady=10, padx=10)
        l_part_of_lang = tk.Label(top, text="Часть речи")
        l_gen = tk.Label(top, text="Род")
        l_number = tk.Label(top, text="Число")
        l_padeJ = tk.Label(top, text="Падеж")
        e_part_of_lang = tk.Entry(top)
        e_gen = tk.Entry(top)
        e_number = tk.Entry(top)
        e_padeJ = tk.Entry(top)
        l_part_of_lang.grid(row=1, column=0, pady=10, padx=10)
        l_gen.grid(row=2, column=0, pady=10, padx=10)
        l_number.grid(row=3, column=0, pady=10, padx=10)
        l_padeJ.grid(row=4, column=0, pady=10, padx=10)
        e_part_of_lang.grid(row=1, column=1, pady=10, padx=10)
        e_gen.grid(row=2, column=1, pady=10, padx=10)
        e_number.grid(row=3, column=1, pady=10, padx=10)
        e_padeJ.grid(row=4, column=1, pady=10, padx=10)
        top.count = e_count
        top.part_of_lang = e_part_of_lang
        top.gen = e_gen
        top.number = e_number
        top.padej = e_padeJ

        l_morph_format_info = tk.Label(top, text="Включать слова с неформатированным вводом?")
        l_morph_format_info.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        r_buttons = tk.IntVar()
        r_buttons.set(1)
        top.r_but = r_buttons
        tk.Radiobutton(top, text="да", variable=r_buttons, value=True).grid(row=6, column=0, pady=10, padx=10)
        tk.Radiobutton(top, text="нет", variable=r_buttons, value=False).grid(row=6, column=1, pady=10, padx=10)

        l_filename = tk.Label(top, text="Имя файла")
        l_filename.grid(row=7, column=0, padx=10, pady=10)
        e_filename = tk.Entry(top)
        e_filename.grid(row=7, column=1, padx=10, pady=10)
        top.filename = e_filename

        submit = tk.Button(top, text="Задокуметировать", command=lambda: self.__process_save_as_doc(top))
        submit.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

    def __process_save_as_doc(self, top):
        settings = [top.count.get(),
                    top.part_of_lang.get(),
                    top.gen.get(),
                    top.number.get(),
                    top.padej.get(),
                    top.r_but.get()]
        fname = top.filename.get()
        top.destroy()
        self.__controller.set_filter_settings(settings)
        self.__controller.set_filter_enable(True)
        self.__controller.save_as_doc(fname)
        self.__controller.set_filter_enable(False)

    def __command_find_by(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Найти")
        l_count = tk.Label(top, text="Кол-во")
        e_count = tk.Entry(top)
        l_count.grid(row=0, column=0, pady=10, padx=10)
        e_count.grid(row=0, column=1, pady=10, padx=10)
        l_part_of_lang = tk.Label(top, text="Часть речи")
        l_gen = tk.Label(top, text="Род")
        l_number = tk.Label(top, text="Число")
        l_padeJ = tk.Label(top, text="Падеж")
        e_part_of_lang = tk.Entry(top)
        e_gen = tk.Entry(top)
        e_number = tk.Entry(top)
        e_padeJ = tk.Entry(top)
        l_part_of_lang.grid(row=1, column=0, pady=10, padx=10)
        l_gen.grid(row=2, column=0, pady=10, padx=10)
        l_number.grid(row=3, column=0, pady=10, padx=10)
        l_padeJ.grid(row=4, column=0, pady=10, padx=10)
        e_part_of_lang.grid(row=1, column=1, pady=10, padx=10)
        e_gen.grid(row=2, column=1, pady=10, padx=10)
        e_number.grid(row=3, column=1, pady=10, padx=10)
        e_padeJ.grid(row=4, column=1, pady=10, padx=10)
        top.count = e_count
        top.part_of_lang = e_part_of_lang
        top.gen = e_gen
        top.number = e_number
        top.padej = e_padeJ

        content_frame = tk.Frame(top)
        top.table = Table.Table(content_frame, Vocabulary.Vocabulary())
        content_frame.grid(row=8, column=0, columnspan=2)
        top.content_frame = content_frame

        l_morph_format_info = tk.Label(top, text="Включать слова с неформатированным вводом?")
        l_morph_format_info.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        r_buttons = tk.IntVar()
        r_buttons.set(1)
        top.r_but = r_buttons
        tk.Radiobutton(top, text="да", variable=r_buttons, value=True).grid(row=6, column=0, pady=10, padx=10)
        tk.Radiobutton(top, text="нет", variable=r_buttons, value=False).grid(row=6, column=1, pady=10, padx=10)

        submit = tk.Button(top, text="Найти", command=lambda: self.__process_find_by(top))
        submit.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

    def __process_find_by(self, top):
        settings = [top.count.get(),
                    top.part_of_lang.get(),
                    top.gen.get(),
                    top.number.get(),
                    top.padej.get(),
                    top.r_but.get()]
        self.__controller.set_filter_settings(settings)
        self.__controller.set_filter_enable(True)
        voc = self.__controller.get_voc()
        if top.table and top.content_frame:
            top.content_frame.destroy()
        content_frame = tk.Frame(top)
        top.table = Table.Table(content_frame, voc)
        content_frame.grid(row=8, column=0, columnspan=2)
        top.content_frame = content_frame
        self.__controller.set_filter_enable(False)

    def __command_filter_table(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Фильтр")
        l_count = tk.Label(top, text="Кол-во")
        e_count = tk.Entry(top)
        l_count.grid(row=0, column=0, pady=10, padx=10)
        e_count.grid(row=0, column=1, pady=10, padx=10)
        l_part_of_lang = tk.Label(top, text="Часть речи")
        l_gen = tk.Label(top, text="Род")
        l_number = tk.Label(top, text="Число")
        l_padeJ = tk.Label(top, text="Падеж")
        e_part_of_lang = tk.Entry(top)
        e_gen = tk.Entry(top)
        e_number = tk.Entry(top)
        e_padeJ = tk.Entry(top)
        l_part_of_lang.grid(row=1, column=0, pady=10, padx=10)
        l_gen.grid(row=2, column=0, pady=10, padx=10)
        l_number.grid(row=3, column=0, pady=10, padx=10)
        l_padeJ.grid(row=4, column=0, pady=10, padx=10)
        e_part_of_lang.grid(row=1, column=1, pady=10, padx=10)
        e_gen.grid(row=2, column=1, pady=10, padx=10)
        e_number.grid(row=3, column=1, pady=10, padx=10)
        e_padeJ.grid(row=4, column=1, pady=10, padx=10)
        top.count = e_count
        top.part_of_lang = e_part_of_lang
        top.gen = e_gen
        top.number = e_number
        top.padej = e_padeJ

        l_morph_format_info = tk.Label(top, text="Включать слова с неформатированным вводом?")
        l_morph_format_info.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        r_buttons = tk.IntVar()
        r_buttons.set(1)
        top.r_but = r_buttons
        tk.Radiobutton(top, text="да", variable=r_buttons, value=True).grid(row=6, column=0, pady=10, padx=10)
        tk.Radiobutton(top, text="нет", variable=r_buttons, value=False).grid(row=6, column=1, pady=10, padx=10)

        submit = tk.Button(top, text="Применить", command=lambda: self.__process_filter_button(top))
        submit.grid(row=7, column=0, columnspan=2, pady=10, padx=10)
        reset = tk.Button(top, text="Сбросить изменения", command=lambda: self.__reset_filter(top))
        reset.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

    def __process_filter_button(self, top):
        settings = [top.count.get(),
                    top.part_of_lang.get(),
                    top.gen.get(),
                    top.number.get(),
                    top.padej.get(),
                    top.r_but.get()]
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

    def __command_edit_word(self):
        words = sorted(self.__controller.get_voc().get_all_words())
        if len(words) < 1:
            messagebox.showerror("Редактирование", "Нет подходящих слов для редактирования")
        else:
            top = tk.Toplevel()
            top.resizable(False, False)
            top.title("Редактирование")
            menu_choice = tk.StringVar()
            menu_choice.set(words[0])
            top.choice = menu_choice

            drop = tk.OptionMenu(top, menu_choice, *words)
            drop.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

            l_count = tk.Label(top, text="Кол-во")
            e_count = tk.Entry(top)
            l_count.grid(row=1, column=0, pady=10, padx=10)
            e_count.grid(row=1, column=1, pady=10, padx=10)
            l_part_of_lang = tk.Label(top, text="Часть речи")
            l_gen = tk.Label(top, text="Род")
            l_number = tk.Label(top, text="Число")
            l_padeJ = tk.Label(top, text="Падеж")
            e_part_of_lang = tk.Entry(top)
            e_gen = tk.Entry(top)
            e_number = tk.Entry(top)
            e_padeJ = tk.Entry(top)
            l_part_of_lang.grid(row=2, column=0, pady=10, padx=10)
            l_gen.grid(row=3, column=0, pady=10, padx=10)
            l_number.grid(row=4, column=0, pady=10, padx=10)
            l_padeJ.grid(row=5, column=0, pady=10, padx=10)
            e_part_of_lang.grid(row=2, column=1, pady=10, padx=10)
            e_gen.grid(row=3, column=1, pady=10, padx=10)
            e_number.grid(row=4, column=1, pady=10, padx=10)
            e_padeJ.grid(row=5, column=1, pady=10, padx=10)
            top.count = e_count
            top.part_of_lang = e_part_of_lang
            top.gen = e_gen
            top.number = e_number
            top.padej = e_padeJ

            submit = tk.Button(top, text="Изменить", command=lambda: self.__edit_words_process(top))
            submit.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    def __edit_words_process(self, top):
        info = [top.part_of_lang.get(), top.gen.get(), top.number.get(), top.padej.get()]
        count = top.count.get()
        word = top.choice.get()
        top.destroy()
        voc = self.__controller.edit_word_in_voc(word, count, info)
        self.__set_content_table(voc)

    def __command_new_word_to_voc(self):
        top = tk.Toplevel()
        top.resizable(False, False)
        top.title("Добавить нвоое слово")
        l_word = tk.Label(top, text="Словоформа")
        l_count = tk.Label(top, text="Кол-во")
        e_word = tk.Entry(top)
        e_count = tk.Entry(top)
        l_word.grid(row=0, column=0, pady=10, padx=10)
        l_count.grid(row=0, column=1, pady=10, padx=10)
        e_word.grid(row=1, column=0, pady=10, padx=10)
        e_count.grid(row=1, column=1, pady=10, padx=10)
        top.word = e_word
        top.count = e_count

        format_frame = tk.Frame(top)
        l_part_of_lang = tk.Label(format_frame, text="Часть речи")
        l_gen = tk.Label(format_frame, text="Род")
        l_number = tk.Label(format_frame, text="Число")
        l_padeJ = tk.Label(format_frame, text="Падеж")
        e_part_of_lang = tk.Entry(format_frame)
        e_gen = tk.Entry(format_frame)
        e_number = tk.Entry(format_frame)
        e_padeJ = tk.Entry(format_frame)
        l_part_of_lang.grid(row=0, column=0)
        l_gen.grid(row=1, column=0)
        l_number.grid(row=2, column=0)
        l_padeJ.grid(row=3, column=0)
        e_part_of_lang.grid(row=0, column=1)
        e_gen.grid(row=1, column=1)
        e_number.grid(row=2, column=1)
        e_padeJ.grid(row=3, column=1)
        format_frame.part_of_lang = e_part_of_lang
        format_frame.gen = e_gen
        format_frame.number = e_number
        format_frame.padeJ = e_padeJ
        format_frame.grid(row=2, column=1)

        own_format_str = tk.Frame(top)
        l_str_input = tk.Label(own_format_str, text="Морфологическая информация")
        e_str_input = tk.Entry(own_format_str)
        l_str_input.grid(row=0, column=0)
        e_str_input.grid(row=1, column=0)
        own_format_str.str_input = e_str_input

        top.format_frame = format_frame
        top.own_format = own_format_str

        r_buttons = tk.IntVar()
        r_buttons.set(1)
        top.r_but = r_buttons
        tk.Radiobutton(top, text="Форматированный ввод", variable=r_buttons, value=1,
                       command=lambda: self.__change_new_word_input(r_buttons.get(), top)).grid(row=2, column=0,
                                                                                                pady=10,
                                                                                                padx=10)
        tk.Radiobutton(top, text="Как строка", variable=r_buttons, value=2,
                       command=lambda: self.__change_new_word_input(r_buttons.get(), top)).grid(row=3, column=0,
                                                                                                pady=10,
                                                                                                padx=10)
        b_add = tk.Button(top, text="Добавить", command=lambda: self.__add_new_word_process(top))
        b_add.grid(row=4, column=0, columnspan=2)

    def __add_new_word_process(self, top):
        word = top.word.get()
        count = top.count.get()
        if top.r_but.get() == 1:
            morphological_info = [top.format_frame.part_of_lang.get(),
                                  top.format_frame.gen.get(),
                                  top.format_frame.number.get(),
                                  top.format_frame.padeJ.get()]
        else:
            morphological_info = [top.own_format.str_input.get()]
        top.destroy()
        voc = self.__controller.add_new_word_to_voc(word, count, morphological_info)
        self.__set_content_table(voc)

    def __change_new_word_input(self, value, top):
        if value == 1:
            top.own_format.grid_forget()
            top.format_frame.grid(row=2, column=1, pady=10, padx=10)
        else:
            top.own_format.grid(row=2, column=1, pady=10, padx=10)
            top.format_frame.grid_forget()

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
