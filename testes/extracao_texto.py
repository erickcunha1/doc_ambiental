import fitz  # PyMuPDF

def extrair_texto_pdf(pdf_path, txt_path):
    # Abre o arquivo PDF
    pdf_documento = fitz.open(pdf_path)
    
    # Variável para armazenar o texto extraído
    texto_completo = ""
    
    # Itera por todas as páginas do PDF
    for pagina in pdf_documento:
        # Extrai o texto da página atual
        texto_completo += pagina.get_text()
    
    # Salva o texto extraído em um arquivo .txt
    with open(txt_path, 'w', encoding='utf-8') as arquivo_txt:
        arquivo_txt.write(texto_completo)
    
    # Fecha o documento PDF
    pdf_documento.close()
    
    print(f"Texto extraído com sucesso para {txt_path}")

# Exemplo de uso:
pdf_path = "testes/relatorio.pdf"  # Caminho do PDF
txt_path = "testes/saida.txt"    # Caminho de saída para o arquivo .txt
extrair_texto_pdf(pdf_path, txt_path)
