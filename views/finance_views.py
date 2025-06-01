import tkinter as tk
from tkinter import ttk, messagebox
from views.styles import configure_styles

class FinanceViews:
    def __init__(self, controller):
        self.controller = controller
        self.style = configure_styles()
    
    def show_finance_management(self):
        self.controller.main.clear_window()
        
        control_frame = ttk.Frame(self.controller.main.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="Thêm giao dịch", 
                  command=self.show_add_transaction_form, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)
        self.finance_search_entry = ttk.Entry(search_frame, width=20)
        self.finance_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Tìm", 
                  command=lambda: self.controller.search_transactions(self.finance_search_entry.get().lower()), 
                  style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Tạo Treeview
        columns = ("ID", "Ngày", "Loại", "Danh mục", "Số tiền", "Mô tả")
        self.finance_tree = ttk.Treeview(self.controller.main.root, columns=columns, show="headings")
        
        for col in columns:
            self.finance_tree.heading(col, text=col)
        
        self.finance_tree.column("ID", width=50, anchor=tk.CENTER)
        self.finance_tree.column("Ngày", width=120, anchor=tk.CENTER)
        self.finance_tree.column("Loại", width=80, anchor=tk.CENTER)
        self.finance_tree.column("Danh mục", width=120)
        self.finance_tree.column("Số tiền", width=100, anchor=tk.E)
        self.finance_tree.column("Mô tả", width=200)
        
        self.finance_tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.finance_tree, orient=tk.VERTICAL, command=self.finance_tree.yview)
        self.finance_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        self.balance_frame = ttk.Frame(self.controller.main.root)
        self.balance_frame.pack(fill=tk.X, padx=10, pady=5)
         
        self.balance_label = ttk.Label(
            self.balance_frame, 
            text=f"Tổng số dư hiện tại: {self._format_currency(self.controller.get_balance())}",
            font=('Times New Roman', 10, 'bold')
        )
        self.balance_label.pack(side=tk.RIGHT)
        

        # Khung nút hành động
        action_frame = ttk.Frame(self.controller.main.root, padding="10")
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Sửa", 
                  command=self.show_edit_transaction_form, 
                  style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Xóa", 
                  command=self.delete_selected_transaction, 
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Quay lại", 
                  command=self.controller.main.show_main_menu, 
                  style='Secondary.TButton').pack(side=tk.RIGHT)
        
        self.display_transactions()
    
    def display_transactions(self, transactions=None):
        for item in self.finance_tree.get_children():
            self.finance_tree.delete(item)
     
        transactions_to_display = transactions or self.controller.finance_manager.transactions
        for idx, trans in enumerate(transactions_to_display, 1):
            # Thêm logic hiển thị nhà cung cấp nếu có
            description = trans["description"]
            if "supplier_id" in trans:
                supplier = next((s for s in self.controller.main.inventory_controller.inventory_manager.suppliersz 
                               if s["id"] == trans["supplier_id"]), None)
                if supplier:
                    description = f"{description} (Nhà cung cấp: {supplier['name']})"
            
            amount = f"{trans['amount']:,.0f}" if isinstance(trans['amount'], (int, float)) else trans['amount']
            self.finance_tree.insert("", tk.END, values=(
                idx,
                trans["date"],
                "Thu" if trans["type"] == "income" else "Chi",
                trans["category"],
                amount,
                description  # Sử dụng description đã được cập nhật
            ))
     
        self.update_balance()

    def update_balance(self):
        balance = self.controller.get_balance()
        self.balance_label.config(text=f"Tổng số dư hiện tại: {self._format_currency(balance)}")

    def _on_add_transaction_success(self):
        self.update_balance()
        self.show_success_message("Thêm giao dịch thành công")    

    def _on_edit_transaction_success(self):
        self.update_balance()
        self.show_success_message("Cập nhật giao dịch thành công")    

    def _on_delete_transaction_success(self):
        self.update_balance()
        self.show_success_message("Xóa giao dịch thành công")
    
    def show_add_transaction_form(self):
        add_window = tk.Toplevel(self.controller.main.root)
        add_window.title("Thêm giao dịch mới")
        add_window.geometry("500x350")
        
        ttk.Label(add_window, text="THÊM GIAO DỊCH MỚI", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(add_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Loại giao dịch
        ttk.Label(form_frame, text="Loại giao dịch:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.trans_type = tk.StringVar(value="income")
        ttk.Radiobutton(form_frame, text="Thu", variable=self.trans_type, value="income").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(form_frame, text="Chi", variable=self.trans_type, value="expense").grid(row=0, column=2, sticky=tk.W)
        
        # Danh mục
        ttk.Label(form_frame, text="Danh mục:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.trans_category = ttk.Combobox(form_frame)
        self.trans_category.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        self._update_category_options()
        
        # Số tiền
        ttk.Label(form_frame, text="Số tiền:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.trans_amount = ttk.Entry(form_frame)
        self.trans_amount.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        
        # Mô tả
        ttk.Label(form_frame, text="Mô tả:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.trans_description = tk.Text(form_frame, height=4, width=30)
        self.trans_description.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        
        def save_transaction():
            transaction_data = {
                "type": self.trans_type.get(),
                "category": self.trans_category.get(),
                "amount": self.trans_amount.get(),
                "description": self.trans_description.get("1.0", tk.END).strip()
            }
            
            if not transaction_data["category"]:
                self.show_error_message("Vui lòng chọn danh mục")
                return
            
            if self.controller.add_transaction(transaction_data):
                add_window.destroy()
        
        ttk.Button(form_frame, text="Lưu", 
                  command=save_transaction, 
                  style='Primary.TButton').grid(row=4, column=0, columnspan=3, pady=15, sticky=tk.EW)
        
        # Cập nhật danh mục khi thay đổi loại giao dịch
        self.trans_type.trace_add("write", lambda *args: self._update_category_options())
        
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)
    
    def show_edit_transaction_form(self):
        selected_item = self.finance_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn giao dịch cần sửa")
            return
        
        item_data = self.finance_tree.item(selected_item[0], "values")
        display_id = int(item_data[0])
        trans = self.controller.finance_manager.transactions[display_id - 1]
        
        edit_window = tk.Toplevel(self.controller.main.root)
        edit_window.title("Sửa thông tin giao dịch")
        edit_window.geometry("500x350")
        
        ttk.Label(edit_window, text="SỬA THÔNG TIN GIAO DỊCH", style='Header.TLabel').pack(pady=10)
        
        form_frame = ttk.Frame(edit_window, padding="10")
        form_frame.pack(expand=True, fill=tk.BOTH)
        
        # Loại giao dịch
        ttk.Label(form_frame, text="Loại giao dịch:").grid(row=0, column=0, sticky=tk.W, pady=5)
        trans_type = tk.StringVar(value=trans["type"])
        ttk.Radiobutton(form_frame, text="Thu", variable=trans_type, value="income").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(form_frame, text="Chi", variable=trans_type, value="expense").grid(row=0, column=2, sticky=tk.W)
        
        # Danh mục
        ttk.Label(form_frame, text="Danh mục:").grid(row=1, column=0, sticky=tk.W, pady=5)
        trans_category = ttk.Combobox(form_frame)
        trans_category.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        trans_category.set(trans["category"])
        
        # Số tiền
        ttk.Label(form_frame, text="Số tiền:").grid(row=2, column=0, sticky=tk.W, pady=5)
        trans_amount = ttk.Entry(form_frame)
        trans_amount.insert(0, str(trans["amount"]))
        trans_amount.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        
        # Mô tả
        ttk.Label(form_frame, text="Mô tả:").grid(row=3, column=0, sticky=tk.W, pady=5)
        trans_description = tk.Text(form_frame, height=4, width=30)
        trans_description.insert("1.0", trans.get("description", ""))
        trans_description.grid(row=3, column=1, columnspan=2, pady=5, padx=5, sticky=tk.EW)
        
        def update_category_options(*args):
            current_type = trans_type.get()
            if current_type == "income":
                trans_category["values"] = self.controller.finance_manager.categories["income"]
            else:
                trans_category["values"] = self.controller.finance_manager.categories["expense"]
        
        def update_transaction():
            update_data = {
                "type": trans_type.get(),
                "category": trans_category.get(),
                "amount": trans_amount.get(),
                "description": trans_description.get("1.0", tk.END).strip()
            }
            
            if not update_data["category"]:
                self.show_error_message("Vui lòng chọn danh mục")
                return
            
            if self.controller.edit_transaction(trans["id"], update_data):
                edit_window.destroy()
        
        trans_type.trace_add("write", update_category_options)
        update_category_options()
        
        ttk.Button(form_frame, text="Cập nhật", 
                  command=update_transaction, 
                  style='Primary.TButton').grid(row=4, column=0, columnspan=3, pady=15, sticky=tk.EW)
        
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)
    
    def delete_selected_transaction(self):
        selected_item = self.finance_tree.selection()
        if not selected_item:
            self.show_error_message("Vui lòng chọn giao dịch cần xóa")
            return
        
        item_data = self.finance_tree.item(selected_item[0], "values")
        display_id = int(item_data[0])
        trans = self.controller.finance_manager.transactions[display_id - 1]
        
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giao dịch này?")
        if confirm:
            self.controller.delete_transaction(trans["id"])
    
    def _update_category_options(self):
        current_type = self.trans_type.get()
        if current_type == "income":
            self.trans_category["values"] = self.controller.finance_manager.categories["income"]
        else:
            self.trans_category["values"] = self.controller.finance_manager.categories["expense"]
        self.trans_category.set("")
    
    def _format_currency(self, amount):
        return f"{amount:,.0f} VND"
    
    def show_error_message(self, message):
        messagebox.showerror("Lỗi", message)
    
    def show_success_message(self, message):
        messagebox.showinfo("Thành công", message)