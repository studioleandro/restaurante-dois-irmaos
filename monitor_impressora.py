import time
import database as db  # <--- Aqui dizemos para o Python: "puxe o database.py mas mude o apelido para db"
import imprimir as imp

print("🤖 [NEXUS AUTOMAÇÕES] Sentinela Dois Irmãos Ativo!")
print("Waiting for new orders from the Digital Menu... Press CTRL+C to stop.")

while True:
    try:
        # Pega todos os pedidos do banco de dados
        pedidos = db.listar_pedidos()
        
        if pedidos:
            # O último pedido inserido fica na posição 0 por causa do ORDER BY id DESC
            ultimo_pedido = pedidos[0]
            pedido_id, cliente, telefone, itens, total, status = ultimo_pedido
            
            # Se o status for 'Pendente', significa que veio do cardápio e não foi impresso ainda!
            if status == "Pendente":
                print(f"🔔 NOVO PEDIDO DETECTADO! ID: {pedido_id} - Cliente: {cliente}")
                
                # Envia direto para a sua função iFood Bold de 58mm
                # Como juntamos os itens e as observações no cardápio, passamos as observações vazias
                sucesso = imp.imprimir_cupom_profissional(cliente, telefone, itens, total, observacoes="")
                
                if sucesso:
                    # Atualiza o status para 'Impresso' para o sistema não imprimir o mesmo cupom repetidamente
                    db.atualizar_status_pedido(pedido_id, "Impresso")
                    print(f"🖨️ Cupom do cliente {cliente} impresso com sucesso!")
                else:
                    print(f"❌ Falha ao imprimir pedido {pedido_id}. Verifique a impressora.")
                    
    except Exception as e:
        print(f"Erro no monitoramento: {e}")
        
    time.sleep(3) # Checa o banco de dados a cada 3 segundos sem travar o PC