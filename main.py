import sys
from typing import Optional
from datetime import datetime, timedelta
from PyQt5 import QtWidgets, uic
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QCheckBox, QComboBox,
    QDateEdit, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QToolBox, QVBoxLayout, QWidget)
from layout_CC import Ui_MainWindow
#import funcoes

def extrair_codigo():
    codigo = ui.cod_boleta.text()
    cod_inst = codigo[0:3]
    ################ DATA DE VENCIMENTO ################
    cod_vencimento = int(codigo[31:35])
    data_base = '07/10/1997'
    formato_data = "%d/%m/%Y"
    data_base_obj = datetime.strptime(data_base, formato_data)
    data_calculada = data_base_obj + timedelta(days=cod_vencimento)
    ano_vencimento = data_calculada.year
    mes_vencimento = data_calculada.month
    dia_vencimento = data_calculada.day
    data = QDate(ano_vencimento, mes_vencimento, dia_vencimento)
    ui.vencimento_boleta.setDate(data)

    #################### VALOR BOLETO ##################
    cod_reais = int(codigo[35:43])
    reais_format = str(cod_reais)
    cod_centavos = codigo[43:45]
    valor_boleto = (reais_format + ',' + cod_centavos)
    ui.valor_boleta.setText(valor_boleto)

    ##################### FORNECEDOR ###################
    
    ################### LIMPAR CODIGO ##################
    ui.cod_boleta.clear()

    return 

def gravar_boleto():
    #gravar informações no banco de dados sqlite
    return

class MainWindow(QMainWindow, Ui_MainWindow):  

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Controle de Contas')
        ################################################ SELEÇÃO DE ABAS ##############################################################
        self.btn_home.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pag_home))
        self.btn_receitas.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pag_receitas))
        self.btn_despesas.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pag_despesas))
        self.btn_consultar.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pag_consultar))

        ################################### EXTRACAO DE INFORMAÇÕES DO COD DE BARRAS ##################################################
        self.btn_extrair.clicked.connect(extrair_codigo)
        self.btn_adicionar.clicked.connect(gravar_boleto)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    app.exec()