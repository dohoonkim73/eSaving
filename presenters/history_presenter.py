import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QRadioButton, QStackedWidget
from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

from eSaving.views.history_view import HistoryView
from eSaving.workers.plc_worker import PlcWorker

class HistoryPresenter(QObject):
    
    switch_to_main = pyqtSignal()
    
    
    def __init__(self, history_view: HistoryView, plc_worker: PlcWorker):
        super().__init__()
        self.history_view = history_view
        self.plc_worker = plc_worker
        self.plc_worker.data_received_historyMonth.connect(self.set_table)
        
        self.connect_signals()
        
    def connect_signals(self):
        self.history_view.ui.btn_to_main.clicked.connect(self.switch_to_main.emit)
        
        
    def set_table(self):
        table = self.history_view.ui.table_history
        
        table.setRowCount(15)
        table.setColumnCount(13)
        print("테이블 데이터")
        
        