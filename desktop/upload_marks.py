import tkinter as tk
from tkinter import filedialog

import requests

from app import TkApp
from crypto.rsa_signer import RSASigner
from request import send_request


class UploadMarksScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Add Project Form")
        self.select_button = None
        self.upload_button = None
        self.file_path_label = None
        self.back_button = None
        self.result_label = None
        self.selected_file_path = None
        self.render()

    def render(self):
        self.file_path_label = tk.Label(self.root, text="Selected File:")
        self.file_path_label.pack()

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.pack()

        self.back_button = tk.Button(self.root, text="Back to Home", command=self.back_to_home, width=15, height=2)
        self.back_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=f"Selected File: {file_path}")
        self.selected_file_path = file_path

    def upload_file(self):
        try:
            files = {'file': open(self.selected_file_path, 'rb')}
            with open(self.selected_file_path) as file:
                file_data = file.read()
            private_key, public_key = RSASigner.generate_key_pair()
            signature = RSASigner.sign_data(private_key, file_data)
            data = {'signature': signature, 'public_key': public_key}
            # TODO: change URL
            url = 'http://127.0.0.1:8000/api/system/mark/'
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                tk.messagebox.showinfo('Success', 'File uploaded successfully!')
            else:
                tk.messagebox.showerror('Error', f'Failed to upload file. Status code: {response.status_code}')

        except Exception as e:
            tk.messagebox.showerror('Error', f'An error occurred: {e}')

    def back_to_home(self):
        from home import HomeScreen
        self.root.destroy()
        HomeScreen()
