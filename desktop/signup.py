import tkinter as tk
from app import TkApp
from login import LoginScreen
from request import send_request


class SignupScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Signup Form")
        self.session_key_entry = None
        self.password_entry = None
        self.username_entry = None
        self.result_label = None
        self.render()

    def render(self):
        tk.Label(self.root, text="IdNumber:").pack(pady=5)
        self.session_key_entry = tk.Entry(self.root, width=30)
        self.session_key_entry.pack(pady=5)

        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        signup_button = tk.Button(self.root, text="Signup", command=self.signup, width=15, height=2)
        signup_button.pack(pady=10)

        login_button = tk.Button(self.root, text="Login", command=self.navigate_to_login, width=15, height=2)
        login_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    def navigate_to_login(self):
        self.root.destroy()
        LoginScreen()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        session_key = self.session_key_entry.get()
        if username == '' or password == '':
            return

        url = 'http://127.0.0.1:8000/api/auth/un/signup/'

        data = {
            'username': username,
            'password': password,
            'session_key': session_key,
        }

        send_request(
            'post',
            url,
            data,
            self.navigate_to_login,
            self.result_label,
        )
