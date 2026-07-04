import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import database as db  # Puxa o seu arquivo de banco de dados atualizado

# Configuração de Página Única
st.set_page_config(page_title="Dois Irmãos - Delivery", page_icon="🍕", layout="centered")

# --- CSS AVANÇADO ESTILO PREMIUM CLEAN (BASEADO NA LOGO 1000017409.png) ---
st.markdown("""
    <style>
    /* Fundo da aplicação e fontes */
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Cabeçalho Premium Light & Gold */
    .header-container { 
        text-align: center; 
        padding: 10px 20px 25px 20px; 
        border-radius: 12px; 
        background-color: #ffffff; 
        color: #1a1a1a; 
        margin-bottom: 25px; 
        border: 2px solid #d4af37;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.15);
    }
    .header-subtitle { 
        margin: 5px 0 0 0; 
        font-size: 14px; 
        color: #555555; 
        font-weight: 500; 
        font-style: italic;
    }
    .status-loja { 
        color: #ffffff; 
        font-size: 12px; 
        font-weight: bold; 
        margin-top: 10px; 
        display: inline-block; 
        background: #2b9348; /* Verde dinâmico estilo iFood */
        padding: 4px 14px; 
        border-radius: 20px; 
    }
    
    /* Linha do Produto */
    .product-box { padding: 5px 0px; margin-bottom: 5px; }
    .product-title { font-size: 18px; font-weight: bold; color: #1a1a1a; margin-bottom: 2px; }
    .product-desc { font-size: 14px; color: #666666; margin-bottom: 6px; font-weight: 400; line-height: 1.3; }
    .product-price-tag { font-size: 16px; color: #2b9348; font-weight: bold; margin-bottom: 10px; }
    
    /* Sacola */
    .sacola-titulo { color: #1a1a1a; font-size: 20px; font-weight: 700; margin-top: 20px; border-bottom: 2px solid #d4af37; padding-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# 🎯 RENDERIZAÇÃO DO TOPO COM A SUA LOGO LOCAL CENTRALIZADA
with st.container():
    st.markdown("<div class='header-container'>", unsafe_allow_html=True)
    
    if os.path.exists("logo.jpg"):
        col_img_1, col_img_2, col_img_3 = st.columns([1, 1.8, 1])
        with col_img_2:
            st.image("logo.jpg", use_container_width=True)
    else:
        st.markdown("<div style='font-size: 26px; font-weight: 800; color: #d4af37; letter-spacing: 1px; text-transform: uppercase;'>🔱 2 Irmãos Restaurante 🔱</div>", unsafe_allow_html=True)
        
    st.markdown("""
            <div class='header-subtitle'>Marmitex Executiva • Comida Caseira • 10-30 min</div>
            <div class='status-loja'>● ABERTO • ENTREGA GRÁTIS</div>
        </div>
    """, unsafe_allow_html=True)

# Inicializa a sacola/carrinho no Streamlit para não sumir ao recarregar a página
if "carrinho_ifood" not in st.session_state:
    st.session_state.carrinho_ifood = []

# 🎯 BUSCA OS PRODUTOS ATUALIZADOS DIRETO DO BANCO DE DADOS EM TEMPO REAL
produtos_banco = db.listar_produtos()

# Listas vazias dinâmicas para organizar as categorias
pratos_marmitex = []
lista_bebidas = []
lista_sobremesas = []
lista_porcoes = []

# Mapeia e distribui os itens retornados do banco automaticamente
for prod in produtos_banco:
    # Estrutura esperada do banco: (id, nome, preco, categoria, descricao)
    item_formatado = {
        "id": prod[0],
        "nome": prod[1],
        "preco_base": prod[2],
        "desc": prod[4] if len(prod) > 4 else ""
    }
    
    cat = prod[3]
    if cat == "Marmitex":
        pratos_marmitex.append(item_formatado)
    elif cat == "Bebidas":
        lista_bebidas.append(item_formatado)
    elif cat == "Sobremesas":
        lista_sobremesas.append(item_formatado)
    elif cat == "Porções":
        lista_porcoes.append(item_formatado)

# Criando as Abas Dinâmicas do Cardápio baseadas no iFood
aba_marmitex, aba_bebidas = st.tabs(["🍱 Marmitex", "🥤 Bebidas"])

# --- ABA 1: MARMITEX (PUXANDO DO BANCO DE DADOS) ---
with aba_marmitex:
    st.markdown("### 🍱 Escolha sua Marmitex")
    st.write("---")
    
    if pratos_marmitex:
        for idx, prato in enumerate(pratos_marmitex):
            nome_p = prato["nome"]
            desc_p = prato["desc"]
            preco_base = prato["preco_base"]
            p_id = prato["id"]
            
            # Renderização com Design Limpo e Profissional
            st.markdown(f"<div class='product-title'>{nome_p}</div>", unsafe_allow_html=True)
            if desc_p:
                st.markdown(f"<div class='product-desc'>{desc_p}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-price-tag'>R$ {preco_base:.2f}</div>", unsafe_allow_html=True)
            
            with st.expander(f"➕ Selecionar tamanho e adicionar {nome_p}"):
                tamanho = st.radio(
                    "Selecione o tamanho da Marmitex:",
                    ["P (Preço Normal)", "M (+ R$ 4,00)", "G (+ R$ 8,00)"],
                    key=f"tamanho_{p_id}_{idx}"
                )
                
                preco_final = preco_base
                tamanho_texto = "P"
                if "M " in tamanho:
                    preco_final += 4.0
                    tamanho_texto = "M"
                elif "G " in tamanho:
                    preco_final += 8.0
                    tamanho_texto = "G"
                    
                st.write(f"💵 **Valor do prato selecionado:** R$ {preco_final:.2f}")
                
                obs_item = st.text_input(
                    "Alguma observação? (Ex: Sem cebola, sem macarrão, ovo bem passado)",
                    placeholder="Digite aqui...",
                    key=f"obs_item_{p_id}_{idx}"
                )
                
                if st.button("🔴 ADICIONAR À SACOLA", key=f"btn_{p_id}_{idx}", use_container_width=True):
                    st.session_state.carrinho_ifood.append({
                        "nome": f"{nome_p} ({tamanho_texto})",
                        "preco": preco_final,
                        "obs": obs_item.strip()
                    })
                    st.success(f"✅ {nome_p} ({tamanho_texto}) adicionado à sacola!")
                    st.rerun()
            st.write("---")
    else:
        st.info("🏪 Nenhuma opção de Marmitex cadastrada no momento.")

# --- ABA 2: BEBIDAS (PUXANDO DO BANCO DE DADOS) ---
with aba_bebidas:
    st.markdown("### 🥤 Bebidas Geladas")
    st.write("---")
    
    if lista_bebidas:
        for idx_b, bebida in enumerate(lista_bebidas):
            nome_b = bebida["nome"]
            desc_b = bebida["desc"]
            preco_b = bebida["preco_base"]
            b_id = bebida["id"]
            
            st.markdown(f"<div class='product-title'>{nome_b}</div>", unsafe_allow_html=True)
            if desc_b:
                st.markdown(f"<div class='product-desc'>{desc_b}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='product-price-tag'>R$ {preco_b:.2f}</div>", unsafe_allow_html=True)
            
            with st.expander(f"➕ Adicionar {nome_b}"):
                st.write(f"💵 **Valor da unidade:** R$ {preco_b:.2f}")
                
                obs_bebida = st.text_input(
                    "Alguma observação para a bebida? (Opcional)",
                    placeholder="Ex: Mandar bem gelada",
                    key=f"obs_bebida_{b_id}_{idx_b}"
                )
                
                if st.button("🔴 ADICIONAR À SACOLA", key=f"btn_bebida_{b_id}_{idx_b}", use_container_width=True):
                    st.session_state.carrinho_ifood.append({
                        "nome": nome_b,
                        "preco": preco_b,
                        "obs": obs_bebida.strip()
                    })
                    st.success(f"✅ {nome_b} adicionado à sacola!")
                    st.rerun()
            st.write("---")
    else:
        st.info("🏪 Nenhuma bebida cadastrada no momento.")


# --- EXIBIÇÃO DA SACOLA INTELIGENTE IFOOD ---
if st.session_state.carrinho_ifood:
    st.markdown("<div class='sacola-titulo'>🛒 Minha Sacola</div>", unsafe_allow_html=True)
    texto_itens_banco = ""
    total_carrinho = 0.0
    
    for idx, item in enumerate(st.session_state.carrinho_ifood):
        total_carrinho += item['preco']
        
        st.write(f"🔹 **1x {item['nome']}** — <span style='color:green; font-weight:bold;'>R$ {item['preco']:.2f}</span>", unsafe_allow_html=True)
        if item['obs']:
            st.caption(f"💬 Obs: {item['obs']}")
            
        texto_itens_banco += f"1x {item['nome']} R$ {item['preco']:.2f}\n"
        if item['obs']:
            texto_itens_banco += f"   OBS: {item['obs']}\n"
            
    st.metric(label="Total do Pedido", value=f"R$ {total_carrinho:.2f}")
    
    if st.button("🗑️ Limpar Sacola", type="secondary"):
        st.session_state.carrinho_ifood = []
        st.rerun()
        
    st.markdown("### 📍 Dados para Entrega")
    nome_cliente = st.text_input("Nome Completo", key="cli_nome")
    tel_cliente = st.text_input("WhatsApp com DDD", placeholder="Ex: 19990053317", key="cli_tel")
    endereco_cliente = st.text_input("Endereço Completo (Rua, Número, Bairro)", placeholder="Ex: Rua das Flores, 123 - Centro", key="cli_end")
    
    st.markdown("### 💳 Forma de Pagamento")
    forma_pagto = st.selectbox("Selecione como deseja pagar:", ["PIX", "Cartão de Crédito (na entrega)", "Cartão de Débito (na entrega)", "Dinheiro"])
    
    valor_dinheiro = 0.0
    if forma_pagto == "Dinheiro":
        valor_dinheiro = st.number_input("Precisa de troco para quanto?", min_value=0.0, format="%.2f")

    # BOTÃO FINAL DE CONFIRMAÇÃO DO DELIVERY (SALVANDO COMPLETO COM ENDEREÇO)
    if st.button("🔴 FAZER PEDIDO", type="primary", use_container_width=True):
        if nome_cliente and tel_cliente and endereco_cliente:
            
            detalhes_pagto = f"PAGTO: {forma_pagto.upper()}"
            if "DINHEIRO" in forma_pagto.upper() and valor_dinheiro > 0:
                troco = valor_dinheiro - total_carrinho if valor_dinheiro > total_carrinho else 0.0
                detalhes_pagto += f" (PAGO: R${valor_dinheiro:.2f} / TROCO: R${troco:.2f})"
                
            obs_final = f"ENDEREÇO: {endereco_cliente.upper()}\n"
            obs_final += f"------------------------\n{detalhes_pagto}"
            
            texto_com_obs = f"{texto_itens_banco}\n------------------------\n{obs_final}"
            
            # Salva no banco de dados local incluindo o endereço na nova coluna que criamos
            db.salvar_pedido(
                cliente=nome_cliente.strip(), 
                telephone=tel_cliente.strip(), 
                itens=texto_com_obs, 
                total=total_carrinho, 
                status='Pendente', 
                endereco=endereco_cliente.strip()
            )
            
            st.session_state.carrinho_ifood = []
            st.success("✅ Pedido enviado! Seu prato já está em preparo. Acompanhe pelo WhatsApp!")
            st.balloons()
            st.rerun()
        else:
            st.error("⚠️ Atenção: Por favor, preencha o Nome, WhatsApp e Endereço para confirmar seu pedido!")