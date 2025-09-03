import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root753",
        database="ecommerce"
    )

def inserir_categoria():
    nome = entry_nome.get()
    if not nome:
        messagebox.showwarning("Atenção", "Informe o nome da categoria.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO categoria (nome) VALUES (%s)", (nome,))
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    entry_nome.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Categoria cadastrada.")

def listar():
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM categoria")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    cursor.close()
    conexao.close()

def iniciar():
    global entry_nome, tree
    janela = tk.Toplevel()
    janela.title("Cadastro de Categorias")
    janela.geometry("400x300")

    tk.Label(janela, text="Nome da Categoria").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Button(janela, text="Cadastrar", command=inserir_categoria).pack(pady=5)

    tree = ttk.Treeview(janela, columns=("ID", "Nome"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.pack(fill="both", expand=True)

    listar()