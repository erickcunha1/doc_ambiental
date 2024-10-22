import os

def excluir_arquivos_comecam_com_tac(caminho_pasta):
    """Exclui todos os arquivos na pasta que começam com 'TAC'."""
    for raiz, subpastas, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            if arquivo.startswith('TAC'):
                caminho_completo = os.path.join(raiz, arquivo)
                try:
                    # Exclui o arquivo
                    os.remove(caminho_completo)
                    print(f"Arquivo excluído: {caminho_completo}")
                except OSError as e:
                    print(f"Erro ao excluir o arquivo: {caminho_completo}, Erro: {e}")

# Caminho para a pasta "TESTES NOVOS" na área de trabalho
caminho_area_trabalho = os.path.join(os.path.expanduser("~"), "Desktop", "TESTES NOVOS")

# Executa a exclusão
excluir_arquivos_comecam_com_tac(caminho_area_trabalho)
