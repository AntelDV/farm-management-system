from views.activity_views import ActivityViews
from models.activity_manager import ActivityManager

class ActivityController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = ActivityViews(self)
        self.activity_manager = ActivityManager()
        self.activity_manager.load_data()
    
    def show_activity_management(self):
        self.main.clear_window()
        self.main.weather_controller.views.show_weather_widget(force_clear=True)
        if self.main.auth_controller.current_user["role"] == "admin":
            try:
                self.activity_manager.load_data()  
                self.views.show_activity_management()
                self.display_activities()
            except Exception as e:
                self.views.show_error_message(f"Lỗi khi tải dữ liệu: {str(e)}")
                self.main.show_main_menu()
    def show_activity_view(self):
        self.activity_manager.load_data()
        self.views.show_activity_management()
        self.display_activities()
    

    def display_activities(self, activities=None):
        self.views.display_activities(activities or self.activity_manager.activities)
    
    def search_activities(self, keyword):
        if not keyword:
            self.display_activities()
            return
        
        filtered_activities = [
            activity for activity in self.activity_manager.activities
            if (keyword.lower() in activity["name"].lower() or 
                keyword.lower() in activity["type"].lower())
        ]
        self.display_activities(filtered_activities)
    
    def show_add_activity_form(self):
        self.views.show_add_activity_form()
    
    def add_activity(self, activity_data):
        try:
            result = self.activity_manager.add_activity(activity_data)
            if result:
                self.activity_manager.save_data()
                self.display_activities()
                self.views.show_activity_management
                self.views.show_success_message("Thêm hoạt động thành công")
                return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def show_edit_activity_form(self):
        selected_item = self.views.get_selected_activity()
        if selected_item:
            self.views.show_edit_activity_form(selected_item)
    
    def edit_activity(self, activity_id, update_data):
        try:
            result = self.activity_manager.update_activity(activity_id, update_data)
            if result:
                self.activity_manager.save_data()
                self.display_activities()
                self.views.show_activity_management()
                self.views.show_success_message("Cập nhật thành công")
                return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def delete_activity(self):
        selected_item = self.views.get_selected_activity()
        if selected_item:
            confirm = self.views.show_confirm_dialog("Bạn có chắc muốn xóa?")
            if confirm:
                try:
                    result = self.activity_manager.delete_activity(selected_item["id"])
                    if result:
                        self.activity_manager.save_data()
                        self.display_activities()  # Cập nhật lại hiển thị
                        self.views.show_success_message("Xóa thành công")
                        return True
                    return False
                except Exception as e:
                    self.views.show_error_message(f"Lỗi: {str(e)}")
                    return False
        return False
    
    def get_activity_by_id(self, activity_id):
        for activity in self.activity_manager.activities:
            if activity.get("id") == activity_id:
                return activity
        return None