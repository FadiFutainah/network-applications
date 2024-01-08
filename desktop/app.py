import tkinter as tk
from data import LocalStorage


class TkApp:
    def __init__(self):
        self.root = tk.Toplevel()
        self.init_root()
        # if LocalStorage.SESSION_KEY is not None:
        #     self.aes_cipher = AESCipher(key=LocalStorage.SESSION_KEY)

    def init_root(self):
        window_width = 500
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
