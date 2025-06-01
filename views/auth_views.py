import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles

class AuthViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()
    
    def show_login_screen(self):
        """Hiển thị giao diện đăng nhập"""
        self.controller.main.clear_window()
        
        login_frame = ttk.Frame(self.controller.main.root, padding="30 15 30 15", style='TFrame')
        login_frame.pack(expand=True)
        
        # Tiêu đề
        ttk.Label(login_frame, text="ĐĂNG NHẬP HỆ THỐNG", style='Header.TLabel').grid(
            row=0, column=0, columnspan=2, pady=10
        )
        
        # Tên đăng nhập
        ttk.Label(login_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(login_frame, font=('Times New Roman', 10))
        self.username_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Mật khẩu
        ttk.Label(login_frame, text="Mật khẩu:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", font=('Times New Roman', 10))
        self.password_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Nút đăng nhập
        ttk.Button(
            login_frame, 
            text="Đăng nhập", 
            command=self._on_login,
            style='Primary.TButton'
        ).grid(row=3, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        # Nút đăng ký
        ttk.Button(
            login_frame, 
            text="Đăng ký tài khoản mới", 
            command=self.controller.show_register_screen,
            style='Secondary.TButton'
        ).grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.EW)
        
        # Cấu hình grid
        login_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)
        
        # Focus vào ô username
        self.username_entry.focus()
    
    def show_register_screen(self):
        """Hiển thị giao diện đăng ký"""
        self.controller.main.clear_window()
        
        register_frame = ttk.Frame(self.controller.main.root, padding="30 15 30 15", style='TFrame')
        register_frame.pack(expand=True)
        
        # Tiêu đề
        ttk.Label(register_frame, text="ĐĂNG KÝ TÀI KHOẢN MỚI", style='Header.TLabel').grid(
            row=0, column=0, columnspan=2, pady=10
        )
        
        # Tên đăng nhập
        ttk.Label(register_frame, text="Tên đăng nhập:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_username = ttk.Entry(register_frame, font=('Times New Roman', 10))
        self.reg_username.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Mật khẩu
        ttk.Label(register_frame, text="Mật khẩu:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_password = ttk.Entry(register_frame, show="*", font=('Times New Roman', 10))
        self.reg_password.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Xác nhận mật khẩu
        ttk.Label(register_frame, text="Xác nhận mật khẩu:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_confirm = ttk.Entry(register_frame, show="*", font=('Times New Roman', 10))
        self.reg_confirm.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Loại tài khoản
        ttk.Label(register_frame, text="Loại tài khoản:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.user_role = tk.StringVar(value="user")
        ttk.Radiobutton(
            register_frame, 
            text="Người dùng thường", 
            variable=self.user_role, 
            value="user"
        ).grid(row=4, column=1, sticky=tk.W)
        
        ttk.Radiobutton(
            register_frame, 
            text="Quản trị viên", 
            variable=self.user_role, 
            value="admin"
        ).grid(row=5, column=1, sticky=tk.W)
        
        # Nút đăng ký
        ttk.Button(
            register_frame, 
            text="Đăng ký", 
            command=self._on_register,
            style='Primary.TButton'
        ).grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        # Nút quay lại
        ttk.Button(
            register_frame, 
            text="Quay lại đăng nhập", 
            command=self.controller.show_login_screen,
            style='Secondary.TButton'
        ).grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.EW)
        
        # Cấu hình grid
        register_frame.grid_columnconfigure(0, weight=1)
        register_frame.grid_columnconfigure(1, weight=1)
        
        # Focus vào ô username
        self.reg_username.focus()
    
    def show_change_password_form(self):
        """Hiển thị form đổi mật khẩu"""
        change_pass_window = tk.Toplevel(self.controller.main.root)
        change_pass_window.title("Đổi mật khẩu")
        change_pass_window.geometry("400x250")
        
        # Tiêu đề
        ttk.Label(
            change_pass_window, 
            text="ĐỔI MẬT KHẨU", 
            style='Header.TLabel'
        ).pack(pady=10)
        
        form_frame = ttk.Frame(change_pass_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Mật khẩu hiện tại
        ttk.Label(form_frame, text="Mật khẩu hiện tại:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.current_pass_entry = ttk.Entry(form_frame, show="*")
        self.current_pass_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Mật khẩu mới
        ttk.Label(form_frame, text="Mật khẩu mới:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.new_pass_entry = ttk.Entry(form_frame, show="*")
        self.new_pass_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Xác nhận mật khẩu mới
        ttk.Label(form_frame, text="Xác nhận mật khẩu:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.confirm_pass_entry = ttk.Entry(form_frame, show="*")
        self.confirm_pass_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Nút đổi mật khẩu
        ttk.Button(
            form_frame, 
            text="Đổi mật khẩu", 
            command=self._on_change_password,
            style='Primary.TButton'
        ).grid(row=3, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        # Cấu hình grid
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Focus vào ô mật khẩu hiện tại
        self.current_pass_entry.focus()
    
    def _on_login(self):
        """Xử lý sự kiện đăng nhập"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # thêm validation logic nếu cần
        if not username or not password:
            self.show_error_message("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return 
        try:
            self.controller.handle_login(username, password)
        except Exception as e:
            self.show_error_message(f"Đăng nhập thất bại: {str(e)}")

    
    def _on_register(self):
        """Xử lý sự kiện đăng ký"""
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        role = self.user_role.get()
        self.controller.handle_register(username, password, confirm, role)
    
    def _on_change_password(self):
        """Xử lý sự kiện đổi mật khẩu"""
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        self.controller.handle_change_password(current_pass, new_pass, confirm_pass)
    
    def show_error_message(self, message):
        """Hiển thị thông báo lỗi"""
        messagebox.showerror("Lỗi", message)
    
    def show_success_message(self, message):
        """Hiển thị thông báo thành công"""
        messagebox.showinfo("Thành công", message)