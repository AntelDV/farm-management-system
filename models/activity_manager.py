import json
import os
from datetime import datetime

class ActivityManager:
    def __init__(self):
        self.activities = []
        self.data_file = "data/activities.json"
        self._ensure_data_directory()
        self.load_data()
    
    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.activities = json.load(f)
            else:
                self.activities = []
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu hoạt động: {str(e)}")
            self.activities = []
    
    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.activities, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu hoạt động: {str(e)}")
            return False
    
    def add_activity(self, activity_data):
        try:
            new_id = max([a["id"] for a in self.activities], default=0) + 1
            activity_data["id"] = new_id
            activity_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.activities.append(activity_data)
            return True
        except Exception as e:
            print(f"Lỗi khi thêm hoạt động: {str(e)}")
            return False
    
    def update_activity(self, activity_id, update_data):
        try:
            for i, activity in enumerate(self.activities):
                if activity["id"] == activity_id:
                    update_data["id"] = activity_id
                    update_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if "created_at" in activity:
                        update_data["created_at"] = activity["created_at"]
                    self.activities[i] = update_data
                    return True
            return False
        except Exception as e:
            print(f"Lỗi khi cập nhật hoạt động: {str(e)}")
            return False
    
    def delete_activity(self, activity_id):
        try:
            initial_count = len(self.activities)
            # Xóa hoạt động theo ID
            self.activities = [a for a in self.activities if a["id"] != activity_id]
            
            if len(self.activities) < initial_count:
                # Cập nhật lại ID cho các hoạt động còn lại
                for index, activity in enumerate(self.activities, 1):
                    activity["id"] = index
                self.save_data()
                return True
            return False
        except Exception as e:
            print(f"Lỗi khi xóa hoạt động: {str(e)}")
            return False