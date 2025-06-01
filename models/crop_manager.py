import json
import os
from datetime import datetime

class CropManager:
    def __init__(self):
        self.crops = []
        self.data_file = "data/crops.json"
        self._ensure_data_directory()
        self.load_data()
    
    def _ensure_data_directory(self):
        """Đảm bảo thư mục data tồn tại"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_data(self):
        """Tải dữ liệu từ file JSON"""
        try:
            if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.crops = json.load(f)
            else:
                self.crops = []
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu cây trồng: {str(e)}")
            self.crops = []
    
    def save_data(self):
        """Lưu dữ liệu vào file JSON"""
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.crops, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu cây trồng: {str(e)}")
            return False
    
    def add_crop(self, crop_data):
        """Thêm cây trồng mới"""
        try:
            # Tạo ID mới
            new_id = max([c["id"] for c in self.crops], default=0) + 1
            crop_data["id"] = new_id
            crop_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.crops.append(crop_data)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm cây trồng: {str(e)}")
            return False
    
    def update_crop(self, crop_id, update_data):
        """Cập nhật thông tin cây trồng"""
        try:
            for i, crop in enumerate(self.crops):
                if crop["id"] == crop_id:
                    update_data["id"] = crop_id
                    update_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if "created_at" in crop:
                        update_data["created_at"] = crop["created_at"]
                    self.crops[i] = update_data
                    return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật cây trồng: {str(e)}")
            return False
    
    

    def delete_crop(self, crop_id):
        try:
            initial_count = len(self.crops)
            self.crops = [c for c in self.crops if c["id"] != crop_id]
            
            if len(self.crops) < initial_count:
                # Cập nhật lại ID
                for i, crop in enumerate(self.crops, 1):
                    crop["id"] = i
                self.save_data()
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi xóa cây trồng: {str(e)}")
            return False
        
    