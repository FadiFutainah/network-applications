import tkinter as tk
from app import TkApp
from request import send_request


class CompleteInfoScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Complete SignUp Form")
        self.first_name_entry = None
        self.last_name_entry = None
        self.email_entry = None
        self.result_label = None
        self.back_button = None
        self.render()

    def render(self):
        tk.Label(self.root, text="First Name:").pack(pady=5)
        self.first_name_entry = tk.Entry(self.root, width=30)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.root, text="Last Name:").pack(pady=5)
        self.last_name_entry = tk.Entry(self.root, width=30)
        self.last_name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.pack(pady=5)

        signup_button = tk.Button(self.root, text="Add Info", command=self.add_info, width=15, height=2)
        signup_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Back to Home", command=self.back_to_home, width=15, height=2)
        self.back_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def back_to_home(self):
        from home import HomeScreen
        self.root.destroy()
        HomeScreen()

    def add_info(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()

        url = 'http://127.0.0.1:8000/api/auth/complete-info/'
        
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }

        send_request(
            'put',
            url,
            data,
            self.back_to_home,
            self.result_label,
        )
