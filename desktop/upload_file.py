import tkinter as tk
from tkinter import filedialog

import requests

from app import TkApp
from data import LocalStorage
from request import send_request


class UploadFileScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Home Screen")
        self.label = None
        self.result_label = None
        self.message_label = None
        self.select_button = None
        self.file_path_label = None
        self.back_button = None
        self.upload_button = None
        self.selected_file_path = ''
        self.render()

    def render(self):
        self.message_label = tk.Label(self.root, text="Choose File to upload", font=('Helvetica', 14, 'bold'))
        self.message_label.pack(pady=20)

        self.file_path_label = tk.Label(self.root, text="Selected File:")
        self.file_path_label.pack()

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.back_button = tk.Button(self.root, text="Upload", command=self.upload, width=15, height=2)
        self.back_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back", command=self.pop_back, width=15, height=2)
        self.back_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=f"Selected File: {file_path}")
        self.selected_file_path = file_path

    def upload(self):
        try:
            file = {'file': open(self.selected_file_path, 'rb').read()}
            local_storage = LocalStorage()
            url = 'http://127.0.0.1:8000/api/files/file/'
            headers = {}
            token = local_storage.get_token()
            if token:
                headers['Authorization'] = f'Token {token}'
            response = requests.post(url, headers=headers, files=file, data={})
            if 200 <= response.status_code < 300:
                tk.messagebox.showinfo('Success', 'File uploaded successfully!')
            else:
                tk.messagebox.showerror('Error', f'Failed to upload file. Status code: {response.status_code}')
        except Exception as e:
            tk.messagebox.showerror('Error', f'An error occurred: {e}')

    def pop_back(self):
        self.root.destroy()
        from home import HomeScreen
        HomeScreen()
