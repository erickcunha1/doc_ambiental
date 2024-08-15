import os
import docx

def gerar_nome_arquivo_unico(base_name, ext, directory):

    counter = 1
    new_path = os.path.join(directory, f"{base_name}{ext}")
    while os.path.exists(new_path):
        new_path = os.path.join(directory, f"{base_name} ({counter}){ext}")
        counter += 1
    return new_path

def substituir_textos_docx(doc_path, substituicoes, output_path):
    
    doc = docx.Document(doc_path)
    
    for paragrafo in doc.paragraphs:
        for texto_a_substituir, novo_texto in substituicoes.items():
            if texto_a_substituir in paragrafo.text:
                paragrafo.text = paragrafo.text.replace(texto_a_substituir, str(novo_texto))
    
    doc.save(output_path)
