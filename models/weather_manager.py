import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('config/.env')


class WeatherManager:
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.data_file = "data/weather_history.json"
        self._ensure_data_directory()
        self.weather_history = []
        self.current_weather = None
        self.load_weather_history()

    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def load_weather_history(self):
        """Tải lịch sử thời tiết từ file"""
        try:
            if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.weather_history = json.load(f)
                    # Trả về dữ liệu thời tiết gần nhất nếu có
                    if self.weather_history:
                        return self.weather_history[-1]
        except Exception as e:
            print(f"Lỗi khi tải lịch sử thời tiết: {str(e)}")
        return None

    def save_weather_history(self):
        """Lưu lịch sử thời tiết vào file"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.weather_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu lịch sử thời tiết: {str(e)}")

    def get_weather(self, location):
        """Lấy thông tin thời tiết từ API"""
        try:
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric",
                "lang": "vi",
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            weather_data = response.json()
            weather_data["fetched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            weather_data["location"] = location

            # Lưu vào lịch sử
            self._add_to_history(weather_data)
            self.current_weather = weather_data

            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi lấy dữ liệu thời tiết: {str(e)}")
            return None
        except Exception as e:
            print(f"Lỗi không xác định: {str(e)}")
            return None

    def _add_to_history(self, weather_data):
        """Thêm dữ liệu thời tiết vào lịch sử"""
        # Kiểm tra trùng lặp
        for item in self.weather_history:
            if item.get("location") == weather_data.get("location"):
                self.weather_history.remove(item)
                break

        self.weather_history.append(weather_data)

        # Giới hạn lịch sử
        if len(self.weather_history) > 10:
            self.weather_history = self.weather_history[-10:]

        self.save_weather_history()

    def clear_weather_history(self):
        """Xóa hoàn toàn lịch sử thời tiết"""
        self.weather_history = []
        self.current_weather = None
        self.save_weather_history()

    def clear_weather_display(self):
        """Chỉ xóa dữ liệu hiển thị (giữ nguyên file JSON)"""
        self.current_weather = None

    def clear_all_weather_data(self):
        """Xóa toàn bộ dữ liệu thời tiết (cả hiển thị và trong bộ nhớ)"""
        self.current_weather = None
        self.weather_history = []
        self.save_weather_history()  # Lưu file rỗng
