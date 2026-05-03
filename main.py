import sys

from PyQt6.QtWidgets import QApplication

from eSaving.views.main_view import MainView

class AppManager:
    
    def __init__(self):
        
        self.main_view = MainView()
        
        self.main_view.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = AppManager()
    sys.exit(app.exec())
    