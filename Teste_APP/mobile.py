import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add an image
        self.image = Image(source='images/large_test_image.png')
        layout.add_widget(self.image)

        # Add buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        registar_horas_button = Button(text='Registar Horas')
        registar_horas_button.bind(on_press=self.registar_horas)
        button_layout.add_widget(registar_horas_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def registar_horas(self, instance):
        self.manager.current = 'registar_horas'

class RegistarHorasScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistarHorasScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='Registar Horas Screen')
        layout.add_widget(label)
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RegistarHorasScreen(name='registar_horas'))
        return sm

if __name__ == '__main__':
    MyApp().run()
