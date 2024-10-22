import os
import fitz  # PyMuPDF
import re  # Para trabalhar com expressões regulares

def extrair_linha_por_referencia(caminho_arquivo_pdf, palavra_referencia):
    """Extrai o item 10 após uma palavra de referência, ou o item 11 se o item 10 contiver um número.
    Se o item for '- Endereço:', retorna um espaço vazio."""
    # Abre o arquivo PDF
    pdf_documento = fitz.open(caminho_arquivo_pdf)
    
    texto_completo = ""
    
    # Itera por todas as páginas do PDF e extrai o texto completo
    for pagina_num in range(pdf_documento.page_count):
        pagina = pdf_documento.load_page(pagina_num)
        texto_completo += pagina.get_text("text") + "\n"
    
    # Fecha o arquivo PDF
    pdf_documento.close()

    # Divide o texto por quebras de linha
    linhas = texto_completo.splitlines()
    
    try:
        # Encontra o índice da linha que contém a palavra de referência
        for i, linha in enumerate(linhas):
            if palavra_referencia.lower() in linha.lower():
                # Extrai a linha no índice 10 após a referência
                indice_item_10 = i + 10
                indice_item_11 = i + 11

                if 0 <= indice_item_10 < len(linhas):
                    item_10 = linhas[indice_item_10].strip()
                    
                    # Verifica se o item 10 contém um número
                    if re.search(r'\d', item_10):
                        # Se contiver número, pega o item 11
                        if 0 <= indice_item_11 < len(linhas):
                            item_11 = linhas[indice_item_11].strip()
                            # Verifica se o item é '- Endereço:'
                            return "" if item_11 == "- Endereço:" else item_11
                        else:
                            return "Item 11 fora do intervalo."
                    else:
                        # Verifica se o item é '- Endereço:'
                        return "" if item_10 == "- Endereço:" else item_10
                else:
                    return "Item 10 fora do intervalo."
    
        return "Palavra de referência não encontrada."
    
    except ValueError:
        return "Erro ao processar o documento."
    

# def extrair_item_anterior(linha_referencia, pdf_path):
#     """Extrai a segunda linha anterior à linha de referência de um PDF."""
#     # Extrai o texto do PDF
#     # linhas = extrair_texto_pdf(pdf_path)
    
#     # Percorre as linhas para encontrar a linha de referência
#     for i, linha in enumerate(linhas):
#         if linha_referencia in linha:
#             # Verifica se há pelo menos duas linhas antes da linha de referência
#             if i >= 2:
#                 return linhas[i - 2].strip()  # Retorna a segunda linha anterior (removendo espaços em branco)
#             return "Não há linhas suficientes antes da linha de referência."
        
#     return "Linha de referência não encontrada."