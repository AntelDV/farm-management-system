import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles

class InventoryViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()
    
    def show_inventory_management(self):
        self.controller.main.clear_window()
        
        control_frame = ttk.Frame(self.controller.main.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.LEFT)
        
        ttk.Button(button_frame, text="Thêm vật tư", 
                  command=self.show_add_item_form, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Nhà cung cấp", 
                  command=self.controller.show_suppliers, 
                  style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.inventory_search_entry = ttk.Entry(search_frame, width=20)
        self.inventory_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", 
                  command=lambda: self.controller.search_inventory(self.inventory_search_entry.get().lower()), 
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Tạo Treeview
        columns = ("ID", "Tên", "Số lượng", "Đơn vị", "Đơn giá", "Tổng giá trị", "Nhà cung cấp")
        self.inventory_tree = ttk.Treeview(self.controller.main.root, columns=columns, show="headings")
        
        for col in columns:
            self.inventory_tree.heading(col, text=col)
        
        self.inventory_tree.column("ID", width=50, anchor=tk.CENTER)
        self.inventory_tree.column("Tên", width=150)
        self.inventory_tree.column("Số lượng", width=80, anchor=tk.E)
        self.inventory_tree.column("Đơn vị", width=80, anchor=tk.CENTER)
        self.inventory_tree.column("Đơn giá", width=100, anchor=tk.E)
        self.inventory_tree.column("Tổng giá trị", width=120, anchor=tk.E)
        self.inventory_tree.column("Nhà cung cấp", width=150)
        
        self.inventory_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.inventory_tree, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Hiển thị tổng giá trị kho
        self.value_frame = ttk.Frame(self.controller.main.root)
        self.value_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.value_label = ttk.Label(self.value_frame, 
                                   text=f"Tổng giá trị kho: {self._format_currency(self.controller.get_inventory_value())}", 
                                   font=('Times New Roman', 10, 'bold'))
        self.value_label.pack(side=tk.RIGHT)
        
        # Khung nút hành động
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
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        items_to_display = items or self.controller.inventory_manager.inventory
        
        for idx, item in enumerate(items_to_display, 1):
            supplier_name = "N/A"
            if "supplier" in item:
                supplier = next(
                    (s for s in self.controller.inventory_manager.suppliers 
                     if s["id"] == item["supplier"]), 
                    None
                )
                supplier_name = supplier["name"] if supplier else "N/A"
                
            total_value = item["current_quantity"] * item["unit_price"]
            self.inventory_tree.insert("", tk.END, values=(
                idx,
                item["name"],
                item["current_quantity"],
                item["unit"],
                f"{item['unit_price']:,.0f}",
                f"{total_value:,.0f}",
                supplier_name
            ))
        # Cập nhật tổng giá trị kho
        self.update_inventory_value()
    
    def update_inventory_value(self):
        inventory_value = sum(
            item["current_quantity"] * item["unit_price"] 
            for item in self.controller.inventory_manager.inventory
        )
        self.value_label.config(text=f"Tổng giá trị kho: {self._format_currency(inventory_value)}")

    def show_add_item_form(self):
        add_window = tk.Toplevel(self.controller.main.root)
        add_window.title("Thêm vật tư mới")
        add_window.geometry("500x450")
        
        ttk.Label(add_window, text="THÊM VẬT TƯ MỚI", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tạo các trường nhập liệu
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
        
        # Nhà cung cấp
        ttk.Label(form_frame, text="Nhà cung cấp:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.supplier_combobox = ttk.Combobox(form_frame)
        self.supplier_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        self.supplier_combobox["values"] = [s["name"] for s in self.controller.get_suppliers()]
        
        # Ghi chú
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Text(form_frame, height=5, width=30)
        self.notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def save_item():
            item_data = {
                field: entry.get() for field, entry in self.add_item_entries.items()
            }
            item_data["supplier"] = self.supplier_combobox.get()
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
                self.display_inventory()  # Cập nhật ngay lập tức
        
        ttk.Button(form_frame, text="Lưu", 
                  command=save_item, 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_edit_item_form(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn vật tư cần sửa")
            return
        
        item_data = self.inventory_tree.item(selected_item[0], "values")
        display_id = int(item_data[0])
        item = self.controller.inventory_manager.inventory[display_id - 1]
        
        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Sửa thông tin vật tư")
        edit_window.geometry("500x450")
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN VẬT TƯ", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tạo các trường nhập liệu
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
        
        # Nhà cung cấp
        ttk.Label(form_frame, text="Nhà cung cấp:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.edit_supplier_combobox = ttk.Combobox(form_frame)
        self.edit_supplier_combobox.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        self.edit_supplier_combobox["values"] = [s["name"] for s in self.controller.get_suppliers()]
        self.edit_supplier_combobox.set(item.get("supplier", ""))
        
        # Ghi chú
        ttk.Label(form_frame, text="Ghi chú:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.edit_notes_entry = tk.Text(form_frame, height=5, width=30)
        self.edit_notes_entry.insert("1.0", item.get("notes", ""))
        self.edit_notes_entry.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_item():
            update_data = {
                field: entry.get() for field, entry in self.edit_item_entries.items()
            }
            update_data["supplier"] = self.edit_supplier_combobox.get()
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
                self.display_inventory()  
        
        ttk.Button(form_frame, text="Cập nhật", 
                  command=update_item, 
                  style='Primary.TButton').grid(row=6, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_use_item_form(self, item_id=None):
        if not item_id:
            selected_item = self.inventory_tree.selection()
            if not selected_item:
                self.show_error_message("Vui lòng chọn vật tư cần sử dụng")
                return
            
            item_data = self.inventory_tree.item(selected_item[0], "values")
            display_id = int(item_data[0])
            item = self.controller.inventory_manager.inventory[display_id - 1]
        else:
            item = next((i for i in self.controller.inventory_manager.inventory if i["id"] == item_id), None)
            if not item:
                self.show_error_message("Không tìm thấy vật tư")
                return
        
        use_window = tk.Toplevel(self.controller.main.root)
        use_window.title(f"Sử dụng vật tư: {item['name']}")
        use_window.geometry("400x300")
        
        ttk.Label(use_window, text=f"SỬ DỤNG VẬT TƯ: {item['name']}", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(use_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(form_frame, text=f"Số lượng hiện có: {item['current_quantity']} {item['unit']}").pack(anchor=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Số lượng sử dụng:").pack(anchor=tk.W, pady=5)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(form_frame, text="Mục đích sử dụng:").pack(anchor=tk.W, pady=5)
        self.purpose_entry = ttk.Entry(form_frame)
        self.purpose_entry.pack(fill=tk.X, pady=5)
        
        def use_item():
            quantity = self.quantity_entry.get()
            purpose = self.purpose_entry.get()
            
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
                self.display_inventory()  
        
        ttk.Button(form_frame, text="Ghi nhận", 
                  command=use_item, 
                  style='Primary.TButton').pack(pady=15, fill=tk.X)
    
    def show_suppliers(self):
        suppliers_window = tk.Toplevel(self.controller.main.root)
        suppliers_window.title("Danh sách nhà cung cấp")
        suppliers_window.geometry("800x500")
        
        ttk.Label(suppliers_window, text="DANH SÁCH NHÀ CUNG CẤP", style='Header.TLabel').pack(pady=10)
        
        # Tạo Treeview
        columns = ("ID", "Tên", "Liên hệ", "Ghi chú")
        self.suppliers_tree = ttk.Treeview(suppliers_window, columns=columns, show="headings")
        
        for col in columns:
            self.suppliers_tree.heading(col, text=col)
        
        self.suppliers_tree.column("ID", width=50, anchor=tk.CENTER)
        self.suppliers_tree.column("Tên", width=200)
        self.suppliers_tree.column("Liên hệ", width=150)
        self.suppliers_tree.column("Ghi chú", width=350)
        
        self.suppliers_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.suppliers_tree, orient=tk.VERTICAL, command=self.suppliers_tree.yview)
        self.suppliers_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Hiển thị danh sách nhà cung cấp
        self.display_suppliers()
        
        # Khung nút
        button_frame = ttk.Frame(suppliers_window, padding="10")
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Thêm nhà cung cấp", 
                  command=lambda: self.show_add_supplier_form(suppliers_window), 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Sửa", 
                  command=lambda: self.show_edit_supplier_form(), 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Xóa", 
                  command=lambda: self.delete_supplier(), 
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Đóng", 
                  command=suppliers_window.destroy, 
                  style='Secondary.TButton').pack(side=tk.RIGHT, padx=5)
        
        
    
    def display_suppliers(self):
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        for supplier in self.controller.get_suppliers():
            self.suppliers_tree.insert("", tk.END, values=(
                supplier["id"],
                supplier["name"],
                supplier["contact"],
                supplier.get("notes", "")
            ))
    
    def show_add_supplier_form(self, parent_window):
        add_window = tk.Toplevel(parent_window)
        add_window.title("Thêm nhà cung cấp mới")
        add_window.geometry("400x300")
        
        ttk.Label(add_window, text="THÊM NHÀ CUNG CẤP MỚI", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tạo các trường nhập liệu
        fields = [
            ("Tên nhà cung cấp:", "name"),
            ("Liên hệ:", "contact")
        ]
        
        self.add_supplier_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.add_supplier_entries[field] = entry
        
        # Ghi chú
        ttk.Label(form_frame, text="Ghi chú:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.supplier_notes_entry = tk.Text(form_frame, height=5, width=30)
        self.supplier_notes_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        

        def save_supplier(self):
            supplier_data = {
                field: entry.get() for field, entry in self.add_supplier_entries.items()
            }
            supplier_data["notes"] = self.supplier_notes_entry.get("1.0", tk.END).strip()
             
            if not supplier_data["name"] or not supplier_data["contact"]:
                self.show_error_message("Tên và liên hệ không được để trống")
                return
             
            if self.controller.add_supplier(supplier_data):
                self.display_suppliers()  # Cập nhật danh sách
                self.show_success_message("Đã thêm nhà cung cấp mới")
                # Không đóng cửa sổ nhà cung cấp
        
        ttk.Button(form_frame, text="Lưu", 
                  command=save_supplier, 
                  style='Primary.TButton').grid(row=3, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def show_edit_supplier_form(self):
        selected_item = self.suppliers_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn nhà cung cấp cần sửa")
            return
        
        supplier_id = int(self.suppliers_tree.item(selected_item[0], "values")[0])
        supplier = next((s for s in self.controller.get_suppliers() if s["id"] == supplier_id), None)
        
        if not supplier:
            self.show_error_message("Không tìm thấy nhà cung cấp")
            return
        
        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Sửa nhà cung cấp")
        edit_window.geometry("400x300")
        
        ttk.Label(edit_window, text="SỬA NHÀ CUNG CẤP", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Tạo các trường nhập liệu
        fields = [
            ("Tên nhà cung cấp:", "name", supplier["name"]),
            ("Liên hệ:", "contact", supplier["contact"])
        ]
        
        self.edit_supplier_entries = {}
        for i, (label, field, value) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(form_frame)
            entry.insert(0, value)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky=tk.EW)
            self.edit_supplier_entries[field] = entry
        
        # Ghi chú
        ttk.Label(form_frame, text="Ghi chú:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.edit_supplier_notes_entry = tk.Text(form_frame, height=5, width=30)
        self.edit_supplier_notes_entry.insert("1.0", supplier.get("notes", ""))
        self.edit_supplier_notes_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.EW)
        
        def update_supplier():
            update_data = {
                field: entry.get() for field, entry in self.edit_supplier_entries.items()
            }
            update_data["notes"] = self.edit_supplier_notes_entry.get("1.0", tk.END).strip()
            
            if not update_data["name"] or not update_data["contact"]:
                self.show_error_message("Tên và liên hệ không được để trống")
                return
            
            if self.controller.update_supplier(supplier_id, update_data):
                self.display_suppliers()  # Cập nhật danh sách
                edit_window.destroy()
        
        ttk.Button(form_frame, text="Cập nhật", 
                  command=update_supplier, 
                  style='Primary.TButton').grid(row=3, column=0, columnspan=2, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)
    
   
    def delete_supplier(self):
        selected_item = self.suppliers_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn nhà cung cấp cần xóa")
            return
    
        supplier_id = int(self.suppliers_tree.item(selected_item[0], "values")[0])
        supplier_name = self.suppliers_tree.item(selected_item[0], "values")[1]
    
        # Kiểm tra xem có vật tư nào sử dụng nhà cung cấp này không
        items_count = sum(1 for item in self.controller.inventory_manager.inventory 
                    if item.get("supplier") == supplier_id)
    
        if items_count > 0:
            confirm = messagebox.askyesno(
                "Xác nhận",
                f"Bạn có chắc chắn muốn xóa nhà cung cấp '{supplier_name}'?\n"
                f"Sẽ có {items_count} vật tư sử dụng nhà cung cấp này bị xóa theo."
            )
        else:
            confirm = messagebox.askyesno(
                "Xác nhận", 
                f"Bạn có chắc chắn muốn xóa nhà cung cấp '{supplier_name}'?"
            )
    
        if confirm:
            deleted_items = self.controller.delete_supplier(supplier_id)
            if deleted_items >= 0:
                if deleted_items > 0:
                    message = (f"Đã xóa nhà cung cấp và {deleted_items} vật tư liên quan.\n"
                            "Vui lòng kiểm tra lại kho hàng.")
                else:
                    message = "Đã xóa nhà cung cấp thành công."
            
                self.show_success_message(message)
                self.display_suppliers()
                self.controller.views.display_inventory()  # Cập nhật lại giao diện kho
            else:
                self.show_error_message("Có lỗi xảy ra khi xóa nhà cung cấp")
    
    
    def delete_selected_item(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn vật tư cần xóa")
            return
         
        item_data = self.inventory_tree.item(selected_item[0], "values")
        display_id = int(item_data[0])
        item = self.controller.inventory_manager.inventory[display_id - 1]
         
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa vật tư này?")
        if confirm:
            try:
                if self.controller.inventory_manager.delete_item(item["id"]):
                    self.controller.inventory_manager.save_data()
                    self.display_inventory()
                    self.show_success_message("Xóa thành công")
                else:
                    self.show_error_message("Xóa không thành công")
            except Exception as e:
                self.show_error_message(f"Lỗi khi xóa: {str(e)}")
    
    def _format_currency(self, amount):
        """Định dạng tiền tệ"""
        return f"{amount:,.0f} VND" if amount else "0 VND"
    
    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)
    
    def show_success_message(self, message):
        messagebox.showinfo("Thành công", message)