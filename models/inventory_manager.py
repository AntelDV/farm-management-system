import json
import os
from datetime import datetime

class InventoryManager:
    def __init__(self):
        self.inventory = []
        self.suppliers = []
        self.data_file = "data/inventory.json"
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.inventory = data.get("inventory", [])
                    self.suppliers = data.get("suppliers", [])
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu kho: {str(e)}")
            self.inventory = []
            self.suppliers = []
    
    def save_data(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            data = {
                "inventory": self.inventory,
                "suppliers": self.suppliers
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu kho: {str(e)}")
    
    def add_item(self, item_data):
        if not all(key in item_data for key in ["name", "quantity", "unit", "unit_price"]):
            raise ValueError("Thiếu thông tin bắt buộc cho vật tư")
        
        if item_data["quantity"] <= 0:
            raise ValueError("Số lượng phải lớn hơn 0")
        
        if item_data["unit_price"] <= 0:
            raise ValueError("Đơn giá phải lớn hơn 0")
        
        new_id = max([item["id"] for item in self.inventory], default=0) + 1
        
        item_data["id"] = new_id
        item_data["created_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        item_data["current_quantity"] = item_data["quantity"]
        self.inventory.append(item_data)
        self.save_data()
        return item_data
    
    def update_item(self, item_id, update_data):
        for item in self.inventory:
            if item["id"] == item_id:
                if "quantity" in update_data and update_data["quantity"] <= 0:
                    raise ValueError("Số lượng phải lớn hơn 0")
                
                if "unit_price" in update_data and update_data["unit_price"] <= 0:
                    raise ValueError("Đơn giá phải lớn hơn 0")
                
                for key, value in update_data.items():
                    if key == "quantity":
                        diff = value - item["current_quantity"]
                        item["current_quantity"] = value
                        item["quantity"] = item.get("quantity", 0) + diff
                    else:
                        item[key] = value
                item["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                self.save_data()
                return item
        raise ValueError(f"Không tìm thấy vật tư với ID {item_id}")
    
    def delete_item(self, item_id):
        try:
            initial_count = len(self.inventory)
            self.inventory = [item for item in self.inventory if item["id"] != item_id]
            if len(self.inventory) < initial_count:
                self.save_data()
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi xóa vật tư: {str(e)}")
            return False
    
    def record_usage(self, item_id, quantity, purpose):
        if quantity <= 0:
            raise ValueError("Số lượng sử dụng phải lớn hơn 0")
        
        for item in self.inventory:
            if item["id"] == item_id:
                if item["current_quantity"] >= quantity:
                    item["current_quantity"] -= quantity
                    usage_record = {
                        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "quantity": quantity,
                        "purpose": purpose,
                        "remaining": item["current_quantity"]
                    }
                    item.setdefault("usage_history", []).append(usage_record)
                    self.save_data()
                    return True
                else:
                    raise ValueError("Số lượng sử dụng vượt quá số lượng hiện có")
        raise ValueError(f"Không tìm thấy vật tư với ID {item_id}")
    
    def search_items(self, keyword, field="name"):
        keyword = keyword.lower()
        return [item for item in self.inventory 
                if keyword in str(item.get(field, "")).lower()]
    
    def sort_items(self, sort_by="name", reverse=False):
        if sort_by == "name":
            return sorted(self.inventory, key=lambda x: x["name"].lower(), reverse=reverse)
        elif sort_by == "quantity":
            return sorted(self.inventory, key=lambda x: x["current_quantity"], reverse=reverse)
        elif sort_by == "value":
            return sorted(self.inventory, 
                          key=lambda x: x["current_quantity"] * x["unit_price"], 
                          reverse=reverse)
        return self.inventory
    
    def get_low_stock_items(self, threshold=5):
        return [item for item in self.inventory if item["current_quantity"] <= threshold]
    
    def get_inventory_value(self):
        return sum(item["current_quantity"] * item["unit_price"] for item in self.inventory)
    
    def add_supplier(self, supplier_data):
        if not all(key in supplier_data for key in ["name", "contact"]):
            raise ValueError("Thiếu thông tin bắt buộc cho nhà cung cấp")
        
        new_id = max([s["id"] for s in self.suppliers], default=0) + 1
        
        supplier = {
            "id": new_id,
            "name": supplier_data["name"],
            "contact": supplier_data["contact"],
            "notes": supplier_data.get("notes", ""),
            "created_at": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        self.suppliers.append(supplier)
        self.save_data()
        return supplier
    
    def delete_supplier(self, supplier_id):
        try:
            related_items = [item for item in self.inventory 
                           if item.get("supplier") == supplier_id]
            # Thực sự xóa các vật tư liên quan
            self.inventory = [item for item in self.inventory 
                             if item.get("supplier") != supplier_id]
            initial_supplier_count = len(self.suppliers)
            self.suppliers = [s for s in self.suppliers if s["id"] != supplier_id]
            
            if len(self.suppliers) < initial_supplier_count:
                for index, supplier in enumerate(self.suppliers):
                    supplier["id"] = index + 1
                
                self.save_data()
                return len(related_items)  
            return -1
        except Exception as e:
            print(f"Lỗi khi xóa nhà cung cấp: {str(e)}")
            return -1
        
    def update_supplier(self, supplier_id, update_data):
        for i, supplier in enumerate(self.suppliers):
            if supplier["id"] == supplier_id:
                self.suppliers[i] = {**supplier, **update_data}
                for item in self.inventory:
                    if item.get("supplier") == supplier_id:
                        item["supplier_name"] = update_data["name"]
                return True
        return False
    
    def get_supplier_by_id(self, supplier_id):
        return next((s for s in self.suppliers if s["id"] == supplier_id), None)
