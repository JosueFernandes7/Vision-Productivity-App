# src/data_processing/log_manager.py

import os
import json
from collections import defaultdict
from datetime import datetime, timedelta

class LogManager:
    def __init__(self):
        self.base_path = "./logs"
        self._ensure_dirs()
        
    def _ensure_dirs(self):
        os.makedirs(f"{self.base_path}/cellphone", exist_ok=True)
        os.makedirs(f"{self.base_path}/human", exist_ok=True)

    def save_log(self, event_type, duration):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_data = {
                "type": event_type,
                "duration": duration,
                "timestamp": timestamp
            }
            
            category = "cellphone" if "celular" in event_type.lower() else "human"
            filename = f"{self.base_path}/{category}/log_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=4)
                
            return True
        except Exception as e:
            print(f"Erro ao salvar log: {str(e)}")
            return False

    def load_logs(self, category, period='day'):
        logs = []
        path = f"{self.base_path}/{category}"
        
        now = datetime.now()
        if period == 'day':
            start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start_time = now - timedelta(days=now.weekday())
            start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'month':
            start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_time = None

        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(f"{path}/{filename}") as f:
                    log = json.load(f)
                    log_time = datetime.strptime(log['timestamp'], "%Y-%m-%d_%H-%M-%S")
                    
                    if start_time and log_time < start_time:
                        continue
                        
                    logs.append(log)
        return logs