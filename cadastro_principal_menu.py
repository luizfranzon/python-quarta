import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import os

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

def cadastrar_pedido():
    # Tem que fazer esse:
    import cadastro_pedido
    cadastro_pedido.iniciar()

def consultar_pedidos():
    # Tem que fazer esse tbm:
    import consulta_pedidos
    consulta_pedidos.iniciar()

def consultar_produto():
    import consultar_produto
    consultar_produto.iniciar()

def sair():
    root.quit()

# Janela principal
root = ThemedTk(theme="radiance")
root.title("Sistema de Comércio")
root.geometry("800x600")

# Frame de boas-vindas
frame_welcome = tk.LabelFrame(root, text="Bem-vindo!", padx=20, pady=20)
frame_welcome.pack(padx=30, pady=30, fill="both", expand=True)

label_info = tk.Label(
    frame_welcome,
    text="Selecione uma opção no menu acima para começar.\nSistema de Gestão de Comércio v1.0"
)
label_info.pack()

# Barra de menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Cliente"
menu_cliente = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Cliente", menu=menu_cliente)
menu_cliente.add_command(label="Cadastrar Cliente", command=cadastrar_cliente)

# Menu "Produto"
menu_produto = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Produto", menu=menu_produto)
menu_produto.add_command(label="Cadastrar Produto", command=cadastrar_produto)
menu_produto.add_command(label="Consultar Produto", command=consultar_produto)
menu_produto.add_command(label="Cadastrar Categoria", command=abrir_categorias)

# Menu "Pedido"
menu_pedido = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Pedido", menu=menu_pedido)
menu_pedido.add_command(label="Cadastrar Pedido", command=cadastrar_pedido)
menu_pedido.add_command(label="Consultar Pedidos", command=consultar_pedidos)

# Menu "Sair"
menu_bar.add_command(label="Sair", command=sair)

# Ícone (opcional: verifica se o arquivo existe para evitar erro)
if os.path.exists("logo.ico"):
    root.iconbitmap("logo.ico")

# Loop principal
root.mainloop()
