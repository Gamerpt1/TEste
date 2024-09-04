import os
import json
import calendar
from datetime import datetime
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

# Função para carregar dados de agenda a partir de um arquivo JSON
def carregar_agenda():
    arquivo = 'agenda_teste.json'
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return {}

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_registar_horas = Button(text="Registar Horas")
        btn_registar_horas.bind(on_release=self.go_to_registar_horas)
        layout.add_widget(btn_registar_horas)

        btn_orcamento = Button(text="Orçamento")
        btn_orcamento.bind(on_release=self.go_to_orcamento)
        layout.add_widget(btn_orcamento)

        btn_picar_ponto = Button(text="Picar Ponto")
        btn_picar_ponto.bind(on_release=self.go_to_picar_ponto)
        layout.add_widget(btn_picar_ponto)

        btn_precario = Button(text="Preçario")
        btn_precario.bind(on_release=self.go_to_precario)
        layout.add_widget(btn_precario)

        btn_pendentes = Button(text="Pendentes")
        btn_pendentes.bind(on_release=self.go_to_pendentes)
        layout.add_widget(btn_pendentes)

        btn_agenda = Button(text="Agenda")
        btn_agenda.bind(on_release=self.go_to_agenda)
        layout.add_widget(btn_agenda)

        self.add_widget(layout)

    def go_to_registar_horas(self, instance):
        self.manager.current = 'registar_horas'

    def go_to_orcamento(self, instance):
        self.manager.current = 'orcamento'

    def go_to_picar_ponto(self, instance):
        self.manager.current = 'picar_ponto'

    def go_to_precario(self, instance):
        self.manager.current = 'precario'

    def go_to_pendentes(self, instance):
        self.manager.current = 'pendentes'

    def go_to_agenda(self, instance):
        self.manager.current = 'agenda'

class RegistarHorasScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistarHorasScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Registar Horas"))

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class OrcamentoScreen(Screen):
    def __init__(self, **kwargs):
        super(OrcamentoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Orçamento"))

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class PicarPontoScreen(Screen):
    def __init__(self, **kwargs):
        super(PicarPontoScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Picar Ponto"))

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class PrecarioScreen(Screen):
    def __init__(self, **kwargs):
        super(PrecarioScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Preçario"))

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class PendentesScreen(Screen):
    def __init__(self, **kwargs):
        super(PendentesScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text="Pendentes"))

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class AgendaScreen(Screen):
    def __init__(self, **kwargs):
        super(AgendaScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)

        self.year = datetime.now().year
        self.month = datetime.now().month

        self.frame_calend = GridLayout(cols=7)
        layout.add_widget(self.frame_calend)

        btn_prev = Button(text="Mês Anterior")
        btn_prev.bind(on_release=self.prev_month)
        layout.add_widget(btn_prev)

        btn_next = Button(text="Próximo Mês")
        btn_next.bind(on_release=self.next_month)
        layout.add_widget(btn_next)

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.agenda_dados = carregar_agenda()
        self.update_calendar(self.year, self.month)

        self.add_widget(layout)

    def update_calendar(self, year, month):
        self.frame_calend.clear_widgets()

        # Nome do mês
        month_name = calendar.month_name[month]
        lbl_month = Label(text=f"{month_name} {year}")
        self.frame_calend.add_widget(lbl_month)

        # Dias da semana
        days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for day in days_of_week:
            lbl_day = Label(text=day)
            self.frame_calend.add_widget(lbl_day)

        cal = calendar.monthcalendar(year, month)
        for week in cal:
            for day in week:
                if day != 0:
                    btn = Button(text=str(day))
                    if self.has_work(year, month, day):
                        btn.background_color = (1, 0, 0, 1)  # Marca os dias com trabalho
                    btn.bind(on_release=lambda instance, y=year, m=month, d=day: self.show_info(y, m, d))
                else:
                    btn = Label(text="")
                self.frame_calend.add_widget(btn)

    def has_work(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        return date_str in self.agenda_dados

    def next_month(self, instance):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_calendar(self.year, self.month)

    def prev_month(self, instance):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar(self.year, self.month)

    def show_info(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        if date_str in self.agenda_dados:
            info = self.agenda_dados[date_str]
        else:
            info = "Nenhum trabalho marcado."

        popup = Popup(title=f"Informações do dia {day}/{month}/{year}",
                      content=Label(text=info),
                      size_hint=(0.6, 0.4))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'home'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RegistarHorasScreen(name='registar_horas'))
        sm.add_widget(OrcamentoScreen(name='orcamento'))
        sm.add_widget(PicarPontoScreen(name='picar_ponto'))
        sm.add_widget(PrecarioScreen(name='precario'))
        sm.add_widget(PendentesScreen(name='pendentes'))
        sm.add_widget(AgendaScreen(name='agenda'))
        return sm

if __name__ == "__main__":
    MyApp().run()
