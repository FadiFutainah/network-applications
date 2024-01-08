import tkinter as tk
from app import TkApp
from request import send_request
from data import LocalStorage


class HomeScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Home Screen")
        self.label = None
        self.result_label = None
        self.message_label = None
        self.logout_button = None
        self.checkbox_frame = None
        self.all_files_button = None
        self.currently_editing = None
        self.upload = None
        self.render()

    def render(self):
        self.message_label = tk.Label(self.root, text="You are logged in", font=('Helvetica', 14, 'bold'))
        self.message_label.pack(pady=20)

        self.label = tk.Label(self.root, text="List of Files:")
        self.label.pack(pady=10)

        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.pack()

        self.all_files_button = tk.Button(self.root, text="All files", command=self.navigate_to_all_files, width=15,
                                          height=2)
        self.all_files_button.pack(pady=10)

        self.currently_editing = tk.Button(self.root, text="Currently editing", command=self.navigate_to_my_files,
                                           width=15, height=2)
        self.currently_editing.pack(pady=10)

        self.upload = tk.Button(self.root, text="Upload", command=self.upload_files, width=15, height=2)
        self.upload.pack(pady=10)

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout, width=15, height=2)
        self.logout_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def logout(self):
        url = 'http://127.0.0.1:8000/api/auth/token/logout/'
        send_request(
            'post',
            url,
            {},
            self.logout_callback,
            self.result_label,
        )

    def logout_callback(self, response):
        self.root.destroy()
        LocalStorage.TOKEN = ''
        from login import LoginScreen
        LoginScreen()

    def navigate_to_all_files(self):
        self.root.destroy()
        from all_files import AllFilesScreen
        AllFilesScreen()

    def navigate_to_my_files(self):
        from my_files import MyFilesScreen
        self.root.destroy()
        MyFilesScreen()

    def upload_files(self):
        pass
        # from upload_files import UploadFilesScreen
        # self.root.destroy()
        # UploadFilesScreen()
