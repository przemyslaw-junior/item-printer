import socket
from datetime import datetime

class ZebraPrinter:
    
    def __init__(self, ip, port, font_size):
        self.ip = ip
        self.port = port
        self.font_size = font_size
        
        
    def print_label(self, item, quantity):
        current_data = datetime.now().strftime("%d.%m.%Y")
        
        zpl = f"""
        ^XA
        ^C128
        ^CF0,{self.font_size}
        ^FO50,30^FD{item}^FS
        ^CF0,30
        ^FO50,80^FD{current_data}^FS
        ^XZ
        """
        
        for _ in range(quantity):
            self._send_to_printer(zpl)
            
            
    def _send_to_printer(self, zpl):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.ip, self.port))
                s.sendall(zpl.encode('utf-8'))
        except Exception as e:
            print(f"Błąd podczas drukowania: {e}")