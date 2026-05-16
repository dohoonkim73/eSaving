import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QRadioButton, QStackedWidget
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QTableWidgetItem

from eSaving.views.history_view import HistoryView
from eSaving.presenters.main_presenter import MainPresenter

class HistoryPresenter(QObject):
    
    switch_to_main = pyqtSignal()
    
    
    def __init__(self, history_view: HistoryView, main_presenter: MainPresenter):
        super().__init__()
        self.history_view = history_view
        self.main_presenter = main_presenter
        
        
        self.connect_signals()
        
    def connect_signals(self):
        self.history_view.ui.btn_to_main.clicked.connect(self.switch_to_main.emit)
        #self.main_presenter.history_date.connect(self.set_table)
        self.main_presenter.history_data.connect(self.set_table)
        
        
    def set_table(self, data):
       
        table = self.history_view.ui.table_history
        
        table.setRowCount(15)
        table.setColumnCount(13)
        
        #table.setItem(0, 0, QTableWidgetItem("Month"))
        
        for i in range(15):
            table.setItem(i, 0, QTableWidgetItem(str(data[0][i*2])))
            table.setItem(i, 1, QTableWidgetItem(str(data[1][i*2])))
            table.setItem(i, 2, QTableWidgetItem(str(data[2][i*2])))
            table.setItem(i, 3, QTableWidgetItem(str(data[3][i*2])))
            table.setItem(i, 4, QTableWidgetItem(str(data[4][i*2])))
            table.setItem(i, 5, QTableWidgetItem(str(data[5][i*2])))
            table.setItem(i, 6, QTableWidgetItem(str(data[6][i*2])))
            table.setItem(i, 7, QTableWidgetItem(str(data[7][i*2])))
            table.setItem(i, 8, QTableWidgetItem(str(data[8][i*2])))
            table.setItem(i, 9, QTableWidgetItem(str(data[9][i*2])))
            table.setItem(i, 10, QTableWidgetItem(str(data[10][i*2])))
            table.setItem(i, 11, QTableWidgetItem(str(data[11][i*2])))
            table.setItem(i, 12, QTableWidgetItem(str(data[12][i*2])))
        
        