def status_bar(current, max_value=255, size=20):
    # Calcula a porcentagem
    percentage = current / max_value
    # Calcula o comprimento da parte preenchida da barra
    filled_length = round(size * percentage)
    # Construa a barra com caracteres "█"
    bar = "█" * filled_length
    # Retorna a barra formatada
    return f"```Fix\n{bar}```"