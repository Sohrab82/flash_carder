# https://realpython.com/mobile-app-kivy-python/
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import random
from datetime import datetime


class Ui_MainWindow(App):
    def __init__(self, dict_handler, **kwargs):
        super().__init__(**kwargs)
        self.dh = dict_handler
        self.selected_word_idx = -1
        self.shown_cntr = 0
        self.passed_cntr = 0
        self.translation_is_shown = False

    def build(self):
        self.title = "FlashCarder"
        from kivy.core.window import Window
        Window.size = (818, 610)
        main_layout = BoxLayout(orientation="vertical")

        self.btnWord = Button(
            text="sdfhgsdjhf",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            height=250,
            font_size=48,
            size_hint_y=None,
            background_normal='',
            background_color='white',
            color='black'
        )
        main_layout.add_widget(self.btnWord)

        self.btnTranslation = Button(
            text="eriutyieurty",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            height=250,
            font_size=48,
            size_hint_y=None,
            background_normal='',
            background_color='white',
            color='black'
        )
        main_layout.add_widget(self.btnTranslation)

        self.h_layout = BoxLayout(orientation="horizontal")
        self.h_layout.size_hint = (1, None)

        self.btnFail = Button(
            text="Fail",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size=48,
            background_color='red'
        )

        self.btnKeep = Button(
            text="Keep",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size=48,
            background_color='yellow',
        )
        # self.btnKeep.bind(on_press=self.btnKeepClick)

        self.btnPass = Button(
            text="Pass",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size=48,
            background_color='green',
        )
        self.h_layout.add_widget(self.btnFail)
        self.h_layout.add_widget(self.btnKeep)
        self.h_layout.add_widget(self.btnPass)
        main_layout.add_widget(self.h_layout)

        self.btnFail.bind(on_press=self.btnFailClick)
        self.btnKeep.bind(on_press=self.btnKeepClick)
        self.btnPass.bind(on_press=self.btnPassClick)

        self.btnTranslation.bind(on_press=self.btnShowClick)
        self.btnWord.bind(on_press=self.btnShowClick)
        self.btnTranslation.text = ""

        self.find_new_word()
        self.hide_frame()

        return main_layout

    def hide_frame(self):
        self.h_layout.opacity = 0

    def show_frame(self):
        self.h_layout.opacity = 1

    def find_new_word(self):
        self.btnTranslation.text = ""

        self.title = "FlashCarder " + \
            str(self.passed_cntr) + '/' + str(self.shown_cntr)
        self.shown_cntr += 1

        rand_num = random.randint(0, len(self.dh.dictionary) - 1)
        n = rand_num
        all_words_used = False
        while not all_words_used:
            # if self.dh.dictionary[n].should_show(datetime.strptime('2022-01-01', '%Y-%m-%d')):
            if self.dh.dictionary[n].should_show(datetime.today()):
                self.selected_word_idx = n
                self.btnWord.text = self.dh.dictionary[n].word
                break
            else:
                n += 1
                if n == len(self.dh.dictionary):
                    n = 0
                if n == rand_num:
                    all_words_used = True

        self.translation_is_shown = False
        self.hide_frame()

    def btnShowClick(self, instance):
        if self.translation_is_shown:
            return
        self.btnTranslation.text = self.dh.dictionary[self.selected_word_idx].translation
        self.translation_is_shown = True
        self.show_frame()

    def btnPassClick(self, instance):
        if not self.translation_is_shown:
            self.btnShowClick(instance)
            return
        self.dh.dictionary[self.selected_word_idx].onPass()
        self.passed_cntr += 1
        self.find_new_word()

    def btnFailClick(self, instance):
        if not self.translation_is_shown:
            self.btnShowClick(instance)
            return
        self.dh.dictionary[self.selected_word_idx].onFail()
        self.find_new_word()

    def btnKeepClick(self, instance):
        if not self.translation_is_shown:
            self.btnShowClick(instance)
            return
        self.dh.dictionary[self.selected_word_idx].onKeep()
        self.find_new_word()

    def btnDeleteWord(self, instance):
        if self.selected_word_idx != -1:
            del(self.dh.dictionary[self.selected_word_idx])
        self.find_new_word()


if __name__ == "__main__":
    app = Ui_MainWindow()
    run()
