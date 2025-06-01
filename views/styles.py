import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Màu sắc
    primary_color = '#3498db'
    secondary_color = '#95a5a6'
    danger_color = '#e74c3c'
    success_color = '#2ecc71'
    background_color = '#f0f0f0'
    text_color = '#2c3e50'
    
    # Cấu hình style chung
    style.configure('.', background=background_color, foreground=text_color)
    
    # Frame
    style.configure('TFrame', background=background_color)
    style.configure('TLabelframe', background=background_color, bordercolor=secondary_color)
    style.configure('TLabelframe.Label', background=background_color, foreground=text_color, font=('Times New Roman', 10, 'bold'))
    
    # Label
    style.configure('TLabel', background=background_color, font=('Times New Roman', 10))
    style.configure('Header.TLabel', font=('Times New Roman', 16, 'bold'), foreground=primary_color)
    style.configure('Title.TLabel', font=('Times New Roman', 14, 'bold'), foreground=primary_color)
    style.configure('StatTitle.TLabel', font=('Times New Roman', 10, 'bold'), padding=5, ANCHOR = 'center')
    style.configure('StatValue.TLabel', font=('Times New Roman', 14, 'bold'), ANCHOR = 'center')
    
    # Button
    style.configure('TButton', font=('Times New Roman', 10), padding=5)
    style.configure('Primary.TButton', foreground='white', background=primary_color)
    style.configure('Secondary.TButton', foreground='white', background=secondary_color)
    style.configure('Danger.TButton', foreground='white', background=danger_color)
    style.configure('Success.TButton', foreground='white', background=success_color)
    
    # Entry
    style.configure('TEntry', fieldbackground='white', bordercolor=secondary_color, relief='solid')
    
    # Combobox
    style.configure('TCombobox', fieldbackground='white', selectbackground=primary_color)
    
    # Treeview
    style.configure('Treeview', font=('Times New Roman', 10), rowheight=25, background='white')
    style.configure('Treeview.Heading', font=('Times New Roman', 10, 'bold'), background=secondary_color, foreground='white')
    style.map('Treeview', background=[('selected', primary_color)])
    
    # Scrollbar
    style.configure('Vertical.TScrollbar', background=secondary_color)
    
    # Radiobutton
    style.configure('TRadiobutton', background=background_color)
    
    # Cấu hình style khi hover
    style.map('Primary.TButton', background=[('active', '#2980b9')])
    style.map('Secondary.TButton', background=[('active', '#7f8c8d')])
    style.map('Danger.TButton', background=[('active', '#c0392b')])
    style.map('Success.TButton', background=[('active', '#27ae60')])
    

    # style mới cho dashboard
    style.configure('StatFrame.TFrame', anchor='center')
    style.configure('StatTitle.TLabel', font=('Times New Roman', 10, 'bold'), padding=5, anchor='center', relief='raised')
    style.configure('StatValue.TLabel', font=('Times New Roman', 14, 'bold'), anchor='center', padding=10)
    
    # style cho thanh điều hướng
    style.configure('Nav.TFrame', background='#f0f0f0', relief=tk.RAISED, borderwidth=1)
    style.configure('Nav.TButton', font=('Times New Roman', 10), padding=5)
    style.map('Nav.TButton', background=[('active', '#3498db'), ('!active', '#95a5a6')], 
                            foreground=[('active', 'white'), ('!active', 'white')])
    
    # style mới cho cảnh báo
    style.configure('Alert.TFrame', background='#FDEDEC', relief=tk.RIDGE, borderwidth=1, padding = 5)
    style.configure('Weather.TFrame', background='#EBF5FB', relief=tk.RIDGE, borderwidth=1, padding = 5)
    
    return style