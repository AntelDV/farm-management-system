from views.finance_views import FinanceViews
from models.finance_manager import FinanceManager

class FinanceController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = FinanceViews(self)
        self.finance_manager = FinanceManager()
    
    def show_finance_management(self):
        self.finance_manager.load_data() 
        if not self._check_permission():
            return
        self.views.show_finance_management()
        self.display_transactions(self.finance_manager.transactions)

    def display_transactions(self, transactions=None):
        self.views.display_transactions(transactions or self.finance_manager.transactions)
    
    def search_transactions(self, keyword):
        if not keyword:
            self.display_transactions()
            return
        
        filtered_trans = [
            trans for trans in self.finance_manager.transactions
            if (keyword in trans["category"].lower() or 
                keyword in trans["description"].lower())
        ]
        self.display_transactions(filtered_trans)
    
    def show_add_transaction_form(self):
        if not self._check_permission():
            return
        self.views.show_add_transaction_form()
    
    def add_transaction(self, transaction_data):
        try:
            transaction_data["amount"] = float(transaction_data["amount"])
            result = self.finance_manager.add_transaction(transaction_data)
            if result:
                self.finance_manager.save_data()
                self.display_transactions()
                self.views._on_add_transaction_success()  # Gọi hàm cập nhật balance
                return True
            return False
        except ValueError:
            self.views.show_error_message("Số tiền phải là số hợp lệ")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False

    def edit_transaction(self, transaction_id, update_data):
        try:
            if "amount" in update_data:
                update_data["amount"] = float(update_data["amount"])
            result = self.finance_manager.update_transaction(transaction_id, update_data)
            if result:
                self.finance_manager.save_data()
                self.display_transactions()
                self.views._on_edit_transaction_success()  
                return True
            return False
        except ValueError:
            self.views.show_error_message("Số tiền phải là số hợp lệ")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False    

    def delete_transaction(self, transaction_id):
        try:
            result = self.finance_manager.delete_transaction(transaction_id)
            if result:
                self.finance_manager.save_data()
                self.display_transactions()
                self.views._on_delete_transaction_success()  
                return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
        
    def get_balance(self):
        return self.finance_manager.get_balance()
    
    def get_transaction_by_id(self, transaction_id):
        return next((t for t in self.finance_manager.transactions if t["id"] == transaction_id), None)
    
    def update_category_options(self, trans_type):
        if trans_type == "income":
            return self.finance_manager.categories["income"]
        else:
            return self.finance_manager.categories["expense"]
    
    def _check_permission(self):
        if self.main.auth_controller.current_user["role"] != "admin":
            self.views.show_error_message("Bạn không có quyền truy cập chức năng này")
            self.main.show_main_menu()
            return False
        return True