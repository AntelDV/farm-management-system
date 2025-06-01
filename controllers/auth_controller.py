from tkinter import messagebox
from views.auth_views import AuthViews
from models.auth import AuthManager

class AuthController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = AuthViews(self)
        self.auth_manager = AuthManager()
        self.current_user = None
    
    def show_login_screen(self):
        """Hiển thị màn hình đăng nhập"""
        self.views.show_login_screen()
    
    def show_register_screen(self):
        """Hiển thị màn hình đăng ký"""
        self.views.show_register_screen()
    
    def show_change_password(self):
        """Hiển thị form đổi mật khẩu"""
        if self.current_user:
            self.views.show_change_password_form()
    
    def handle_login(self, username, password):
        """Xử lý đăng nhập"""
        result = self.auth_manager.login(username, password)
        if result["success"]:
            self.current_user = result["user"]
            self.main.update_menu()  # cập nhật menu theo vai trò
            self.main.show_main_menu()
            self.views.show_success_message(result["message"])
        else:
            self.views.show_error_message(result["message"])
    
    def handle_register(self, username, password, confirm, role):
        """Xử lý đăng ký"""
        if not username or not password:
            self.views.show_error_message("Tên đăng nhập và mật khẩu không được để trống")
            return
            
        if password != confirm:
            self.views.show_error_message("Mật khẩu xác nhận không khớp")
            return
            
        result = self.auth_manager.register_user(username, password, role)
        if result["success"]:
            self.views.show_success_message(result["message"])
            self.show_login_screen()
        else:
            self.views.show_error_message(result["message"])
    
    def handle_change_password(self, current_password, new_password, confirm_password):
        """Xử lý đổi mật khẩu"""
        if not self.current_user:
            return
            
        if new_password != confirm_password:
            self.views.show_error_message("Mật khẩu mới và xác nhận không khớp")
            return
            
        result = self.auth_manager.change_password(
            self.current_user["username"],
            current_password,
            new_password
        )
        
        if result["success"]:
            self.views.show_success_message(result["message"])
            self.main.show_main_menu()
        else:
            self.views.show_error_message(result["message"])
    
    def logout(self):
        """Xử lý đăng xuất"""
        if hasattr(self.main, 'weather_controller'):
            # Xóa toàn bộ dữ liệu và widget thời tiết
            self.main.weather_controller.manager.clear_all_weather_data()
            self.main.weather_controller.views.clear_weather_display()
     
        self.current_user = None
        self.main.clear_widget()
        self.show_login_screen()