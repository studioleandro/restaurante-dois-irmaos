import sqlite3

def conectar():
    # 🎯 check_same_thread=False permite que múltiplos clientes acessem o site ao mesmo tempo sem travar
    return sqlite3.connect("restaurante.db", check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # 🎯 Tabela de Produtos (Atualizada com 'descricao')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT,
            descricao TEXT DEFAULT ''
        )
    ''')
    
    # 🎯 Tabela de Pedidos (Atualizada com 'endereco')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            telefone TEXT NOT NULL,
            itens TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Pendente',
            endereco TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    
    # 🛡️ MÁGICA DA CORREÇÃO AUTOMÁTICA (Migração de Banco Seguro)
    # Se o banco já existia antigo no seu computador, esse bloco injeta as colunas que faltam sem quebrar nada!
    try:
        cursor.execute("ALTER TABLE produtos ADD COLUMN descricao TEXT DEFAULT ''")
        conn.commit()
    except sqlite3.OperationalError:
        pass # Se a coluna já existir, ele ignora e não dá erro
        
    try:
        cursor.execute("ALTER TABLE pedidos ADD COLUMN endereco TEXT DEFAULT ''")
        conn.commit()
    except sqlite3.OperationalError:
        pass # Se a coluna já existir, ele ignora e não dá erro

    conn.close()

# ========================================================
# 📦 FUNÇÕES PARA PRODUTOS
# ========================================================

# 🎯 Atualizada com 4 argumentos para aceitar a descrição!
def salvar_produto(nome, preco, categoria, descricao=""):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, preco, categoria, descricao) VALUES (?, ?, ?, ?)", 
        (nome, preco, categoria, descricao)
    )
    conn.commit()
    conn.close()

def listar_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados = cursor.fetchall()
    conn.close()
    return dados

def excluir_produto(produto_id):
    """
    ❌ Remove um produto do cardápio permanentemente usando o ID selecionado.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()

# ========================================================
# 📋 FUNÇÕES PARA PEDIDOS
# ========================================================

# 🎯 Atualizada para salvar também o endereço que criamos no PDV!
def salvar_pedido(cliente, telephone, itens, total, status='Pendente', endereco=''):
    """
    Ajustado para salvar o status e o endereço corretamente!
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pedidos (cliente, telefone, itens, total, status, endereco) VALUES (?, ?, ?, ?, ?, ?)", 
        (cliente, telephone, itens, total, status, endereco)
    )
    conn.commit()
    conn.close()

def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def atualizar_status_pedido(pedido_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    conn.commit()
    conn.close()

# ========================================================
# 🎯 INICIALIZAÇÃO AUTOMÁTICA DE SEGURANÇA
# ========================================================
# Garante que as tabelas nasçam sozinhas assim que o Streamlit abrir na internet!
criar_tabelas()