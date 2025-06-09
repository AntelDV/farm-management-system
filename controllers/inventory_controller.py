import tk
from views.inventory_views import InventoryViews
from models.inventory_manager import InventoryManager

class InventoryController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = InventoryViews(self)
        self.inventory_manager = InventoryManager()
    
    def _check_permission(self):
        """Kiểm tra quyền truy cập của người dùng"""
        if not hasattr(self.main.auth_controller, 'current_user'):
            self.main.auth_controller.show_login_screen()
            return False
        
        if self.main.auth_controller.current_user["role"] != "admin":
            self.views.show_error_message("Bạn không có quyền truy cập chức năng này")
            self.main.show_main_menu()
            return False
        return True
    
    def show_inventory_management(self):
        """Hiển thị màn hình quản lý kho"""
        if not self._check_permission():
            return
        
        self.inventory_manager.load_data()
        self.views.show_inventory_management()
    
    def display_inventory(self, items=None):
        """Hiển thị danh sách vật tư"""
        self.views.display_inventory(items or self.inventory_manager.inventory)
    
    def search_inventory(self, keyword):
        """Tìm kiếm vật tư"""
        if not keyword.strip():
            self.display_inventory()
            return
        
        keyword = keyword.lower()
        filtered_items = []
        
        for item in self.inventory_manager.inventory:
            # Tìm theo tên vật tư
            if keyword in item["name"].lower():
                filtered_items.append(item)
                continue
                
            # Tìm theo tên nhà cung cấp
            if "supplier" in item:
                supplier = next((s for s in self.inventory_manager.suppliers 
                              if s["id"] == item["supplier"]), None)
                if supplier and keyword in supplier["name"].lower():
                    filtered_items.append(item)
                    continue
            # Tìm theo ghi chú
            if "notes" in item and keyword in item["notes"].lower():
                filtered_items.append(item)
        
        self.display_inventory(filtered_items)
    
    def show_add_item_form(self):
        """Hiển thị form thêm vật tư mới"""
        if not self._check_permission():
            return
        self.views.show_add_item_form()
    
    def add_item(self, item_data):
        """Thêm vật tư mới"""
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
        """Cập nhật thông tin vật tư"""
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
        """Xóa vật tư"""
        try:
            self.inventory_manager.delete_item(item_id)
            self.inventory_manager.save_data()
            self.display_inventory()
            self.views.show_success_message("Đã xóa vật tư")
            return True
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def show_use_item_form(self, item_id=None):
        """Hiển thị form sử dụng vật tư"""
        if not self._check_permission():
            return
        self.views.show_use_item_form(item_id)
    
    def use_item(self, item_id, quantity, purpose):
        """Ghi nhận sử dụng vật tư"""
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
        """Hiển thị danh sách nhà cung cấp"""
        if not self._check_permission():
            return
            
        if hasattr(self.views, 'suppliers_window'):
            try:
                if self.views.suppliers_window.winfo_exists():
                    self.views.suppliers_window.destroy()
            except:
                pass
                
        self.views.show_suppliers()
    
    def add_supplier(self, supplier_data):
        """Thêm nhà cung cấp mới"""
        try:
            self.inventory_manager.add_supplier(supplier_data)
            self.inventory_manager.save_data()
            return True
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def update_supplier(self, supplier_id, update_data):
        try:
            updated = self.inventory_manager.update_supplier(supplier_id, update_data)
            if updated:
                self.inventory_manager.save_data()
                self.refresh_data()  
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật nhà cung cấp: {str(e)}")
            return False
    
    def delete_supplier(self, supplier_id):
        """Xóa nhà cung cấp và các vật tư liên quan"""
        try:
            deleted_items = self.inventory_manager.delete_supplier(supplier_id)
            if deleted_items >= 0:
                self.inventory_manager.save_data()
                return deleted_items
            return -1
        except Exception as e:
            print(f"Lỗi khi xóa nhà cung cấp: {str(e)}")
            return -1
    
    def get_inventory_value(self):
        """Lấy tổng giá trị kho"""
        return self.inventory_manager.get_inventory_value()
    
    def get_item_by_id(self, item_id):
        """Lấy vật tư theo ID"""
        return next((i for i in self.inventory_manager.inventory if i["id"] == item_id), None)
    
    def get_suppliers(self):
        """Lấy danh sách nhà cung cấp"""
        return self.inventory_manager.suppliers
    
    def refresh_data(self):
        try:
            self.inventory_manager.load_data()
            if not hasattr(self, 'views'):
                return

            self.views.display_inventory()
            
            # Kiểm tra và cập nhật cửa sổ nhà cung cấp nếu đang mở
            if hasattr(self.views, 'suppliers_window'):
                try:
                    if (self.views.suppliers_window is not None and 
                        isinstance(self.views.suppliers_window, tk.Toplevel) and 
                        self.views.suppliers_window.winfo_exists()):
                        self.views.display_suppliers()
                except (AttributeError, tk.TclError):
                    # Nếu có lỗi, đặt lại suppliers_window về None
                    self.views.suppliers_window = None
        except Exception as e:
            print(f"Lỗi khi làm mới dữ liệu: {str(e)}")
