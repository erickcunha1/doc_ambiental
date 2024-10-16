import fitz  # PyMuPDF

def extrair_linha_por_referencia(caminho_arquivo_pdf, palavra_referencia, distancia_linha):
    # Abre o arquivo PDF usando o caminho fornecido
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
                # Calcula o índice da linha alvo com a distância fornecida
                indice_alvo = i + distancia_linha
                if 0 <= indice_alvo < len(linhas):
                    return linhas[indice_alvo].strip()  # Retorna a linha encontrada, removendo espaços extras
                else:
                    return "Linha fora do intervalo."
    
        return "Palavra de referência não encontrada."
    
    except ValueError:
        return "Erro ao processar o documento."


# print(extrair_linha_por_referencia('anexo.pdf', '2.4. Requerente do cadastro', 11))