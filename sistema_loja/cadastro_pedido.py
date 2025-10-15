import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root753",
        database="ecommerce",
    )


def carregar_clientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT idClientes, nome FROM Clientes ORDER BY nome")
    dados = cur.fetchall()
    cur.close()
    con.close()
    return dados


def carregar_produtos():
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT p.idProdutos, CONCAT(p.nome, ' (', c.nome, ')'), p.preco FROM Produtos p JOIN Categoria c ON c.idCategoria = p.Categoria_idCategoria WHERE IFNULL(p.ativo,1)=1 ORDER BY p.nome"
    )
    dados = cur.fetchall()
    cur.close()
    con.close()
    return dados


def iniciar():
    janela = tk.Toplevel()
    janela.title("Cadastrar Pedido")
    janela.geometry("800x500")

    tk.Label(janela, text="Cliente").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    clientes = carregar_clientes()
    map_cli = {nome: cid for cid, nome in clientes}
    cb_cliente = ttk.Combobox(janela, values=list(map_cli.keys()), width=40)
    cb_cliente.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    tk.Label(janela, text="Produto").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    produtos = carregar_produtos()
    map_prod = {nome: pid for pid, nome, _preco in produtos}
    map_preco = {pid: float(preco) for pid, _nome, preco in produtos}
    cb_produto = ttk.Combobox(janela, values=list(map_prod.keys()), width=40)
    cb_produto.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    tk.Label(janela, text="Quantidade").grid(row=1, column=2, sticky="e", padx=5, pady=5)
    entry_qtd = tk.Entry(janela, width=8)
    entry_qtd.grid(row=1, column=3, sticky="w", padx=5, pady=5)

    cols = ("ProdutoId", "Produto", "Quantidade")
    tree = ttk.Treeview(janela, columns=cols, show="headings", height=10)
    for c in cols:
        tree.heading(c, text=c)
    tree.column("ProdutoId", width=90)
    tree.column("Quantidade", width=100)
    tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    janela.grid_rowconfigure(2, weight=1)
    janela.grid_columnconfigure(1, weight=1)

    total_var = tk.StringVar(value="0.00")
    tk.Label(janela, text="Total R$").grid(row=3, column=2, sticky="e")
    tk.Label(janela, textvariable=total_var).grid(row=3, column=3, sticky="w")

    def adicionar_item():
        prod_nome = cb_produto.get()
        if prod_nome not in map_prod:
            messagebox.showwarning("Produto", "Selecione um produto.")
            return
        try:
            qtd = int(entry_qtd.get())
            if qtd <= 0:
                raise ValueError
        except Exception:
            messagebox.showwarning("Quantidade", "Informe uma quantidade válida.")
            return

        pid = map_prod[prod_nome]
        for iid in tree.get_children():
            vals = tree.item(iid, 'values')
            if int(vals[0]) == pid:
                nova_qtd = int(vals[2]) + qtd
                tree.item(iid, values=(pid, prod_nome, nova_qtd))
                atualizar_total()
                return

        tree.insert('', 'end', values=(pid, prod_nome, qtd))
        atualizar_total()

    def atualizar_total():
        total_val = 0.0
        for iid in tree.get_children():
            vals = tree.item(iid, 'values')
            pid = int(vals[0])
            qtd = int(vals[2])
            preco = map_preco.get(pid, 0.0)
            total_val += float(preco) * qtd
        total_var.set(f"{total_val:.2f}")

    def remover_item():
        sel = tree.selection()
        if not sel:
            return
        tree.delete(sel[0])
        atualizar_total()

    def salvar_pedido():
        cli_nome = cb_cliente.get()
        if cli_nome not in map_cli:
            messagebox.showwarning("Cliente", "Selecione um cliente.")
            return
        if not tree.get_children():
            messagebox.showwarning("Itens", "Adicione ao menos um item.")
            return

        con = conectar()
        cur = con.cursor()
        try:
            con.start_transaction()
            cliente_id = map_cli[cli_nome]

            total = 0.0
            for iid in tree.get_children():
                pid, _, qtd = tree.item(iid, 'values')
                cur.execute("SELECT preco FROM Produtos WHERE idProdutos=%s", (pid,))
                preco = cur.fetchone()[0]
                total += float(preco) * int(qtd)

            cur.execute(
                "INSERT INTO Pedidos (dataPedido, status, total, Clientes_idClientes) VALUES (%s, %s, %s, %s)",
                (date.today(), 'em processamento', total, cliente_id)
            )
            pedido_id = cur.lastrowid

            for iid in tree.get_children():
                pid, _, qtd = tree.item(iid, 'values')
                cur.execute("SELECT preco FROM Produtos WHERE idProdutos=%s", (pid,))
                preco = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO ItemPedido (quantidade, precoTotal, Pedidos_idPedidos, Produtos_idProdutos) VALUES (%s, %s, %s, %s)",
                    (int(qtd), float(preco) * int(qtd), pedido_id, int(pid))
                )

            con.commit()
            messagebox.showinfo("Sucesso", f"Pedido #{pedido_id} salvo com total R$ {total:.2f}")
            tree.delete(*tree.get_children())
            atualizar_total()
        except Exception as e:
            con.rollback()
            messagebox.showerror("Erro", f"Falha ao salvar pedido: {e}")
        finally:
            cur.close()
            con.close()

    frame_btn = tk.Frame(janela)
    frame_btn.grid(row=4, column=0, columnspan=4, pady=10)
    tk.Button(frame_btn, text="Adicionar Item", command=adicionar_item).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Remover Item", command=remover_item).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btn, text="Salvar Pedido", command=salvar_pedido).pack(side=tk.LEFT, padx=5)
