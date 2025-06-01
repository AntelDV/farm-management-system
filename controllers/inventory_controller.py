from views.inventory_views import InventoryViews
from models.inventory_manager import InventoryManager

class InventoryController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = InventoryViews(self)
        self.inventory_manager = InventoryManager()
    
    def show_inventory_management(self):
        self.inventory_manager.load_data() 
        if not self._check_permission():
            return
        self.views.show_inventory_management()
    
    def display_inventory(self, items=None):
        self.views.display_inventory(items or self.inventory_manager.inventory)
    
    def search_inventory(self, keyword):
        if not keyword:
            self.display_inventory()
            return
        
        filtered_items = [
            item for item in self.inventory_manager.inventory
            if (keyword in item["name"].lower() or 
                keyword in item.get("supplier", "").lower())
        ]
        self.display_inventory(filtered_items)
    
    def show_add_item_form(self):
        if not self._check_permission():
            return
        self.views.show_add_item_form()
    
    def add_item(self, item_data):
        try:
            item_data["quantity"] = float(item_data["quantity"])
            item_data["unit_price"] = float(item_data["unit_price"])
            self.inventory_manager.add_item(item_data)
            self.inventory_manager.save_data()
            self.display_inventory()
            self.views.show_success_message("Đã thêm vật tư mới")
            return True
        except ValueError:
            self.views.show_error_message("Số lượng và đơn giá phải là số hợp lệ")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def edit_item(self, item_id, update_data):
        try:
            if "quantity" in update_data:
                update_data["quantity"] = float(update_data["quantity"])
            if "unit_price" in update_data:
                update_data["unit_price"] = float(update_data["unit_price"])
            self.inventory_manager.update_item(item_id, update_data)
            self.inventory_manager.save_data()
            self.display_inventory()
            self.views.show_success_message("Đã cập nhật thông tin vật tư")
            return True
        except ValueError:
            self.views.show_error_message("Số lượng và đơn giá phải là số hợp lệ")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def delete_item(self, item_id):
        try:
            self.inventory_manager.delete_item(item_id)
            self.inventory_manager.save_data()
            self.display_inventory()
            self.views.show_success_message("Đã xóa vật tư")
            return True
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def show_use_item_form(self, item_id):
        if not self._check_permission():
            return
        self.views.show_use_item_form(item_id)
    
    def use_item(self, item_id, quantity, purpose):
        try:
            quantity = float(quantity)
            self.inventory_manager.record_usage(item_id, quantity, purpose)
            self.inventory_manager.save_data()
            self.display_inventory()
            self.views.show_success_message("Đã ghi nhận sử dụng vật tư")
            return True
        except ValueError:
            self.views.show_error_message("Số lượng phải là số hợp lệ")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def show_suppliers(self):
        if not self._check_permission():
            return
        self.views.show_suppliers()
    
    def add_supplier(self, supplier_data):
        try:
            self.inventory_manager.add_supplier(supplier_data)
            self.inventory_manager.save_data()
            self.views.show_success_message("Đã thêm nhà cung cấp mới")
            return True
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
        

    def show_suppliers(self):
        try:
            self.inventory_manager.load_data()
            self.views.show_suppliers()
        except Exception as e:
            self.views.show_error_message(f"Lỗi khi tải nhà cung cấp: {str(e)}") 
    

    def delete_supplier(self, supplier_id):
        try:
            # Gọi phương thức từ manager và kiểm tra kết quả
            deleted_items = self.inventory_manager.delete_supplier(supplier_id)
            if deleted_items >= 0:
                self.inventory_manager.save_data()
                if deleted_items > 0:
                    self.views.show_success_message(f"Đã xóa nhà cung cấp và {deleted_items} vật tư liên quan")
                else:
                    self.views.show_success_message("Đã xóa nhà cung cấp")
                self.views.display_suppliers()
                self.views.display_inventory()
                return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi khi xóa nhà cung cấp: {str(e)}")
            return False
            
    def update_supplier(self, supplier_id, update_data):
        try:
            for i, supplier in enumerate(self.inventory_manager.suppliers):
                if supplier["id"] == supplier_id:
                    self.inventory_manager.suppliers[i] = {**supplier, **update_data}
                    self.inventory_manager.save_data()
                    self.views.show_success_message("Đã cập nhật nhà cung cấp")
                    self.show_suppliers()
                    return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def get_inventory_value(self):
        return self.inventory_manager.get_inventory_value()
    
    def get_item_by_id(self, item_id):
        return next((i for i in self.inventory_manager.inventory if i["id"] == item_id), None)
    
    def get_suppliers(self):
        return self.inventory_manager.suppliers
    
    def _check_permission(self):
        if self.main.auth_controller.current_user["role"] != "admin":
            self.views.show_error_message("Bạn không có quyền truy cập chức năng này")
            self.main.show_main_menu()
            return False
        return True