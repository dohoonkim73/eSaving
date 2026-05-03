""" 메인화면 + stacked widget 관리 """
""" 메인화면 관리 pyuic6 방식사용 """
""" pyuic6 main_window.ui -o ui_main_window.py """
""" pyuic6 power_screen.ui -o ui_power_screen.py"""
""" pyuic6 temp_screen.ui -o ui_temp_screen.py"""
""" GT Designer에서 수정시 위 내용 반드시 수행 """
""" 위 내용을 수행하기전에 터미널창에서 해당 폴더위치(ui폴더)로 가는 것 잊지말것"""

from PyQt6.QtWidgets import QMainWindow, QTableWidget, QRadioButton
from eSaving.ui.ui_main_window import Ui_MainWindow

class MainView(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # 메인화면 직접로딩
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.presenter = None  # Presenter를 담을 공간을 마련(main.py에서 주입)