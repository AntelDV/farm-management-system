from views.crop_views import CropViews
from models.crop_manager import CropManager

class CropController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = CropViews(self)
        self.crop_manager = CropManager()
        self.crop_manager.load_data()
    
  
    def show_crop_management(self):
        self.main.clear_window()
        self.main.weather_controller.views.show_weather_widget(force_clear=True)
        if self.main.auth_controller.current_user["role"] != "admin":
            self.views.show_error_message("Bạn không có quyền truy cập chức năng này")
            return
        
        try:
            self.crop_manager.load_data()  
            self.views.show_crop_management()
            self.display_crops()
        except Exception as e:
            self.views.show_error_message(f"Lỗi khi tải dữ liệu: {str(e)}")

    def show_crop_view(self):
        self.crop_manager.load_data()
        self.views.show_crop_management()
        self.display_crops()

    
    def display_crops(self, crops=None):
        """Hiển thị danh sách cây trồng"""
        self.views.display_crops(crops or self.crop_manager.crops)
    
    def search_crops(self, keyword):
        """Tìm kiếm cây trồng"""
        if not keyword:
            self.display_crops()
            return
        
        filtered_crops = [
            crop for crop in self.crop_manager.crops
            if (keyword.lower() in crop["name"].lower() or 
                keyword.lower() in crop["type"].lower() or
                keyword.lower() in crop["status"].lower())
        ]
        self.display_crops(filtered_crops)
    
    def show_add_crop_form(self):
        """Hiển thị form thêm cây trồng"""
        self.views.show_add_crop_form()
    
    def add_crop(self, crop_data):
        """Thêm cây trồng mới và tự động lưu"""
        try:
            result = self.crop_manager.add_crop(crop_data)
            if result:
                self.crop_manager.save_data()
                self.display_crops()
                self.views.show_crop_management()
                self.views.show_success_message("Thêm cây trồng thành công")
                return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def show_edit_crop_form(self):
        """Hiển thị form chỉnh sửa"""
        selected_item = self.views.get_selected_crop()
        if selected_item:
            self.views.show_edit_crop_form(selected_item)
    
    def edit_crop(self, crop_id, update_data):
        """Cập nhật thông tin cây trồng"""
        try:
            result = self.crop_manager.update_crop(crop_id, update_data)
            if result:
                self.crop_manager.save_data()
                self.display_crops()
                self.views.show_crop_management()
                self.views.show_success_message("Cập nhật thành công")
                return True
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False

    def delete_crop(self, crop_id=None):
        if crop_id is None:
            selected_item = self.views.get_selected_crop()
            if selected_item:
                crop_id = selected_item["id"]
            else:
                return False
        
        confirm = self.views.show_confirm_dialog("Bạn có chắc muốn xóa?")
        if confirm:
            try:
                result = self.crop_manager.delete_crop(crop_id)
                if result:
                    self.crop_manager.save_data()
                    self.display_crops()
                    self.views.show_success_message("Xóa thành công")
                    return True
                return False
            except Exception as e:
                self.views.show_error_message(f"Lỗi: {str(e)}")
                return False
        return False
    
    def get_crop_by_id(self, crop_id):
        """Lấy thông tin cây trồng theo ID"""
        return self.crop_manager.get_crop_by_id(crop_id)