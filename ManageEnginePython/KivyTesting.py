# install kivy.deps.glew
from kivy.app import App
from kivy.label import Label
class FirstKivy(App):
    def build(self):
        return Label(test = "Hello Kivy")