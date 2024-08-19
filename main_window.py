from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar
from processar_pasta_thread import ProcessarPastaThread
from dados_manager import DadosManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pasta_selecionada = None
        self.tac_arquivo_selecionado = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Processador de Arquivos TAC')

        # Configuração dos widgets
        self.status_label = QLabel('Nenhuma pasta ou arquivo TAC selecionado.', self)
        self.select_button = QPushButton('Selecionar Pasta', self)
        self.select_tac_button = QPushButton('Selecionar TAC Escopo', self)
        self.iniciar_button = QPushButton('Iniciar Processamento', self)
        self.iniciar_button.setEnabled(False)  # Desabilitado até que os dois arquivos sejam selecionados
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        # Conectando botões aos métodos
        self.select_button.clicked.connect(self.selecionar_pasta)
        self.select_tac_button.clicked.connect(self.selecionar_tac_escopo)
        self.iniciar_button.clicked.connect(self.iniciar_processamento)

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.select_tac_button)
        button_layout.addWidget(self.iniciar_button)

        # Layout vertical para a estrutura geral
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.resize(500, 200)

        self.thread = None  # Inicializa a thread como None

    def selecionar_pasta(self):
        self.pasta_selecionada = QFileDialog.getExistingDirectory(self, 'Selecionar Pasta Principal')
        if self.pasta_selecionada:
            self.status_label.setText(f'Pasta selecionada: {self.pasta_selecionada}')
            self.verificar_selecao_completa()

    def selecionar_tac_escopo(self):
        self.tac_arquivo_selecionado, _ = QFileDialog.getOpenFileName(self, 'Selecionar TAC Escopo', '', 'Documentos Word (*.docx)')
        if self.tac_arquivo_selecionado:
            self.status_label.setText(f'Arquivo TAC selecionado: {self.tac_arquivo_selecionado}')
            print(self.tac_arquivo_selecionado)
            self.verificar_selecao_completa()

    def verificar_selecao_completa(self):
        if self.pasta_selecionada and self.tac_arquivo_selecionado:
            self.status_label.setText(f'Selecionado: {self.pasta_selecionada} e {self.tac_arquivo_selecionado}')
            self.iniciar_button.setEnabled(True)  # Habilita o botão de iniciar processamento
        else:
            self.iniciar_button.setEnabled(False)  # Desabilita se faltar algo

    def iniciar_processamento(self):
        if self.pasta_selecionada and self.tac_arquivo_selecionado:
            self.status_label.setText(f'Processando pasta: {self.pasta_selecionada}')
            self.thread = ProcessarPastaThread(self.pasta_selecionada)
            self.thread.atualizacao_status.connect(self.atualizar_status)
            self.thread.progresso_atualizado.connect(self.atualizar_progresso)
            self.thread.processamento_concluido.connect(self.exibir_mensagem_conclusao)
            self.thread.start()

    def atualizar_status(self, mensagem):
        self.status_label.setText(mensagem)

    def atualizar_progresso(self, valor):
        self.progress_bar.setValue(valor)

    def exibir_mensagem_conclusao(self):
        self.status_label.setText("Documento(s) gerado(s) com sucesso!")