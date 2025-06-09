import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles

class InventoryViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()
        self.suppliers_window = None
        self.add_supplier_window = None
        self.edit_supplier_window = None

    def show_inventory_management(self):
        self.controller.main.clear_window()
        
        # Control frame
        control_frame = ttk.Frame(self.controller.main.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Thêm vật tư", 
                  command=self.show_add_item_form, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Nhà cung cấp", 
                  command=self.controller.show_suppliers, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Search
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.controller.search_inventory(self.search_entry.get()))
        ttk.Button(search_frame, text="Tìm", 
                  command=lambda: self.controller.search_inventory(self.search_entry.get()), 
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Treeview
        columns = ("ID", "Tên", "Số lượng", "Đơn vị", "Đơn giá", "Tổng giá trị", "Nhà cung cấp")
        self.tree = ttk.Treeview(self.controller.main.root, columns=columns, show="headings", height=20)
        
        # Configure columns
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Tên", width=150)
        self.tree.column("Số lượng", width=80, anchor=tk.E)
        self.tree.column("Đơn vị", width=80, anchor=tk.CENTER)
        self.tree.column("Đơn giá", width=100, anchor=tk.E)
        self.tree.column("Tổng giá trị", width=120, anchor=tk.E)
        self.tree.column("Nhà cung cấp", width=150)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Total value
        value_frame = ttk.Frame(self.controller.main.root)
        value_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.value_label = ttk.Label(value_frame, 
                                   text=f"Tổng giá trị kho: {self._format_currency(self.controller.get_inventory_value())}", 
                                   font=('Times New Roman', 10, 'bold'))
        self.value_label.pack(side=tk.RIGHT)
        
        # Action buttons
        action_frame = ttk.Frame(self.controller.main.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Sửa", 
                  command=self.show_edit_item_form, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Xóa", 
                  command=self.delete_selected_item, 
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Sử dụng", 
                  command=self.show_use_item_form, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Quay lại", 
                  command=self.controller.main.show_main_menu, 
                  style='Secondary.TButton').pack(side=tk.RIGHT)
        
        self.display_inventory()

    def display_inventory(self, items=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        items_to_display = items if items is not None else self.controller.inventory_manager.inventory
        
        for idx, item in enumerate(items_to_display, 1):
            supplier_name = "N/A"
            if "supplier" in item:
                supplier = next((s for s in self.controller.inventory_manager.suppliers 
                               if s["id"] == item["supplier"]), None)
                supplier_name = supplier["name"] if supplier else "N/A"
            
            total_value = item["current_quantity"] * item["unit_price"]
            self.tree.insert("", tk.END, values=(
                idx,
                item["name"],
                item["current_quantity"],
                item["unit"],
                f"{item['unit_price']:,.0f}",
                f"{total_value:,.0f}",
                supplier_name
            ))
        
        self.update_inventory_value()

    def update_inventory_value(self):
        total_value = sum(item["current_quantity"] * item["unit_price"] 
                       for item in self.controller.inventory_manager.inventory)
        self.value_label.config(text=f"Tổng giá trị kho: {self._format_currency(total_value)}")

    def show_add_item_form(self):
        add_window = tk.Toplevel(self.controller.main.root)
        add_window.title("Thêm vật tư mới")
        add_window.geometry("500x450")
        add_window.grab_set()
        
        ttk.Label(add_window, text="THÊM VẬT TƯ MỚI", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        fields = [
            ("Tên vật tư:", "name"),
            ("Số lượng:", "quantity"),
            ("Đơn vị:", "unit"),
            ("Đơn giá:", "unit_price")
        ]
        
        self.add_item_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.add_item_entries[field] = entry
        
        # Supplier combobox
        ttk.Label(form_frame, text="Nhà cung cấp:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.supplier_combobox = ttk.Combobox(form_frame, state="readonly")
        self.supplier_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Load suppliers
        suppliers = self.controller.get_suppliers()
        supplier_names = [s["name"] for s in suppliers]
        self.supplier_combobox["values"] = supplier_names
        
        # Notes
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Text(form_frame, height=5, width=30)
        self.notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def save_item():
            item_data = {
                field: entry.get() for field, entry in self.add_item_entries.items()
            }
            
            # Handle supplier selection
            selected_supplier_name = self.supplier_combobox.get()
            if selected_supplier_name:
                selected_supplier = next((s for s in suppliers if s["name"] == selected_supplier_name), None)
                if selected_supplier:
                    item_data["supplier"] = selected_supplier["id"]
            
            item_data["notes"] = self.notes_entry.get("1.0", tk.END).strip()
            
            if not item_data["name"]:
                self.show_error_message("Tên vật tư không được để trống")
                return
            
            try:
                item_data["quantity"] = float(item_data["quantity"])
                item_data["unit_price"] = float(item_data["unit_price"])
            except ValueError:
                self.show_error_message("Số lượng và đơn giá phải là số hợp lệ")
                return
            
            if self.controller.add_item(item_data):
                add_window.destroy()
                self.controller.refresh_data()

        ttk.Button(form_frame, text="Lưu", 
                  command=save_item, 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)

    def show_edit_item_form(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error_message("Vui lòng chọn vật tư cần sửa")
            return
        
        item_values = self.tree.item(selected[0], "values")
        item_id = int(item_values[0]) - 1  
        item = self.controller.inventory_manager.inventory[item_id]
        
        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Sửa thông tin vật tư")
        edit_window.geometry("500x450")
        edit_window.grab_set()
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN VẬT TƯ", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        fields = [
            ("Tên vật tư:", "name", item["name"]),
            ("Số lượng:", "quantity", str(item["current_quantity"])),
            ("Đơn vị:", "unit", item["unit"]),
            ("Đơn giá:", "unit_price", str(item["unit_price"]))
        ]
        
        self.edit_item_entries = {}
        for i, (label, field, value) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.insert(0, value)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.edit_item_entries[field] = entry
        
        # Supplier combobox
        ttk.Label(form_frame, text="Nhà cung cấp:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.edit_supplier_combobox = ttk.Combobox(form_frame, state="readonly")
        self.edit_supplier_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Load suppliers and set current supplier
        suppliers = self.controller.get_suppliers()
        supplier_names = [s["name"] for s in suppliers]
        self.edit_supplier_combobox["values"] = supplier_names
        
        current_supplier = next((s for s in suppliers if s["id"] == item.get("supplier")), None)
        if current_supplier:
            self.edit_supplier_combobox.set(current_supplier["name"])
        
        # Notes
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.edit_notes_entry = tk.Text(form_frame, height=5, width=30)
        self.edit_notes_entry.insert("1.0", item.get("notes", ""))
        self.edit_notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_item():
            update_data = {
                field: entry.get() for field, entry in self.edit_item_entries.items()
            }
            
            # Handle supplier selection
            selected_supplier_name = self.edit_supplier_combobox.get()
            if selected_supplier_name:
                selected_supplier = next((s for s in suppliers if s["name"] == selected_supplier_name), None)
                if selected_supplier:
                    update_data["supplier"] = selected_supplier["id"]
            else:
                update_data["supplier"] = None
            
            update_data["notes"] = self.edit_notes_entry.get("1.0", tk.END).strip()
            
            if not update_data["name"]:
                self.show_error_message("Tên vật tư không được để trống")
                return
            
            try:
                update_data["quantity"] = float(update_data["quantity"])
                update_data["unit_price"] = float(update_data["unit_price"])
            except ValueError:
                self.show_error_message("Số lượng và đơn giá phải là số hợp lệ")
                return
            
            if self.controller.edit_item(item["id"], update_data):
                edit_window.destroy()
                self.controller.refresh_data()

        ttk.Button(form_frame, text="Cập nhật", 
                  command=update_item, 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            self.show_error_message("Vui lòng chọn vật tư cần xóa")
            return
        
        item_values = self.tree.item(selected[0], "values")
        item_id = int(item_values[0]) - 1  
        item = self.controller.inventory_manager.inventory[item_id]
        
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa vật tư '{item['name']}'?")
        if confirm:
            if self.controller.delete_item(item["id"]):
                self.controller.refresh_data()
                self.show_success_message(f"Đã xóa vật tư '{item['name']}' thành công")

    def show_use_item_form(self, item_id=None):
        if not item_id:
            selected = self.tree.selection()
            if not selected:
                self.show_error_message("Vui lòng chọn vật tư cần sử dụng")
                return
            
            item_values = self.tree.item(selected[0], "values")
            item_id = int(item_values[0]) - 1 
            item = self.controller.inventory_manager.inventory[item_id]
        else:
            item = next((i for i in self.controller.inventory_manager.inventory if i["id"] == item_id), None)
            if not item:
                self.show_error_message("Không tìm thấy vật tư")
                return
        
        use_window = tk.Toplevel(self.controller.main.root)
        use_window.title(f"Sử dụng vật tư: {item['name']}")
        use_window.geometry("400x300")
        use_window.grab_set()
        
        ttk.Label(use_window, text=f"SỬ DỤNG VẬT TƯ: {item['name']}", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(use_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(form_frame, text=f"Số lượng hiện có: {item['current_quantity']} {item['unit']}").pack(anchor=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Số lượng sử dụng:").pack(anchor=tk.W, pady=5)
        self.use_quantity_entry = ttk.Entry(form_frame)
        self.use_quantity_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(form_frame, text="Mục đích sử dụng:").pack(anchor=tk.W, pady=5)
        self.use_purpose_entry = ttk.Entry(form_frame)
        self.use_purpose_entry.pack(fill=tk.X, pady=5)
        
        def use_item():
            quantity = self.use_quantity_entry.get()
            purpose = self.use_purpose_entry.get()
            
            if not quantity or not purpose:
                self.show_error_message("Vui lòng nhập đầy đủ thông tin")
                return
            
            try:
                quantity = float(quantity)
                if quantity <= 0:
                    self.show_error_message("Số lượng phải lớn hơn 0")
                    return
            except ValueError:
                self.show_error_message("Số lượng phải là số hợp lệ")
                return
            
            if self.controller.use_item(item["id"], quantity, purpose):
                use_window.destroy()
                self.controller.refresh_data()

        ttk.Button(form_frame, text="Ghi nhận", 
                  command=use_item, 
                  style='Primary.TButton').pack(pady=15, fill=tk.X)

    def show_suppliers(self):
        """Hiển thị danh sách nhà cung cấp"""
        if hasattr(self, 'suppliers_window'):
            try:
                if self.suppliers_window.winfo_exists():
                    self.suppliers_window.lift()
                    return
            except:
                pass

        self.suppliers_window = tk.Toplevel(self.controller.main.root)
        self.suppliers_window.title("Danh sách nhà cung cấp")
        self.suppliers_window.geometry("800x600")
        self.suppliers_window.protocol("WM_DELETE_WINDOW", self.close_suppliers_window)

        # Header
        header_frame = ttk.Frame(self.suppliers_window, padding="10")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, 
                 text="DANH SÁCH NHÀ CUNG CẤP", 
                 style='Header.TLabel').pack(side=tk.LEFT)

        # Treeview
        tree_frame = ttk.Frame(self.suppliers_window)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        columns = ("ID", "Tên", "Liên hệ", "Ghi chú")
        self.suppliers_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        self.suppliers_tree.column("ID", width=50, anchor=tk.CENTER)
        self.suppliers_tree.column("Tên", width=200)
        self.suppliers_tree.column("Liên hệ", width=150)
        self.suppliers_tree.column("Ghi chú", width=350)
        
        for col in columns:
            self.suppliers_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.suppliers_tree.yview)
        self.suppliers_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.suppliers_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        button_frame = ttk.Frame(self.suppliers_window, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Thêm mới",
                  command=self.show_add_supplier_form,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Sửa",
                  command=self.show_edit_supplier_form,
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Xóa",
                  command=self.delete_supplier,
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Đóng",
                  command=self.close_suppliers_window,
                  style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)
        
        self.display_suppliers()
        self.suppliers_window.grab_set()

    def close_suppliers_window(self):
        """Đóng cửa sổ quản lý nhà cung cấp"""
        if hasattr(self, 'suppliers_window'):
            try:
                if self.suppliers_window.winfo_exists():
                    self.suppliers_window.destroy()
            except:
                pass
        self.suppliers_window = None

    def display_suppliers(self):
        """Hiển thị danh sách nhà cung cấp mới nhất"""
        if not hasattr(self, 'suppliers_tree'):
            return
        # Xóa dữ liệu cũ
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        # Tải lại dữ liệu mới nhất từ controller
        suppliers = self.controller.get_suppliers()
        for supplier in suppliers:
            self.suppliers_tree.insert("", tk.END, values=(
                supplier["id"],
                supplier["name"],
                supplier["contact"],
                supplier.get("notes", "")
            ))

    def show_add_supplier_form(self):
        """Hiển thị form thêm nhà cung cấp mới"""
        if hasattr(self, 'add_supplier_window'):
            try:
                if self.add_supplier_window.winfo_exists():
                    self.add_supplier_window.lift()
                    return
            except:
                pass
                
        self.add_supplier_window = tk.Toplevel(self.suppliers_window)
        self.add_supplier_window.title("Thêm nhà cung cấp mới")
        self.add_supplier_window.geometry("400x300")
        self.add_supplier_window.transient(self.suppliers_window)
        self.add_supplier_window.grab_set()
        
        ttk.Label(self.add_supplier_window, 
                 text="THÊM NHÀ CUNG CẤP MỚI", 
                 style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(self.add_supplier_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        fields = [
            ("Tên nhà cung cấp:", "name"),
            ("Liên hệ:", "contact"),
            ("Ghi chú:", "notes")
        ]
        
        self.add_supplier_entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if field == "notes":
                entry = tk.Text(form_frame, height=5, width=30)
                entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            else:
                entry = ttk.Entry(form_frame)
                entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            
            self.add_supplier_entries[field] = entry
        
        def save_supplier():
            supplier_data = {
                "name": self.add_supplier_entries["name"].get(),
                "contact": self.add_supplier_entries["contact"].get(),
                "notes": self.add_supplier_entries["notes"].get("1.0", tk.END).strip()
            }
            
            if not supplier_data["name"] or not supplier_data["contact"]:
                self.show_error_message("Vui lòng nhập đầy đủ tên và thông tin liên hệ")
                return
            
            if self.controller.add_supplier(supplier_data):
                self.add_supplier_window.destroy()
                self.add_supplier_window = None
                self.display_suppliers()
                self.show_success_message("Thêm nhà cung cấp thành công!")
                self.suppliers_window.lift()

        ttk.Button(form_frame, text="Lưu",
                  command=save_supplier,
                  style='Primary.TButton').grid(row=len(fields), column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)

    def show_edit_supplier_form(self):
        selected = self.suppliers_tree.selection()
        if not selected:
            self.show_error_message("Vui lòng chọn nhà cung cấp cần sửa")
            return
            
        supplier_id = int(self.suppliers_tree.item(selected[0], "values")[0])
        supplier = next((s for s in self.controller.get_suppliers() if s["id"] == supplier_id), None)
         
        if not supplier:
            self.show_error_message("Không tìm thấy nhà cung cấp")
            return
            
        if hasattr(self, 'edit_supplier_window'):
            try:
                if self.edit_supplier_window.winfo_exists():
                    self.edit_supplier_window.destroy()
            except:
                pass
                
        self.edit_supplier_window = tk.Toplevel(self.suppliers_window)
        self.edit_supplier_window.title("Chỉnh sửa nhà cung cấp")
        self.edit_supplier_window.geometry("400x300")
        self.edit_supplier_window.transient(self.suppliers_window)
        self.edit_supplier_window.grab_set()
         
        ttk.Label(self.edit_supplier_window, 
                 text="CHỈNH SỬA NHÀ CUNG CẤP", 
                 style='Header.TLabel').pack(pady=10)
         
        form_frame = ttk.Frame(self.edit_supplier_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
         
        fields = [
            ("Tên nhà cung cấp:", "name", supplier["name"]),
            ("Liên hệ:", "contact", supplier["contact"]),
            ("Ghi chú:", "notes", supplier.get("notes", ""))
        ]
         
        self.edit_supplier_entries = {}
         
        for i, (label, field, value) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if field == "notes":
                entry = tk.Text(form_frame, height=5, width=30)
                entry.insert("1.0", value)
                entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            else:
                entry = ttk.Entry(form_frame)
                entry.insert(0, value)
                entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            
            self.edit_supplier_entries[field] = entry
         
        def perform_update():
            update_data = {
                "name": self.edit_supplier_entries["name"].get(),
                "contact": self.edit_supplier_entries["contact"].get(),
                "notes": self.edit_supplier_entries["notes"].get("1.0", tk.END).strip()
            }
            
            if not update_data["name"] or not update_data["contact"]:
                self.show_error_message("Vui lòng nhập đầy đủ tên và thông tin liên hệ")
                return
            
            if self.controller.update_supplier(supplier_id, update_data):
                self.edit_supplier_window.destroy()
                self.edit_supplier_window = None
                self.display_suppliers()
                self.controller.display_inventory()  # Cập nhật cả danh sách vật tư
                self.show_success_message("Cập nhật nhà cung cấp thành công!")
                self.suppliers_window.lift()
         
        ttk.Button(form_frame, text="Cập nhật",
                  command=perform_update,  # Sửa lại chỗ này
                  style='Primary.TButton').grid(row=len(fields), column=0, columnspan=2, pady=15, sticky=tk.EW)
         
        form_frame.grid_columnconfigure(1, weight=1)

    def delete_supplier(self):
        """Xử lý xóa nhà cung cấp"""
        selected = self.suppliers_tree.selection()
        if not selected:
            self.show_error_message("Vui lòng chọn nhà cung cấp cần xóa")
            return
            
        supplier_id = int(self.suppliers_tree.item(selected[0], "values")[0])
        supplier_name = self.suppliers_tree.item(selected[0], "values")[1]
        
        # Kiểm tra vật tư liên quan
        related_items = [item for item in self.controller.inventory_manager.inventory 
                        if item.get("supplier") == supplier_id]
        
        confirm_msg = f"Bạn có chắc muốn xóa NHÀ CUNG CẤP '{supplier_name}'?"
        if related_items:
            confirm_msg += f"\n\nCẢNH BÁO: Có {len(related_items)} vật tư liên quan sẽ bị XÓA VĨNH VIỄN!"
        
        if not messagebox.askyesno("XÁC NHẬN XÓA", confirm_msg):
            return
        
        deleted_count = self.controller.delete_supplier(supplier_id)
        
        if deleted_count >= 0:
            # Làm mới toàn bộ dữ liệu
            self.controller.refresh_data()
            
            msg = f"Đã xóa nhà cung cấp '{supplier_name}' thành công!"
            if deleted_count > 0:
                msg += f"\nĐã xóa {deleted_count} vật tư liên quan."
            
            self.show_success_message(msg)
        else:
            self.show_error_message("Có lỗi xảy ra khi xóa nhà cung cấp")

    def _format_currency(self, amount):
        """Định dạng tiền tệ"""
        return f"{amount:,.0f} VND" if amount else "0 VND"
    
    def show_error_message(self, message):
        """Hiển thị thông báo lỗi"""
        messagebox.showerror("Lỗi", message)
    
    def show_success_message(self, message):
        """Hiển thị thông báo thành công"""
        messagebox.showinfo("Thành công", message)
