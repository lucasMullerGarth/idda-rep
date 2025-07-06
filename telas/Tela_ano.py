import tkinter as tk
from telas.Tela_Base import TelaBase
from Bot_ODS import Bot_ODS


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

        self.criar_botao("2024", lambda: self.bot_navegador(controle,"//button[text()='Baixar a base de dados do IDSC-BR 2023 ']","Base_de_Dados_IDSC-BR_2024.xlsx")).pack(pady=30)
        self.criar_botao("2023", lambda: self.bot_navegador(controle,"//button[text()='Baixar a base de dados do IDSC-BR 2023 ']","Base_de_Dados_IDSC-BR_2023.xlsx")).pack(pady=30)
        self.criar_botao("2022", lambda: self.bot_navegador(controle,"//button[text()='Baixar a base de dados do IDSC-BR 2022 ']","Base_de_Dados_IDSC-BR_2022.xlsx")).pack(pady=30)
    
    def bot_navegador(self, controle, nome, nome_do_arquivo):
        
        Bot = Bot_ODS()
        
        if (Bot.verifica_arquivos(nome_do_arquivo)):
            
            controle.mostrar_tela("TelaODS")
            
        else:
            controle.mostrar_tela("TelaDeEspera")
            self.after(100, lambda: self.executa_bot(Bot, controle, nome,))

     
    def executa_bot(self, Bot, controle, nome,):
        
        Bot.baixa_arquivos(nome)
        controle.mostrar_tela("TelaODS")
        
    
        

   
    