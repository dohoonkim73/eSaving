from PyQt6.QtWidgets import QMainWindow, QDialog
from eSaving.ui.ui_temp_screen import Ui_TempScreen

class TemperatureView(QDialog):
    
    def __init__(self):
        super().__init__()
        # 메인화면 직접로딩
        self.ui = Ui_TempScreen()
        self.ui.setupUi(self)