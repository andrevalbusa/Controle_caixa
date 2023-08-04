import sys
import os
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
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,QMessageBox,
    QToolBox, QVBoxLayout, QWidget)
from layout_CC import Ui_MainWindow
import sqlite3

######################################### CRIAÇÃO DATABASE E TABELAS #################################
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
nome_arquivo_db = 'database_CC.db'
caminho_banco_dados = os.path.join(diretorio_atual, nome_arquivo_db)

# Cria a conexão com o banco de dados
conn = sqlite3.connect(caminho_banco_dados)

cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS despesas (id INTEGER PRIMARY KEY, descricao TEXT, vencimento DATE ,valor REAL, codigo TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS receitas (id INTEGER PRIMARY KEY, origem TEXT, dia DATE ,valor REAL, descricao TEXT)')




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
        self.btn_extrair.clicked.connect(self.extrair_codigo)
        self.btn_adicionar.clicked.connect(self.gravar_boleto)
        self.checkBox.clicked.connect(self.checkbox_despesas)
        self.btn_adicionar_outros.clicked.connect(self.gravar_outros)
        self.checkBox_2.clicked.connect(self.checkbox_receitas)
        self.salvar_receita.clicked.connect(self.gravar_receita)


    def extrair_codigo(self):
        codigo = self.cod_boleta.text()
        check = codigo.isnumeric()
        chavepk = None
        fornecedor = None
        data =  None
        valor_boleto = None

        if check == True:
            cod_inst = codigo[0:3]
             ################ DATA DE VENCIMENTO ################
            cod_vencimento = int(codigo[31:35])
            cod_pk = str(cod_vencimento)
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
            fornecedor = ("escrever logica dos fornecedores")
            ################### ID / LIMPAR CODIGO #############
            chavepk = (cod_inst + reais_format + cod_pk)
        else:
            error_message = "Erro: Código de barras inválido. O código deve ser numérico."
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Erro")
            error_box.setText(error_message)
            error_box.setStandardButtons(QMessageBox.Ok)
        
            error_box.exec()
        return chavepk, fornecedor, data, valor_boleto, codigo

    def gravar_boleto(self):

        valores = self.extrair_codigo()

        if valores[0] is not None:  
            conn = sqlite3.connect(caminho_banco_dados)
            cursor = conn.cursor()
            data_str = valores[2].toString("dd-MM-yyyy")
            cursor.execute('INSERT INTO despesas(descricao, vencimento, valor, codigo) VALUES (?, ?, ?, ?)',
                                            (valores[1], data_str, valores[3], valores[4]))  
            conn.commit()
            conn.close()
        else:
            error_message = "Erro: Código de barras inválido. O código deve ser numérico."
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Erro")
            error_box.setText(error_message)
            error_box.setStandardButtons(QMessageBox.Ok)
            error_box.exec()

        self.cod_boleta.clear()
        self.vencimento_boleta.clear()
        self.valor_boleta.clear()
        self.fornecedor.clear()
        return

    def checkbox_despesas(self, state):
        if state == True:
            current_date = QDate.currentDate()
            self.data_outros.setDate(current_date)
            self.data_outros.setEnabled(True)
        return

    def gravar_outros(self):
        descricaooutros = self.descricao_outros.text()
        valoroutros = self.valor_outros.text()
        dataoutros = self.data_outros.date()
        dataoutrosform = dataoutros.toString("dd-MM-yyyy")
        codigo = 'N/A'

        conn = sqlite3.connect(caminho_banco_dados)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO despesas(descricao, vencimento, valor, codigo) VALUES (?, ?, ?, ?)',
                                                (descricaooutros, dataoutrosform, valoroutros, codigo))
        conn.commit()
        conn.close()

        self.descricao_outros.clear()
        self.valor_outros.clear()
        self.data_outros.clear()

        return

    def checkbox_receitas(self, state):
        if state == True:
            current_date = QDate.currentDate()
            self.data_receita.setDate(current_date)
            self.data_receita.setEnabled(True)
        return
    
    def gravar_receita(self):
        origem = self.origem_receita.currentText()
        valor_r = self.valor_receita.text()
        data_r = self.data_receita.date().toString('dd/MM/yyyy')
        descricao = self.descricao_receita.toPlainText()

        if origem is not None and valor_r is not None and data_r is not None:
            conn = sqlite3.connect(caminho_banco_dados)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO receitas (origem, dia, valor, descricao) VALUES (?, ?, ?, ?)',
                                                (origem, data_r, valor_r, descricao))
            conn.commit()
            conn.close()
        else:
            error_message = "Erro: verifique os dados inseridos"
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Erro")
            error_box.setText(error_message)
            error_box.setStandardButtons(QMessageBox.Ok)
            error_box.exec()
        
        self.origem_receita.clear()
        self.valor_receita.clear()
        self.data_receita.clear()
        self.descricao_receita.clear()
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    app.exec()