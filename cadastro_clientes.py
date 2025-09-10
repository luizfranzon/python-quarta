import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Conexão com o banco
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root753",
        database="ecommerce"
    )

# Funções de banco
def inserir():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    senha = entry_senha.get()

    if not nome or not email or not telefone or not senha:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO Clientes (nome, `e-mail`, telefone, senha) VALUES (%s, %s, %s, %s)",
        (nome, email, telefone, senha)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    listar()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Cadastro realizado.")

def atualizar():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um cliente.")
        return

    id_cliente = tree.item(selecionado)["values"][0]
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    senha = entry_senha.get()

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE Clientes SET nome=%s, `e-mail`=%s, telefone=%s, senha=%s WHERE idClientes=%s",
        (nome, email, telefone, senha, id_cliente)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    listar()
    limpar_campos()
    messagebox.showinfo("Atualizado", "Cadastro atualizado.")

def remover():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um cliente.")
        return

    id_cliente = tree.item(selecionado)["values"][0]

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM Clientes WHERE idClientes = %s", (id_cliente,))
    conexao.commit()
    cursor.close()
    conexao.close()

    listar()
    limpar_campos()
    messagebox.showinfo("Removido", "Cadastro removido.")

def listar():
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Clientes")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    cursor.close()
    conexao.close()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

def iniciar():
    global entry_nome, entry_email, entry_telefone, tree, entry_senha

    # Interface
    janela = tk.Toplevel()
    janela.title("Cadastro de clientes")
    janela.geometry("1024x568")

    # Campos
    tk.Label(janela, text="Nome").grid(row=0, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(janela, text="Email").grid(row=1, column=0, padx=5, pady=5)
    entry_email = tk.Entry(janela)
    entry_email.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(janela, text="Telefone").grid(row=2, column=0, padx=5, pady=5)
    entry_telefone = tk.Entry(janela)
    entry_telefone.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(janela, text="Senha").grid(row=3, column=0, padx=5, pady=5)
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.grid(row=3, column=1, padx=5, pady=5)

    # Botões
    tk.Button(janela, text="Inserir", command=inserir).grid(row=4, column=0, pady=10)
    tk.Button(janela, text="Atualizar", command=atualizar).grid(row=4, column=1, pady=10)
    tk.Button(janela, text="Remover", command=remover).grid(row=4, column=2, pady=10)

    # Tabela
    tree = ttk.Treeview(
        janela,
        columns=("ID", "Nome", "Email", "Telefone", "Senha"),
        show="headings"
    )
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Email", text="Email")
    tree.heading("Telefone", text="Telefone")
    tree.heading("Senha", text="Senha")
    tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Expandir tabela ao redimensionar
    janela.grid_rowconfigure(5, weight=1)
    janela.grid_columnconfigure(2, weight=1)

    listar()
