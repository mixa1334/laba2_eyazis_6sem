class Vocabulary:
    def __init__(self):
        self.__sentences = []
        self.__do_filter = False
        self.__filter_settings = []

    def set_sentences(self, sentences):
        del self.__sentences
        self.__sentences = sentences

    def add_sentence(self, sentence):
        self.__sentences.append(sentence)

    def get_sentence_by_id(self, id):
        return self.__sentences[id]

    def replace_sentence_by_id(self, id, sentence):
        self.__sentences[id] = sentence

    def set_filter_settings(self, settings):
        del self.__filter_settings
        self.__filter_settings = list(settings)

    def set_enable_settings(self, enable):
        self.__do_filter = enable

    def get_all_sentences(self):
        result_sentences = {}
        for i in range(len(self.__sentences)):
            sent = self.__sentences[i]
            if self.__do_filter:
                status = True
                for filter in self.__filter_settings:
                    if filter not in sent.get_elements():
                        status = False
                if status:
                    result_sentences[i] = sent
            else:
                result_sentences[i] = sent
        return result_sentences

    def __del__(self):
        del self.__sentences
        del self.__do_filter
        del self.__filter_settings
