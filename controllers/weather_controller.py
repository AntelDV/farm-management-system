from models.weather_manager import WeatherManager
from views.weather_views import WeatherViews


class WeatherController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.manager = WeatherManager()
        self.views = WeatherViews(self)

    # Trong weather_controller.py
    def get_weather(self, location):
        """Chỉ admin mới được lấy thời tiết"""
        if not self._is_admin():
            return None

        weather_data = self.manager.get_weather(location)
        if weather_data:
            self.views._safe_display_weather_info(weather_data)
        return weather_data

    def _is_admin(self):
        current_user = self.main.auth_controller.current_user
        return current_user and current_user.get("role") == "admin"

    def show_weather_widget(self):
        """Hiển thị widget thời tiết"""
        self.views.show_weather_widget()

    def clear_weather(self):
        """Xóa toàn bộ thông tin thời tiết"""
        self.manager.clear_weather_history()
        if hasattr(self, "views"):
            self.views.clear_weather()
