import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles
from tkcalendar import DateEntry
class ActivityViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()
    
    def show_activity_management(self):
        self.controller.main.clear_window()
        # Thêm widget thời tiết tổng quan
        if hasattr(self.controller.main, 'weather_controller'):
            weather_view = self.controller.main.weather_controller.views
            weather_view.create_weather_alert_widget(self.controller.main.root)

            # Thêm cảnh báo cụ thể cho hoạt động
            activity_alerts = weather_view.get_activity_alerts()
            if activity_alerts:
                alert_frame = ttk.Frame(self.controller.main.root, style='Alert.TFrame')
                alert_frame.pack(fill=tk.X, pady=5, padx=5)

                ttk.Label(alert_frame,
                         text="⚠️ Cảnh báo cho hoạt động: " + " | ".join(activity_alerts),
                         font=('Arial', 9, 'bold'),
                         foreground='#E74C3C').pack(pady=3)

        # Control frame (top)
        control_frame = ttk.Frame(self.controller.main.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        if self.controller.main.auth_controller.current_user["role"] == "admin":
            ttk.Button(control_frame, 
                      text="Thêm hoạt động", 
                      command=self.show_add_activity_form,
                      style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, 
                  text="Tìm", 
                  command=lambda: self.controller.search_activities(self.search_entry.get()),
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Treeview
        self.tree = ttk.Treeview(self.controller.main.root, 
                                columns=("ID", "Tên", "Loại", "Ngày", "Trạng thái", "Người phụ trách"), 
                                show="headings")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên hoạt động")
        self.tree.heading("Loại", text="Loại hoạt động")
        self.tree.heading("Ngày", text="Ngày thực hiện")
        self.tree.heading("Trạng thái", text="Trạng thái")
        self.tree.heading("Người phụ trách", text="Người phụ trách")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Tên", width=200)
        self.tree.column("Loại", width=120)
        self.tree.column("Ngày", width=100, anchor=tk.CENTER)
        self.tree.column("Trạng thái", width=100)
        self.tree.column("Người phụ trách", width=150)
        
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action frame (bottom)
        action_frame = ttk.Frame(self.controller.main.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        if self.controller.main.auth_controller.current_user["role"] == "admin":
            ttk.Button(action_frame,
                      text="Sửa",
                      command=self.controller.show_edit_activity_form,
                      style='Primary.TButton').pack(side=tk.LEFT, padx=5)
            
            ttk.Button(action_frame,
                      text="Xóa",
                      command=self.controller.delete_activity,
                      style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame,
                  text="Quay lại",
                  command=self.controller.main.show_main_menu,
                  style='Secondary.TButton').pack(side=tk.RIGHT)
        
        self.display_activities()
    
    def show_activity_view(self):
        self._setup_ui(show_buttons=False)
    
    def display_activities(self, activities=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        # Hiển thị theo thứ tự ID mới
        for activity in activities or self.controller.activity_manager.activities:
            self.tree.insert("", tk.END, values=(
                activity["id"],  # Hiển thị ID đã được cập nhật
                activity["name"],
                activity["type"],
                activity.get("date", ""),
                activity.get("status", "Đang lên kế hoạch"),
                activity.get("responsible", "")
            ))
    
    def get_selected_activity(self):
        selected_item = self.tree.focus()
        if selected_item:
            item_data = self.tree.item(selected_item)
            activity_id = item_data["values"][0]
            return self.controller.get_activity_by_id(activity_id)
        return None

    def show_add_activity_form(self):
        add_window = tk.Toplevel(self.controller.main.root)
        add_window.title("Thêm hoạt động mới")
        add_window.geometry("500x450")
        
        ttk.Label(add_window, text="THÊM HOẠT ĐỘNG MỚI", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tên hoạt động
        ttk.Label(form_frame, text="Tên hoạt động:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Loại hoạt động
        ttk.Label(form_frame, text="Loại hoạt động:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_entry = ttk.Entry(form_frame)
        self.type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Ngày thực hiện (DatePicker)
        ttk.Label(form_frame, text="Ngày thực hiện:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = DateEntry(
            form_frame,
            date_pattern='dd/mm/yyyy',
            locale='vi_VN',
            font=('Arial', 10)
        )
        self.date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Người phụ trách
        ttk.Label(form_frame, text="Người phụ trách:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.responsible_entry = ttk.Entry(form_frame)
        self.responsible_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Trạng thái
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar()
        status_options = ["Đang lên kế hoạch", "Đang diễn ra", "Đã hoàn thành", "Đã hủy"]
        status_combobox = ttk.Combobox(form_frame, textvariable=self.status_var, 
                                     values=status_options, state="readonly")
        status_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        status_combobox.current(0)
        
        # Mô tả
        ttk.Label(form_frame, text="Mô tả:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.description_text = tk.Text(form_frame, height=5, width=30)
        self.description_text.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Nút lưu
        ttk.Button(form_frame, text="Lưu", 
                  command=lambda: self.save_activity(add_window), 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)

    def save_activity(self, window):
        activity_data = {
            "name": self.name_entry.get(),
            "type": self.type_entry.get(),
            "date": self.date_entry.get_date().strftime("%d/%m/%Y"),
            "responsible": self.responsible_entry.get(),
            "status": self.status_var.get(),
            "description": self.description_text.get("1.0", tk.END).strip()
        }
        
        if not activity_data["name"] or not activity_data["type"]:
            self.show_error_message("Tên và loại hoạt động không được để trống")
            return
        
        if self.controller.add_activity(activity_data):
            window.destroy()
    
    def show_edit_activity_form(self, activity_data):
        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Chỉnh sửa hoạt động")
        edit_window.geometry("500x450")
        
        ttk.Label(edit_window, text="CHỈNH SỬA HOẠT ĐỘNG", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        fields = [
            ("Tên hoạt động:", "name", activity_data["name"]),
            ("Loại hoạt động:", "type", activity_data["type"]),
            ("Ngày thực hiện:", "date", activity_data.get("date", "")),
            ("Người phụ trách:", "responsible", activity_data.get("responsible", ""))
        ]
        
        self.edit_activity_entries = {}
        for i, (label, field, value) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.insert(0, value)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.edit_activity_entries[field] = entry
        
        # Combobox trạng thái khi chỉnh sửa
        ttk.Label(form_frame, text="Trạng thái:").grid(row=len(fields), column=0, sticky=tk.W, pady=5)
        self.edit_status_var = tk.StringVar(value=activity_data.get("status", "Đang lên kế hoạch"))
        status_options = ["Đang lên kế hoạch", "Đang diễn ra", "Đã hoàn thành", "Đã hủy"]
        edit_status_combobox = ttk.Combobox(form_frame, textvariable=self.edit_status_var,
                                          values=status_options, state="readonly")
        edit_status_combobox.grid(row=len(fields), column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Mô tả:").grid(row=len(fields)+1, column=0, sticky=tk.W, pady=5)
        self.edit_description_text = tk.Text(form_frame, height=5, width=30)
        self.edit_description_text.insert("1.0", activity_data.get("description", ""))
        self.edit_description_text.grid(row=len(fields)+1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_activity():
            update_data = {
                field: entry.get() for field, entry in self.edit_activity_entries.items()
            }
            update_data["status"] = self.edit_status_var.get()
            update_data["description"] = self.edit_description_text.get("1.0", tk.END).strip()
            
            if not update_data["name"] or not update_data["type"]:
                self.show_error_message("Tên và loại hoạt động không được để trống")
                return
            
            if self.controller.edit_activity(activity_data["id"], update_data):
                edit_window.destroy()
        
        ttk.Button(form_frame, 
                  text="Cập nhật", 
                  command=update_activity, 
                  style='Primary.TButton').grid(row=len(fields)+2, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_confirm_dialog(self, message):
        return messagebox.askyesno("Xác nhận", message)
    
    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)
    
    def show_success_message(self, message):
        messagebox.showinfo("Thành công", message)