class Sentence:
    def __init__(self):
        self.__string = ""
        self.__elements = []
        self.__tree = None
        self.__tagged = []

    def __del__(self):
        del self.__string
        del self.__elements
        del self.__tree
        del self.__tagged

    def get_string(self):
        return self.__string

    def get_elements(self):
        return self.__elements

    def get_tree(self):
        return self.__tree

    def get_tugged(self):
        return self.__tagged

    def set_tugged(self, tagged):
        del self.__tagged
        self.__tagged = tagged

    def set_string(self, string):
        del self.__string
        self.__string = string

    def set_elements(self, elements):
        del self.__elements
        self.__elements = elements

    def set_tree(self, tree):
        if self.__tree:
            del self.__tree
        self.__tree = tree
