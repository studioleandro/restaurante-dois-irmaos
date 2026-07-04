import sys
from datetime import datetime

# ☁️ VALIDAÇÃO DE AMBIENTE: Evita que o Streamlit Cloud (Linux) quebre ao iniciar
try:
    import win32print
    import win32ui
    WINDOWS_DISPONIVEL = True
except ImportError:
    WINDOWS_DISPONIVEL = False

def imprimir_cupom_profissional(cliente, telefone, itens, total, observacoes=""):
    """
    Imprime um cupom idêntico ao modelo do iFood TOTALMENTE EM NEGRITO.
    Otimizado para bobinas de 58mm (Estrito em 24 caracteres por linha).
    Seguro para rodar tanto localmente no Windows quanto na Nuvem (Linux).
    """
    
    # Se estiver rodando na nuvem do Streamlit, pula a impressão física e retorna sucesso
    if not WINDOWS_DISPONIVEL:
        print("☁️ Rodando na Nuvem: Pedido registrado no banco com sucesso (impressão local pulada).")
        return True

    try:
        nome_impressora = win32print.GetDefaultPrinter()
        
        hprinter = win32print.OpenPrinter(nome_impressora)
        pdc = win32ui.CreateDC()
        pdc.CreatePrinterDC(nome_impressora)
        
        pdc.StartDoc("Cupom iFood Bold - Dois Irmaos")
        pdc.StartPage()

        # Fonte Courier New com WEIGHT em 700 para ativar o NEGRITO em tudo
        fonte = win32ui.CreateFont({
            "name": "Courier New",  
            "height": 30,           
            "weight": 700,          # <--- AQUI A MÁGICA: 700 deixa TUDO em negrito!
        })
        pdc.SelectObject(fonte)

        linha_y = 10
        espacamento = 32 
        
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Grid estrito de 24 caracteres tudo em letras maiúsculas para destacar ainda mais
        linhas = [
            "========================",
            "      DOIS IRMÃO        ",
            "   * RESTAURANTE * ",
            "========================",
            "     [ENTREGA RAPIDA]   ", 
            "------------------------",
            "PEDIDO EM: " + str(data_hora[:10]),
            "HORÁRIO:      " + str(data_hora[11:]),
            "------------------------",
            "CLIENTE MENSAGEM WA:",
            f"{cliente[:24].upper()}",
            f"TEL: {telefone[:19]}",
            "========================",
            " QTD  ITEM        PREÇO ",
            "------------------------",
        ]

        # Processamento dos itens
        for idx, item in enumerate(itens.split("\n"), start=1):
            if item.strip():
                item_limpo = item.replace("- ", "").replace("*", "").strip().upper()
                
                if "R$" in item_limpo:
                    partes = item_limpo.split("R$")
                    nome_produto = partes[0].strip()
                    preco_texto = f"R${partes[1].strip()}"
                else:
                    nome_produto = item_limpo
                    preco_texto = ""

                prefixo_item = f"{idx:02d} 1x "
                nome_formatado = f"{prefixo_item}{nome_produto}"

                if preco_texto:
                    if len(nome_formatado) > 16:
                        linhas.append(nome_formatado[:16])
                        resto = nome_formatado[16:30]
                        linhas.append(f"{resto:<16}{preco_texto:>8}")
                    else:
                        linhas.append(f"{nome_formatado:<16}{preco_texto:>8}")
                else:
                    for i in range(0, len(nome_formatado), 24):
                        linhas.append(nome_formatado[i:i+24])

        # Bloco de Observações
        if observacoes:
            linhas.extend([
                "------------------------",
                "  OBS. DO CLIENTE:      ",
                "------------------------"
            ])
            obs_texto = observacoes.replace("*", "").strip().upper()
            for i in range(0, len(obs_texto), 24):
                linhas.append(f"-> {obs_texto[i:i+21]}")
                
        # Fechamento do Cupom iFood
        str_total = f"R${total:.2f}"
        linhas.extend([
            "========================",
            "RESUMO DOS VALORES:     ",
            f"SUBTOTAL:       {str_total:>8}",
            "TAXA ENTREGA:    R$0,00 ",
            "------------------------",
            f"TOTAL GERAL:    {str_total:>8}",
            "========================",
            "  * PAGO VIA WHATSAPP * ",
            "========================",
            "   DOIS IRMÃOS RESTAURANTE  ",
            "   IMPRESSO COM SUCESSO ",
            "\n\n\n\n\n" 
        ])

        # Envia para a impressora
        for texto in linhas:
            pdc.TextOut(2, linha_y, texto) 
            linha_y += espacamento

        pdc.EndPage()
        pdc.EndDoc()
        pdc.DeleteDC()
        win32print.ClosePrinter(hprinter)
        return True

    except Exception as e:
        print(f"❌ Erro na impressão iFood Bold: {e}")
        return False