import json
import os
from datetime import datetime

class AnimalManager:
    def __init__(self):
        self.animals = []
        self.data_file = "data/animals.json"
        self._ensure_data_directory()
        self.load_data()
    
    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.animals = json.load(f)
            else:
                self.animals = []
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu vật nuôi: {str(e)}")
            self.animals = []
    
    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.animals, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu vật nuôi: {str(e)}")
            return False
    
    def add_animal(self, animal_data):
        try:
            new_id = max([a["id"] for a in self.animals], default=0) + 1
            animal_data["id"] = new_id
            animal_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.animals.append(animal_data)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm vật nuôi: {str(e)}")
            return False
    
    def update_animal(self, animal_id, update_data):
        try:
            for i, animal in enumerate(self.animals):
                if animal["id"] == animal_id:
                    update_data["id"] = animal_id
                    update_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if "created_at" in animal:
                        update_data["created_at"] = animal["created_at"]
                    self.animals[i] = update_data
                    return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật vật nuôi: {str(e)}")
            return False
    

    def delete_animal(self, animal_id):
        try:
            initial_count = len(self.animals)
            self.animals = [a for a in self.animals if a["id"] != animal_id]
            
            if len(self.animals) < initial_count:
                # Cập nhật lại ID
                for i, animal in enumerate(self.animals, 1):
                    animal["id"] = i
                self.save_data()
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi xóa vật nuôi: {str(e)}")
            return False

        
    def get_animal_by_id(self, animal_id):
        for animal in self.animals:
            if animal["id"] == animal_id:
                return animal
        return None