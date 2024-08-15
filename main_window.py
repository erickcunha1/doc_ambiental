from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget, QProgressBar
from processar_pasta_thread import ProcessarPastaThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Processador de Arquivos TAC')

        # Configuração dos widgets
        self.status_label = QLabel('Nenhuma pasta selecionada.', self)
        self.select_button = QPushButton('Selecionar Pasta', self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)
        self.select_button.clicked.connect(self.selecionar_pasta)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.resize(400, 200)

        self.thread = None  # Inicializa a thread como None

    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, 'Selecionar Pasta Principal')
        if pasta:
            self.status_label.setText(f'Processando pasta: {pasta}')
            self.thread = ProcessarPastaThread(pasta)
            self.thread.atualizacao_status.connect(self.atualizar_status)
            self.thread.progresso_atualizado.connect(self.atualizar_progresso)
            self.thread.processamento_concluido.connect(self.exibir_mensagem_conclusao)
            self.thread.start()
        else:
            self.status_label.setText("Nenhuma pasta selecionada.")

    def atualizar_status(self, mensagem):
        self.status_label.setText(mensagem)

    def atualizar_progresso(self, valor):
        self.progress_bar.setValue(valor)

    def exibir_mensagem_conclusao(self):
        self.status_label.setText("Documento(s) gerado(s) com sucesso!")
