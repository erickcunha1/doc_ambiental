import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from main_window import MainWindow
from datetime import datetime

def verificar_data_limite():
    data_limite = datetime(2024, 10, 15)  # Define a data limite
    data_atual = datetime.now()  # Obtém a data atual
    
    if data_atual > data_limite:  # Verifica se a data atual ultrapassa a data limite
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("O prazo para executar este código expirou. O programa será encerrado.")
        msg.setWindowTitle("Erro")
        msg.exec_()
        return False  # Retorna False para indicar que a execução não deve continuar
    return True  # Retorna True para continuar a execução

def main():
    app = QApplication(sys.argv)  # Cria a QApplication primeiro
    if not verificar_data_limite():  # Verifica a data limite, se expirada, não continua
        sys.exit()  # Encerra o programa se a data limite tiver sido ultrapassada
    
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()