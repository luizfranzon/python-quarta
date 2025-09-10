import tkinter as tk
from tkinter import messagebox

# Funções de exemplo
def cadastrar_cliente():
    import cadastro_clientes
    cadastro_clientes.iniciar()

def cadastrar_produto():
    import cadastro_produtos
    cadastro_produtos.iniciar()

def abrir_categorias():
    import cadastro_categorias
    cadastro_categorias.iniciar()

def sair():
    root.quit()

# Janela principal
root = tk.Tk()
root.title("Sistema de Comércio")
root.geometry("800x600")

# Barra de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Cadastros"
menu_cadastros = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Cadastros", menu=menu_cadastros)
menu_cadastros.add_command(label="Cadastrar Cliente", command=cadastrar_cliente)
menu_cadastros.add_command(label="Cadastrar Produto", command=cadastrar_produto)
menu_cadastros.add_command(label="Cadastrar Categoria", command=abrir_categorias)

# Menu "Sair"
menu_bar.add_command(label="Sair", command=sair)

# Loop principal
root.mainloop()
