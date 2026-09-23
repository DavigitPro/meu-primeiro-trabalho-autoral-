import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import sqlite3
from datetime import datetime

DB = "darcy_organizado.db"

# =========================
# BANCO DE DADOS
# =========================

def conectar():
    return sqlite3.connect(DB)


def criar_banco():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            categoria TEXT NOT NULL,
            ano INTEGER,
            quantidade INTEGER NOT NULL DEFAULT 1,
            disponiveis INTEGER NOT NULL DEFAULT 1
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            livro_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(livro_id) REFERENCES livros(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS uniformes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            cor TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS solicitacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            uniforme_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
            FOREIGN KEY(uniforme_id) REFERENCES uniformes(id)
        )
    """)

    cur.execute("SELECT COUNT(*) FROM usuarios")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO usuarios (usuario, senha, nome, cargo) VALUES (?, ?, ?, ?)",
            ("aluno", "1234", "Aluno Exemplo", "Aluno")
        )
        cur.execute(
            "INSERT INTO usuarios (usuario, senha, nome, cargo) VALUES (?, ?, ?, ?)",
            ("admin", "admin123", "Administrador", "Administrador")
        )

    cur.execute("SELECT COUNT(*) FROM livros")
    if cur.fetchone()[0] == 0:
        livros = [
            ("Dom Casmurro", "Machado de Assis", "Romance", 1899, 4, 4),
            ("O Cortiço", "Aluísio Azevedo", "Romance", 1890, 3, 3),
            ("Capitães da Areia", "Jorge Amado", "Romance", 1937, 2, 2),
            ("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "Infantil", 1943, 5, 5),
            ("Vidas Secas", "Graciliano Ramos", "Drama", 1938, 2, 2),
            ("Harry Potter e a Pedra Filosofal", "J. K. Rowling", "Fantasia", 1997, 3, 3),
        ]
        cur.executemany(
            """
            INSERT INTO livros
            (titulo, autor, categoria, ano, quantidade, disponiveis)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            livros
        )

    cur.execute("SELECT COUNT(*) FROM uniformes")
    if cur.fetchone()[0] == 0:
        uniformes = [
            ("Camisa", "Azul", "P", 8),
            ("Camisa", "Azul", "M", 14),
            ("Camisa", "Azul", "G", 12),
            ("Camisa", "Azul", "GG", 6),
            ("Short", "Azul", "P", 6),
            ("Short", "Azul", "M", 10),
            ("Short", "Azul", "G", 9),
            ("Short", "Azul", "GG", 5),
            ("Agasalho", "Azul", "M", 7),
            ("Agasalho", "Azul", "G", 5),
        ]
        cur.executemany(
            """
            INSERT INTO uniformes (tipo, cor, tamanho, quantidade)
            VALUES (?, ?, ?, ?)
            """,
            uniformes
        )

    conn.commit()
    conn.close()


# =========================
# CONFIGURAÇÃO DO CUSTOM TKINTER
# =========================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# =========================
# APLICAÇÃO
# =========================

