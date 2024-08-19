# processar_arquivos.py

import os
import datetime
import logging
from extrair_bioma import extrair_palavra
from extrair_gpt import criar_tac
from manipular_documento import substituir_textos_docx, gerar_nome_arquivo_unico
from funcoes_bioma import realizar_calculo
from extenso import numero_completo_por_extenso
from extrair_data import extracao_anos
from dados_manager import DadosManager 

dados_manager = DadosManager()

def processar_arquivo_alerta(caminho_arquivo):
    try:
        bioma = extrair_palavra(caminho_arquivo, 'BIOMAS', 2)
        bioma = bioma.replace('MUNICÍPIO', '').strip()
        dados_manager.set_bioma(bioma)

        anos = extracao_anos(caminho_arquivo)
        dados_manager.set_anos(datetime.date.today().year - anos.year)
        print(dados_manager)

        logging.info(f'Bioma extraído: {dados_manager.get_bioma()}')
    except Exception as e:
        logging.error(f'Erro ao processar arquivo de alerta: {str(e)}')

def processar_arquivo_relatorio(caminho_arquivo):
    try:
        dicionario = criar_tac(caminho_arquivo)
        
        bioma = dados_manager.get_bioma()
        area_afetada = dicionario['$area']

        n1 = dados_manager.get_anos()
        print(n1)

        valor = realizar_calculo(bioma, area_afetada, n1)
        dicionario['$valor'] = valor
        numero_extenso = numero_completo_por_extenso(valor)
        dicionario['$extenso'] = numero_extenso
        
        pasta_saida = os.path.dirname(caminho_arquivo) 
        output_base_name = 'TAC_CODALERTA'
        output_ext = '.docx'
        output_path = gerar_nome_arquivo_unico(output_base_name, output_ext, pasta_saida)

        substituir_textos_docx('TAC.docx', dicionario, output_path)
        logging.info(f'Relatório processado e salvo em: {output_path}')
    except Exception as e:
        logging.error(f'Erro ao processar arquivo de relatório: {str(e)}')

def processar_arquivo(caminho_arquivo):
    try:
        nome_arquivo = os.path.basename(caminho_arquivo)
        if nome_arquivo.startswith('ANEXO 01'):
            processar_arquivo_alerta(caminho_arquivo)
        elif nome_arquivo.startswith('Relatório'):
            processar_arquivo_relatorio(caminho_arquivo)
    except Exception as e:
        logging.error(f'Erro ao processar arquivo: {str(e)}')