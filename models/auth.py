import json
import os
from datetime import datetime

class AuthManager:
    def __init__(self):
        self.users = []
        self.current_user = None
        self.users_file = "data/users.json"
        self._ensure_data_directory()
        self.load_users()
        
    def _ensure_data_directory(self):
        """Đảm bảo thư mục data tồn tại"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        
    def load_users(self):
        """Tải danh sách người dùng từ file JSON"""
        try:
            if os.path.exists(self.users_file) and os.path.getsize(self.users_file) > 0:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            else:
                # Tạo admin mặc định nếu file không tồn tại hoặc trống
                self.users = [
                    {
                        "username": "admin",
                        "password": "admin123",
                        "role": "admin",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ]
                self.save_users()
        except Exception as e:
            print(f"Lỗi khi tải người dùng: {str(e)}")
            self.users = []

    def save_users(self):
        """Lưu danh sách người dùng vào file JSON"""
        try:
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu người dùng: {str(e)}")

    def register_user(self, username, password, role="user"):
        """Đăng ký người dùng mới"""
        if not username or not password:
            return {"success": False, "message": "Tên đăng nhập và mật khẩu không được để trống"}
            
        if any(user["username"] == username for user in self.users):
            return {"success": False, "message": "Tên đăng nhập đã tồn tại"}
            
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.users.append(new_user)
        self.save_users()
        return {"success": True, "message": "Đăng ký thành công", "user": new_user}

    def login(self, username, password):
        """Đăng nhập hệ thống"""
        try:
            for user in self.users:
                if user["username"] == username and user["password"] == password:
                    self.current_user = user
                    return {
                        "success": True, 
                        "message": "Đăng nhập thành công",  
                        "user": user
                    }
            return {
                "success": False, 
                "message": "Tên đăng nhập hoặc mật khẩu không đúng"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi hệ thống: {str(e)}"
            }
    def change_password(self, username, current_password, new_password):
        """Đổi mật khẩu người dùng"""
        for user in self.users:
            if user["username"] == username and user["password"] == current_password:
                user["password"] = new_password
                user["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_users()
                return {"success": True, "message": "Đổi mật khẩu thành công"}
        return {"success": False, "message": "Mật khẩu hiện tại không đúng"}

    def logout(self):
        """Đăng xuất hệ thống"""
        self.current_user = None
        return {"success": True, "message": "Đăng xuất thành công"}