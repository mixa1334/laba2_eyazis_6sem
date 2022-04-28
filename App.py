import Vocabulary
import Controller
import View


class App:
    def __init__(self):
        voc = Vocabulary.Vocabulary()
        view = View.View()
        controller = Controller.Controller(voc, view)
        view.set_controller(controller)
        self.__voc = voc
        self.__view = view
        self.__controller = controller

    def __del__(self):
        del self.__controller
        del self.__view
        del self.__voc

    def start(self):
        self.__view.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
