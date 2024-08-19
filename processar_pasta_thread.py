import os
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from processar_arquivos import processar_arquivo


class ProcessarPastaThread(QThread):
    atualizacao_status = pyqtSignal(str)
    progresso_atualizado = pyqtSignal(int)
    processamento_concluido = pyqtSignal()

    def __init__(self, pasta, caminho_tac):
        super().__init__()
        self.pasta = pasta
        self.total_itens = 0
        self.caminho_tac = caminho_tac
        self.itens_processados = 0

    def run(self):
        self.total_itens = self.contar_itens(self.pasta)
        self.processar_pasta(self.pasta, self.caminho_tac)
        self.processamento_concluido.emit()

    def contar_itens(self, pasta):
        total = 0
        for root, dirs, files in os.walk(pasta):
            total += len(files)
        return total

    def processar_pasta(self, pasta, caminho_tac):
        try:
            if not os.path.isdir(pasta):
                raise ValueError(f'{pasta} não é um diretório válido.')

            conteudos = os.listdir(pasta)

            for item in conteudos:
                caminho_item = os.path.join(pasta, item)

                if os.path.isdir(caminho_item):
                    logging.info(f'Processando subpasta: {item}')
                    self.atualizacao_status.emit(f'Processando subpasta: {item}')
                    self.processar_pasta(caminho_item, self.caminho_tac)
                else:
                    self.atualizacao_status.emit(f'Processando arquivo: {item}')
                    caminho_tac = self.caminho_tac
                    processar_arquivo(caminho_item, caminho_tac)
                    self.itens_processados += 1
                    progresso = int((self.itens_processados / self.total_itens) * 100)
                    self.progresso_atualizado.emit(progresso)

        except Exception as e:
            logging.error(f'Ocorreu um erro ao processar a pasta: {str(e)}')
            self.atualizacao_status.emit(f'Erro: {str(e)}')