import tkinter as tk
from telas.Tela_Base import TelaBase

class TelaAno(TelaBase):
    
    def __init__(self, pai, controle):
        super().__init__(pai, controle)
        
        tk.Label(self, 
        text = "Escolha o ano da ODS",
        bg="#363636",
        fg="white",
        font=("Arial", 20, "bold"),
        width=36,
        height=1,
        bd=10,
        anchor="center"
        ).pack(pady=50)

        self.criar_botao("2024", lambda: self.bot_navegador(controle,200001)).pack(pady=30)
        self.criar_botao("2023", lambda: self.bot_navegador(controle,200001)).pack(pady=30)
        self.criar_botao("2022", lambda: self.bot_navegador(controle,200001)).pack(pady=30)
    
    def bot_navegador(self, controle, IP):
        
        controle.mostrar_tela("TelaODS")

     

        
    
        

   
    