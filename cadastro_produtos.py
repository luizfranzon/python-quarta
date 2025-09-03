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

def carregar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    conexao.close()
    return categorias

def inserir_produto():
    nome = entry_nome.get()
    preco = entry_preco.get()
    categoria = combo_categoria.get()

    if not nome or not preco or not categoria:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    try:
        preco = float(preco)
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido.")
        return

    categoria_id = dict_categorias[categoria]

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO produtos (nome, preco, categoria_id) VALUES (%s, %s, %s)",
                   (nome, preco, categoria_id))
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    combo_categoria.set("")
    messagebox.showinfo("Sucesso", "Produto cadastrado.")

def listar():
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT produtos.id, produtos.nome, produtos.preco, categorias.nome
        FROM produtos
        JOIN categorias ON produtos.categoria_id = categorias.id
    """)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    cursor.close()
    conexao.close()

def iniciar():
    global entry_nome, entry_preco, combo_categoria, tree, dict_categorias

    janela = tk.Toplevel()
    janela.title("Cadastro de Produtos")
    janela.geometry("600x400")

    tk.Label(janela, text="Nome do Produto").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Preço").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()

    tk.Label(janela, text="Categoria").pack()
    categorias = carregar_categorias()
    dict_categorias = {nome: id for id, nome in categorias}
    combo_categoria = ttk.Combobox(janela, values=list(dict_categorias.keys()))
    combo_categoria.pack()

    tk.Button(janela, text="Cadastrar", command=inserir_produto).pack(pady=5)

    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Preço", "Categoria"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Preço", text="Preço")
    tree.heading("Categoria", text="Categoria")
    tree.pack(fill="both", expand=True)

    listar()