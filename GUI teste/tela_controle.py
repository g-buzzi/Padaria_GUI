import tkinter as tk
from tkinter.constants import BOTH, CENTER, S
from widgets import RoundedButton

"""
class Tela():
    def __init__(self):
        self.__tela = tk.Tk()
"""

window = tk.Tk()
window.geometry("1680x1050")


window.rowconfigure(0, weight=2)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=30)
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)


cabecalho = tk.Frame(window, bg="#3A312C", width="100")

titulo = tk.Label(cabecalho, text="Ingredientes", fg="#f08e21", bg="#3A312C", font="Arial 24 bold")
titulo.pack(anchor= CENTER)


corpo = tk.Frame(window, bg="#FFEDB7", height="100", width="100")
opcoes = tk.Frame(window, bg="red", width="100")

menu_lateral = tk.Frame(window, bg="#3A312C")

lista_botoes = ["Ingredientes", "Receitas", "Produtos", "Estoque", "Vendas", "Funcionarios", "Clientes", "Sair"]



for i in range(len(lista_botoes)):
    bt_ingrediente = RoundedButton(menu_lateral, 200, 40, 20, 0, "#f08e21", "#3A312C", lista_botoes[i], text_fill="#3a312c")
    bt_ingrediente.grid(row=i + 1, column=0, padx= 10, pady= 10)



menu_lateral.grid(row=0, column= 0, rowspan=3, sticky="nwse")
cabecalho.grid(row=0, column=1, sticky="nwse")
corpo.grid(row=2, column=1, sticky="nwse")
opcoes.grid(row=1, column=1, sticky="nwse")
corpo.name = "corpo"

def clicado():
    print("clicaram")

opcoes_dict = {"Cadastrar": clicado, "Listar": clicado, "Alterar": clicado, "Voltar": clicado}

opcoes.rowconfigure(0, weight=1)
i = 0
for nome, funcao in opcoes_dict.items():
    opcoes.columnconfigure(i, weight=1)
    botao = tk.Button(opcoes, bg="#3A312C", fg = "#f08e21", text = nome, command = funcao,  activebackground="#f08e21", activeforeground="#3A312C")
    botao.grid(row=0, column=i, sticky="nwse")
    i += 1



ent_nome = tk.Entry(corpo)
ent_nome.pack()
ent_nome.name = "entrada_1"

def submit():
    for widget in window.winfo_children():
        try:
            if widget.name == "corpo":
                corpo = widget
                break
        except AttributeError:
            pass
    for widget in corpo.winfo_children():
        if isinstance(widget, tk.Entry):
            print("{}: {}".format(widget.name, widget.get()))

bt_submit = RoundedButton(corpo, 100, 20, 10, 0, "#3a312c", "#FFEDB7", "Submit", text_fill="#f08e21", text_font= "Arial 10 bold", command=submit)
bt_submit.pack()

            

window.resizable(True, True)
 
window.mainloop()
"""
while True:
    window.update()
"""