import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

def buscar_produto(nome):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root753',
        database='ecommerce'
    )
    cursor = conn.cursor()

    try:
        cursor.callproc('buscar_produto', [nome])
        resultado = []
        for res in cursor.stored_results():
            resultado = res.fetchall()
        return resultado
    finally:
        cursor.close()
        conn.close()

def iniciar():
    def consultar():
        nome = entry_nome.get()

        resultados = buscar_produto(nome)

        for item in tree.get_children():
            tree.delete(item)

        if resultados:
            for linha in resultados:
                tree.insert('', tk.END, values=linha)
        else:
            messagebox.showinfo("Consulta", "Produto não encontrado.")

    janela = tk.Toplevel()
    janela.title("Consultar Produto")
    janela.geometry("700x350")

    tk.Label(janela, text="Nome do Produto:").pack(pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.pack(pady=5)

    tk.Button(janela, text="Consultar", command=consultar).pack(pady=5)

    colunas = ("ID", "Nome", "Preço", "Categoria")

    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(pady=10, fill=tk.BOTH, expand=True)
