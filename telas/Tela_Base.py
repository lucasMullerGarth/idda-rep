import tkinter as tk
class TelaBase(tk.Frame):

    def __init__(self, pai, controle):
        super(). __init__(pai, bg = "#363636")
        self.controle = controle
        
    def criar_botao(self,texto,comando):
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


