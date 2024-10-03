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
from kivy.uix.textinput import TextInput

# Função para carregar dados de agenda a partir de um arquivo JSON
def carregar_agenda():
    arquivo = 'agenda_teste.json'
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return {}

# Função para salvar dados de agenda em um arquivo JSON
def salvar_agenda(agenda):
    with open('agenda_teste.json', 'w') as f:
        json.dump(agenda, f, indent=4)

# Função para carregar dados do préçário a partir de um arquivo JSON
def carregar_precario():
    arquivo = 'precario.json'
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return []

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

        self.precario_data = carregar_precario()

        # Layout para exibir os dados do préçário
        precario_layout = BoxLayout(orientation='vertical', padding=10)
        for item in self.precario_data:
            nome_label = Label(text=f"Nome: {item['nome']}")
            preco_label = Label(text=f"Preço: {item['preco']}")
            descricao_label = Label(text=f"Descrição: {item['descricao']}")
            precario_layout.add_widget(nome_label)
            precario_layout.add_widget(preco_label)
            precario_layout.add_widget(descricao_label)
            precario_layout.add_widget(Label(text=""))  # Espaçamento entre itens

        layout.add_widget(precario_layout)

        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

class PendentesScreen(Screen):
    def __init__(self, **kwargs):
        super(PendentesScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10)
        
        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.update_pendentes_list()

    def update_pendentes_list(self):
        # Limpar widgets antigos
        self.layout.clear_widgets()

        # Carregar os dados da agenda
        agenda_dados = carregar_agenda()
        trabalhos_pendentes = []

        # Obter a data atual
        data_atual = datetime.now().strftime("%Y-%m-%d")

        # Iterar pelos dados da agenda para encontrar trabalhos pendentes
        for date_str, trabalhos in agenda_dados.items():
            for trabalho in trabalhos:
                # Verificar se o trabalho não está concluído e se a data é atual ou futura
                if not trabalho.get('concluido', False) and date_str >= data_atual:
                    trabalhos_pendentes.append((date_str, trabalho))

        # Exibir trabalhos pendentes
        if trabalhos_pendentes:
            for date_str, trabalho in sorted(trabalhos_pendentes):
                trabalho_label = Label(text=f"{date_str} - {trabalho['hora']} - {trabalho['descricao']}")
                self.layout.add_widget(trabalho_label)
        else:
            # Exibir uma mensagem se não houver trabalhos pendentes
            self.layout.add_widget(Label(text="Nenhum trabalho pendente."))

        # Adicionar o botão de voltar ao final
        btn_back = Button(text="Voltar")
        btn_back.bind(on_release=self.go_back)
        self.layout.add_widget(btn_back)

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

        self.add_widget(layout)

        self.update_calendar()

    def update_calendar(self):
        self.frame_calend.clear_widgets()

        # Nome do mês
        month_name = calendar.month_name[self.month]
        lbl_month = Label(text=f"{month_name} {self.year}")
        self.frame_calend.add_widget(lbl_month)

        # Dias da semana
        days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for day in days_of_week:
            lbl_day = Label(text=day)
            self.frame_calend.add_widget(lbl_day)

        cal = calendar.monthcalendar(self.year, self.month)
        for week in cal:
            for day in week:
                if day != 0:
                    btn = Button(text=str(day))
                    if self.has_work(self.year, self.month, day):
                        btn.background_color = (1, 0, 0, 1)  # Marca os dias com trabalho
                    btn.bind(on_release=lambda instance, y=self.year, m=self.month, d=day: self.show_info(y, m, d))
                else:
                    btn = Label(text="")
                self.frame_calend.add_widget(btn)

    def has_work(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        agenda_dados = carregar_agenda()
        return date_str in agenda_dados and len(agenda_dados[date_str]) > 0

    def next_month(self, instance):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_calendar()

    def prev_month(self, instance):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()

    def show_info(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        agenda_dados = carregar_agenda()
        trabalhos = agenda_dados.get(date_str, [])

        layout = BoxLayout(orientation='vertical', padding=10)

        # Adiciona trabalhos ao layout
        if trabalhos:
            for trabalho in trabalhos:
                trabalho_label = Label(text=f"{trabalho['hora']} - {trabalho['descricao']}")
                layout.add_widget(trabalho_label)

        btn_modify = Button(text="Modificar Trabalhos")
        btn_modify.bind(on_release=lambda instance, ds=date_str: self.modify_work(ds))
        layout.add_widget(btn_modify)

        btn_close = Button(text="Fechar")
        btn_close.bind(on_release=self.close_popup)
        layout.add_widget(btn_close)

        self.popup = Popup(title="Trabalhos no Dia", content=layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def modify_work(self, date_str):
        self.close_popup(self)
        modify_screen = self.manager.get_screen('modify_work')
        modify_screen.prepare_for_modification(date_str)
        self.manager.current = 'modify_work'

    def close_popup(self, instance):
        self.popup.dismiss()

    def go_back(self, instance):
        self.manager.current = 'home'

class ModifyWorkScreen(Screen):
    def __init__(self, **kwargs):
        super(ModifyWorkScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)

        self.desc_input = TextInput(multiline=False, size_hint_y=None, height=30)
        layout.add_widget(self.desc_input)

        self.time_input = TextInput(multiline=False, size_hint_y=None, height=30)
        layout.add_widget(self.time_input)

        btn_save = Button(text="Salvar Alterações")
        btn_save.bind(on_release=self.save_info)
        layout.add_widget(btn_save)

        btn_cancel = Button(text="Cancelar")
        btn_cancel.bind(on_release=self.go_back)
        layout.add_widget(btn_cancel)

        btn_delete = Button(text="Eliminar Todos os Trabalhos")
        btn_delete.bind(on_release=self.delete_info)
        layout.add_widget(btn_delete)

        self.add_widget(layout)

    def prepare_for_modification(self, date_str):
        self.date_str = date_str
        agenda_dados = carregar_agenda()
        trabalhos = agenda_dados.get(date_str, [])
        if trabalhos:
            trabalho = trabalhos[0]
            self.time_input.text = trabalho['hora']
            self.desc_input.text = trabalho['descricao']

        else:
            self.time_input.text = ''
            self.desc_input.text = ''

    def save_info(self, instance):
        hora = self.time_input.text
        descricao = self.desc_input.text
        concluido = False
        if hora and descricao:
            agenda_dados = carregar_agenda()
            trabalhos = agenda_dados.get(self.date_str, [])
            found = False
            for trabalho in trabalhos:
                if trabalho['hora'] == hora:
                    trabalho['descricao'] = descricao
                    found = True
                    break
            if not found:
                if not trabalhos:
                    agenda_dados[self.date_str] = []
                agenda_dados[self.date_str].append({'hora': hora, 'descricao': descricao, 'concluido': concluido})
            salvar_agenda(agenda_dados)
            self.manager.get_screen('agenda').update_calendar()
            self.manager.current = 'agenda'

    def delete_info(self, instance):
        agenda_dados = carregar_agenda()
        if self.date_str in agenda_dados:
            del agenda_dados[self.date_str]
            salvar_agenda(agenda_dados)
            self.manager.get_screen('agenda').update_calendar()
            self.manager.current = 'agenda'

    def go_back(self, instance):
        self.manager.current = 'agenda'

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
        sm.add_widget(ModifyWorkScreen(name='modify_work'))
        return sm

if __name__ == '__main__':
    MyApp().run()
