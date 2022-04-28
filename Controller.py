import Vocabulary
import engine


class Controller:
    def __init__(self, voc, view):
        self.__voc = voc
        self.__view = view
        self.__filter_set = []
        self.__do_filter = False

    def save_vocabulary(self, filename):
        engine.write_vocabulary_to_file(self.__voc, filename)

    def open_vocabulary(self, filename):
        del self.__voc
        self.__voc = engine.read_vocabulary_from_file(filename)
        return self.__voc

    def create_empty(self):
        del self.__voc
        self.__voc = Vocabulary.Vocabulary()
        return self.__voc

    def create_from_doc(self, filename):
        del self.__voc
        text = engine.read_text_from_file(filename)
        self.__voc = engine.process_text(text)
        return self.__voc

    def add_new_sentence_to_voc(self, sentence):
        sentence = engine.process_sentence(sentence)
        self.__voc.add_sentence(sentence)
        return self.__voc

    def get_voc(self):
        return self.__voc

    def edit_word_in_voc(self, id, str_sent):
        return None

    def set_filter_settings(self, setting):
        self.__voc.set_filter_settings(list(setting))

    def set_filter_enable(self, enable):
        self.__voc.set_enable_settings(enable)

    def save_as_doc(self, filename):
        engine.write_text_to_file(filename, self.__voc)
