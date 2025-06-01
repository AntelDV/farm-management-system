import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles
from tkcalendar import DateEntry


class AnimalViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()


    def show_animal_management(self):
        self.controller.main.clear_window()

        # Thêm widget thời tiết tổng quan
        if hasattr(self.controller.main, 'weather_controller'):
            weather_view = self.controller.main.weather_controller.views
            weather_view.create_weather_alert_widget(self.controller.main.root)

            # Thêm cảnh báo cụ thể cho vật nuôi
            animal_alerts = weather_view.get_animal_alerts()
            if animal_alerts:
                alert_frame = ttk.Frame(self.controller.main.root, style='Alert.TFrame')
                alert_frame.pack(fill=tk.X, pady=5, padx=5)

                ttk.Label(alert_frame,
                         text="⚠️ Cảnh báo cho vật nuôi: " + " | ".join(animal_alerts),
                         font=('Arial', 9, 'bold'),
                         foreground='#E74C3C').pack(pady=3)

        control_frame = ttk.Frame(self.controller.main.root, padding="10")
        control_frame.pack(fill=tk.X)

        if self.controller.main.auth_controller.current_user["role"] == "admin":
            ttk.Button(
                control_frame,
                text="Thêm vật nuôi",
                command=self.show_add_animal_form,
                style="Primary.TButton",
            ).pack(side=tk.LEFT, padx=5)

        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)

        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.animal_search_entry = ttk.Entry(search_frame, width=30)
        self.animal_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(
            search_frame,
            text="Tìm",
            command=lambda: self.controller.search_animals(
                self.animal_search_entry.get().lower()
            ),
            style="Secondary.TButton",
        ).pack(side=tk.LEFT)

        self.animal_tree = ttk.Treeview(
            self.controller.main.root,
            columns=("ID", "Tên", "Loại", "Ngày nhập", "Số lượng", "Trạng thái"),
            show="headings",
        )

        self.animal_tree.heading("ID", text="ID")
        self.animal_tree.heading("Tên", text="Tên")
        self.animal_tree.heading("Loại", text="Loại")
        self.animal_tree.heading("Ngày nhập", text="Ngày nhập")
        self.animal_tree.heading("Số lượng", text="Số lượng")
        self.animal_tree.heading("Trạng thái", text="Trạng thái")

        self.animal_tree.column("ID", width=50, anchor=tk.CENTER)
        self.animal_tree.column("Tên", width=150)
        self.animal_tree.column("Loại", width=100)
        self.animal_tree.column("Ngày nhập", width=100, anchor=tk.CENTER)
        self.animal_tree.column("Số lượng", width=80, anchor=tk.CENTER)
        self.animal_tree.column("Trạng thái", width=100)

        self.animal_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(
            self.animal_tree, orient=tk.VERTICAL, command=self.animal_tree.yview
        )
        self.animal_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        action_frame = ttk.Frame(self.controller.main.root, padding="10")
        action_frame.pack(fill=tk.X)

        if self.controller.main.auth_controller.current_user["role"] == "admin":
            ttk.Button(
                action_frame,
                text="Sửa",
                command=self.show_edit_animal_form,
                style="Primary.TButton",
            ).pack(side=tk.LEFT, padx=5)
            ttk.Button(
                action_frame,
                text="Xóa",
                command=self.delete_selected_animal,
                style="Danger.TButton",
            ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            action_frame,
            text="Quay lại",
            command=self.controller.main.show_main_menu,
            style="Secondary.TButton",
        ).pack(side=tk.RIGHT)

        self.display_animals()

    def show_animal_view(self):
        self.show_animal_management()
        
    def display_animals(self, animals=None):
        for item in self.animal_tree.get_children():
            self.animal_tree.delete(item)

        for idx, animal in enumerate(
            animals or self.controller.animal_manager.animals, 1
        ):
            self.animal_tree.insert(
                "",
                tk.END,
                values=(
                    idx,
                    animal["name"],
                    animal["type"],
                    animal["entry_date"],
                    animal["quantity"],
                    animal["status"],
                ),
            )

    def show_add_animal_form(self):
        add_window = tk.Toplevel(self.controller.main.root)
        add_window.title("Thêm vật nuôi mới")
        add_window.geometry("500x450")

        ttk.Label(add_window, text="THÊM VẬT NUÔI MỚI", style="Header.TLabel").pack(
            pady=10
        )

        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)

        # Tên vật nuôi
        ttk.Label(form_frame, text="Tên vật nuôi:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)

        # Loại vật nuôi
        ttk.Label(form_frame, text="Loại vật nuôi:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.type_entry = ttk.Entry(form_frame)
        self.type_entry.grid(row=1, column=1, pady=5, padx=5, sticky=tk.EW)

        # Ngày nhập (DatePicker)
        ttk.Label(form_frame, text="Ngày nhập:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.entry_date_entry = DateEntry(
            form_frame, date_pattern="dd/mm/yyyy", locale="vi_VN", font=("Arial", 10)
        )
        self.entry_date_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)

        # Số lượng
        ttk.Label(form_frame, text="Số lượng:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)

        # Trạng thái
        ttk.Label(form_frame, text="Trạng thái:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.status_var = tk.StringVar()
        status_options = ["Khỏe mạnh", "Bệnh", "Đang điều trị", "Đã xuất chuồng"]
        status_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=status_options,
            state="readonly",
        )
        status_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        status_combobox.current(0)

        # Ghi chú
        ttk.Label(form_frame, text="Ghi chú:").grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        self.notes_entry = tk.Text(form_frame, height=5, width=30)
        self.notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)

        # Nút lưu
        ttk.Button(
            form_frame,
            text="Lưu",
            command=lambda: self.save_animal(add_window),
            style="Primary.TButton",
        ).grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)

        form_frame.grid_columnconfigure(1, weight=1)

    def save_animal(self, window):
        animal_data = {
            "name": self.name_entry.get(),
            "type": self.type_entry.get(),
            "entry_date": self.entry_date_entry.get_date().strftime("%d/%m/%Y"),
            "quantity": self.quantity_entry.get(),
            "status": self.status_var.get(),
            "notes": self.notes_entry.get("1.0", tk.END).strip(),
        }

        # Validate và xử lý lưu dữ liệu
        if not animal_data["name"] or not animal_data["type"]:
            self.show_error_message("Tên và loại vật nuôi không được để trống")
            return

        try:
            animal_data["quantity"] = int(animal_data["quantity"])
            if animal_data["quantity"] <= 0:
                self.show_error_message("Số lượng phải lớn hơn 0")
                return
        except ValueError:
            self.show_error_message("Số lượng phải là số nguyên")
            return

        if self.controller.add_animal(animal_data):
            window.destroy()

    def show_edit_animal_form(self):
        selected_item = self.animal_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn vật nuôi cần sửa")
            return

        item_data = self.animal_tree.item(selected_item[0], "values")
        display_id = int(item_data[0])
        animal = self.controller.animal_manager.animals[display_id - 1]

        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Sửa thông tin vật nuôi")
        edit_window.geometry("500x450")

        ttk.Label(
            edit_window, text="SỬA THÔNG TIN VẬT NUÔI", style="Header.TLabel"
        ).pack(pady=10)

        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)

        fields = [
            ("Tên vật nuôi:", "name", animal["name"]),
            ("Loại vật nuôi:", "type", animal["type"]),
            ("Ngày nhập:", "entry_date", animal["entry_date"]),
            ("Số lượng:", "quantity", str(animal["quantity"])),
        ]

        self.edit_animal_entries = {}
        for i, (label, field, value) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.insert(0, value)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.edit_animal_entries[field] = entry

        # Phần trạng thái dạng Combobox
        ttk.Label(form_frame, text="Trạng thái:").grid(
            row=4, column=0, sticky=tk.W, pady=5
        )
        self.edit_status_var = tk.StringVar(value=animal["status"])
        status_options = ["Khỏe mạnh", "Bệnh", "Đang điều trị", "Đã xuất chuồng"]
        edit_status_combobox = ttk.Combobox(
            form_frame,
            textvariable=self.edit_status_var,
            values=status_options,
            state="readonly",
        )
        edit_status_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)

        ttk.Label(form_frame, text="Ghi chú:").grid(
            row=5, column=0, sticky=tk.W, pady=5
        )
        self.edit_notes_entry = tk.Text(form_frame, height=5, width=30)
        self.edit_notes_entry.insert("1.0", animal.get("notes", ""))
        self.edit_notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)

        def update_animal():
            update_data = {
                field: entry.get() for field, entry in self.edit_animal_entries.items()
            }
            update_data["status"] = self.edit_status_var.get()
            update_data["notes"] = self.edit_notes_entry.get("1.0", tk.END).strip()

            if not update_data["name"] or not update_data["type"]:
                self.show_error_message("Tên và loại vật nuôi không được để trống")
                return

            try:
                update_data["quantity"] = int(update_data["quantity"])
                if update_data["quantity"] <= 0:
                    self.show_error_message("Số lượng phải lớn hơn 0")
                    return
            except ValueError:
                self.show_error_message("Số lượng phải là số nguyên")
                return

            if self.controller.edit_animal(animal["id"], update_data):
                edit_window.destroy()

        ttk.Button(
            form_frame, text="Cập nhật", command=update_animal, style="Primary.TButton"
        ).grid(row=6, column=0, columnspan=2, pady=15)

    
    def delete_selected_animal(self):
        selected_item = self.animal_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn vật nuôi cần xóa")
            return

        item_data = self.animal_tree.item(selected_item[0], "values")
        animal_id = int(item_data[0])

        # Gọi đúng phương thức với 1 tham số
        self.controller.delete_animal(animal_id)

    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)

    def show_success_message(self, message):
        messagebox.showinfo("Thành công", message)
    def show_confirm_dialog(self, message):
        return messagebox.askyesno("Xác nhận", message)