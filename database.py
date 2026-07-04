import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json
import os

# ========================================================
# 🔐 INICIALIZAÇÃO BLINDADA DO FIREBASE
# ========================================================

if not firebase_admin._apps:
    cred = None
    
    # 1. Tenta carregar os segredos se estiver no Streamlit Cloud (Produção)
    if "firebase" in st.secrets:
        try:
            secret_json = json.loads(st.secrets["firebase"]["json"])
            cred = credentials.Certificate(secret_json)
        except Exception as e:
            st.error(f"Erro ao ler as credenciais dos Secrets do Streamlit: {e}")
            
    # 2. Se não estiver na nuvem, busca o arquivo local (No seu PC)
    if cred is None:
        caminho_local = "firebase_credentials.json"
        if os.path.exists(caminho_local):
            cred = credentials.Certificate(caminho_local)
        else:
            st.error(f"⚠️ Erro Crítico: O arquivo '{caminho_local}' não foi encontrado na pasta atual ({os.getcwd()}).")
            st.info("💡 Certifique-se de que o arquivo JSON com as chaves do Firebase está na raiz do projeto!")
            st.stop() # Interrompe a execução antes de estourar o erro de conexão

    # Inicializa o app com a credencial validada
    firebase_admin.initialize_app(cred)

# Instancia o cliente do Firestore
db = firestore.client()

# ========================================================
# 📦 FUNÇÕES PARA PRODUTOS (FIREBASE)
# ========================================================

def salvar_produto(nome, preco, categoria, descricao=""):
    """🔥 Salva um novo produto direto na nuvem do Firebase e retorna o status"""
    try:
        dados = {
            "nome": nome,
            "preco": float(preco),
            "categoria": categoria,
            "descricao": descricao
        }
        # Cria um novo documento na coleção 'produtos'
        db.collection("produtos").add(dados)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar produto no Firebase: {e}")
        return False

def listar_produtos():
    """🔥 Puxa todos os produtos direto da nuvem em tempo real formatado para o front"""
    try:
        produtos = []
        docs = db.collection("produtos").stream()
        for doc in docs:
            p = doc.to_dict()
            # Mantém a tupla idêntica ao SQLite antigo: (id, nome, preco, categoria, descricao)
            produtos.append((
                doc.id, 
                p.get("nome", "Sem Nome"), 
                p.get("preco", 0.0), 
                p.get("categoria", "Marmitex"), 
                p.get("descricao", "")
            ))
        return produtos
    except Exception as e:
        print(f"❌ Erro ao listar produtos do Firebase: {e}")
        return []

def excluir_produto(produto_id):
    """❌ Remove o produto usando o ID único gerado pelo Firebase"""
    try:
        db.collection("produtos").document(produto_id).delete()
        return True
    except Exception as e:
        print(f"❌ Erro ao excluir produto {produto_id}: {e}")
        return False

# ========================================================
# 📋 FUNÇÕES PARA PEDIDOS (FIREBASE)
# ========================================================

def salvar_pedido(cliente, telephone, itens, total, status='Pendente', endereco=''):
    """🔥 Salva o pedido na nuvem para a gestão ler instantaneamente"""
    try:
        dados = {
            "cliente": cliente,
            "telefone": telephone,
            "itens": itens,
            "total": float(total),
            "status": status,
            "endereco": endereco,
            "data_hora": firestore.SERVER_TIMESTAMP # Organiza por ordem de chegada na cozinha
        }
        db.collection("pedidos").add(dados)
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar pedido no Firebase: {e}")
        return False

def listar_pedidos():
    """🔥 Lista todos os pedidos ordenados pelos mais recentes"""
    try:
        pedidos = []
        # Busca os pedidos ordenando pela data/hora que foram criados
        docs = db.collection("pedidos").order_by("data_hora", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            p = doc.to_dict()
            pedidos.append((
                doc.id, 
                p.get("cliente", "Cliente Anônimo"), 
                p.get("telefone", ""), 
                p.get("itens", ""), 
                p.get("total", 0.0), 
                p.get("status", "Pendente"), 
                p.get("endereco", "")
            ))
        return pedidos
    except Exception as e:
        print(f"❌ Erro ao listar pedidos do Firebase: {e}")
        return []

def atualizar_status_pedido(pedido_id, novo_status):
    """🔥 Atualiza o status (Ex: De 'Pendente' para 'Em Preparo') na nuvem"""
    try:
        db.collection("pedidos").document(pedido_id).update({"status": novo_status})
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar status do pedido {pedido_id}: {e}")
        return False