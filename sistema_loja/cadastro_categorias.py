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
    descricao = entry_descricao.get()

    if not nome or not descricao:
        messagebox.showwarning("Atenção", "Informe nome e descrição da categoria.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO Categoria (nome, descricao) VALUES (%s, %s)", (nome, descricao))
    conexao.commit()
    cursor.close()
    conexao.close()
    
    listar()
    entry_nome.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Categoria cadastrada.")

def listar():
    for item in tree.get_children():
        tree.delete(item)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT idCategoria, nome, descricao FROM Categoria ORDER BY idCategoria DESC")
    
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    
    cursor.close()
    conexao.close()


def preencher_campos(event=None):
    selecionado = tree.selection()
    if not selecionado:
        return
    valores = tree.item(selecionado[0], 'values')
    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, valores[1])
    entry_descricao.delete(0, tk.END)
    entry_descricao.insert(0, valores[2])


def atualizar_categoria():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione uma categoria.")
        return
    cat_id = tree.item(selecionado[0], 'values')[0]
    nome = entry_nome.get()
    descricao = entry_descricao.get()
    if not nome:
        messagebox.showwarning("Validação", "Informe o nome da categoria.")
        return
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE Categoria SET nome=%s, descricao=%s WHERE idCategoria=%s", (nome, descricao, cat_id))
    conexao.commit()
    cursor.close()
    conexao.close()
    listar()
    messagebox.showinfo("Atualizado", "Categoria atualizada.")


def remover_categoria():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showwarning("Seleção", "Selecione uma categoria.")
        return
    cat_id = tree.item(selecionado[0], 'values')[0]
    if not messagebox.askyesno("Confirmar", "Deseja remover esta categoria?"):
        return
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM Categoria WHERE idCategoria=%s", (cat_id,))
        conexao.commit()
        messagebox.showinfo("Removida", "Categoria removida.")
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Não foi possível remover. Verifique se há produtos vinculados.\nDetalhes: {e}")
    finally:
        cursor.close()
        conexao.close()
    listar()

def iniciar():
    global entry_nome, tree, entry_descricao

    janela = tk.Toplevel()
    janela.title("Cadastro de Categorias")
    janela.geometry("400x300")

    tk.Label(janela, text="Nome da Categoria").pack()
    entry_nome = tk.Entry(janela)   
    entry_nome.pack()

    tk.Label(janela, text="Descrição da Categoria").pack()
    entry_descricao = tk.Entry(janela)
    entry_descricao.pack()

    frame_btn = tk.Frame(janela)
    frame_btn.pack(pady=5)
    tk.Button(frame_btn, text="Cadastrar", command=inserir_categoria).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Atualizar", command=atualizar_categoria).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Remover", command=remover_categoria).pack(side=tk.LEFT, padx=5)

    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Descrição"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Descrição", text="Descrição")
    tree.pack(fill="both", expand=True)
    tree.bind('<<TreeviewSelect>>', preencher_campos)

    listar()
