import json
import os
from datetime import datetime

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.data_file = "data/finance.json"
        self.categories = {
            "income": ["Bán sản phẩm", "Trợ cấp", "Đầu tư", "Khác"],
            "expense": ["Mua giống", "Mua thức ăn", "Lương nhân viên", "Thuốc thú y", "Bảo trì", "Khác"]
        }
        self.load_data()
    
    def load_data(self):
        """Tải dữ liệu giao dịch từ file JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.transactions = data.get("transactions", [])
                    self.categories = data.get("categories", self.categories)
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu tài chính: {str(e)}")
            self.transactions = []
    
    def save_data(self):
        """Lưu dữ liệu giao dịch vào file JSON"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            data = {
                "transactions": self.transactions,
                "categories": self.categories
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu tài chính: {str(e)}")
    
    def add_transaction(self, transaction_data):
        """Thêm giao dịch mới"""
        # Validate dữ liệu
        if not all(key in transaction_data for key in ["type", "amount", "category", "description"]):
            raise ValueError("Thiếu thông tin bắt buộc cho giao dịch")
        
        if transaction_data["amount"] <= 0:
            raise ValueError("Số tiền phải lớn hơn 0")
        
        # Tạo ID mới (tìm ID lớn nhất hiện có + 1)
        new_id = max([t["id"] for t in self.transactions], default=0) + 1
        
        transaction_data["id"] = new_id
        transaction_data["date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.transactions.append(transaction_data)
        self.save_data()
        return transaction_data
    
    def update_transaction(self, transaction_id, update_data):
        """Cập nhật giao dịch"""
        for transaction in self.transactions:
            if transaction["id"] == transaction_id:
                # Validate dữ liệu
                if "amount" in update_data and update_data["amount"] <= 0:
                    raise ValueError("Số tiền phải lớn hơn 0")
                
                for key, value in update_data.items():
                    if key in ["type", "amount", "category", "description"]:
                        transaction[key] = value
                transaction["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
                self.save_data()
                return transaction
        raise ValueError(f"Không tìm thấy giao dịch với ID {transaction_id}")
    
    def delete_transaction(self, transaction_id):
        """Xóa giao dịch"""
        original_count = len(self.transactions)
        self.transactions = [t for t in self.transactions if t["id"] != transaction_id]
        
        if len(self.transactions) == original_count:
            raise ValueError(f"Không tìm thấy giao dịch với ID {transaction_id}")
        
        self.save_data()
        return True
    
    def get_transactions(self, start_date=None, end_date=None, trans_type=None, category=None, sort_by="date", reverse=True):
        """Lấy danh sách giao dịch với bộ lọc và sắp xếp"""
        filtered = self.transactions
        
        if start_date:
            filtered = [t for t in filtered if datetime.strptime(t["date"], "%d/%m/%Y %H:%M") >= datetime.strptime(start_date, "%d/%m/%Y")]
        if end_date:
            filtered = [t for t in filtered if datetime.strptime(t["date"], "%d/%m/%Y %H:%M") <= datetime.strptime(end_date, "%d/%m/%Y")]
        if trans_type:
            filtered = [t for t in filtered if t["type"] == trans_type]
        if category:
            filtered = [t for t in filtered if t["category"] == category]
        
        # Sắp xếp
        if sort_by == "date":
            filtered.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y %H:%M"), reverse=reverse)
        elif sort_by == "amount":
            filtered.sort(key=lambda x: x["amount"], reverse=reverse)
        
        return filtered
    
    def get_balance(self):
        """Tính toán số dư hiện tại"""
        balance = 0.0
        for transaction in self.transactions:
            if transaction["type"] == "income":
                balance += transaction["amount"]
            else:
                balance -= transaction["amount"]
        return balance
    
    def get_summary(self, period="month"):
        """Tổng hợp doanh thu, chi phí theo period (day/week/month/year)"""
        now = datetime.now()
        summaries = {}
        
        for trans in self.transactions:
            trans_date = datetime.strptime(trans["date"], "%d/%m/%Y %H:%M")
            
            if period == "day":
                key = trans_date.strftime("%d/%m/%Y")
            elif period == "week":
                key = f"{trans_date.isocalendar()[1]}-{trans_date.year}"
            elif period == "month":
                key = trans_date.strftime("%m/%Y")
            else:  # year
                key = trans_date.strftime("%Y")
            
            if key not in summaries:
                summaries[key] = {"income": 0, "expense": 0}
            
            summaries[key][trans["type"]] += trans["amount"]
        
        return summaries