import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root753",
        database="ecommerce",
    )

def carregar_categorias():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT idCategoria, nome FROM Categoria")
    categorias = cursor.fetchall()
    cursor.close()
    conexao.close()
    return categorias

def inserir_produto():
    nome = entry_nome.get()
    preco = entry_preco.get()
    categoria = combo_categoria.get()
    descricao = entry_descricao.get()

    if not nome or not preco or not categoria:
        messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
        return

    try:
        preco = float(preco)
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido.")
        return

    categoria_id = dict_categorias.get(categoria)
    if not categoria_id:
        messagebox.showerror("Erro", "Categoria inválida.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO Produtos (nome, descricao, preco, Categoria_idCategoria) VALUES (%s, %s, %s, %s)",
        (nome, descricao, preco, categoria_id)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    listar()
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    combo_categoria.set("")
    messagebox.showinfo("Sucesso", "Produto cadastrado.")

def listar():
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT p.idProdutos, p.nome, p.descricao, p.preco, c.nome
        FROM Produtos p
        JOIN Categoria c ON p.Categoria_idCategoria = c.idCategoria
        WHERE IFNULL(p.ativo, 1) = 1
        ORDER BY p.idProdutos DESC
        """
    )
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
def preencher_campos(event=None):
    selecionado = tree.selection()
    if not selecionado:
        return
    valores = tree.item(selecionado[0], 'values')
    pid, nome, descricao, preco, categoria = valores
    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, nome)
    entry_descricao.delete(0, tk.END)
    entry_descricao.insert(0, descricao)
    entry_preco.delete(0, tk.END)
    entry_preco.insert(0, str(preco))
    combo_categoria.set(categoria)


def atualizar_produto():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um produto na lista.")
        return
    valores = tree.item(selecionado[0], 'values')
    produto_id = valores[0]

    nome = entry_nome.get()
    preco = entry_preco.get()
    categoria = combo_categoria.get()
    descricao = entry_descricao.get()

    if not nome or not preco or not categoria:
        messagebox.showwarning("Campos vazios", "Preencha nome, preço e categoria.")
        return
    try:
        preco = float(preco)
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido.")
        return

    categoria_id = dict_categorias.get(categoria)
    if not categoria_id:
        messagebox.showerror("Erro", "Categoria inválida.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE Produtos SET nome=%s, descricao=%s, preco=%s, Categoria_idCategoria=%s WHERE idProdutos=%s",
        (nome, descricao, preco, categoria_id, produto_id)
    )
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    messagebox.showinfo("Atualizado", "Produto atualizado.")


def remover_produto():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione um produto na lista.")
        return
    valores = tree.item(selecionado[0], 'values')
    produto_id = valores[0]

    if messagebox.askyesno("Confirmar", "Deseja remover este produto?"):
        conexao = conectar()
        cursor = conexao.cursor()
        try:
            cursor.execute("UPDATE Produtos SET ativo=0 WHERE idProdutos=%s", (produto_id,))
        except mysql.connector.Error:
            cursor.execute("DELETE FROM Produtos WHERE idProdutos=%s", (produto_id,))
        conexao.commit()
        cursor.close()
        conexao.close()
        listar()
        messagebox.showinfo("Removido", "Produto removido.")


def iniciar():
    global entry_nome, entry_preco, combo_categoria, tree, dict_categorias, entry_descricao

    janela = tk.Toplevel()
    janela.title("Cadastro de Produtos")
    janela.geometry("600x400")

    tk.Label(janela, text="Nome do Produto").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Descrição do Produto").pack()
    entry_descricao = tk.Entry(janela)
    entry_descricao.pack()

    tk.Label(janela, text="Preço").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()

    tk.Label(janela, text="Categoria").pack()
    categorias = carregar_categorias()
    dict_categorias = {nome: id for id, nome in categorias}
    combo_categoria = ttk.Combobox(janela, values=list(dict_categorias.keys()), state="readonly")
    combo_categoria.pack()

    frame_btn = tk.Frame(janela)
    frame_btn.pack(pady=5)
    tk.Button(frame_btn, text="Cadastrar", command=inserir_produto).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Atualizar", command=atualizar_produto).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Remover", command=remover_produto).pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(
        janela,
        columns=("ID", "Nome", "Descrição", "Preço", "Categoria"),
        show="headings"
    )
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Preço", text="Preço")
    tree.heading("Categoria", text="Categoria")
    tree.pack(fill="both", expand=True)
    tree.bind('<<TreeviewSelect>>', preencher_campos)

    listar()
