import tkinter as tk
from tkinter import messagebox

import cadastro_pessoas
import cadastro_produtos
import cadastro_categorias

# Funções de exemplo
def cadastrar_pessoa():
    cadastro_pessoas.iniciar()
   # messagebox.showinfo("Cadastro", "Cadastro de Pessoa iniciado.")

def cadastrar_produto():
    cadastro_produtos.iniciar()

def abrir_categorias():
    cadastro_categorias.iniciar()

def sair():
    root.quit()

# Janela principal
root = tk.Tk()
root.title("Sistema de Cadastro")
root.geometry("500x300")

# Barra de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Cadastros"
menu_cadastros = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Cadastros", menu=menu_cadastros)

menu_cadastros.add_command(label="Cadastrar Pessoa", command=cadastrar_pessoa)
menu_cadastros.add_command(label="Cadastrar Produto", command=cadastrar_produto)
menu_cadastros.add_command(label="Cadastrar Categoria", command=abrir_categorias)

# Menu "Sair"
menu_bar.add_command(label="Sair", command=sair)

# Loop principal
root.mainloop()