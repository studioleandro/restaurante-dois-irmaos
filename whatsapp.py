import urllib.parse
import webbrowser

def enviar_notificacao_pedido(telefone, cliente, itens, total, status):
    """
    Formata e gera o disparo de mensagem.
    Filtra o número para garantir o formato internacional correto.
    """
    # Remove caracteres especiais do telefone
    telefone_limpo = "".join(filter(str.isdigit, telefone))
    if not telefone_limpo.startswith("55"):
        telefone_limpo = "55" + telefone_limpo

    # Formata o texto com base no status do pedido
    if status == "Em Preparo":
        texto = f"*Olá, {cliente}!* 👋\n\nSeu pedido já foi para a cozinha e está sendo preparado com muito carinho! 🍳\n\n*Detalhes:* \n{itens}\n\n*Total:* R$ {total:.2f}"
    elif status == "Saiu para Entrega":
        texto = f"*Boa notícia, {cliente}!* 🛵\n\nSeu pedido acabou de sair com o nosso entregador. Logo chega aí!"
    else:
        texto = f"Olá {cliente}, seu pedido mudou para o status: *{status}*."

    # Codifica o texto para URL
    texto_url = urllib.parse.quote(texto)
    link_whatsapp = f"https://web.whatsapp.com/send?phone={telefone_limpo}&text={texto_url}"
    
    # Abre no navegador em segundo plano/nova aba de forma nativa
    webbrowser.open(link_whatsapp)