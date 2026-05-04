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