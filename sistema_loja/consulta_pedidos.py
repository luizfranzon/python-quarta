import tkinter as tk
from tkinter import ttk
import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root753",
        database="ecommerce",
    )


def iniciar():
    janela = tk.Toplevel()
    janela.title("Consultar Pedidos")
    janela.geometry("900x500")

    cols = ("ID", "Data", "Status", "Total", "Cliente")
    tree = ttk.Treeview(janela, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c)
    tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    cols_it = ("Produto", "Qtd", "Preço Total")
    tree_it = ttk.Treeview(janela, columns=cols_it, show="headings", height=8)
    for c in cols_it:
        tree_it.heading(c, text=c)
    tree_it.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def carregar_pedidos():
        tree.delete(*tree.get_children())
        con = conectar()
        cur = con.cursor()
        cur.execute(
            """
            SELECT p.idPedidos, p.dataPedido, p.status, p.total, c.nome
            FROM Pedidos p
            JOIN Clientes c ON c.idClientes = p.Clientes_idClientes
            ORDER BY p.idPedidos DESC
            """
        )
        for row in cur.fetchall():
            tree.insert('', 'end', values=row)
        cur.close()
        con.close()

    def carregar_itens(_event=None):
        tree_it.delete(*tree_it.get_children())
        sel = tree.selection()
        if not sel:
            return
        pid = tree.item(sel[0], 'values')[0]
        con = conectar()
        cur = con.cursor()
        cur.execute(
            """
            SELECT pr.nome, i.quantidade, i.precoTotal
            FROM ItemPedido i
            JOIN Produtos pr ON pr.idProdutos = i.Produtos_idProdutos
            WHERE i.Pedidos_idPedidos = %s
            """,
            (pid,)
        )
        for row in cur.fetchall():
            tree_it.insert('', 'end', values=row)
        cur.close()
        con.close()

    tree.bind('<<TreeviewSelect>>', carregar_itens)
    carregar_pedidos()
