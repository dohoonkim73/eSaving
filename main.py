""" gitHub """
""" 1. git status로 상태 확인 """
""" 2. git add . 파일 추가 """
""" 3. git commit -m " 내용 기입 " """
""" 4. git push -u  origin main """
""" 5. gitHub repository에 제대로 저장되었는지 확인 """

import sys

from PyQt6.QtWidgets import QApplication

from eSaving.views.main_view import MainView
from eSaving.services.plc_service import PlcService
from eSaving.workers.plc_worker import PlcWorker
from eSaving.presenters.main_presenter import MainPresenter

from eSaving.views.energy_view import EnergyView
from eSaving.workers.energy_worker import EnergyWorker
from eSaving.models.energy_model import EnergyModel
from eSaving.presenters.energy_presenter import EnergyPresenter

from eSaving.views.temp_view import TemperatureView
from eSaving.workers.temp_worker import TemperatureWorker
from eSaving.presenters.temp_presenter import TemperaturePresenter

from eSaving.views.history_view import HistoryView
from eSaving.presenters.history_presenter import HistoryPresenter

class AppManager:
    
    def __init__(self):
        
        
        
        # 2. 전력량계 관련 인스턴스 생성
        self.energy_view = EnergyView()
        self.energy_model = EnergyModel()
        self.energy_worker = EnergyWorker(self.energy_model)
        self.energy_presenter = EnergyPresenter(self.energy_view, self.energy_model, self.energy_worker)
        
        # 3. 온도컨트롤 관련 인스턴스 생성
        self.temp_view = TemperatureView()
        self.temp_worker = TemperatureWorker()
        self.temp_presenter = TemperaturePresenter(self.temp_view, self.temp_worker)
        
        
        
        # 1. 메인화면관련 인스턴스 생성
        self.main_view = MainView()
        self.plc_service = PlcService()
        self.plc_worker = PlcWorker(self.plc_service)
        
        self.ePresenter = self.energy_presenter
        
        self.main_presenter = MainPresenter(self.main_view, self.plc_service, self.plc_worker, self.ePresenter)
        
        # 4. 이력화면 관련 인스턴스 생성
        self.history_view = HistoryView()
        self.history_presenter = HistoryPresenter(self.history_view, self.main_presenter)
        
        
        
        # 화면 표시 시그널 연결
        self.main_presenter.switch_to_energy.connect(self.show_energy_screen)   # 전력량계 시뮬레이터 표시
        self.main_presenter.switch_to_tmep.connect(self.show_temp_screen)       # 온도컨트롤 시뮬레이터 표시
        self.main_presenter.switch_to_history.connect(self.show_history_screen) # 이력화면 표시
        self.energy_presenter.switch_to_main.connect(self.show_main_screen)     # 메인 스크린만 표시
        self.history_presenter.switch_to_main.connect(self.out_history_screen)
        
        
        self.main_view.show()
        
    def show_energy_screen(self):
        print("전력량계 화면")
        self.energy_view.show()
        
    def show_temp_screen(self):
        self.temp_view.show()
        
    def show_history_screen(self):
        print("history 화면")
        self.history_view.show()
        
    def out_history_screen(self):
        self.history_view.hide()
        self.main_view.show()
    
    def show_main_screen(self):
        self.energy_view.hide()
        self.temp_view.hide()
        self.main_view.show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = AppManager()
    sys.exit(app.exec())
    