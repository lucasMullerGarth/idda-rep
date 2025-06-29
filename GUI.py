import tkinter as tk

#Botão padrão

def criar_botao(janela, texto, comando):
    return tk.Button(
        janela,
        text=texto,
        bg="#B2B0B0",        # Cor de fundo
        fg="black",      # Cor do texto
        font=("Arial", 11, "bold"),  # Fonte, tamanho e estilo
        width=36,        # Largura em caracteres
        height=1,        # Altura em linhas
        bd = 10,
        command=comando
    )


#Tela ODS
   
def ods():

    tela_ods = tk.Tk()
    tela_ods.title("IDDA")
    tela_ods.geometry("800x605")
    tela_ods.configure(bg = "#363636")

    Bods1 = criar_botao(tela_ods,"1.Erradicação da pobreza",tela_ods.destroy).grid(row = 1, column = 1,padx=32,pady=(10,5))
    Bods2 = criar_botao(tela_ods,"2.Fome zero e agricultura sustentável.",tela_ods.destroy).grid(row = 2, column = 1,pady=10)
    Bods3 = criar_botao(tela_ods,"3.Saúde e Bem-Estar",tela_ods.destroy).grid(row = 3, column = 1,pady=10)
    Bods4 = criar_botao(tela_ods,"4.Educação de qualidade",tela_ods.destroy).grid(row = 4, column = 1,pady=10)
    Bods5 = criar_botao(tela_ods,"5.Igualdade de gênero",tela_ods.destroy).grid(row = 5, column = 1,pady=10)
    Bods6 = criar_botao(tela_ods,"6.Água potável e saneamento",tela_ods.destroy).grid(row = 6, column = 1,pady=10)
    Bods7 = criar_botao(tela_ods,"7.Energia acessível e limpa",tela_ods.destroy).grid(row = 7, column = 1,pady=10)
    Bods8 = criar_botao(tela_ods,"8.Trabalho decente e crescimento econômico",tela_ods.destroy).grid(row = 8, column = 1,pady=10)
    Bods9 = criar_botao(tela_ods,"9.Indústria, inovação e infraestrutura",tela_ods.destroy).grid(row = 9, column = 1,pady=10)
    Bods10 = criar_botao(tela_ods,"10.Redução das Desigualdades",tela_ods.destroy).grid(row = 1, column = 2, pady=(10,5))
    Bods11 = criar_botao(tela_ods,"11.Cidades e comunidades sustentáveis",tela_ods.destroy).grid(row = 2, column = 2)
    Bods13 = criar_botao(tela_ods,"12.Consumo e produção responsáveis",tela_ods.destroy).grid(row = 3, column = 2)
    Bods14 = criar_botao(tela_ods,"13.Combate às alterações climáticas",tela_ods.destroy).grid(row = 4, column = 2)
    Bods15 = criar_botao(tela_ods,"14.Vida de baixo d`água",tela_ods.destroy).grid(row = 5, column = 2)
    Bods16 = criar_botao(tela_ods,"15.Vida terrestre",tela_ods.destroy).grid(row = 6, column = 2)
    Bods17 = criar_botao(tela_ods,"16.Paz, justiça e instituições fortes",tela_ods.destroy).grid(row = 7, column = 2)
    Bods18 = criar_botao(tela_ods,"17.Parcerias em prol das metas",tela_ods.destroy).grid(row = 8, column = 2)

def Tela_inicial():

    #Tela inicial

    tela_inicial = tk.Tk()
    tela_inicial.title("IDDA")
    tela_inicial.geometry("800x600")

    tela_inicial.configure(bg = "#363636")

    def abrir_ods():

        tela_inicial.destroy()
        ods() 


    titulo = tk.Label(tela_inicial, 
    text= "IDDA",
    font=("Arial", 30,"bold"),
    bg="#363636")
    #origem (0,0)canto superior esquerdo
    titulo.pack(pady= 80)

    Biniciar = criar_botao(tela_inicial,"Iniciar",abrir_ods).pack(pady=30)

    Bsair = criar_botao(tela_inicial,"Sair",tela_inicial.destroy).pack(pady=30)
    
    tela_inicial.mainloop()

Tela_inicial()