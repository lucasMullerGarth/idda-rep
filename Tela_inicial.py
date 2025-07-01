import os
import tkinter as tk
from tkinter import PhotoImage

# Tela inicial com botão iniciar e sair
class TelaInicial(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#363636")

        # Logo da empresa
        caminho_base = os.path.dirname(__file__)
        caminho_logo = os.path.join(caminho_base, "IDDAlogo-com-texto.png")

        logo = tk.PhotoImage(file=caminho_logo)
        imagem = tk.Label(self, image=logo, bg="#363636")
        imagem.image = logo
        imagem.pack(pady=60)
       

        self.criar_botao("Iniciar", lambda: master.mostrar_tela("TelaODS")).pack(pady=30)
        self.criar_botao("Sair", master.destroy).pack(pady=30)

    def criar_botao(self, texto, comando):
        return tk.Button(
            self,
            text=texto,
            bg="#B2B0B0",
            fg="black",
            font=("Arial", 11, "bold"),
            width=36,
            height=1,
            bd=10,
            command=comando
        )
    
    

