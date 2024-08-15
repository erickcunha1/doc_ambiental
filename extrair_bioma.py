import fitz

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extrair_palavra(arquivo, palavra_referencia, indice):
    documento = fitz.open(arquivo)
    texto_completo = ""
    
    for num_pagina in range(len(documento)):
        pagina = documento.load_page(num_pagina)
        texto_completo += pagina.get_text()

    palavras = texto_completo.split()
    
    try:
        indice_referencia = palavras.index(palavra_referencia)
        palavras_desejadas = []
        
        for i in range(indice):
            palavras_desejadas.append(palavras[indice_referencia + 1 + i])
        
        return ' '.join(palavras_desejadas)
    except (ValueError, IndexError):
        return "Erro: Palavra de referência não encontrada ou índice fora do alcance."