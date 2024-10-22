import os

def verificar_documentos(caminho_pasta):
    """Verifica se em todas as subpastas existem dois documentos: um com 'RECUPERAÇÃO' no nome e outro com 'COMPENSAÇÃO'.
    Informa quais documentos estão faltando, se houver."""
    valor = 0
    for raiz, subpastas, arquivos in os.walk(caminho_pasta):
        for subpasta in subpastas:
            caminho_completo_subpasta = os.path.join(raiz, subpasta)
            arquivos_subpasta = os.listdir(caminho_completo_subpasta)
            
            # Variáveis para verificar se os documentos estão presentes
            tem_recuperacao = any("RECUPERAÇÃO" in arquivo.upper() for arquivo in arquivos_subpasta)
            tem_compensacao = any("COMPENSAÇÃO" in arquivo.upper() for arquivo in arquivos_subpasta)
            
            # Verifica se algum dos documentos está faltando e exibe o resultado
            if not tem_recuperacao or not tem_compensacao:
                valor+=1
                print(f"Verificando pasta: {caminho_completo_subpasta}")
                if not tem_recuperacao:
                    print("Faltando documento com 'RECUPERAÇÃO' no nome.")
                if not tem_compensacao:
                    print("Faltando documento com 'COMPENSAÇÃO' no nome.")
                print("-" * 40)
    print(valor)

# Caminho para a pasta "TESTES NOVOS" na área de trabalho
caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", "TESTES NOVOS")

# Executa a verificação
verificar_documentos(caminho_area_trabalho)
