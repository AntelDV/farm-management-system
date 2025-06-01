import sys
import os
from pathlib import Path

# Thêm đường dẫn gốc vào sys.path để Python có thể tìm thấy các module
sys.path.append(str(Path(__file__).parent.parent))
from controllers.main_controller import MainController
import tkinter as tk


def main():
    root = tk.Tk()
    app = MainController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
