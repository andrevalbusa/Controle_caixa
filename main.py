import sys
from typing import Optional
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
import funcoes


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
        self.btn_extrair.clicked.connect(funcoes.extrair_codigo)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    app.exec()