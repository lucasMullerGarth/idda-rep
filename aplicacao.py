import tkinter as tk
from Tela_inicial import TelaInicial
from Tela_ods import TelaODS

# Classe principal da aplicação
class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IDDA")
        self.geometry("800x605")
        self.configure(bg="#363636")

        # Dicionário de telas (frames)
        self.telas = {}

        for Tela in (TelaInicial, TelaODS):
            frame = Tela(self)
            self.telas[Tela.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("TelaInicial")

    def mostrar_tela(self, nome):
        frame = self.telas[nome]
        frame.tkraise()