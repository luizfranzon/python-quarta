import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
import re
import os
import hashlib
import binascii

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root753",
        database="ecommerce"
    )

def _validar_email(email: str) -> bool:
    padrao = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None


def _hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100_000)
    return f"{binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"


def inserir():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    senha = entry_senha.get()
    dataNascimento = entry_dataNascimento.get()

    if not nome or not email or not senha:
        messagebox.showwarning("Campos obrigatórios", "Preencha Nome, E-mail e Senha.")
        return

    if not _validar_email(email):
        messagebox.showwarning("E-mail inválido", "Informe um e-mail válido.")
        return

    if len(senha) < 6:
        messagebox.showwarning("Senha fraca", "A senha deve ter ao menos 6 caracteres.")
        return

    senha_hash = _hash_senha(senha)

    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO Clientes (nome, `e-mail`, telefone, senha, dataNascimento) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, telefone, senha_hash, dataNascimento if dataNascimento else None)
        )
        conexao.commit()
    except mysql.connector.Error as e:
        if getattr(e, 'errno', None) == 1062:
            messagebox.showerror("E-mail duplicado", "Já existe um cliente cadastrado com este e-mail.")
        else:
            messagebox.showerror("Erro", f"Falha ao inserir: {e}")
    finally:
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
    dataNascimento = entry_dataNascimento.get()

    conexao = conectar()
    cursor = conexao.cursor()
    if senha:
        if not _validar_email(email):
            messagebox.showwarning("E-mail inválido", "Informe um e-mail válido.")
            return
        if len(senha) < 6:
            messagebox.showwarning("Senha fraca", "A senha deve ter ao menos 6 caracteres.")
            return
        senha_hash = _hash_senha(senha)
        cursor.execute(
            "UPDATE Clientes SET nome=%s, `e-mail`=%s, telefone=%s, senha=%s, dataNascimento=%s WHERE idClientes=%s",
            (nome, email, telefone, senha_hash, dataNascimento if dataNascimento else None, id_cliente)
        )
    else:
        cursor.execute(
            "UPDATE Clientes SET nome=%s, `e-mail`=%s, telefone=%s, dataNascimento=%s WHERE idClientes=%s",
            (nome, email, telefone, dataNascimento if dataNascimento else None, id_cliente)
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
    cursor.execute("SELECT idClientes, nome, `e-mail`, telefone, senha, dataNascimento FROM Clientes")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    cursor.close()
    conexao.close()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_dataNascimento.delete(0, tk.END)

def iniciar():
    global entry_nome, entry_dataNascimento, entry_email, entry_telefone, tree, entry_senha

    janela = tk.Toplevel()
    janela.title("Cadastro de clientes")
    janela.geometry("1024x568")

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
    
    tk.Label(janela, text="Data Nascimento (YYYY-MM-DD)").grid(row=4, column=0, padx=5, pady=5)
    entry_dataNascimento = tk.Entry(janela)
    entry_dataNascimento.grid(row=4, column=1, padx=5, pady=5)

    tk.Button(janela, text="Inserir", command=inserir).grid(row=5, column=0, pady=10)
    tk.Button(janela, text="Atualizar", command=atualizar).grid(row=5, column=1, pady=10)
    tk.Button(janela, text="Remover", command=remover).grid(row=5, column=2, pady=10)

    tree = ttk.Treeview(
        janela,
        columns=("ID", "Nome", "Email", "Telefone", "Senha", "Data"),
        show="headings"
    )
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Email", text="Email")
    tree.heading("Telefone", text="Telefone")
    tree.heading("Senha", text="Senha")
    tree.heading("Data", text="Data Nascimento")
    tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    janela.grid_rowconfigure(5, weight=1)
    janela.grid_columnconfigure(2, weight=1)

    listar()
