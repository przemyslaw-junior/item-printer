import json

class Config:
    def __init__(self, file_path="config.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.printer_ip = data.get("printer_ip")
        self.printer_port = data.get("printer_port")
        self.font_size = data.get("font_size")