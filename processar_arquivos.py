import os
import datetime
import logging
from complementares.extrair_bioma import extrair_palavra
from extrair_gpt import criar_tac
from complementares.manipular_documento import substituir_textos_docx, gerar_nome_arquivo_unico
from calculo import realizar_calculo
from complementares.extenso import numero_completo_por_extenso
from complementares.extrair_data import extracao_anos
from complementares.dados_manager import DadosManager 

# Inicializando o gerenciador de dados
dados_manager = DadosManager()

def processar_arquivo_alerta(caminho_arquivo):
    try:
        # Extraindo o bioma do arquivo
        bioma = extrair_palavra(caminho_arquivo, 'BIOMAS', 2)
        bioma = bioma.replace('MUNICÍPIO', '').strip()
        dados_manager.set_bioma(bioma)

        # Extraindo os anos e calculando a diferença em relação ao ano atual
        anos = extracao_anos(caminho_arquivo)
        dados_manager.set_anos(datetime.date.today().year - anos.year)
        print(dados_manager)

        # Log da extração do bioma
        logging.info(f'Bioma extraído: {dados_manager.get_bioma()}')
    except Exception as e:
        logging.error(f'Erro ao processar arquivo de alerta: {str(e)}')

def processar_arquivo_relatorio(caminho_arquivo, caminho_tac_lista):
    for caminho_tac in caminho_tac_lista:
        sucesso = False
        while not sucesso:
            try:
                # Cria o dicionário TAC a partir do caminho do arquivo
                dicionario = criar_tac(caminho_arquivo)

                # Recupera o bioma e a área afetada
                bioma = dados_manager.get_bioma()
                area_afetada = dicionario['$area']

                # Obtém os anos para o cálculo
                n1 = dados_manager.get_anos()

                # Realiza o cálculo do valor baseado no bioma, área e tempo
                valor = realizar_calculo(bioma, area_afetada, n1)
                print(bioma, area_afetada, n1)
                dicionario['$valor'] = valor

                # Transforma o valor em extenso
                numero_extenso = numero_completo_por_extenso(valor)
                dicionario['$extenso'] = numero_extenso

                # Define o caminho de saída e o nome do alerta
                pasta_saida = os.path.dirname(caminho_arquivo)
                inicio = pasta_saida.find("Alerta") + len("Alerta ")
                numeros_alerta = pasta_saida[inicio:inicio + 4]
                output_ext = '.docx'

                # Verifica o tipo de modelo a ser usado
                if 'COMPENSAÇÃO' in caminho_tac:
                    modelo = 'COMPENSAÇÃO'
                else:
                    modelo = 'RECUPERAÇÃO'

                # Define o nome do arquivo de saída baseado no modelo
                output_base_name = f'TAC_{numeros_alerta} - {modelo}'
                output_path = gerar_nome_arquivo_unico(output_base_name, output_ext, pasta_saida)

                # Substitui os textos no documento e gera o arquivo final
                substituir_textos_docx(caminho_tac, dicionario, output_path)
                logging.info(f'Relatório processado e salvo em: {output_path}')

                # Se o processamento for bem-sucedido, define sucesso como True para sair do loop
                sucesso = True

            except Exception as e:
                logging.error(f'Erro ao processar arquivo de relatório {caminho_tac}: {str(e)}')
                # Continua tentando até processar corretamente
                print(f"Tentando novamente o arquivo {caminho_tac} devido ao erro...")


def processar_arquivo(caminho_arquivo, caminho_tac_lista):
    try:
        # Verifica o tipo de arquivo e executa o processamento correspondente
        nome_arquivo = os.path.basename(caminho_arquivo)
        if nome_arquivo.startswith('ANEXO 01'):
            processar_arquivo_alerta(caminho_arquivo)
        elif nome_arquivo.startswith('Relatório'):
            processar_arquivo_relatorio(caminho_arquivo, caminho_tac_lista)
    except Exception as e:
        logging.error(f'Erro ao processar arquivo: {str(e)}')
