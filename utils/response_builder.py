def build_response(message, status, data=None, page=None, limit=None, count=None):
    """
    Constrói um objeto de resposta padronizado para os use cases.
    
    Args:
        message (str): Mensagem descritiva da resposta (ex.: "Success").
        status (str): Status da operação (ex.: "success", "error").
        data (any, optional): Dados retornados pela operação.
        page (int, optional): Número da página (para respostas paginadas).
        limit (int, optional): Limite de itens por página (para respostas paginadas).
        count (int, optional): Total de itens (para respostas paginadas).
    
    Returns:
        dict: Objeto de resposta padronizado.
    """
    response = {
        "message": message,
        "status": status,
        "data": data if data is not None else {}
    }
    
    if page is not None:
        response["page"] = page
    if limit is not None:
        response["limit"] = limit
    if count is not None:
        response["count"] = count
        
    return response