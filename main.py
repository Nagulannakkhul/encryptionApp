import customtkinter as ctk
import tkinter as tk
from ui.home import MainUI


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("SteganTheLier")
    app.geometry("500x400")
    app.resizable(False, False)
    #app.iconbitmap("assets\\logo.ico")
    MainUI(app)

    app.mainloop()
