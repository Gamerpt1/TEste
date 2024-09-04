import customtkinter as ctk
import os
from PIL import Image  
import calendar
from datetime import datetime, date
from tkinter import messagebox    
import json   

class App(ctk.CTk):
    def __init__(self):

        def Registar_Horas():
            janela_registo = ctk.CTk()
            janela_registo.mainloop()

        def Orcamento():
            janela_orcamento = ctk.CTk()
            janela_orcamento.mainloop()
        
        def PicarPonto():
            janela_PP = ctk.CTk()
            janela_PP.mainloop()

        def Precario():
            janela_P = ctk.CTk()
            janela_P.mainloop()

        def Pendentes():
            janela_Pendentes = ctk.CTk()
            janela_Pendentes.mainloop()

        def get_last_id(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                infos = json.load(file)
    
            trabalhos = infos["Trabalhos"]
            if not trabalhos:
                return None
    
            last_id = max(trabalho["id"] for trabalho in trabalhos)
    
            return last_id

        def Ler_Agenda():
            # Leitura do ficheiro JSON
            with open("Agenda.json", 'r', encoding='utf-8') as ficheiro:
                dados = json.load(ficheiro)

            eventos = dados.get("Trabalhos", [])
            # Extraindo datas dos eventos
            trabalhos = {}
            for evento in eventos:
                data_str = evento.get("data", "")
                try:
                    data = datetime.strptime(data_str, "%Y-%m-%d").date()
                    descricao = {
                        "Tipo": evento.get("Tipo", ""),
                        "Descricao": evento.get("Descricao", ""),
                        "Materiais": evento.get("Materiais", ""),
                        "Patrao": evento.get ("Patrao", ""),
                        "Orcamento": evento.get("Orcamento", 0.0)
                    }
                    if data not in trabalhos:
                        trabalhos[data] = []
                    trabalhos[data].append(descricao)
                except ValueError:
                    pass  # Ignorar datas inválidas
            return trabalhos
        
        # Função para exibir o evento do dia clicado
        def show_info(year, month, day):
            def Adicionar(date):
                def Submeter():
                    
                    R_info = {
                                'id': Id + 1,
                                'data': date,
                                'Tipo': info.get(),
                                'Descricao': info2.get(),
                                'Patrao': info3.get(),
                                'Materiais': info4.get(),
                                'Orcamento': info5.get()
                            }
                    print(R_info)
                    
                    with open("Agenda.json", 'r', encoding='utf-8') as ficheiro:
                        dados = json.load(ficheiro)

                    # Salvar os dados tratados num novo ficheiro JSON
                    dados['Trabalhos'].append(R_info)

                    # Escrever de volta ao ficheiro JSON
                    with open('Agenda.json', 'w') as file:
                        json.dump(dados, file, indent=4)
                    
                    janela_adic.destroy()
            
                janela_adic = ctk.CTk ()
                janela_adic.title("Adicionar trabalho")
                janela_Trab.destroy()
                Label = ctk.CTkLabel (janela_adic, text ="Insira aqui as informações")
                Label.pack()
                Frame_adic = ctk.CTkFrame(janela_adic)
                Frame_adic.pack()

                tipos= ["Agricula", "Limpeza", "Outro"]

                Id = get_last_id("Agenda.json")

                info = ctk.CTkComboBox (Frame_adic, values=tipos)
                info.grid(row = 0, pady = 10)
                info2 = ctk.CTkEntry (Frame_adic, placeholder_text="Descrição")
                info2.grid(row = 1, pady = 10)
                info3 = ctk.CTkEntry (Frame_adic, placeholder_text="Patrão")
                info3.grid (row = 2, pady = 10) 
                info4 = ctk.CTkEntry (Frame_adic, placeholder_text="Materiais")
                info4.grid (row = 3, pady = 10) 
                info5 = ctk.CTkEntry (Frame_adic, placeholder_text="Orçamento")
                info5.grid (row = 4, pady = 10) 

                Frame_botoes = ctk.CTkFrame (janela_adic)
                Frame_botoes.pack(pady=10)

                botao_Confirm = ctk.CTkButton (Frame_botoes, text = "Confirmar", command=Submeter)
                botao_Confirm.grid(row = 6, column = 0, padx = 10)
                botao_Cancelar = ctk.CTkButton (Frame_botoes, text = "Cancelar", command = janela_adic.destroy)
                botao_Cancelar.grid(row = 6, column = 1, padx = 10)


                janela_adic.geometry("500x500")
                janela_adic.mainloop()

            def Alterar(data):
                print()

            def Apagar(data):
                def apaga_trabalhos_por_condicao(caminho_ficheiro, condicao):
                    # Verifica se o ficheiro existe
                    if os.path.exists(caminho_ficheiro):
                        # Abre o ficheiro no modo de leitura e carrega os dados
                        with open(caminho_ficheiro, 'r') as ficheiro:
                            dados = json.load(ficheiro)
        
                        # Filtra a lista de trabalhos conforme a condição
                        dados["Trabalhos"] = [trabalho for trabalho in dados["Trabalhos"] if not condicao(trabalho)]

                        # Abre o ficheiro no modo de escrita para atualizar os dados
                        with open(caminho_ficheiro, 'w') as ficheiro:
                            json.dump(dados, ficheiro, indent=4)  # Escreve os dados atualizados no ficheiro JSON
                        print(f"Os trabalhos que atendiam à condição foram apagados do ficheiro '{caminho_ficheiro}'.")
                    else:
                        print(f"O ficheiro '{caminho_ficheiro}' não existe.")

                # Exemplo de uso
                def condicao(trabalho):

                    return trabalho["data"] == data  # Condição para apagar trabalhos do tipo "Agricula"

                caminho = 'Agenda.json'
                Crt = 0
                while Crt != 1:
                    #Escrever código para PopUP de certeza
                    Op = messagebox.askokcancel("Trabalhos do Dia", f"Certeza que quer eliminar os Trabalhos a {day}/{month}/{year}:\n{info}")
                    if Op == True:
                        apaga_trabalhos_por_condicao(caminho, condicao)
                        Crt=1
                        janela_Trab.destroy()
                    else:
                        janela_Trab.destroy()
                        break
                        
                
                
            if day != 0:
                janela_Trab = ctk.CTk()
                janela_Trab.title(f"{day}/{month}/{year}")
                janela_Trab.geometry("600x600")
                Dia_label = ctk.CTkLabel(janela_Trab, text= f"{day}/{month}/{year}")
                Dia_label.pack()

                Text_label = ctk.CTkLabel(janela_Trab, text= "Trabalhos:")
                Text_label.pack()
                
                data_frame = ctk.CTkFrame(janela_Trab)
                data_frame.pack()

                data = date(year, month, day)
                data1 = str(data)
                if data in trabalhos:
                    eventos = trabalhos[data]
                    info = ""
                    for evento in eventos:
                        info += (f"\nTipo: {evento['Tipo']}\n"
                                f"Descrição: {evento['Descricao']}\n"
                                f"Materiais: {evento['Materiais']}\n"
                                f"Patrão: {evento['Patrao']}\n"
                                f"Orçamento: {evento['Orcamento']}\n")
                else:
                    info = "\nNenhum Trabalho marcado."

                label_infos = ctk.CTkLabel (data_frame, text= f"{info}" )
                label_infos.grid(pady = 10)

                botoes_frame = ctk.CTkFrame(janela_Trab)
                botoes_frame.pack(pady = 50)    

                label_infos = ctk.CTkButton (botoes_frame, text= "Adicionar", command=lambda:Adicionar(data1))
                label_infos.grid(row =0,column= 0, pady = 10, padx = 10)
                label_infos = ctk.CTkButton (botoes_frame, text= "Apagar", command=lambda:Apagar(data1) )
                label_infos.grid(row =0,column= 1, pady = 10, padx = 10)                            
                label_infos = ctk.CTkButton (botoes_frame, text= "Alterar", command=lambda:Alterar(data1) )
                label_infos.grid(row =0,column= 2, pady = 10, padx = 10)
                
                #messagebox.showinfo("Trabalhos do Dia", f"Trabalhos a {day}/{month}/{year}:\n{info}")
                janela_Trab.mainloop()

        # Função para atualizar o calendário
        def update_calendar(year, month):
            for widget in frame_calend.winfo_children():
                widget.destroy()

            trabalhos = Ler_Agenda()
            
            # Nome do mês
            month_name = calendar.month_name[month]
            lbl_month = ctk.CTkLabel(frame_calend, text=f"{month_name} {year}", font=("Arial", 16))
            lbl_month.grid(row=0, column=0, columnspan=7, pady=10)

            # Dias da semana
            days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            for i, day in enumerate(days_of_week):
                lbl_day = ctk.CTkLabel(frame_calend, text=day)
                lbl_day.grid(row=1, column=i, padx=5, pady=5)

            cal = calendar.monthcalendar(year, month)
            for row_idx, week in enumerate(cal, start=2):
                for col_idx, day in enumerate(week):
                    day_str = str(day) if day != 0 else ''
                    if day != 0 and date(year, month, day) in trabalhos:
                        btn = ctk.CTkButton(frame_calend, text=day_str,command=lambda y=year, m=month, d=day: show_info(y, m, d), fg_color="red")
                    else:
                        btn = ctk.CTkButton(frame_calend, text=day_str, command=lambda y=year, m=month, d=day: show_info(y, m, d))
                    btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)

        def next_month():
            global year, month
            month += 1
            if month > 12:
                month = 1
                year += 1
            update_calendar(year, month)

        def prev_month():
            global year, month
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            update_calendar(year, month)

        super().__init__()

        self.title("Programa")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "Simbolo.jpg")), size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text=" Rosa Work", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Agenda",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Patrões",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=20, border_spacing=10, text="Trabalhos",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_buttons = ctk.CTkFrame (self.home_frame)
        self.home_frame_buttons.grid (row = 1, column = 0, padx=20, pady=10)

        self.home_frame_button_1 = ctk.CTkButton(self.home_frame_buttons, text="Registar Horas", command= Registar_Horas, hover_color="#FFCCCC")
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.home_frame_button_5 = ctk.CTkButton(self.home_frame_buttons, text="Orçamento", command=Orcamento, hover_color="#FFCCCC")
        self.home_frame_button_5.grid(row=1, column=2, padx=20, pady=10)
        self.home_frame_button_2 = ctk.CTkButton(self.home_frame_buttons, text="Picar Ponto", compound="right", command=PicarPonto, hover_color="#FFCCCC")
        self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.home_frame_button_3 = ctk.CTkButton(self.home_frame_buttons, text="Preçario", compound="top", command=Precario, hover_color="#FFCCCC")
        self.home_frame_button_3.grid(row=2, column=2, padx=20, pady=10)
        self.home_frame_button_4 = ctk.CTkButton(self.home_frame_buttons, text="Pendentes", compound="bottom", command=Pendentes, hover_color="#FFCCCC")
        self.home_frame_button_4.grid(row=3, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        # Frame para o calendário
        frame_calend = ctk.CTkFrame(self.second_frame)
        frame_calend.pack(pady=20)

        # Obter o ano e mês atual
        global year, month
        now = datetime.now()
        year = now.year
        month = now.month
        

        # Nome do mês
        month_name = calendar.month_name[month]
        lbl_month = ctk.CTkLabel(frame_calend, text=f"{month_name} {year}", font=("Arial", 16))
        lbl_month.grid(row=0, column=0, columnspan=7, pady=10)

        # Dias da semana
        days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        for i, day in enumerate(days_of_week):
            lbl_day = ctk.CTkLabel(frame_calend, text=day)
            lbl_day.grid(row=1, column=i, padx=5, pady=5)
        
        cal = calendar.monthcalendar(year, month)
        trabalhos = Ler_Agenda()
        
        for row_idx, week in enumerate(cal, start=2):
            for col_idx, day in enumerate(week):
                day_str = str(day) if day != 0 else ''
                if day != 0 and date(year, month, day) in trabalhos:
                    btn = ctk.CTkButton(frame_calend, text=day_str,command=lambda d=day: show_info(year, month, d), fg_color="red", hover_color="#FFCCCC")
                else:
                    btn = ctk.CTkButton(frame_calend, text=day_str, command=lambda d=day: show_info(year, month, d), hover_color="#FFCCCC")
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)

        bt_prev = ctk.CTkButton(self.second_frame, text="Mês Anterior", command=prev_month, hover_color="#FFCCCC")
        bt_prev.pack(side="left", padx=10, pady=10)

        bt_next = ctk.CTkButton(self.second_frame, text="Próximo Mês", command=next_month, hover_color="#FFCCCC")
        bt_next.pack(side="right", padx=10, pady=10)

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create forth frame
        self.forth_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "Red") if name == "Patrões" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "Green") if name == "Materiais" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "Purple") if name == "Agenda" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "Patrões":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "Trabalhos":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "Agenda":
            self.forth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.forth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("Patrões")

    def frame_3_button_event(self):
        self.select_frame_by_name("Trabalhos")
            
    def frame_4_button_event(self):
        self.select_frame_by_name("Agenda")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
