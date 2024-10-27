import kivy
from kivy.properties import ListProperty
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.clock import Clock
import random

Window.size = (2040, 1080)

class SignButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])

class OptionButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])

class MathSolver(MDApp):
    selected_sign = ""
    answer = ""
    correct = 0
    wrong = 0
    start_music = None
    game_music = None
    correct_sound = None
    wrong_sound = None

    def build(self):
        global screen_manager
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(Builder.load_file("widget/start.kv"))
        screen_manager.add_widget(Builder.load_file("widget/select_sign.kv"))
        screen_manager.add_widget(Builder.load_file("widget/quiz.kv"))
        screen_manager.add_widget(Builder.load_file("widget/final_score.kv"))

        self.start_music = SoundLoader.load("sound/imawaiindayo-mimi2.mp3")
        self.game_music = SoundLoader.load("sound/bgm-pekora.mp3")
        self.correct_sound = SoundLoader.load("sound/suara-benar.mp3")
        self.wrong_sound = SoundLoader.load("sound/suara-salah.mp3")

        if self.start_music:
            self.start_music.loop = True
            self.start_music.play()

        self.animate_play_button()
        self.animate_buah_tomat()
        self.animate_buah_strawberry()
        self.animate_sign_buttons()

        return screen_manager

    def on_start(self):
        if self.start_music:
            self.start_music.play()

    def animate_play_button(self):
        play_button = screen_manager.get_screen("start").ids.play_button
        animation = (
            Animation(size=(420, 370), duration=0.8) +
            Animation(size=(400, 350), duration=0.8)
        )
        animation.repeat = True
        animation.start(play_button)

    def animate_buah_tomat(self):
        buah = screen_manager.get_screen("select_sign").ids.buah_image
        buah_animation = (
            Animation(pos_hint={"center_y": .32}, duration=1) +
            Animation(pos_hint={"center_y": .25}, duration=1)
        )
        buah_animation.repeat = True
        buah_animation.start(buah)

        tomat = screen_manager.get_screen("select_sign").ids.tomat_image
        tomat_animation = (
            Animation(pos_hint={"center_y": .32}, duration=1) +
            Animation(pos_hint={"center_y": .25}, duration=1)
        )
        tomat_animation.repeat = True
        tomat_animation.start(tomat)
        
    def animate_buah_strawberry(self):
        strbr = screen_manager.get_screen("quiz").ids.strawberry_image
        strawberry_animation = (
            Animation(pos_hint={"center_y": .32}, duration=1) +
            Animation(pos_hint={"center_y": .25}, duration=1)
        )
        strawberry_animation.repeat = True
        strawberry_animation.start(strbr)

        mngga = screen_manager.get_screen("quiz").ids.mangga_image
        mangga_animation = (
            Animation(pos_hint={"center_y": .32}, duration=1) +
            Animation(pos_hint={"center_y": .25}, duration=1)
        )
        mangga_animation.repeat = True
        mangga_animation.start(mngga)

    def animate_sign_buttons(self):
        buttons = [
            screen_manager.get_screen("select_sign").children[0].children[4],
            screen_manager.get_screen("select_sign").children[0].children[3],
            screen_manager.get_screen("select_sign").children[0].children[2],
            screen_manager.get_screen("select_sign").children[0].children[1],
        ]
        
        def animate_button(index):
            button = buttons[index]
            animation = Animation(size=(button.width * 1.1, button.height * 1.1), duration=0.3) + Animation(size=(button.width, button.height), duration=0.3)
            animation.bind(on_complete=lambda *args: animate_button((index + 1) % len(buttons)))
            animation.start(button)

        animate_button(0)

    def switch_to_game_music(self):
        if self.start_music and self.start_music.state == 'play':
            self.start_music.stop()

        if self.game_music:
            self.game_music.loop = True
            self.game_music.play()

    def switch_to_start_music(self):
        if self.game_music and self.game_music.state == 'play':
            self.game_music.stop()

        if self.start_music:
            self.start_music.play()
    
    def select_sign(self, sign):
        self.switch_to_game_music()
        self.selected_sign = sign
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)

        if sign == ":":
            num1 = random.randint(1, 10) * 2
            num2 = random.randint(1, 5)
            while num1 % num2 != 0 or (num1 // num2) % 2 != 0:
                num1 = random.randint(1, 10) * 2
                num2 = random.randint(1, 5)
        elif sign == "-":
            if num1 < num2:
                num1, num2 = num2, num1

        screen_manager.get_screen("quiz").ids.question.text = f"{num1} {sign} {num2} = ?"

        if sign == "+":
            self.answer = str(num1 + num2)
        elif sign == "-":
            self.answer = str(num1 - num2)
        elif sign == "x":
            self.answer = str(num1 * num2)
        elif sign == ":":
            self.answer = str(num1 // num2)

        option_list = [self.answer]
        while len(option_list) < 4:
            option = str(self.generate_option(sign))
            if option not in option_list:
                option_list.append(option)

        random.shuffle(option_list)
        for i in range(1, 5):
            screen_manager.get_screen("quiz").ids[f"option{i}"].text = option_list[i - 1]


        self.start_timer()
        screen_manager.current = "quiz"

    def generate_option(self, sign):
        if sign == "+":
            return random.randint(1, 10)
        elif sign == "-":
            return random.randint(0, 10)
        elif sign == "x":
            return random.randint(1, 10)
        elif sign == ":":
            num1 = random.randint(1, 10) * 2
            num2 = random.randint(1, 5)
            while num1 % num2 != 0 or (num1 // num2) % 2 != 0:
                num1 = random.randint(1, 10) * 2
                num2 = random.randint(1, 5)
            return num1 // num2
    
    def quiz(self, option, instance):
        Clock.unschedule(self.timer_event)
        
        if option == self.answer:
            self.correct += 1
            instance.bg_color = (0, 1, 0, 1)
            if self.correct_sound:
                self.correct_sound.play()
        else:
            self.wrong += 1
            instance.bg_color = (1, 0, 0, 1)
            if self.wrong_sound:
                self.wrong_sound.play()
            self.disable_wrong_options(instance)
        
        Clock.unschedule(self.timer_event)


    def disable_wrong_options(self, instance):
        for i in range(1, 5):
            button = screen_manager.get_screen("quiz").ids[f"option{i}"]
            if button.text != self.answer:
                button.disabled = True

    def next_question(self):
        self.start_timer()
        self.select_sign(self.selected_sign)
        for i in range(1, 5):
            option_button = screen_manager.get_screen("quiz").ids[f"option{i}"]
            option_button.disabled = False
            option_button.bg_color = (34 / 255, 139 / 255, 34 / 255, 1)

    def final_score(self):
        if self.correct == 0 and self.wrong == 0:
            screen_manager.current = "start"
        else:
            success_rate = round((self.correct / (self.correct + self.wrong)) * 100)
            screen_manager.get_screen("final_score").ids.correct.text = f"{self.correct} Benar!"
            screen_manager.get_screen("final_score").ids.wrong.text = f"{self.wrong} Salah!"
            screen_manager.get_screen("final_score").ids.success_rate.text = f"{success_rate}% Score!"
            
            self.animate_lemon_avocado()

            screen_manager.current = "final_score"
        if self.timer_event:
            Clock.unschedule(self.timer_event)

    def animate_lemon_avocado(self):
        
        lemon = screen_manager.get_screen("final_score").ids.lemon_image
        lemon_animation = (
            Animation(pos_hint={"center_y": .30}, duration=1) +
            Animation(pos_hint={"center_y": .25}, duration=1)
        )
        lemon_animation.repeat = True
        lemon_animation.start(lemon)

        avocado = screen_manager.get_screen("final_score").ids.avocado_image
        avocado_animation = (
            Animation(pos_hint={"center_y": .30}, duration=1) +
            Animation(pos_hint={"center_y": .25}, duration=1)
        )
        avocado_animation.repeat = True
        avocado_animation.start(avocado)

    def replay(self):
        self.correct = 0
        self.wrong = 0
        screen_manager.current = "select_sign"
        self.switch_to_game_music()
        
    def start_timer(self):
        self.countdown = 15
        if self.timer_event:
            Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.countdown -= 1
        screen_manager.get_screen("quiz").ids.timer_label.text = f"{self.countdown}"
        if self.countdown <= 0:
            Clock.unschedule(self.timer_event)
            self.times_up()

    def times_up(self):
        self.wrong += 1
        if self.wrong_sound:
            self.wrong_sound.play()
        self.next_question()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.countdown = 15
        self.screen_manager = ScreenManager()
        self.selected_sign = None 
        
if __name__ == '__main__':
    LabelBase.register(name="LuckiestGuy", fn_regular="assets/LuckiestGuy-Regular.ttf")
    MathSolver().run()
