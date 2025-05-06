import customtkinter as ctk
from PIL import Image
from ui.encrypt import EncryptWindow 
from ui.decrypt import DecryptWindow
import os
import sys


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainUI:
    def __init__(self, root):
        self.root = root
        self.main_menu()

    def main_menu(self):
        self.clear_frame()

        button_width = 150
        button_height = 50

        # Create a frame to hold the buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=20)

        # Load images
        # organize_icon = ctk.CTkImage(Image.open("assets\\organize_icon.png"), size=(70, 70))

        # Organize Files button
        organize_button = ctk.CTkButton(
            button_frame,
            fg_color="black",
            text="Encrypt Files",
            command=self.open_encrypt_files,
            compound="top",
            width=button_width,
            height=button_height

        )
        organize_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Decrypt Files button
        decrypt_button = ctk.CTkButton(
            button_frame,
            fg_color="black",
            text="Decrypt Files",
            command=self.open_decrypt_files,
            compound="top",
            width=button_width,
            height=button_height
        )
        decrypt_button.grid(row=0, column=1, padx=10, pady=10)
        
        

        about_button = ctk.CTkFrame(self.root)
        about_button.pack(side="bottom",fill="x", pady=10)

        about_button = ctk.CTkButton(
            about_button,
            text="About",
            width=50,  
            height=20  
        )
        about_button.pack(side="left",padx=5)
        
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def open_encrypt_files(self):
        self.clear_frame()
        EncryptWindow(self.root, self.main_menu)

    def open_decrypt_files(self):
        self.clear_frame()
        DecryptWindow(self.root, self.main_menu)