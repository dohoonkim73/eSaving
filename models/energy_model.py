class EnergyModel():
    def __init__(self):
        self.energy_kwh = 0.0
        
    def update(self, power_watt, dt_sec):
        power_kw = power_watt / 1000.0
        self.energy_kwh += power_kw *(dt_sec / 3600.0)
        print("모델에서 업데이트 실행")
        
        
    def reset(self):
        self.energy_kwh = 0.0