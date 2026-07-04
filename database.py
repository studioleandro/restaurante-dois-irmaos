import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Verifica se o Firebase já foi iniciado para não dar erro de duplicação
if not firebase_admin._apps:
    # Se estiver rodando na internet (Streamlit Cloud), usa os Secrets
    if "firebase" in st.secrets:
        secret_json = json.loads(st.secrets["firebase"]["json"])
        cred = credentials.Certificate(secret_json)
    # Se estiver rodando no seu computador local, usa o arquivo .json
    else:
        cred = credentials.Certificate("firebase_credentials.json")
        
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ========================================================
# 📦 FUNÇÕES PARA PRODUTOS (FIREBASE)
# ========================================================

def salvar_produto(nome, preco, categoria, descricao=""):
    """🔥 Salva ou atualiza um produto direto na nuvem do Firebase"""
    dados = {
        "nome": nome,
        "preco": float(preco),
        "categoria": categoria,
        "descricao": descricao
    }
    # Cria um novo documento na coleção 'produtos'
    db.collection("produtos").add(dados)

def listar_produtos():
    """🔥 Puxa todos os produtos direto da nuvem em tempo real"""
    produtos = []
    docs = db.collection("produtos").stream()
    for doc in docs:
        p = doc.to_dict()
        # Formatamos igual ao SQLite para não precisar mudar nada no cardapio.py (id, nome, preco, categoria, descricao)
        produtos.append((doc.id, p.get("nome"), p.get("preco"), p.get("categoria"), p.get("descricao", "")))
    return produtos

def excluir_produto(produto_id):
    """❌ Remove o produto usando o ID único gerado pelo Firebase"""
    db.collection("produtos").document(produto_id).delete()

# ========================================================
# 📋 FUNÇÕES PARA PEDIDOS (FIREBASE)
# ========================================================

def salvar_pedido(cliente, telephone, itens, total, status='Pendente', endereco=''):
    """🔥 Salva o pedido na nuvem para a gestão ler instantaneamente"""
    dados = {
        "cliente": cliente,
        "telefone": telephone,
        "itens": itens,
        "total": float(total),
        "status": status,
        "endereco": endereco,
        "data_hora": firestore.SERVER_TIMESTAMP # Organiza por ordem de chegada
    }
    db.collection("pedidos").add(dados)

def listar_pedidos():
    """🔥 Lista todos os pedidos ordenados pelos mais recentes"""
    pedidos = []
    # Busca os pedidos ordenando pela data/hora que foram criados
    docs = db.collection("pedidos").order_by("data_hora", direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        p = doc.to_dict()
        pedidos.append((doc.id, p.get("cliente"), p.get("telefone"), p.get("itens"), p.get("total"), p.get("status"), p.get("endereco")))
    return pedidos

def atualizar_status_pedido(pedido_id, novo_status):
    """🔥 Atualiza o status (Ex: De 'Pendente' para 'Em Preparo') na nuvem"""
    db.collection("pedidos").document(pedido_id).update({"status": novo_status})