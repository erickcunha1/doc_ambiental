from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QPixmap
from processar_pasta_thread import ProcessarPastaThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pasta_selecionada = None
        self.tac_arquivos_selecionados = []  # Lista para armazenar dois arquivos TAC

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Processador de Arquivos TAC')

        # Configuração dos widgets
        self.status_label = QLabel('Nenhuma pasta ou arquivo TAC selecionado.', self)
        self.status_label.setWordWrap(True)
        
        self.select_button = QPushButton('Selecionar Pasta', self)
        self.select_tac_button = QPushButton('Selecionar TAC Escopo', self)
        self.iniciar_button = QPushButton('Iniciar Processamento', self)
        self.iniciar_button.setEnabled(False)  # Desabilitado até que os dois arquivos sejam selecionados
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        # QLabel para exibir a imagem
        self.image_label = QLabel(self)
        pixmap = QPixmap('img/imagem.png')  # Substitua pelo caminho da sua imagem
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Faz a imagem escalar para caber no QLabel
        self.image_label.setFixedSize(400, 200)   # Define um tamanho fixo para o QLabel (opcional)

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
        layout.addWidget(self.image_label)  # Adiciona o QLabel da imagem ao layout
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.resize(500, 400)

        self.thread = None  # Inicializa a thread como None

    def selecionar_pasta(self):
        self.pasta_selecionada = QFileDialog.getExistingDirectory(self, 'Selecionar Pasta Principal')
        if self.pasta_selecionada:
            self.status_label.setText(f'Pasta selecionada: {self.pasta_selecionada}')
            self.verificar_selecao_completa()

    def selecionar_tac_escopo(self):
        # Permitir seleção de até 2 arquivos TAC
        self.tac_arquivos_selecionados, _ = QFileDialog.getOpenFileNames(self, 'Selecionar TAC Escopo', '', 'Documentos Word (*.docx)', options=QFileDialog.DontUseNativeDialog)
        if len(self.tac_arquivos_selecionados) > 2:
            self.status_label.setText("Você só pode selecionar no máximo 2 arquivos TAC.")
            self.tac_arquivos_selecionados = []
        elif len(self.tac_arquivos_selecionados) > 0:
            self.status_label.setText(f'Arquivos TAC selecionados: {", ".join(self.tac_arquivos_selecionados)}')
            self.verificar_selecao_completa()

    def verificar_selecao_completa(self):
        if self.pasta_selecionada and len(self.tac_arquivos_selecionados) > 0:
            self.status_label.setText(f"Pasta selecionada: {self.pasta_selecionada} e\n\nTac(s) selecionados: {", ".join(self.tac_arquivos_selecionados)}")
            self.iniciar_button.setEnabled(True)  # Habilita o botão de iniciar processamento
        else:
            self.iniciar_button.setEnabled(False)  # Desabilita se faltar algo

    def iniciar_processamento(self):
        if self.pasta_selecionada and len(self.tac_arquivos_selecionados) > 0:
            self.status_label.setText(f'Processando pasta: {self.pasta_selecionada}')
            self.thread = ProcessarPastaThread(self.pasta_selecionada, self.tac_arquivos_selecionados)
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