class SistemaEscolar(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.usuario_atual = None

        self.title("Darcy Organizado")
        self.geometry("1050x680")
        self.minsize(900, 620)
        self.configure(fg_color="#F4F7FB")

        self.configurar_treeview()
        self.mostrar_login()

    def configurar_treeview(self):
        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            rowheight=34,
            font=("Segoe UI", 10),
            background="white",
            fieldbackground="white",
            foreground="#1F2937"
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#EAF1FF",
            foreground="#1E3A8A"
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCE8FF")],
            foreground=[("selected", "#1E3A8A")]
        )

    def limpar(self):
        for widget in self.winfo_children():
            widget.destroy()

    def criar_botao(
        self,
        parent,
        texto,
        comando,
        cor="#2563EB",
        largura=18,
        altura=40
    ):
        return ctk.CTkButton(
            parent,
            text=texto,
            command=comando,
            fg_color=cor,
            hover_color=self.cor_hover(cor),
            text_color="white",
            font=("Segoe UI", 10, "bold"),
            width=largura * 8,
            height=altura,
            corner_radius=8,
            cursor="hand2"
        )

    def cor_hover(self, cor):
        mapa = {
            "#2563EB": "#1D4ED8",
            "#16A34A": "#15803D",
            "#64748B": "#475569",
            "#DC2626": "#B91C1C",
            "#1E3A8A": "#172554",
            "#475569": "#334155"
        }
        return mapa.get(cor, cor)

    # =========================
    # LOGIN
    # =========================

    def mostrar_login(self):
        self.limpar()

        fundo = ctk.CTkFrame(
            self,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        fundo.pack(fill="both", expand=True)

        esquerda = ctk.CTkFrame(
            fundo,
            fg_color="#1E3A8A",
            width=430,
            corner_radius=0
        )
        esquerda.pack(side="left", fill="y")
        esquerda.pack_propagate(False)

        ctk.CTkLabel(
            esquerda,
            text="📚",
            font=("Segoe UI Emoji", 64),
            text_color="white"
        ).pack(pady=(105, 15))

        ctk.CTkLabel(
            esquerda,
            text="DARCY ORGANIZADO",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).pack()

        ctk.CTkLabel(
            esquerda,
            text="Biblioteca e Uniformes Escolares",
            font=("Segoe UI", 12),
            text_color="#DCE8FF"
        ).pack(pady=8)

        ctk.CTkLabel(
            esquerda,
            text="Um sistema simples para facilitar a\nvida dos alunos e da escola.",
            font=("Segoe UI", 11),
            text_color="#DCE8FF",
            justify="center"
        ).pack(pady=20)

        direita = ctk.CTkFrame(
            fundo,
            fg_color="white",
            corner_radius=0
        )
        direita.pack(side="left", fill="both", expand=True)

        card = ctk.CTkFrame(
            direita,
            fg_color="white",
            corner_radius=0,
            width=390
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text="Bem-vindo!",
            font=("Segoe UI", 25, "bold"),
            text_color="#1F2937"
        ).pack(anchor="w")

        ctk.CTkLabel(
            card,
            text="Entre para acessar o sistema.",
            font=("Segoe UI", 11),
            text_color="#6B7280"
        ).pack(anchor="w", pady=(3, 25))

        ctk.CTkLabel(
            card,
            text="Usuário",
            font=("Segoe UI", 10, "bold"),
            text_color="#374151"
        ).pack(anchor="w")

        self.entrada_usuario = ctk.CTkEntry(
            card,
            width=390,
            height=42,
            font=("Segoe UI", 12),
            border_width=1,
            border_color="#D1D5DB",
            fg_color="white",
            text_color="#1F2937",
            corner_radius=7
        )
        self.entrada_usuario.pack(pady=(5, 16))

        ctk.CTkLabel(
            card,
            text="Senha",
            font=("Segoe UI", 10, "bold"),
            text_color="#374151"
        ).pack(anchor="w")

        self.entrada_senha = ctk.CTkEntry(
            card,
            width=390,
            height=42,
            font=("Segoe UI", 12),
            show="*",
            border_width=1,
            border_color="#D1D5DB",
            fg_color="white",
            text_color="#1F2937",
            corner_radius=7
        )
        self.entrada_senha.pack(pady=(5, 20))

        self.criar_botao(
            card,
            "ENTRAR",
            self.entrar,
            "#2563EB",
            20,
            44
        ).pack(fill="x")

        ctk.CTkLabel(
            card,
            text="Aluno: aluno / 1234    •    Admin: admin / admin123",
            font=("Segoe UI", 9),
            text_color="#9CA3AF"
        ).pack(pady=18)

        self.entrada_usuario.focus_set()
        self.entrada_senha.bind("<Return>", lambda event: self.entrar())

    def entrar(self):
        usuario = self.entrada_usuario.get().strip()
        senha = self.entrada_senha.get().strip()

        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, usuario, nome, cargo
            FROM usuarios
            WHERE usuario = ? AND senha = ?
            """,
            (usuario, senha)
        )

        resultado = cur.fetchone()
        conn.close()

        if resultado:
            self.usuario_atual = {
                "id": resultado[0],
                "usuario": resultado[1],
                "nome": resultado[2],
                "cargo": resultado[3]
            }
            self.mostrar_dashboard()
        else:
            messagebox.showerror(
                "Login",
                "Usuário ou senha incorretos."
            )

    def sair(self):
        self.usuario_atual = None
        self.mostrar_login()

    # =========================
    # LAYOUT PRINCIPAL
    # =========================

    def criar_layout(self, titulo, subtitulo=""):
        self.limpar()

        topo = ctk.CTkFrame(
            self,
            fg_color="#1E3A8A",
            height=68,
            corner_radius=0
        )
        topo.pack(fill="x")
        topo.pack_propagate(False)

        ctk.CTkLabel(
            topo,
            text="📚  DARCY ORGANIZADO",
            text_color="white",
            font=("Segoe UI", 17, "bold")
        ).pack(side="left", padx=25)

        ctk.CTkLabel(
            topo,
            text=f"{self.usuario_atual['nome']}  •  {self.usuario_atual['cargo']}",
            text_color="#DCE8FF",
            font=("Segoe UI", 10, "bold")
        ).pack(side="right", padx=20)

        corpo = ctk.CTkFrame(
            self,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        corpo.pack(fill="both", expand=True)

        menu = ctk.CTkFrame(
            corpo,
            fg_color="white",
            width=210,
            corner_radius=0
        )
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        ctk.CTkLabel(
            menu,
            text="MENU",
            text_color="#9CA3AF",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(22, 8))

        self.menu_botao(menu, "🏠  Início", self.mostrar_dashboard)
        self.menu_botao(menu, "📚  Biblioteca", self.mostrar_biblioteca)
        self.menu_botao(menu, "📋  Minhas Reservas", self.mostrar_reservas)
        self.menu_botao(menu, "👕  Uniformes", self.mostrar_uniformes)
        self.menu_botao(menu, "📦  Minhas Solicitações", self.mostrar_solicitacoes)

        if self.usuario_atual["cargo"] == "Administrador":
            ctk.CTkLabel(
                menu,
                text="ADMINISTRAÇÃO",
                text_color="#9CA3AF",
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w", padx=18, pady=(22, 8))

            self.menu_botao(
                menu,
                "⚙  Painel Admin",
                self.mostrar_admin
            )

        self.criar_botao(
            menu,
            "🚪  Sair",
            self.sair,
            "#64748B",
            12,
            40
        ).pack(side="bottom", padx=15, pady=18, fill="x")

        area = ctk.CTkFrame(
            corpo,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        area.pack(
            side="left",
            fill="both",
            expand=True,
            padx=28,
            pady=25
        )

        ctk.CTkLabel(
            area,
            text=titulo,
            text_color="#1E3A8A",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        if subtitulo:
            ctk.CTkLabel(
                area,
                text=subtitulo,
                text_color="#6B7280",
                font=("Segoe UI", 10)
            ).pack(anchor="w", pady=(3, 20))

        return area

    def menu_botao(self, parent, texto, comando):
        btn = ctk.CTkButton(
            parent,
            text=texto,
            command=comando,
            fg_color="white",
            hover_color="#EAF1FF",
            text_color="#374151",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            height=40,
            corner_radius=7
        )
        btn.pack(fill="x", padx=8, pady=2)

    # =========================
    # DASHBOARD
    # =========================

    def mostrar_dashboard(self):
        area = self.criar_layout(
            f"Olá, {self.usuario_atual['nome'].split()[0]}! 👋",
            "Escolha uma opção para começar."
        )

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM livros")
        total_livros = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(disponiveis), 0) FROM livros")
        disponiveis = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM reservas
            WHERE usuario_id = ? AND status != 'Cancelada'
            """,
            (self.usuario_atual["id"],)
        )
        minhas_reservas = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(*)
            FROM solicitacoes
            WHERE usuario_id = ? AND status != 'Recusada'
            """,
            (self.usuario_atual["id"],)
        )
        minhas_solicitacoes = cur.fetchone()[0]

        conn.close()

        cards = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        cards.pack(fill="x", pady=(5, 22))

        for i in range(4):
            cards.columnconfigure(i, weight=1)

        self.card_info(
            cards, 0, "📚", "LIVROS",
            total_livros, "cadastrados"
        )

        self.card_info(
            cards, 1, "🟢", "DISPONÍVEIS",
            disponiveis, "exemplares"
        )

        self.card_info(
            cards, 2, "📋", "RESERVAS",
            minhas_reservas, "suas reservas"
        )

        self.card_info(
            cards, 3, "👕", "SOLICITAÇÕES",
            minhas_solicitacoes, "de uniformes"
        )

        bloco = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        bloco.pack(fill="both", expand=True)

        bloco.columnconfigure(0, weight=1)
        bloco.columnconfigure(1, weight=1)
        bloco.rowconfigure(0, weight=1)

        self.dashboard_acao(
            bloco, 0, 0, "📚", "Biblioteca",
            "Consulte livros e faça reservas.",
            self.mostrar_biblioteca
        )

        self.dashboard_acao(
            bloco, 0, 1, "👕", "Uniformes",
            "Veja tamanhos, cores e solicite peças.",
            self.mostrar_uniformes
        )

    def card_info(self, parent, coluna, icone, titulo, numero, legenda):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=10,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.grid(
            row=0,
            column=coluna,
            padx=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=icone,
            font=("Segoe UI Emoji", 22),
            text_color="#1F2937"
        ).pack(anchor="w", padx=16, pady=(14, 0))

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color="#6B7280",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(5, 0))

        ctk.CTkLabel(
            card,
            text=str(numero),
            text_color="#111827",
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", padx=16)

        ctk.CTkLabel(
            card,
            text=legenda,
            text_color="#9CA3AF",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16, pady=(0, 14))

    def dashboard_acao(
        self,
        parent,
        linha,
        coluna,
        icone,
        titulo,
        texto,
        comando
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB"
        )
        card.grid(
            row=linha,
            column=coluna,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=icone,
            font=("Segoe UI Emoji", 32),
            text_color="#1F2937"
        ).pack(pady=(30, 8))

        ctk.CTkLabel(
            card,
            text=titulo,
            text_color="#1E3A8A",
            font=("Segoe UI", 15, "bold")
        ).pack()

        ctk.CTkLabel(
            card,
            text=texto,
            text_color="#6B7280",
            font=("Segoe UI", 10),
            justify="center"
        ).pack(pady=8)

        self.criar_botao(
            card,
            "ACESSAR",
            comando,
            "#2563EB",
            16,
            42
        ).pack(pady=(5, 28))

    # =========================
    # BIBLIOTECA
    # =========================

    def mostrar_biblioteca(self):
        area = self.criar_layout(
            "Biblioteca Escolar",
            "Pesquise um livro e faça sua reserva."
        )

        barra = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        barra.pack(fill="x", pady=(0, 15))

        self.busca_livro = ctk.CTkEntry(
            barra,
            placeholder_text="Digite título, autor ou categoria...",
            height=40,
            font=("Segoe UI", 11)
        )
        self.busca_livro.pack(
            side="left",
            fill="x",
            expand=True
        )
        self.busca_livro.bind(
            "<KeyRelease>",
            lambda event: self.carregar_livros()
        )

        self.criar_botao(
            barra,
            "Pesquisar",
            self.carregar_livros,
            "#2563EB",
            12,
            40
        ).pack(side="left", padx=8)

        tabela_frame = ctk.CTkFrame(
            area,
            fg_color="white",
            corner_radius=8
        )
        tabela_frame.pack(fill="both", expand=True)

        colunas = (
            "titulo",
            "autor",
            "categoria",
            "ano",
            "disponiveis"
        )

        self.tabela_livros = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )

        cabecalhos = {
            "titulo": "Título",
            "autor": "Autor",
            "categoria": "Categoria",
            "ano": "Ano",
            "disponiveis": "Disponíveis"
        }

        larguras = {
            "titulo": 270,
            "autor": 210,
            "categoria": 130,
            "ano": 70,
            "disponiveis": 100
        }

        for col in colunas:
            self.tabela_livros.heading(
                col,
                text=cabecalhos[col]
            )
            self.tabela_livros.column(
                col,
                width=larguras[col],
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela_livros.yview
        )

        self.tabela_livros.configure(
            yscrollcommand=scroll.set
        )

        self.tabela_livros.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(side="right", fill="y")

        self.tabela_livros.bind(
            "<Double-1>",
            lambda event: self.reservar_selecionado()
        )

        botoes = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        botoes.pack(fill="x", pady=12)

        self.criar_botao(
            botoes,
            "📖 Reservar livro",
            self.reservar_selecionado,
            "#16A34A",
            18,
            42
        ).pack(side="left")

        ctk.CTkLabel(
            botoes,
            text="Dica: dê duplo clique em um livro para reservar.",
            text_color="#6B7280",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=15)

        self.carregar_livros()

    def carregar_livros(self):
        if not hasattr(self, "tabela_livros"):
            return

        busca = ""

        if hasattr(self, "busca_livro"):
            busca = self.busca_livro.get().strip()

        for item in self.tabela_livros.get_children():
            self.tabela_livros.delete(item)

        conn = conectar()
        cur = conn.cursor()

        if busca:
            cur.execute(
                """
                SELECT id, titulo, autor, categoria, ano, disponiveis
                FROM livros
                WHERE titulo LIKE ?
                   OR autor LIKE ?
                   OR categoria LIKE ?
                ORDER BY titulo
                """,
                (
                    f"%{busca}%",
                    f"%{busca}%",
                    f"%{busca}%"
                )
            )
        else:
            cur.execute(
                """
                SELECT id, titulo, autor, categoria, ano, disponiveis
                FROM livros
                ORDER BY titulo
                """
            )

        registros = cur.fetchall()
        conn.close()

        for registro in registros:
            self.tabela_livros.insert(
                "",
                "end",
                iid=str(registro[0]),
                values=registro[1:]
            )

    def reservar_selecionado(self):
        selecionado = self.tabela_livros.selection()

        if not selecionado:
            messagebox.showwarning(
                "Biblioteca",
                "Selecione um livro primeiro."
            )
            return

        livro_id = int(selecionado[0])

        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            "SELECT titulo, disponiveis FROM livros WHERE id=?",
            (livro_id,)
        )

        livro = cur.fetchone()

        if not livro:
            conn.close()
            return

        titulo, disponiveis = livro

        if disponiveis <= 0:
            conn.close()
            messagebox.showerror(
                "Biblioteca",
                "Esse livro não possui exemplares disponíveis."
            )
            return

        cur.execute(
            """
            SELECT COUNT(*)
            FROM reservas
            WHERE usuario_id=?
              AND livro_id=?
              AND status IN ('Pendente', 'Aprovada')
            """,
            (self.usuario_atual["id"], livro_id)
        )

        ja_reservou = cur.fetchone()[0]

        if ja_reservou:
            conn.close()
            messagebox.showwarning(
                "Biblioteca",
                "Você já possui uma reserva desse livro."
            )
            return

        cur.execute(
            """
            INSERT INTO reservas
            (usuario_id, livro_id, data, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                self.usuario_atual["id"],
                livro_id,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Aprovada"
            )
        )

        cur.execute(
            """
            UPDATE livros
            SET disponiveis = disponiveis - 1
            WHERE id=?
            """,
            (livro_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Reserva",
            f"Livro reservado com sucesso!\n\n{titulo}"
        )

        self.carregar_livros()

    # =========================
    # MINHAS RESERVAS
    # =========================

    def mostrar_reservas(self):
        area = self.criar_layout(
            "Minhas Reservas",
            "Acompanhe os livros que você reservou."
        )

        tabela = ttk.Treeview(
            area,
            columns=("titulo", "autor", "data", "status"),
            show="headings"
        )

        tabela.heading("titulo", text="Livro")
        tabela.heading("autor", text="Autor")
        tabela.heading("data", text="Data")
        tabela.heading("status", text="Status")

        tabela.column("titulo", width=300)
        tabela.column("autor", width=220)
        tabela.column("data", width=150, anchor="center")
        tabela.column("status", width=130, anchor="center")

        tabela.pack(fill="both", expand=True)

        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT l.titulo, l.autor, r.data, r.status
            FROM reservas r
            JOIN livros l ON l.id = r.livro_id
            WHERE r.usuario_id=?
            ORDER BY r.id DESC
            """,
            (self.usuario_atual["id"],)
        )

        registros = cur.fetchall()
        conn.close()

        for registro in registros:
            tabela.insert(
                "",
                "end",
                values=registro
            )

        self.criar_botao(
            area,
            "← Voltar",
            self.mostrar_dashboard,
            "#64748B",
            12,
            40
        ).pack(anchor="w", pady=12)

    # =========================
    # UNIFORMES
    # =========================

    def mostrar_uniformes(self):
        area = self.criar_layout(
            "Uniformes Escolares",
            "Consulte peça, cor, tamanho e quantidade disponível."
        )

        filtros = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        filtros.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            filtros,
            text="Tipo",
            text_color="#374151",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.filtro_tipo = ttk.Combobox(
            filtros,
            values=["Todos", "Camisa", "Short", "Agasalho"],
            state="readonly",
            width=14
        )
        self.filtro_tipo.set("Todos")
        self.filtro_tipo.pack(side="left", padx=(7, 18))

        ctk.CTkLabel(
            filtros,
            text="Tamanho",
            text_color="#374151",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        self.filtro_tamanho = ttk.Combobox(
            filtros,
            values=["Todos", "P", "M", "G", "GG"],
            state="readonly",
            width=10
        )
        self.filtro_tamanho.set("Todos")
        self.filtro_tamanho.pack(side="left", padx=(7, 18))

        self.criar_botao(
            filtros,
            "Filtrar",
            self.carregar_uniformes,
            "#2563EB",
            10,
            40
        ).pack(side="left")

        tabela_frame = ctk.CTkFrame(
            area,
            fg_color="white",
            corner_radius=8
        )
        tabela_frame.pack(fill="both", expand=True)

        colunas = (
            "tipo",
            "cor",
            "tamanho",
            "quantidade"
        )

        self.tabela_uniformes = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )

        for col, texto, largura in [
            ("tipo", "Peça", 250),
            ("cor", "Cor", 160),
            ("tamanho", "Tamanho", 140),
            ("quantidade", "Disponíveis", 160)
        ]:
            self.tabela_uniformes.heading(
                col,
                text=texto
            )
            self.tabela_uniformes.column(
                col,
                width=largura,
                anchor="center"
            )

        scroll = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela_uniformes.yview
        )

        self.tabela_uniformes.configure(
            yscrollcommand=scroll.set
        )

        self.tabela_uniformes.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(side="right", fill="y")

        botoes = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        botoes.pack(fill="x", pady=12)

        self.criar_botao(
            botoes,
            "👕 Solicitar uniforme",
            self.solicitar_uniforme,
            "#16A34A",
            20,
            42
        ).pack(side="left")

        ctk.CTkLabel(
            botoes,
            text="Selecione uma peça para solicitar.",
            text_color="#6B7280",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=15)

        self.carregar_uniformes()

    def carregar_uniformes(self):
        if not hasattr(self, "tabela_uniformes"):
            return

        tipo = self.filtro_tipo.get()
        tamanho = self.filtro_tamanho.get()

        for item in self.tabela_uniformes.get_children():
            self.tabela_uniformes.delete(item)

        conn = conectar()
        cur = conn.cursor()

        consulta = """
            SELECT id, tipo, cor, tamanho, quantidade
            FROM uniformes
            WHERE 1=1
        """

        params = []

        if tipo != "Todos":
            consulta += " AND tipo=?"
            params.append(tipo)

        if tamanho != "Todos":
            consulta += " AND tamanho=?"
            params.append(tamanho)

        consulta += " ORDER BY tipo, tamanho"

        cur.execute(consulta, params)
        registros = cur.fetchall()
        conn.close()

        for registro in registros:
            self.tabela_uniformes.insert(
                "",
                "end",
                iid=str(registro[0]),
                values=registro[1:]
            )

    def solicitar_uniforme(self):
        selecionado = self.tabela_uniformes.selection()

        if not selecionado:
            messagebox.showwarning(
                "Uniformes",
                "Selecione um uniforme primeiro."
            )
            return

        uniforme_id = int(selecionado[0])

        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT tipo, cor, tamanho, quantidade
            FROM uniformes
            WHERE id=?
            """,
            (uniforme_id,)
        )

        uniforme = cur.fetchone()
        conn.close()

        if not uniforme:
            return

        tipo, cor, tamanho, quantidade = uniforme

        if quantidade <= 0:
            messagebox.showerror(
                "Uniformes",
                "Esse tamanho está esgotado."
            )
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Solicitar uniforme")
        janela.geometry("380x320")
        janela.configure(fg_color="white")
        janela.resizable(False, False)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Solicitar Uniforme",
            text_color="#1E3A8A",
            font=("Segoe UI", 19, "bold")
        ).pack(pady=(24, 10))

        ctk.CTkLabel(
            janela,
            text=f"{tipo} • {cor} • tamanho {tamanho}",
            text_color="#4B5563",
            font=("Segoe UI", 11)
        ).pack()

        ctk.CTkLabel(
            janela,
            text=f"Disponíveis: {quantidade}",
            text_color="#16A34A",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=8)

        ctk.CTkLabel(
            janela,
            text="Quantidade",
            text_color="#374151",
            font=("Segoe UI", 10, "bold")
        ).pack()

        quantidade_var = tk.IntVar(value=1)

        seletor = ctk.CTkFrame(
            janela,
            fg_color="white",
            corner_radius=0
        )
        seletor.pack(pady=8)

        def diminuir():
            if quantidade_var.get() > 1:
                quantidade_var.set(quantidade_var.get() - 1)

        def aumentar():
            if quantidade_var.get() < quantidade:
                quantidade_var.set(quantidade_var.get() + 1)

        ctk.CTkButton(
            seletor,
            text="-",
            width=40,
            height=36,
            command=diminuir,
            fg_color="#64748B",
            hover_color="#475569"
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            seletor,
            textvariable=quantidade_var,
            width=50,
            text_color="#111827",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            seletor,
            text="+",
            width=40,
            height=36,
            command=aumentar,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        ).pack(side="left", padx=5)

        def confirmar():
            qtd = quantidade_var.get()

            if qtd < 1 or qtd > quantidade:
                messagebox.showerror(
                    "Uniformes",
                    "Quantidade inválida.",
                    parent=janela
                )
                return

            conn2 = conectar()
            cur2 = conn2.cursor()

            cur2.execute(
                """
                INSERT INTO solicitacoes
                (usuario_id, uniforme_id, quantidade, data, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.usuario_atual["id"],
                    uniforme_id,
                    qtd,
                    datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Pendente"
                )
            )

            cur2.execute(
                """
                UPDATE uniformes
                SET quantidade = quantidade - ?
                WHERE id=?
                """,
                (qtd, uniforme_id)
            )

            conn2.commit()
            conn2.close()

            janela.destroy()

            messagebox.showinfo(
                "Uniformes",
                "Solicitação enviada com sucesso!"
            )

            self.carregar_uniformes()

        botoes = ctk.CTkFrame(
            janela,
            fg_color="white",
            corner_radius=0
        )
        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=janela.destroy,
            fg_color="#64748B",
            hover_color="#475569",
            width=110,
            height=40
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            botoes,
            text="Enviar solicitação",
            command=confirmar,
            fg_color="#16A34A",
            hover_color="#15803D",
            width=160,
            height=40
        ).pack(side="left", padx=5)

    # =========================
    # MINHAS SOLICITAÇÕES
    # =========================

    def mostrar_solicitacoes(self):
        area = self.criar_layout(
            "Minhas Solicitações",
            "Acompanhe seus pedidos de uniformes."
        )

        tabela = ttk.Treeview(
            area,
            columns=(
                "peca",
                "cor",
                "tamanho",
                "quantidade",
                "data",
                "status"
            ),
            show="headings"
        )

        cabecalhos = {
            "peca": "Peça",
            "cor": "Cor",
            "tamanho": "Tamanho",
            "quantidade": "Qtd.",
            "data": "Data",
            "status": "Status"
        }

        for col in tabela["columns"]:
            tabela.heading(
                col,
                text=cabecalhos[col]
            )
            tabela.column(
                col,
                width=120,
                anchor="center"
            )

        tabela.pack(fill="both", expand=True)

        conn = conectar()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                u.tipo,
                u.cor,
                u.tamanho,
                s.quantidade,
                s.data,
                s.status
            FROM solicitacoes s
            JOIN uniformes u ON u.id = s.uniforme_id
            WHERE s.usuario_id=?
            ORDER BY s.id DESC
            """,
            (self.usuario_atual["id"],)
        )

        registros = cur.fetchall()
        conn.close()

        for registro in registros:
            tabela.insert(
                "",
                "end",
                values=registro
            )

        self.criar_botao(
            area,
            "← Voltar",
            self.mostrar_dashboard,
            "#64748B",
            12,
            40
        ).pack(anchor="w", pady=12)

    # =========================
    # ADMIN
    # =========================

    def mostrar_admin(self):
        if self.usuario_atual["cargo"] != "Administrador":
            messagebox.showerror(
                "Acesso negado",
                "Somente administradores podem acessar esta área."
            )
            return

        area = self.criar_layout(
            "Painel Administrativo",
            "Visualize o sistema e gerencie dados."
        )

        cards = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        cards.pack(fill="x", pady=10)

        for i in range(3):
            cards.columnconfigure(i, weight=1)

        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM usuarios")
        alunos = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM livros")
        livros = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM reservas WHERE status != 'Cancelada'"
        )
        reservas = cur.fetchone()[0]

        conn.close()

        self.card_info(
            cards, 0,  "USUÁRIOS",
            alunos, "cadastrados"
        )

        self.card_info(
            cards, 1,  "LIVROS",
            livros, "cadastrados"
        )

        self.card_info(
            cards, 2,  "RESERVAS",
            reservas, "ativas"
        )

        acoes = ctk.CTkFrame(
            area,
            fg_color="#F4F7FB",
            corner_radius=0
        )
        acoes.pack(
            fill="both",
            expand=True,
            pady=20
        )

        acoes.columnconfigure(0, weight=1)
        acoes.columnconfigure(1, weight=1)

        self.dashboard_acao(
            acoes,
            0,
            0,
            
            "Livros e reservas",
            "Consulte a biblioteca e acompanhe reservas.",
            self.mostrar_biblioteca
        )

        self.dashboard_acao(
            acoes,
            0,
            1,
            
            "Uniformes",
            "Consulte o estoque de uniformes.",
            self.mostrar_uniformes
        )


# =========================
# INICIAR SISTEMA
# =========================

if __name__ == "__main__":
    criar_banco()
    app = SistemaEscolar()
    app.mainloop()
