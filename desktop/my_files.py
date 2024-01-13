import tkinter as tk
from tkinter import filedialog

import requests

from app import TkApp
from data import LocalStorage
from request import send_request


class MyFilesScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Home Screen")
        self.label = None
        self.result_label = None
        self.message_label = None
        self.select_button = None
        self.file_path_label = None
        self.back_button = None
        self.radio_button = None
        self.check_out_button = None
        self.radio_frame = None
        self.radio_var = tk.StringVar()
        self.radio_var.set(None)
        self.selected_file_path = ''
        self.file_list = []
        self.render()
        self.initial_state()

    def render(self):
        self.message_label = tk.Label(self.root, text="Choose File to checkout from", font=('Helvetica', 14, 'bold'))
        self.message_label.pack(pady=20)

        self.label = tk.Label(self.root, text="List of Files:")
        self.label.pack(pady=10)

        self.file_path_label = tk.Label(self.root, text="Selected File:")
        self.file_path_label.pack()

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack()

        self.radio_frame = tk.Frame(self.root)
        self.radio_frame.pack()

        self.check_out_button = tk.Button(self.root, text="Check-out", command=self.check_out, width=15, height=2)
        self.check_out_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back", command=self.pop_back, width=15, height=2)
        self.back_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def select_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.config(text=f"Selected File: {file_path}")
        self.selected_file_path = file_path

    def initial_state(self):
        self.get_files()

    def set_state(self, response):
        self.file_list = response.json()
        self.update_radios()

    def get_files(self):
        url = 'http://127.0.0.1:8000/api/files/file/?editing=true'
        send_request(
            'get',
            url,
            {},
            self.set_state,
            self.result_label,
        )

    def check_out(self):
        try:
            files = {'file': open(self.selected_file_path, 'rb').read()}
            local_storage = LocalStorage()
            selected_index = self.radio_var.get()
            selected_id = self.file_list[int(selected_index)]['id']
            url = f'http://127.0.0.1:8000/api/files/checkout/{selected_id}/'
            headers = {}
            token = local_storage.get_token()
            if token:
                headers['Authorization'] = f'Token {token}'
            response = requests.put(url, files=files, headers=headers)
            if response.status_code == 200:
                self.pop_back()
                tk.messagebox.showinfo('Success', 'File uploaded successfully!')
            else:
                tk.messagebox.showerror('Error', f'Failed to upload file. Status code: {response.status_code}')
        except Exception as e:
            tk.messagebox.showerror('Error', f'An error occurred: {e}')

    def update_radios(self):
        for radio_button in self.radio_frame.winfo_children():
            radio_button.destroy()
        for i, file in enumerate(self.file_list):
            radio_button = tk.Radiobutton(self.radio_frame, text=f"{file['name']} - editor is {file['editor']} ",
                                          variable=self.radio_var, value=i, font=("Helvetica", 10))
            radio_button.pack(anchor="w")

    def pop_back(self):
        self.root.destroy()
        from home import HomeScreen
        HomeScreen()
