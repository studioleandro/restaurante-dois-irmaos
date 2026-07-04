import streamlit as st
import database as db
import whatsapp as wa
import pandas as pd
import os
import imprimir as imp  # <-- Adicione esta linha no topo junto com os outros imports

# Inicializa o Banco de Dados
db.criar_tabelas()

st.set_page_config(page_title="GESTAO DOIS IRMAOS", page_icon="logo.jpg", layout="wide")

st.title("SISTEMA INTELIGENTE DOIS IRMAOS - Gestão Integrada")
# CSS Avançado para o Painel Administrativo - Baseado na Logo 1000017409.png
st.markdown("""
    <style>
    /* Estilização Geral do Painel */
    .stApp { background-color: #fdfdfd; }
    h1, h2, h3 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Cabeçalho Administrativo Premium */
    .admin-header-container { 
        text-align: center; 
        padding: 15px 20px 20px 20px; 
        border-radius: 12px; 
        background-color: #ffffff; 
        color: #1a1a1a; 
        margin-bottom: 30px; 
        border: 2px solid #d4af37;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.12);
    }
    .admin-subtitle { 
        margin: 5px 0 0 0; 
        font-size: 15px; 
        color: #444444; 
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# 🎯 RENDERIZAÇÃO DO TOPO DO PAINEL COM A LOGO (logo.jpg)
with st.container():
    st.markdown("<div class='admin-header-container'>", unsafe_allow_html=True)
    
    # Verifica e carrega a logo na raiz para manter a identidade visual unificada
    if os.path.exists("logo.jpg"):
        col_adm_1, col_adm_2, col_adm_3 = st.columns([1, 1.5, 1])
        with col_adm_2:
            st.image("logo.jpg", use_container_width=True)
    else:
        st.markdown("<div style='font-size: 26px; font-weight: 800; color: #d4af37; text-transform: uppercase;'>🔱 2 Irmãos Restaurante 🔱</div>", unsafe_allow_html=True)
        
    st.markdown("""
            <div class='admin-subtitle'>⚙️ PAINEL DE GESTÃO E CENTRAL DE COMANDOS</div>
        </div>
    """, unsafe_allow_html=True)

# Barra Lateral com Resumo Estatístico rápido
pedidos_dados = db.listar_pedidos()
# 🎯 Versão corrigida aceitando as 7 colunas (incluindo o Endereço!)
df_pedidos_total = pd.DataFrame(
    pedidos_dados, 
    columns=["ID", "Cliente", "Telefone", "Itens", "Total", "Status", "Endereço"]
)

st.sidebar.header("📊 Inteligência e Resumo do Dia")
st.sidebar.write("---")

if not df_pedidos_total.empty:
    # 🧼 Filtragem e Cálculos Dinâmicos de Alta Performance
    pedidos_validos = df_pedidos_total[df_pedidos_total["Status"] != "Cancelado"]
    pedidos_cancelados = df_pedidos_total[df_pedidos_total["Status"] == "Cancelado"]
    
    total_pedidos = len(df_pedidos_total)
    total_validos = len(pedidos_validos)
    total_cancelados = len(pedidos_cancelados)
    
    faturamento = pedidos_validos["Total"].sum()
    ticket_medio = faturamento / total_validos if total_validos > 0 else 0.0
    taxa_cancelamento = (total_cancelados / total_pedidos) * 100 if total_pedidos > 0 else 0.0

    # 1. Métrica de Faturamento Bruto (Destaque Principal)
    st.sidebar.metric(
        label="💰 Faturamento Líquido", 
        value=f"R$ {faturamento:.2f}",
        help="Soma total de todos os pedidos do dia, desconsiderando os cancelados."
    )
    
    # 2. Métrica de Volume de Pedidos
    st.sidebar.metric(
        label="📦 Pedidos Confirmados", 
        value=f"{total_validos} un", 
        delta=f"{total_pedidos} totais gerados",
        delta_color="normal"
    )
    
    # 3. Métrica de Ticket Médio (Crucial para Restaurantes!)
    st.sidebar.metric(
        label="🍽️ Ticket Médio por Prato", 
        value=f"R$ {ticket_medio:.2f}",
        help="Valor médio gasto por cada cliente em pedidos confirmados."
    )
    
    st.sidebar.write("---")
    st.sidebar.caption("⚠️ **Indicadores de Perda**")
    
    # 4. Monitoramento de Cancelamentos
    col_sid1, col_sid2 = st.sidebar.columns(2)
    with col_sid1:
        st.sidebar.metric(
            label="❌ Cancelados", 
            value=f"{total_cancelados}",
            delta_color="inverse"
        )
    with col_sid2:
        st.sidebar.metric(
            label="📉 Taxa Erro", 
            value=f"{taxa_cancelamento:.1f}%",
            help="Porcentagem de pedidos que foram perdidos por cancelamento hoje."
        )
        
else:
    # Estado Vazio Elegante (Início do expediente)
    st.sidebar.metric(label="💰 Faturamento Líquido", value="R$ 0,00")
    st.sidebar.metric(label="📦 Pedidos Confirmados", value="0 un")
    st.sidebar.metric(label="🍽️ Ticket Médio por Prato", value="R$ 0,00")
    st.sidebar.write("---")
    st.sidebar.info("🏪 Aguardando as primeiras vendas para calcular os indicadores em tempo real.")
# Organização por Abas Profissionais
aba_PDV, aba_pedidos, aba_produtos = st.tabs(["🛒 Caixa / Novo Pedido", "📋 Painel de Controle (Pedidos)", "📦 Cardápio & Produtos"])

# --- ABA 1: CAIXA / NOVO PEDIDO ---
with aba_PDV:
    st.header("🛒 Lançar Novo Pedido")
    col1, col2 = st.columns(2)
    
    produtos_cadastrados = db.listar_produtos()
    lista_nomes_produtos = [f"{p[1]} (R$ {p[2]:.2f})" for p in produtos_cadastrados]
    
    with col1:
        cliente = st.text_input("Nome do Cliente", key="nome_cli")
        telefone = st.text_input("WhatsApp (com DDD)", placeholder="Ex: 19990053317", key="tel_cli")
        # 🎯 NOVO CAMPO: Endereço do Cliente para o Caixa interno
        endereco = st.text_input("Endereço do Cliente", placeholder="Ex: Rua, Número, Bairro", key="end_cli")
        
        # --- FORMA DE PAGAMENTO ---
        forma_pagamento = st.selectbox(
            "Forma de Pagamento", 
            ["PIX", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"]
        )
        
        # Lógica de Troco caso seja Dinheiro
        valor_pago = 0.0
        if forma_pagamento == "Dinheiro":
            valor_pago = st.number_input("Valor entregue pelo Cliente (R$)", min_value=0.0, format="%.2f")
        
    with col2:
        if lista_nomes_produtos:
            itens_selecionados = st.multiselect("Selecione os Itens do Pedido", lista_nomes_produtos)
        else:
            st.warning("Cadastre produtos na aba de Estoque primeiro!")
            itens_selecionados = []
            
        observacoes = st.text_input("Observações (Ex: Sem cebola)")

        # Cálculo dinâmico em tempo real na tela para te ajudar no caixa
        total_calculado = 0.0
        for item in itens_selecionados:
            total_calculado += float(item.split(" (R$ ")[1].replace(")", ""))
            
        if forma_pagamento == "Dinheiro" and valor_pago > total_calculado:
            troco = valor_pago - total_calculado
            st.metric(label="💵 Troco a devolver:", value=f"R$ {troco:.2f}")
        elif forma_pagamento == "Dinheiro" and valor_pago < total_calculado and valor_pago > 0:
            st.warning("⚠️ Valor pago é menor que o total do pedido!")

    if st.button("Finalizar e Emitir Pedido", type="primary"):
        # 🎯 AJUSTE DE VALIDAÇÃO: Agora também exige o endereço preenchido
        if cliente and telefone and endereco and itens_selecionados:
            # Calcular valor total e estruturar itens
            total_pedido = 0.0
            texto_itens = ""
            for item in itens_selecionados:
                nome_p = item.split(" (R$ ")[0]
                preco_p = float(item.split(" (R$ ")[1].replace(")", ""))
                total_pedido += preco_p
                texto_itens += f"- {nome_p}\n"
            
            # --- CONFIGURAÇÃO AVANÇADA DE PAGAMENTO E TROCO ---
            troco_calculado = 0.0
            if forma_pagamento == "Dinheiro" and valor_pago > total_pedido:
                troco_calculado = valor_pago - total_pedido

            # Estrutura os dados de entrega e pagamento de forma organizada para a impressão
            dados_pagamento = f"ENDEREÇO: {endereco.upper()}\n"
            dados_pagamento += f"PAGTO: {forma_pagamento.upper()}"
            if forma_pagamento == "Dinheiro":
                dados_pagamento += f"\nPAGO:   R${valor_pago:.2f}\nTROCO:  R${troco_calculado:.2f}"
            
            # Junta as observações do cliente (se houver) com os dados novos
            if observacoes:
                obs_final = f"OBS: {observacoes.strip()}\n------------------------\n{dados_pagamento}"
            else:
                obs_final = dados_pagamento

            # Salva no Banco de Dados combinando itens e os detalhes de entrega
            db.salvar_pedido(cliente, telefone, texto_itens, total_pedido)
            
            # --- FUNÇÃO DE IMPRESSÃO ---
            # Enviamos a obs_final completa contendo o Endereço, Forma de Pagamento e Troco!
            sucesso_impressao = imp.imprimir_cupom_profissional(cliente, telefone, texto_itens, total_pedido, obs_final)
            
            if sucesso_impressao:
                st.success(f"Pedido de R$ {total_pedido:.2f} registrado e IMPRESSO com sucesso! 🎉")
            else:
                st.warning(f"Pedido registrado, mas houve uma falha na impressora. Verifique a conexão.")
                
            st.rerun()
        else:
            st.error("⚠️ Preencha todos os campos: Nome, WhatsApp, Endereço e selecione pelo menos 1 item.")
# --- ABA 2: PAINEL DE CONTROLE DE PEDIDOS ---
with aba_pedidos:
    st.header("📋 Gestão de Pedidos em Tempo Real")
    
    pedidos = db.listar_pedidos()
    if not pedidos:
        st.info("Nenhum pedido realizado hoje.")
    else:
        for p in pedidos:
            # 🎯 Versão atualizada para desempacotar as 7 colunas do banco!
            p_id, p_cliente, p_telefone, p_itens, p_total, p_status, p_endereco = p

            # Muda a cor do container baseado no status para efeito visual profissional
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([1, 3, 2, 2])
                
                with c1:
                    st.markdown(f"**#ID: {p_id}**")
                    st.caption(f"Status atual:\n **{p_status}**")
                with c2:
                    st.markdown(f"👤 **{p_cliente}** ({p_telefone})")
                    # 🛵 Mostra o endereço do cliente logo abaixo dos itens na tela de gestão
                    st.text(f"Itens:\n{p_itens}")
                    if p_endereco:
                        st.markdown(f"📍 **Endereço:** {p_endereco}")
                with c3:
                    st.markdown(f"💰 **Total: R$ {p_total:.2f}**")
                with c4:
        # (O restante do seu código selectbox e mudança de status continua igual abaixo...)
                    # 🎯 LISTA ATUALIZADA COM 'Impresso' INCLUSO
                    status_opcoes = ["Pendente", "Impresso", "Em Preparo", "Saiu para Entrega", "Entregue", "Cancelado"]
                    
                    # 🛡️ PROTEÇÃO: Garante que se o status atual não estiver na lista (ou for 'Impresso'), o sistema não quebra
                    if p_status in status_opcoes:
                        status_index = status_opcoes.index(p_status)
                    else:
                        status_index = 0  # Joga para 'Pendente' como padrão de segurança caso venha algo estranho
                    
                    novo_status = st.selectbox(
                        "Mudar Status", 
                        status_opcoes, 
                        index=status_index,
                        key=f"status_{p_id}"
                    )
                    
                    if novo_status != p_status:
                        db.atualizar_status_pedido(p_id, novo_status)
                        # Dispara a mensagem no WhatsApp de acordo com o novo status mudado
                        wa.enviar_notificacao_pedido(p_telefone, p_cliente, p_itens, p_total, novo_status)
                        st.toast(f"Pedido #{p_id} atualizado e Notificação enviada!")
                        st.rerun()
# --- ABA 3: CARDÁPIO & PRODUTOS ---
# --- ABA 3: CARDÁPIO & PRODUTOS ---
with aba_produtos:
    st.header("📦 Gerenciar Cardápio")
    st.caption("Adicione ou remova itens. O cardápio dos clientes atualiza instantaneamente! ⚡")
    
    col_cad1, col_cad2 = st.columns([1, 1.8])
    
    with col_cad1:
        st.subheader("➕ Adicionar Item")
        
        nome_prod = st.text_input("Nome do Prato/Bebida", placeholder="Ex: Marmitex Executiva G", key="cadastro_nome")
        
        # 🎯 NOVO CAMPO: Descrição detalhada do prato para o cliente ver no cardapio.py
        desc_prod = st.text_area("Descrição do Prato", placeholder="Ex: Acompanha arroz, feijão, batata frita, farofa e carne assada.", key="cadastro_desc")
        
        preco_prod = st.number_input("Preço de Venda (R$)", min_value=0.0, format="%.2f", key="cadastro_preco")
        cat_prod = st.selectbox("Categoria", ["Marmitex", "Bebidas", "Sobremesas", "Porções"], key="cadastro_cat")
        
        if st.button("💾 Salvar no Cardápio", type="primary"):
            if nome_prod.strip() and preco_prod > 0:
                # Salva no banco incluindo a descrição digitada
                # Certifique-se de atualizar sua função no 'db' para aceitar a descrição!
                db.salvar_produto(nome_prod.strip(), preco_prod, cat_prod, desc_prod.strip())
                st.success(f"**{nome_prod}** adicionado com sucesso! 🎉")
                
                # Força a atualização da tela em tempo real
                st.rerun()
            else:
                st.error("⚠️ Preencha o nome e um valor maior que R$ 0,00.")
                
    with col_cad2:
        st.subheader("📋 Itens Cadastrados no Sistema")
        produtos = db.listar_produtos()
        
        if produtos:
            # Ajuste os nomes das colunas dependendo de como os dados retornam do seu db.listar_produtos()
            # Se retornar ID, Nome, Preço, Categoria, Descrição:
            try:
                df_prod = pd.DataFrame(produtos, columns=["ID", "Nome", "Preço (R$)", "Categoria", "Descrição"])
            except ValueError:
                # Caso seu banco ainda não retorne a descrição na listagem, ele usa o padrão antigo para não quebrar:
                df_prod = pd.DataFrame(produtos, columns=["ID", "Nome", "Preço (R$)", "Categoria"])
            
            # Filtro rápido por categoria
            categoria_filtro = st.tabs(["Todos", "Marmitex", "Bebidas", "Sobremesas", "Porções"])
            
            with categoria_filtro[0]:
                st.dataframe(df_prod, use_container_width=True, hide_index=True)
            with categoria_filtro[1]:
                st.dataframe(df_prod[df_prod["Categoria"] == "Marmitex"], use_container_width=True, hide_index=True)
            with categoria_filtro[2]:
                st.dataframe(df_prod[df_prod["Categoria"] == "Bebidas"], use_container_width=True, hide_index=True)
            with categoria_filtro[3]:
                st.dataframe(df_prod[df_prod["Categoria"] == "Sobremesas"], use_container_width=True, hide_index=True)
            with categoria_filtro[4]:
                st.dataframe(df_prod[df_prod["Categoria"] == "Porções"], use_container_width=True, hide_index=True)
            
            st.divider()
            
            # --- BLOCO: EXCLUIR PRODUTO ---
            st.markdown("### 🗑️ Remover Item do Cardápio")
            
            opcoes_excluir = [f"{p[0]} - {p[1]} ({p[3]})" for p in produtos]
            item_selecionado = st.selectbox("Selecione o produto para deletar:", opcoes_excluir, key="deletar_item_sel")
            
            id_para_excluir = int(item_selecionado.split(" - ")[0])
            nome_para_excluir = item_selecionado.split(" - ")[1]
            
            if st.button("❌ Confirmar Exclusão", type="secondary"):
                try:
                    db.excluir_produto(id_para_excluir)
                    st.success(f"**{nome_para_excluir}** foi removido com sucesso! 💥")
                    st.rerun()
                except AttributeError:
                    st.error("Erro: A função 'excluir_produto(id)' não foi encontrada no seu arquivo de banco de dados (db).")
        else:
            st.info("Nenhum produto cadastrado no cardápio.")