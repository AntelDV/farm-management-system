import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles
from tkcalendar import DateEntry

class CropViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()

    def show_crop_management(self):
        self.controller.main.clear_window()
        # Thêm widget thời tiết tổng quan
        if hasattr(self.controller.main, 'weather_controller'):
            weather_view = self.controller.main.weather_controller.views
            weather_view.create_weather_alert_widget(self.controller.main.root)
            
            # Thêm cảnh báo cụ thể cho cây trồng
            crop_alerts = weather_view.get_crop_alerts()
            if crop_alerts:
                alert_frame = ttk.Frame(self.controller.main.root, style='Alert.TFrame')
                alert_frame.pack(fill=tk.X, pady=5, padx=5)
                
                ttk.Label(alert_frame, 
                         text="⚠️ Cảnh báo cho cây trồng: " + " | ".join(crop_alerts),
                         font=('Arial', 9, 'bold'),
                         foreground='#E74C3C').pack(pady=3)
                
        control_frame = ttk.Frame(self.controller.main.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        if self.controller.main.auth_controller.current_user["role"] == "admin":
            ttk.Button(control_frame, text="Thêm cây trồng", 
                      command=self.show_add_crop_form, 
                      style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.crop_search_entry = ttk.Entry(search_frame, width=30)
        self.crop_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", 
                  command=lambda: self.controller.search_crops(self.crop_search_entry.get().lower()), 
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        self.crop_tree = ttk.Treeview(self.controller.main.root, 
                                     columns=("ID", "Tên", "Loại", "Ngày trồng", "Diện tích", "Trạng thái"), 
                                     show="headings")
        
        self.crop_tree.heading("ID", text="ID")
        self.crop_tree.heading("Tên", text="Tên")
        self.crop_tree.heading("Loại", text="Loại")
        self.crop_tree.heading("Ngày trồng", text="Ngày trồng")
        self.crop_tree.heading("Diện tích", text="Diện tích (ha)")
        self.crop_tree.heading("Trạng thái", text="Trạng thái")
        
        self.crop_tree.column("ID", width=50, anchor=tk.CENTER)
        self.crop_tree.column("Tên", width=150)
        self.crop_tree.column("Loại", width=100)
        self.crop_tree.column("Ngày trồng", width=100, anchor=tk.CENTER)
        self.crop_tree.column("Diện tích", width=100, anchor=tk.CENTER)
        self.crop_tree.column("Trạng thái", width=100)
        
        self.crop_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(self.crop_tree, orient=tk.VERTICAL, command=self.crop_tree.yview)
        self.crop_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        action_frame = ttk.Frame(self.controller.main.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        if self.controller.main.auth_controller.current_user["role"] == "admin":
            ttk.Button(action_frame, text="Sửa", 
                      command=self.show_edit_crop_form, 
                      style='Primary.TButton').pack(side=tk.LEFT, padx=5)
            ttk.Button(action_frame, text="Xóa", 
                      command=self.delete_selected_crop, 
                      style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Quay lại", 
                  command=self.controller.main.show_main_menu, 
                  style='Secondary.TButton').pack(side=tk.RIGHT)
        
        self.display_crops()
    
    def show_crop_view(self):
        self.show_crop_management()

    def display_crops(self, crops=None):
        for item in self.crop_tree.get_children():
            self.crop_tree.delete(item)
        
        for idx, crop in enumerate(crops or self.controller.crop_manager.crops, 1):
            self.crop_tree.insert("", tk.END, values=(
                idx,
                crop["name"],
                crop["type"],
                crop["planting_date"],
                crop["area"],
                crop["status"]
            ))

    def show_add_crop_form(self):
        add_window = tk.Toplevel(self.controller.main.root)
        add_window.title("Thêm cây trồng mới")
        add_window.geometry("500x450")
        
        ttk.Label(add_window, text="THÊM CÂY TRỒNG MỚI", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tên cây trồng
        ttk.Label(form_frame, text="Tên cây trồng:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Loại cây
        ttk.Label(form_frame, text="Loại cây:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_entry = ttk.Entry(form_frame)
        self.type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Ngày trồng (DatePicker)
        ttk.Label(form_frame, text="Ngày trồng:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.planting_date_entry = DateEntry(
            form_frame,
            date_pattern='dd/mm/yyyy',
            locale='vi_VN',
            font=('Arial', 10)
        )
        self.planting_date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Diện tích
        ttk.Label(form_frame, text="Diện tích (ha):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.area_entry = ttk.Entry(form_frame)
        self.area_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Trạng thái
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar()
        status_options = ["Đang phát triển", "Thu hoạch", "Bệnh", "Đã hủy"]
        status_combobox = ttk.Combobox(form_frame, textvariable=self.status_var, 
                                      values=status_options, state="readonly")
        status_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        status_combobox.current(0)
        
        # Ghi chú
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Text(form_frame, height=5, width=30)
        self.notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def save_crop():
            crop_data = {
                "name": self.name_entry.get(),
                "type": self.type_entry.get(),
                "planting_date": self.planting_date_entry.get_date().strftime("%d/%m/%Y"),
                "area": self.area_entry.get(),
                "status": self.status_var.get(),
                "notes": self.notes_entry.get("1.0", tk.END).strip()
            }
            
            if not crop_data["name"] or not crop_data["type"]:
                self.show_error_message("Tên và loại cây không được để trống")
                return
            
            try:
                crop_data["area"] = float(crop_data["area"])
                if crop_data["area"] <= 0:
                    self.show_error_message("Diện tích phải lớn hơn 0")
                    return
            except ValueError:
                self.show_error_message("Diện tích phải là số hợp lệ")
                return
            
            if self.controller.add_crop(crop_data):
                add_window.destroy()
        
        ttk.Button(form_frame, text="Lưu", 
                  command=save_crop, 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15)
        
        form_frame.grid_columnconfigure(1, weight=1)

    def show_edit_crop_form(self):
        selected_item = self.crop_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn cây trồng cần sửa")
            return
        
        item_data = self.crop_tree.item(selected_item[0], "values")
        display_id = int(item_data[0])
        crop = self.controller.crop_manager.crops[display_id - 1]
        
        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Sửa thông tin cây trồng")
        edit_window.geometry("500x450")
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN CÂY TRỒNG", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        fields = [
            ("Tên cây trồng:", "name", crop["name"]),
            ("Loại cây:", "type", crop["type"]),
            ("Ngày trồng:", "planting_date", crop["planting_date"]),
            ("Diện tích (ha):", "area", crop["area"])
        ]
        
        self.edit_crop_entries = {}
        for i, (label, field, value) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.insert(0, value)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.edit_crop_entries[field] = entry
        
        # Phần trạng thái dạng Combobox
        ttk.Label(form_frame, text="Trạng thái:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.edit_status_var = tk.StringVar(value=crop["status"])
        status_options = ["Đang phát triển", "Thu hoạch", "Bệnh", "Đã hủy"]
        edit_status_combobox = ttk.Combobox(form_frame, textvariable=self.edit_status_var, 
                                          values=status_options, state="readonly")
        edit_status_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.edit_notes_entry = tk.Text(form_frame, height=5, width=30)
        self.edit_notes_entry.insert("1.0", crop.get("notes", ""))
        self.edit_notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_crop():
            update_data = {
                field: entry.get() for field, entry in self.edit_crop_entries.items()
            }
            update_data["status"] = self.edit_status_var.get()
            update_data["notes"] = self.edit_notes_entry.get("1.0", tk.END).strip()
            
            if not update_data["name"] or not update_data["type"]:
                self.show_error_message("Tên và loại cây không được để trống")
                return
            
            try:
                update_data["area"] = float(update_data["area"])
                if update_data["area"] <= 0:
                    self.show_error_message("Diện tích phải lớn hơn 0")
                    return
            except ValueError:
                self.show_error_message("Diện tích phải là số hợp lệ")
                return
            
            if self.controller.edit_crop(crop["id"], update_data):
                edit_window.destroy()
        
        ttk.Button(form_frame, text="Cập nhật", 
                  command=update_crop, 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15)
    
    def delete_selected_crop(self):
        selected_item = self.crop_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn cây trồng cần xóa")
            return
         
        item_data = self.crop_tree.item(selected_item[0], "values")
        crop_id = int(item_data[0])
         
        # Gọi đúng phương thức với 1 tham số
        self.controller.delete_crop(crop_id)
         
    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)
    
    def show_success_message(self, message):
        messagebox.showinfo("Thành công", message)
    
    def show_confirm_dialog(self, message):
        return messagebox.askyesno("Xác nhận", message)