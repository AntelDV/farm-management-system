import tkinter as tk
from tkinter import ttk, messagebox
import os, json
from views.styles import configure_styles
from utils.weather_icons import get_weather_description, get_weather_icon

class WeatherViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()
        self.previous_locations = []
        self.current_weather = None
        self.weather_frame = None
        self.weather_info_frame = None
        self.location_var = None
        self.location_entry = None
        self.load_previous_locations()

    def load_previous_locations(self):
        """Tải danh sách địa điểm từ file JSON"""
        try:
            if os.path.exists("data/weather_locations.json"):
                with open("data/weather_locations.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Đảm bảo dữ liệu là list và không trùng lặp
                    if isinstance(data, list):
                        self.previous_locations = list(dict.fromkeys(data))
                    else:
                        self.previous_locations = []
        except Exception as e:
            print(f"Lỗi khi tải lịch sử địa điểm: {str(e)}")
            self.previous_locations = []

    def save_previous_locations(self):
        """Lưu danh sách địa điểm vào file JSON"""
        try:
            os.makedirs("data", exist_ok=True)
            # Lưu toàn bộ danh sách không giới hạn
            with open("data/weather_locations.json", "w", encoding="utf-8") as f:
                json.dump(self.previous_locations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu lịch sử địa điểm: {str(e)}")

    def show_weather_widget(self, parent=None, force_clear=False):
        # Kiểm tra an toàn trước khi destroy
        if hasattr(self, 'weather_frame') and self.weather_frame is not None:
            try:
                self.weather_frame.destroy()
            except:
                pass  # Bỏ qua nếu có lỗi khi destroy
         
        # Tạo widget mới
        self.weather_frame = ttk.Frame(parent or self.controller.main.root)
        self.weather_frame.pack(fill=tk.X, pady=5)
         
        self._create_widgets()
         
        # Chỉ hiển thị nếu không phải force_clear và có dữ liệu
        if not force_clear and self._is_admin() and hasattr(self.controller.manager, 'current_weather') and self.controller.manager.current_weather:
            self._safe_display_weather_info(self.controller.manager.current_weather)
    
    
    def clear_weather(self):
        """Chỉ xóa hiển thị, không xóa file JSON"""
        self.controller.manager.clear_weather_display()
        self.location_var.set("")
        self._clear_weather_display()

    def _create_widgets(self):
        """Tạo tất cả các widget cần thiết"""
        if not self._is_admin():
            return
        # Ô nhập địa điểm
        ttk.Label(self.weather_frame, text="Địa điểm:").pack(side=tk.LEFT, padx=5)
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Combobox(
            self.weather_frame, 
            textvariable=self.location_var, 
            width=30,
            values=self.previous_locations
        )
        self.location_entry.pack(side=tk.LEFT, padx=5)

        # Nút lấy thời tiết
        ttk.Button(
            self.weather_frame,
            text="⛅ Lấy thời tiết",
            command=self._get_weather,
            style="Primary.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=5)

        # Nút xóa
        ttk.Button(
            self.weather_frame,
            text="❌ Xóa",
            command=self.clear_weather,
            style="Danger.TButton",
            width=10
        ).pack(side=tk.LEFT, padx=5)

        # Frame chứa thông tin thời tiết
        self.weather_info_frame = ttk.Frame(self.weather_frame, style="TFrame")
        self.weather_info_frame.pack(fill=tk.X, expand=True, pady=5)
    
    def _is_admin(self):
        """Kiểm tra quyền admin"""
        current_user = self.controller.main.auth_controller.current_user
        return current_user and current_user.get('role') == 'admin'
    
    def _safe_load_last_weather(self):
        """Chỉ load dữ liệu khi widget đã sẵn sàng"""
        if not self.weather_info_frame:
            return
            
        if hasattr(self.controller, 'manager'):
            last_weather = self.controller.manager.load_weather_history()
            if last_weather:
                self.current_weather = last_weather
                self._safe_display_weather_info(last_weather)

    def _get_weather(self):
        location = self.location_var.get().strip()
        if not location:
            self.clear_weather()
            return
            
        weather_data = self.controller.get_weather(location)
        if weather_data:
            self.current_weather = weather_data
            if location not in self.previous_locations:
                self.previous_locations.append(location)
                self.save_previous_locations()
                self.location_entry['values'] = self.previous_locations
   
    def clear_weather_display(self):
        """Xóa hoàn toàn widget thời tiết"""
        if hasattr(self, 'weather_frame') and self.weather_frame is not None:
            try:
                self.weather_frame.destroy()
            except:
                pass
        self.weather_frame = None

    def _clear_weather_display(self):
        """Chỉ xóa phần hiển thị, giữ nguyên dữ liệu"""
        if hasattr(self, 'weather_info_frame'):
            for widget in self.weather_info_frame.winfo_children():
                widget.destroy()

    def _safe_display_weather_info(self, weather_data):
        """Hiển thị thông tin thời tiết (chỉ đổi màu chữ, giữ nguyên icon)"""
        self._clear_weather_display()
         
        if not weather_data:
            return

        # Lấy dữ liệu từ API
        main = weather_data.get('main', {})
        weather = weather_data.get('weather', [{}])[0]
        wind = weather_data.get('wind', {})
         
        # Tạo frame chính
        container = ttk.Frame(self.weather_info_frame, padding=5)
        container.pack(fill=tk.BOTH, expand=True)

        # Dòng 1: Địa điểm và nhiệt độ
        top_frame = ttk.Frame(container)
        top_frame.pack(fill=tk.X, pady=3)
         
        # Giữ nguyên icon mặc định, chỉ đổi màu chữ
        weather_icon = get_weather_icon(weather.get('icon', ''))
         
        ttk.Label(top_frame, 
                 text=f"📍 {weather_data.get('name', 'N/A')}, {weather_data.get('sys', {}).get('country', '')}",
                 font=('Arial', 10),
                 foreground='#2C3E50').pack(side=tk.LEFT, padx=5)
         
        ttk.Label(top_frame, 
                 text=f"{weather_icon['text']} {main.get('temp', 0):.1f}°C",
                 font=('Arial', 12, 'bold'),
                 foreground=weather_icon['color']).pack(side=tk.RIGHT, padx=5)

        # Dòng 2: Thông tin chi tiết
        bottom_frame = ttk.Frame(container)
        bottom_frame.pack(fill=tk.X, pady=3)
         
        # Sử dụng màu mặc định cho các thông số
        ttk.Label(bottom_frame,
                 text=f"💧 {main.get('humidity', 0)}%",
                 font=('Arial', 9),
                 foreground='#3498DB').pack(side=tk.LEFT, padx=10)
         
        ttk.Label(bottom_frame,
                 text=f"🌀 {wind.get('speed', 0)} m/s",
                 font=('Arial', 9),
                 foreground='#16A085').pack(side=tk.LEFT, padx=10)
         
        ttk.Label(bottom_frame,
                 text=f"🌡️ {main.get('feels_like', 0):.1f}°C",
                 font=('Arial', 9),
                 foreground='#E74C3C').pack(side=tk.LEFT, padx=10)
         
        # Mô tả thời tiết (dịch sang tiếng Việt)
        desc = get_weather_description(weather.get('description', ''))
        ttk.Label(bottom_frame,
                 text=desc.capitalize(),
                 font=('Arial', 9, 'italic'),
                 foreground=weather_icon['color']).pack(side=tk.RIGHT, padx=10)
        
    
    def get_weather_alerts(self):
        """Lấy cảnh báo thời tiết dựa trên dữ liệu hiện tại"""
        if not self.current_weather:
            return []
        
        alerts = []
        temp = self.current_weather.get('main', {}).get('temp', 0)
        weather_main = self.current_weather.get('weather', [{}])[0].get('main', '').lower()
        
        if 'rain' in weather_main:
            alerts.append({
                'type': 'rain',
                'message': 'Trời đang mưa, cần chú ý các hoạt động ngoài trời',
                'icon': '🌧️'
            })
        elif temp > 33:
            alerts.append({
                'type': 'hot',
                'message': 'Nhiệt độ cao, cần chú ý tưới nước và che chắn',
                'icon': '🔥'
            })
        elif temp < 15:
            alerts.append({
                'type': 'cold',
                'message': 'Nhiệt độ thấp, cần chú ý giữ ấm cho vật nuôi',
                'icon': '❄️'
            })
        elif 'storm' in weather_main:
            alerts.append({
                'type': 'storm',
                'message': 'Cảnh báo bão, cần chuẩn bị các biện pháp phòng tránh',
                'icon': '⚠️'
            })
        
        return alerts
    
    def create_weather_alert_widget(self, parent):
        """Tạo widget hiển thị thông tin thời tiết và cảnh báo"""
        if not self._is_admin() or not self.current_weather:
            return None
        
        weather_frame = ttk.Frame(parent, style='Weather.TFrame')
        weather_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Hiển thị thông tin thời tiết với icon lớn hơn
        weather_data = self.current_weather
        main = weather_data.get('main', {})
        weather = weather_data.get('weather', [{}])[0]
        icon = get_weather_icon(weather.get('icon', ''))
        
        # Tạo label riêng cho icon với font lớn
        icon_label = ttk.Label(weather_frame,  text=icon['text'], font=('Arial', 20), foreground=icon['color'])
        icon_label.pack(side=tk.LEFT, padx=5)
        
        # Thông tin nhiệt độ và địa điểm
        info_label = ttk.Label(weather_frame,
                              text=f"{weather_data.get('name', 'N/A')}: {main.get('temp', 0):.1f}°C - {get_weather_description(weather.get('description', ''))}",
                              font=('Arial', 10))
        info_label.pack(side=tk.LEFT, padx=5)
        
        # Hiển thị cảnh báo nếu có
        alerts = self.get_weather_alerts()
        if alerts:
            alert_text = " ".join([f"{alert['icon']} {alert['message']}" for alert in alerts])
            ttk.Label(weather_frame, 
                     text=alert_text,
                     font=('Arial', 9, 'italic'),
                     foreground='#E74C3C').pack(side=tk.RIGHT, padx=5)
        
        return weather_frame
    
    
    def get_crop_alerts(self):
        """Cảnh báo thời tiết cho cây trồng"""
        alerts = []
        if not self.current_weather:
            return alerts
        
        temp = self.current_weather.get('main', {}).get('temp', 0)
        weather_main = self.current_weather.get('weather', [{}])[0].get('main', '').lower()
        
        if 'rain' in weather_main:
            alerts.append("🌧️ Giảm tưới nước cho cây trồng")
        elif temp > 33:
            alerts.append("☀️ Tăng tưới nước cho cây trồng")
        elif temp < 10:
            alerts.append("❄️ Che phủ cây non tránh rét")
        elif 'storm' in weather_main:
            alerts.append("⚠️ Thu hoạch sớm cây trồng tránh bão")
        
        return alerts    

    def get_animal_alerts(self):
        """Cảnh báo thời tiết cho vật nuôi"""
        alerts = []
        if not self.current_weather:
            return alerts
        
        temp = self.current_weather.get('main', {}).get('temp', 0)
        weather_main = self.current_weather.get('weather', [{}])[0].get('main', '').lower()
        
        if 'rain' in weather_main:
            alerts.append("🌧️ Che chắn chuồng trại tránh mưa")
        elif temp > 30:
            alerts.append("🔥 Cho vật nuôi uống nhiều nước")
        elif temp < 15:
            alerts.append("❄️ Kiểm tra hệ thống sưởi ấm")
        elif 'storm' in weather_main:
            alerts.append("⚠️ Di chuyển vật nuôi vào nơi an toàn")
        
        return alerts    

    def get_activity_alerts(self):
        """Cảnh báo thời tiết cho hoạt động"""
        alerts = []
        if not self.current_weather:
            return alerts
        
        weather_main = self.current_weather.get('weather', [{}])[0].get('main', '').lower()
        
        if 'rain' in weather_main:
            alerts.append("🌧️ Hoãn các hoạt động ngoài trời")
        elif 'storm' in weather_main:
            alerts.append("⚠️ Hủy mọi hoạt động ngoài trời")
        
        return alerts
    
    