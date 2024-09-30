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
from docx import Document
from docx.shared import Pt

# Inicializando o gerenciador de dados
dados_manager = DadosManager()

def substituir_textos_docx(caminho_tac, dicionario, output_path):
    try:
        # Carrega o documento
        doc = Document(caminho_tac)

        # Itera sobre os parágrafos e substitui os textos
        for p in doc.paragraphs:
            for key, value in dicionario.items():
                if key in p.text:
                    # Certifica-se de que o valor seja uma string
                    p.text = p.text.replace(key, str(value))
                    # Define a fonte como Arial
                    for run in p.runs:
                        run.font.name = 'Arial'
                        run.font.size = Pt(12)  # Ajuste o tamanho da fonte conforme necessário

        # Se houver tabelas, itere sobre elas também
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in dicionario.items():
                        if key in cell.text:
                            # Certifica-se de que o valor seja uma string
                            cell.text = cell.text.replace(key, str(value))
                            # Define a fonte como Arial
                            for paragraph in cell.paragraphs:
                                for run in paragraph.runs:
                                    run.font.name = 'Arial'
                                    run.font.size = Pt(12)  # Ajuste o tamanho da fonte conforme necessário

        # Salva o documento modificado
        doc.save(output_path)
    except Exception as e:
        logging.error(f'Erro ao substituir textos no documento: {str(e)}')

def processar_arquivo_alerta(caminho_arquivo):
    try:
        # Extraindo o bioma do arquivo
        bioma = extrair_palavra(caminho_arquivo, 'BIOMAS', 2)
        bioma = bioma.replace('MUNICÍPIO', '').strip()
        dados_manager.set_bioma(bioma)

        # Extraindo a data e calculando a diferença em relação à data atual
        data_extraida = extracao_anos(caminho_arquivo)  # Supondo que esta função retorne uma data completa
        data_atual = datetime.date.today()

        # Calculando a diferença
        anos_diferenca = data_atual.year - data_extraida.year
        meses_diferenca = data_atual.month - data_extraida.month
        dias_diferenca = data_atual.day - data_extraida.day

        # Ajuste se o mês ou dia da data extraída for maior
        if meses_diferenca < 0 or (meses_diferenca == 0 and dias_diferenca < 0):
            anos_diferenca -= 1

        # Corrige o número de meses se necessário
        if meses_diferenca < 0:
            meses_diferenca += 12

        # Calcula a representação decimal dos anos e meses com uma casa decimal
        anos_meses = round(anos_diferenca + (meses_diferenca / 12), 1)
        print(anos_meses)

        # Armazena a representação decimal no gerenciador de dados
        dados_manager.set_anos(anos_meses)

        # Log da extração do bioma e anos calculados
        logging.info(f'Bioma extraído: {dados_manager.get_bioma()}')
        logging.info(f'Diferença em anos e meses: {anos_meses}')
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
                modelo = 'COMPENSAÇÃO' if 'COMPENSAÇÃO' in caminho_tac else 'RECUPERAÇÃO'

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