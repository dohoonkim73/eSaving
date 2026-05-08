import pymcprotocol

class PlcService:
    def __init__(self):
        self.plc = pymcprotocol.Type3E()
        self.connected = False
        
    """ PLC 와 연결 """
    
    def connection(self):
        print(" PLC와 연결 시작 ")
        try:
            self.plc.setaccessopt(commtype="binary")
            self.plc.connect("192.168.1.100", 5000)
            self.connected = True
            return True, "PLC 연결 성공"
        except Exception as e:
            return False, f"PLC 연결 실패: {str(e)}"
        
    def closed(self):
        if self.connected:
            self.plc.close()
            self.connected = False
            
    """ PLC 어드레스 읽기/쓰기 """
    
    def read_bitAddress(self, address, point):
        try:
            values = self.plc.batchread_bitunits(headdevice=address, readsize=point)
            return True, values
        except Exception as e:
            return False, str(e)
        
    def read_wordAddress(self, address, point):
        try:
            values = self.plc.batchread_wordunits(headdevice=address, readsize=point)
            return True, values
        except Exception as e:
            return False, str(e)
        
    def write_bitAddress(self, address, values):
        try:
            self.plc.batchwrite_bitunits(headdevice=address, values=[values])
            return True, values
        except Exception as e:
            return False, str(e)
        
    def write_wordAddress(self, address, values):
        try:
            self.plc.batchwrite_wordunits(headdevice=address, values=[values])
            return True, values
        except Exception as e:
            return False, str(e)
        
    def wirte_DwordAddress(self, address, values):
        print("전력량계 값 쓰기")
        print(f"어드레스: {address}", f"값: {values}")
        try:
            self.plc.randomwrite(word_devices=["D7004"], word_values=[333], dword_devices=address, dword_values=values)
            return True, values
        except Exception as e:
            return False, str(e)
    