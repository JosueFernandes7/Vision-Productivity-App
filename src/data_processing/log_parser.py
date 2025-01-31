# src/data_processing/log_parser.py

import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

class LogAnalyzer:
    def __init__(self, log_paths):
        self.log_paths = log_paths
    
    def get_daily_data(self):
        return self._process_logs(lambda d: d.date() == datetime.now().date())
    
    def get_weekly_data(self):
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        return self._process_logs(lambda d: d >= start_of_week)
    
    def get_monthly_data(self):
        now = datetime.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self._process_logs(lambda d: d >= start_of_month)

    def get_global_data(self):
        return self._process_logs()
    
    def _process_logs(self, filter_fn=lambda _: True):
        data = defaultdict(list)
        
        for path in self.log_paths:
            for log_file in os.listdir(path):
                with open(os.path.join(path, log_file)) as f:
                    log = json.load(f)
                    dt = datetime.strptime(log['timestamp'], "%Y-%m-%d_%H-%M-%S")
                    if filter_fn(dt):
                        data[dt.hour].append(log['duration'])
        
        return {h: sum(durations) for h, durations in data.items()}