import base64
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

class DecryptWindow(ctk.CTkFrame):
    def __init__(self, parent, back_callback):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(self, text="Extract & Decrypt Files", font=("Arial", 18, "bold")).pack(pady=5)

        # Image Path Entry
        self.image_entry = ctk.CTkEntry(self, state="disabled", width=300)
        self.image_entry.pack(pady=5)
        ctk.CTkButton(self, text="Select Stego Image", command=self.select_image).pack(pady=5)

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
            text="Decrypt",
            command=self.decrypt_files,
            hover_color="green",
            width=80,
            height=30
        ).pack(side="right", padx=5)

    def select_image(self):
        path = filedialog.askopenfilename(title="Select Stego Image", filetypes=[("PNG Images", "*.png")])
        if path:
            self.image_entry.configure(state="normal")
            self.image_entry.delete(0, "end")
            self.image_entry.insert(0, path)
            self.image_entry.configure(state="disabled")

    def decrypt_files(self):
        stego_image = self.image_entry.get().strip()
        password = self.password_entry.get().strip()

        if not stego_image or not password:
            messagebox.showerror("Error", "Please select the stego image and enter the password.")
            return

        try:
            with open(stego_image, "rb") as img:
                content = img.read()

            marker = b"\n#####HIDDEN_DATA#####\n"
            split_data = content.split(marker)

            if len(split_data) < 2:
                messagebox.showerror("Error", "No hidden data found or incorrect password.")
                return

            file_parts = split_data[1].split(b"\n", 1)
            filename = file_parts[0].decode()
            encrypted_data = file_parts[1]

            key = self.generate_key(password)

            # Save the extracted file in the same directory as the stego image
            stego_dir = os.path.dirname(stego_image)
            output_path = os.path.join(stego_dir, f"extracted_{filename}")

            self.decrypt_file(output_path, encrypted_data, key)

            messagebox.showinfo("Success", f"File extracted and decrypted as: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def generate_key(self, password):
        return Fernet(base64.urlsafe_b64encode(password.encode().ljust(32, b'0')))

    def decrypt_file(self, output_path, encrypted_data, key):
        decrypted_data = key.decrypt(encrypted_data)

        with open(output_path, "wb") as file:
            file.write(decrypted_data)
