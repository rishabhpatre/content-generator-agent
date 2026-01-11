import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, history_file="data/posted_history.json"):
        self.history_file = history_file
        self.history = self._load_history()

    def _load_history(self):
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_history(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def is_posted(self, url):
        return any(item['url'] == url for item in self.history)

    def add_posted(self, url, title, type):
        entry = {
            "url": url,
            "title": title,
            "type": type,
            "date_posted": datetime.now().isoformat()
        }
        self.history.append(entry)
        self._save_history()
