import tkinter as tk

from login import LoginScreen

app_root = tk.Tk()
window_width = 1
window_height = 1
screen_width = app_root.winfo_screenwidth()
screen_height = app_root.winfo_screenheight()
x_position = (screen_width - window_width)
y_position = (screen_height - window_height) // 2
app_root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

LoginScreen()
app_root.mainloop()
