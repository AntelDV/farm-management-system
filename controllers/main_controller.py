import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController
from controllers.crop_controller import CropController
from controllers.animal_controller import AnimalController
from controllers.activity_controller import ActivityController
from controllers.finance_controller import FinanceController
from controllers.inventory_controller import InventoryController
from controllers.weather_controller import WeatherController
from models.report import ReportGenerator
from views.main_view import MainView

class MainController:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Trang Trại")
        self.root.geometry("1100x700")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        # Khởi tạo các controller
        self.auth_controller = AuthController(self)
        self.crop_controller = CropController(self)
        self.animal_controller = AnimalController(self)
        self.activity_controller = ActivityController(self)
        self.finance_controller = FinanceController(self)
        self.inventory_controller = InventoryController(self)
        self.weather_controller = WeatherController(self)
        
        # Khởi tạo view chính
        self.main_view = MainView(self)
        
        # Tạo menu bar
        self.create_menu_bar()
        
        # Hiển thị màn hình đăng nhập ban đầu
        self.auth_controller.show_login_screen()

    def clear_window(self, keep_weather=False):
        """Xóa tất cả widget trên cửa sổ chính"""
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Menu):  # không xóa menu
                if keep_weather and hasattr(self, 'weather_controller'):
                    weather_frame = getattr(self.weather_controller.views, 'weather_frame', None)
                    if weather_frame is not None and widget != weather_frame:
                        widget.destroy()
                else:
                    widget.destroy()

    def show_main_menu(self):
        """Hiển thị menu chính"""
        self.clear_window()    
    
        try:
            if not hasattr(self.auth_controller, 'current_user'):
                self._show_login_screen()
                return
            # Không tự động hiển thị widget thời tiết khi đăng nhập lại
            self.main_view.show_main_menu(self.auth_controller.current_user)
                
        except Exception as e:
            print(f"Lỗi: {str(e)}")
            self._show_fallback_ui()

    def show_management_screen(self, management_func):
        """Hiển thị màn hình quản lý"""
        self.clear_window()    
        # Không tự động hiển thị thời tiết ở các trang quản lý
        management_func()

    def logout(self):
        """Xử lý đăng xuất"""
        # Xử lý weather frame an toàn
        if hasattr(self, 'weather_controller'):
            if hasattr(self.weather_controller.views, 'weather_frame') and self.weather_controller.views.weather_frame is not None:
                try:
                    self.weather_controller.views.weather_frame.destroy()
                except:
                    pass
            
            # Xóa dữ liệu hiển thị
            self.weather_controller.manager.clear_weather_display()
         
        # Đăng xuất
        self.auth_controller.current_user = None
        self.create_menu_bar()
        self.auth_controller.show_login_screen()

    def exit_app(self):
        """Thoát ứng dụng"""
        self.save_all_data()
        self.root.quit()

    def save_all_data(self):
        """Lưu tất cả dữ liệu của các controller"""
        try:
            self.crop_controller.crop_manager.save_data()
            self.animal_controller.animal_manager.save_data()
            self.activity_controller.activity_manager.save_data()
            self.finance_controller.finance_manager.save_data()
            self.inventory_controller.inventory_manager.save_data()
            self.auth_controller.auth_manager.save_users()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi lưu dữ liệu: {str(e)}")

    def export_excel(self):
        """Xuất báo cáo Excel"""
        if not self.auth_controller.current_user or self.auth_controller.current_user["role"] != "admin":
            messagebox.showerror("Lỗi", "Chỉ quản trị viên mới có quyền xuất báo cáo")
            return

        report_type = tk.StringVar(value="crops")
        dialog = tk.Toplevel(self.root)
        dialog.title("Chọn loại báo cáo")
        dialog.geometry("300x250")

        ttk.Label(dialog, text="Chọn loại báo cáo:", font=("Times New Roman", 12)).pack(pady=10)
        ttk.Radiobutton(dialog, text="Cây trồng", variable=report_type, value="crops").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Vật nuôi", variable=report_type, value="animals").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Hoạt động", variable=report_type, value="activities").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Tài chính", variable=report_type, value="finance").pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(dialog, text="Kho", variable=report_type, value="inventory").pack(anchor=tk.W, padx=20)

        def generate_report():
            selected_type = report_type.get()
            data = []
            
            if selected_type == "crops":
                data = self.crop_controller.crop_manager.crops
            elif selected_type == "animals":
                data = self.animal_controller.animal_manager.animals
            elif selected_type == "activities":
                data = self.activity_controller.activity_manager.activities
            elif selected_type == "finance":
                data = self.finance_controller.finance_manager.transactions
            elif selected_type == "inventory":
                data = self.inventory_controller.inventory_manager.inventory
            
            try:
                filepath = ReportGenerator.generate_excel_report(data, selected_type)
                if filepath:
                    messagebox.showinfo("Thành công", f"Báo cáo đã được lưu tại: {filepath}")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo báo cáo: {str(e)}")

        ttk.Button(dialog, text="Xuất báo cáo", command=generate_report, style='Primary.TButton').pack(pady=10)
        ttk.Button(dialog, text="Hủy", command=dialog.destroy, style='Secondary.TButton').pack()

    def create_menu_bar(self):
        """Tạo thanh menu cố định cho ứng dụng"""
        if hasattr(self, 'menubar'):
            self.root.config(menu=None)
         
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
         
        # Menu hệ thống (luôn hiển thị)
        self.system_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Hệ thống", menu=self.system_menu)
         
        # Nếu đã đăng nhập thì thêm các tùy chọn tương ứng
        if hasattr(self.auth_controller, 'current_user') and self.auth_controller.current_user:
            self.system_menu.add_command(label="Đổi mật khẩu", command=self.auth_controller.show_change_password)
            self.system_menu.add_separator()
            self.system_menu.add_command(label="Đăng xuất", command=self.logout)
            self.system_menu.add_command(label="Thoát", command=self.exit_app)
            
            # Thêm menu quản lý/xem dữ liệu tùy theo role
            if self.auth_controller.current_user["role"] == "admin":
                self.management_menu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label="Quản lý", menu=self.management_menu)
                self.management_menu.add_command(label="Cây trồng", command=self.crop_controller.show_crop_management)
                self.management_menu.add_command(label="Vật nuôi", command=self.animal_controller.show_animal_management)
                self.management_menu.add_command(label="Hoạt động", command=self.activity_controller.show_activity_management)
                self.management_menu.add_command(label="Tài chính", command=self.finance_controller.show_finance_management)
                self.management_menu.add_command(label="Kho", command=self.inventory_controller.show_inventory_management)
                self.management_menu.add_command(label="Xuất báo cáo", command=self.export_excel)
            else:
                self.view_menu = tk.Menu(self.menubar, tearoff=0)
                self.menubar.add_cascade(label="Xem dữ liệu", menu=self.view_menu)
                self.view_menu.add_command(label="Cây trồng", command=self.crop_controller.show_crop_view)
                self.view_menu.add_command(label="Vật nuôi", command=self.animal_controller.show_animal_view)
                self.view_menu.add_command(label="Hoạt động", command=self.activity_controller.show_activity_view)
        else:
            # Trạng thái chưa đăng nhập
            self.system_menu.add_command(label="Đăng nhập", command=self.auth_controller.show_login_screen)
            self.system_menu.add_separator()
            self.system_menu.add_command(label="Thoát", command=self.exit_app)

    def update_menu(self):
        """Cập nhật menu theo role người dùng"""
        self.create_menu_bar()

    def _show_fallback_ui(self):
        """Hiển thị giao diện dự phòng khi có lỗi"""
        self.clear_window()
        ttk.Label(self.root, text="Hệ thống tạm thời gián đoạn").pack()
        ttk.Button(self.root, text="Thử lại", command=self.show_main_menu).pack()