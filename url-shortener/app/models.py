import datetime
import threading

class URLStore:
    def __init__(self):
        self._urls = {}
        self._lock = threading.Lock()

    def add_url(self, short_code, long_url):
        with self._lock:
            if short_code in self._urls:
                return None  # Or raise an exception
            self._urls[short_code] = {
                "long_url": long_url,
                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "clicks": 0
            }
            return short_code

    def get_url(self, short_code):
        with self._lock:
            return self._urls.get(short_code)

    def increment_clicks(self, short_code):
        with self._lock:
            if short_code in self._urls:
                self._urls[short_code]["clicks"] += 1
                return self._urls[short_code]["long_url"]
            return None

    def get_stats(self, short_code):
        with self._lock:
            url_data = self._urls.get(short_code)
            if url_data:
                return {
                    "url": url_data["long_url"],
                    "created_at": url_data["created_at"],
                    "clicks": url_data["clicks"]
                }
            return None

# Global instance to be used by the Flask app
url_store = URLStore()