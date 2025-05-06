import base64
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class EncryptWindow(ctk.CTkFrame):
    def __init__(self, parent, back_callback):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(self, text="Encrypt & Hide Files", font=("Arial", 18, "bold")).pack(pady=5)

        # File Path Entry
        self.path_entry = ctk.CTkEntry(self, state="disabled", width=300)
        self.path_entry.pack(pady=5)
        ctk.CTkButton(self, text="Select File", command=self.select_file).pack(pady=5)

        # Image Path Entry
        self.image_entry = ctk.CTkEntry(self, state="disabled", width=300)
        self.image_entry.pack(pady=5)
        ctk.CTkButton(self, text="Select Image", command=self.select_image).pack(pady=5)

        # Password Entry
        ctk.CTkLabel(self, text="Enter Password:", font=("Arial", 14)).pack(pady=5)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter a password", show="*", width=300)
        self.password_entry.pack(pady=5)

        # Bottom-right Buttons
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(side="bottom", fill="x", pady=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Back",
            command=back_callback,
            hover_color="red",
            width=80,
            height=30
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=back_callback,
            hover_color="red",
            width=80,
            height=30
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="Encrypt",
            command=self.encrypt_and_hide,
            hover_color="green",
            width=80,
            height=30
        ).pack(side="right", padx=5)

    def select_file(self):
        path = filedialog.askopenfilename(title="Select File")
        if path:
            self.path_entry.configure(state="normal")
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)
            self.path_entry.configure(state="disabled")

    def select_image(self):
        path = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("PNG Images", "*.png")])
        if path:
            self.image_entry.configure(state="normal")
            self.image_entry.delete(0, "end")
            self.image_entry.insert(0, path)
            self.image_entry.configure(state="disabled")

    def encrypt_and_hide(self):
        file_path = self.path_entry.get().strip()
        image_path = self.image_entry.get().strip()
        password = self.password_entry.get().strip()

        if not file_path or not image_path or not password:
            messagebox.showerror("Error", "Please select a file, an image, and enter a password.")
            return

        try:
            filename = os.path.basename(file_path)  # Extract file name
            file_dir = os.path.dirname(file_path)  # Get directory where the file is from
            key = self.generate_key(password)
            encrypted_data = self.encrypt_file(file_path, key)

            # Modify image filename for output
            image_name, ext = os.path.splitext(os.path.basename(image_path))
            output_filename = f"{image_name}_stego{ext}"  # Example: example_stego.png
            output_path = os.path.join(file_dir, output_filename)  # Save in same directory

            # Embed the encrypted data inside the image
            with open(image_path, "rb") as img, open(output_path, "wb") as out_img:
                out_img.write(img.read())  
                out_img.write(b"\n#####HIDDEN_DATA#####\n")  
                out_img.write(filename.encode() + b"\n")  
                out_img.write(encrypted_data)  

            messagebox.showinfo("Success", f"File encrypted and hidden inside: {file_dir}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_key(self, password):
        return Fernet(base64.urlsafe_b64encode(password.encode().ljust(32, b'0')))

    def encrypt_file(self, file_path, key):
        with open(file_path, "rb") as file:
            data = file.read()
        return key.encrypt(data)

