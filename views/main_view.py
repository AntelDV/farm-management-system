import tkinter as tk
from tkinter import ttk
from views.styles import configure_styles

class MainView:
    def __init__(self, main_controller):
        self.main = main_controller
        self.style = configure_styles()

    def show_main_menu(self, current_user):
        self.main.clear_window()

        # Tạo thanh menu cố định
        menubar = tk.Menu(self.main.root)
        self.main.root.config(menu=menubar)

        # Menu hệ thống
        system_menu = tk.Menu(menubar, tearoff=0)
        system_menu.add_command(
            label="Đổi mật khẩu", command=self.main.auth_controller.show_change_password
        )
        system_menu.add_separator()
        system_menu.add_command(label="Đăng xuất", command=self.main.logout)
        system_menu.add_command(label="Thoát", command=self.main.exit_app)
        menubar.add_cascade(label="Hệ thống", menu=system_menu)

        # Menu xem dữ liệu (chỉ cho user)
        if current_user["role"] == "user":
            view_menu = tk.Menu(menubar, tearoff=0)
            view_menu.add_command(
                label="Xem cây trồng", command=self.main.crop_controller.show_crop_view
            )
            view_menu.add_command(
                label="Xem vật nuôi",
                command=self.main.animal_controller.show_animal_view,
            )
            view_menu.add_command(
                label="Xem hoạt động",
                command=self.main.activity_controller.show_activity_view,
            )
            menubar.add_cascade(label="Xem dữ liệu", menu=view_menu)

        # Menu quản lý (chỉ admin)
        if current_user["role"] == "admin":
            management_menu = tk.Menu(menubar, tearoff=0)
            management_menu.add_command(
                label="Quản lý cây trồng",
                command=self.main.crop_controller.show_crop_management,
            )
            management_menu.add_command(
                label="Quản lý vật nuôi",
                command=self.main.animal_controller.show_animal_management,
            )
            management_menu.add_command(
                label="Quản lý hoạt động",
                command=self.main.activity_controller.show_activity_management,
            )
            management_menu.add_command(
                label="Quản lý tài chính",
                command=self.main.finance_controller.show_finance_management,
            )
            management_menu.add_command(
                label="Quản lý kho",
                command=self.main.inventory_controller.show_inventory_management,
            )
            management_menu.add_command(
                label="Xuất báo cáo", command=self.main.export_excel
            )
            menubar.add_cascade(label="Quản lý", menu=management_menu)

        # Hiển thị dashboard
        self.show_enhanced_dashboard(current_user)

        # Chỉ hiển thị thời tiết cho admin
        if current_user["role"] == "admin":
            self.main.weather_controller.show_weather_widget()


    def show_enhanced_dashboard(self, current_user):
        dashboard_frame = ttk.Frame(self.main.root, padding="20")
        dashboard_frame.pack(expand=True, fill=tk.BOTH)

        # Header
        header_frame = ttk.Frame(dashboard_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            header_frame,
            text=f"TRANG CHỦ - XIN CHÀO {current_user['username'].upper()}",
            style="Header.TLabel",
        ).pack(side=tk.LEFT)

        # Thống kê nhanh
        stats_frame = ttk.LabelFrame(dashboard_frame, text="Thống kê nhanh", padding="15")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Chỉ hiển thị Giao dịch và Vật tư cho admin
        stats_data = [
            (
                "Cây trồng",
                len(self.main.crop_controller.crop_manager.crops),
                "#4CAF50",
                (
                    self.main.crop_controller.show_crop_management
                    if current_user["role"] == "admin"
                    else self.main.crop_controller.show_crop_view
                ),
            ),
            (
                "Vật nuôi",
                len(self.main.animal_controller.animal_manager.animals),
                "#2196F3",
                (
                    self.main.animal_controller.show_animal_management
                    if current_user["role"] == "admin"
                    else self.main.animal_controller.show_animal_view
                ),
            ),
            (
                "Hoạt động",
                len(self.main.activity_controller.activity_manager.activities),
                "#FF9800",
                (
                    self.main.activity_controller.show_activity_management
                    if current_user["role"] == "admin"
                    else self.main.activity_controller.show_activity_view
                ),
            ),
        ]

        # Chỉ thêm Giao dịch và Vật tư nếu là admin
        if current_user["role"] == "admin":
            stats_data.extend([
                (
                    "Giao dịch",
                    len(self.main.finance_controller.finance_manager.transactions),
                    "#9C27B0",
                    self.main.finance_controller.show_finance_management,
                ),
                (
                    "Vật tư",
                    len(self.main.inventory_controller.inventory_manager.inventory),
                    "#607D8B",
                    self.main.inventory_controller.show_inventory_management,
                ),
            ])

        for i, (title, count, color, command) in enumerate(stats_data):
            stat_frame = ttk.Frame(
                stats_frame, relief=tk.RAISED, borderwidth=1, style="StatFrame.TFrame"
            )
            stat_frame.grid(row=0, column=i, padx=10, sticky=tk.NSEW)
            stat_frame.columnconfigure(0, weight=1)

            # Title
            title_label = ttk.Label(
                stat_frame,
                text=title,
                style="StatTitle.TLabel",
                background=color,
                foreground="white",
                padding=5,
                anchor="center",
            )
            title_label.grid(row=0, column=0, sticky="ew")

            # Value
            value_label = ttk.Label(
                stat_frame,
                text=str(count),
                style="StatValue.TLabel",
                padding=10,
                anchor="center",
            )
            value_label.grid(row=1, column=0, sticky="nsew")

            # Thêm sự kiện click
            if command:
                title_label.bind("<Button-1>", lambda e, cmd=command: cmd())
                value_label.bind("<Button-1>", lambda e, cmd=command: cmd())
                title_label.config(cursor="hand2")
                value_label.config(cursor="hand2")

            stats_frame.columnconfigure(i, weight=1)