from PyQt6.QtWidgets import QMainWindow, QDialog
from eSaving.ui.ui_energy_screen import Ui_energyScreen

class EnergyView(QDialog):
    
    def __init__(self):
        super().__init__()
        # 메인화면 직접로딩
        self.ui = Ui_energyScreen()
        self.ui.setupUi(self)