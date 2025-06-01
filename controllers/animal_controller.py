from views.animal_views import AnimalViews
from models.animal_manager import AnimalManager

class AnimalController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.views = AnimalViews(self)
        self.animal_manager = AnimalManager()
        self.animal_manager.load_data()
    
    def show_animal_management(self):
        self.main.clear_window()
        self.main.weather_controller.views.show_weather_widget(force_clear=True)
        if self.main.auth_controller.current_user["role"] == "admin":
            try:
                self.animal_manager.load_data() 
                self.views.show_animal_management()
                self.display_animals()
            except Exception as e:
                self.views.show_error_message(f"Lỗi khi tải dữ liệu: {str(e)}")
                self.main.show_main_menu()
    
    def show_animal_view(self):
        self.animal_manager.load_data()
        self.views.show_animal_management()
        self.display_animals()
    
    def display_animals(self, animals=None):
        self.views.display_animals(animals or self.animal_manager.animals)
    
    def search_animals(self, keyword):
        if not keyword:
            self.display_animals()
            return
        
        filtered_animals = [
            animal for animal in self.animal_manager.animals
            if (keyword.lower() in animal["name"].lower() or 
                keyword.lower() in animal["type"].lower())
        ]
        self.display_animals(filtered_animals)
    
    def show_add_animal_form(self):
        self.views.show_add_animal_form()
    
    def add_animal(self, animal_data):
        try:
            animal_data["quantity"] = int(animal_data["quantity"])
            result = self.animal_manager.add_animal(animal_data)
            if result:
                self.animal_manager.save_data()
                self.display_animals()
                self.views.show_animal_management()
                self.views.show_success_message("Thêm vật nuôi thành công")
                return True
            return False
        except ValueError:
            self.views.show_error_message("Số lượng phải là số nguyên")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    
    def show_edit_animal_form(self):
        selected_item = self.views.get_selected_animal()
        if selected_item:
            self.views.show_edit_animal_form(selected_item)
    
    def edit_animal(self, animal_id, update_data):
        try:
            if "quantity" in update_data:
                update_data["quantity"] = int(update_data["quantity"])
            result = self.animal_manager.update_animal(animal_id, update_data)
            if result:
                self.animal_manager.save_data()
                self.display_animals()
                self.views.show_animal_management()
                self.views.show_success_message("Cập nhật thành công")
                return True
            return False
        except ValueError:
            self.views.show_error_message("Số lượng phải là số nguyên")
            return False
        except Exception as e:
            self.views.show_error_message(f"Lỗi: {str(e)}")
            return False
    

    def delete_animal(self, animal_id=None):
        if animal_id is None:
            selected_item = self.views.get_selected_animal()
            if selected_item:
                animal_id = selected_item["id"]
            else:
                return False
        
        confirm = self.views.show_confirm_dialog("Bạn có chắc muốn xóa?")
        if confirm:
            try:
                result = self.animal_manager.delete_animal(animal_id)
                if result:
                    self.animal_manager.save_data()
                    self.display_animals()
                    self.views.show_success_message("Xóa thành công")
                    return True
                return False
            except Exception as e:
                self.views.show_error_message(f"Lỗi: {str(e)}")
                return False
        return False
    
    def get_animal_by_id(self, animal_id):
        return self.animal_manager.get_animal_by_id(animal_id)