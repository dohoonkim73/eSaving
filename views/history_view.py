from PyQt6.QtWidgets import QMainWindow, QDialog
from eSaving.ui.ui_history_screen import Ui_historyScreen

class HistoryView(QDialog):
    
    def __init__(self):
        super().__init__()
        # 메인화면 직접로딩
        self.ui = Ui_historyScreen()
        self.ui.setupUi(self)