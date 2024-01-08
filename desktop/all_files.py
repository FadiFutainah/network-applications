import tkinter as tk
from app import TkApp
from request import send_request


class AllFilesScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Home Screen")
        self.label = None
        self.result_label = None
        self.message_label = None
        self.back_button = None
        self.check_in_button = None
        self.checkbox_frame = None
        self.checkbox_vars = []
        self.file_list = []
        self.render()
        self.initial_state()

    def render(self):
        self.message_label = tk.Label(self.root, text="Choose File to edit", font=('Helvetica', 14, 'bold'))
        self.message_label.pack(pady=20)

        self.label = tk.Label(self.root, text="List of Files:")
        self.label.pack(pady=10)

        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.pack()

        self.check_in_button = tk.Button(self.root, text="Check-in", command=self.check_in, width=15, height=2)
        self.check_in_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back", command=self.pop_back, width=15, height=2)
        self.back_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def initial_state(self):
        self.get_files()

    def set_state(self, response):
        self.file_list = response.json()
        self.update_checkboxes()

    def get_files(self):
        url = 'http://127.0.0.1:8000/api/files/file/'
        send_request(
            'get',
            url,
            {},
            self.set_state,
            self.result_label,
        )

    def check_in(self):
        selected_files = [file for file, var in zip(self.file_list, self.checkbox_vars) if var.get()]
        id_list = [file['id'] for file in selected_files]
        data = {'id_list': id_list}
        url = 'http://127.0.0.1:8000/api/files/file/check-in/'
        send_request(
            'patch',
            url,
            data,
            self.pop_back,
            self.result_label,
        )

    def update_checkboxes(self):
        for checkbox in self.checkbox_frame.winfo_children():
            checkbox.destroy()
        self.checkbox_vars = []
        for file in self.file_list:
            var = tk.BooleanVar()
            self.checkbox_vars.append(var)
            # TODO: remove this
            file['name'] = 'filename'
            file['editor'] = 'editor'
            checkbox = tk.Checkbutton(self.checkbox_frame, text=f"{file['name']} - editor is {file['editor']} ",
                                      variable=var)
            checkbox.pack(anchor="w")

    def pop_back(self):
        self.root.destroy()
        from home import HomeScreen
        HomeScreen()
