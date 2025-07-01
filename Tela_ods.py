import tkinter as tk

class TelaODS(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#363636")

        self.master = master
        self.ods_nomes = [
            "1. Erradicação da pobreza",
            "2. Fome zero e agricultura sustentável",
            "3. Saúde e Bem-Estar",
            "4. Educação de qualidade",
            "5. Igualdade de gênero",
            "6. Água potável e saneamento",
            "7. Energia acessível e limpa",
            "8. Trabalho decente e crescimento econômico",
            "9. Indústria, inovação e infraestrutura",
            "10. Redução das desigualdades",
            "11. Cidades e comunidades sustentáveis",
            "12. Consumo e produção responsáveis",
            "13. Combate às alterações climáticas",
            "14. Vida debaixo d’água",
            "15. Vida terrestre",
            "16. Paz, justiça e instituições fortes",
            "17. Parcerias em prol das metas"
        ]

        self.criar_botoes()

    def criar_botoes(self):
        for i, nome in enumerate(self.ods_nomes):
            linha = i % 9 + 1
            coluna = 1 if i < 9 else 2
            botao = self.criar_botao(nome, lambda n=nome: self.selecionar_ods(n))
            botao.grid(row=linha, column=coluna, padx=20, pady=10)

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

    def selecionar_ods(self, nome):
        print(f"ODS selecionado: {nome}")