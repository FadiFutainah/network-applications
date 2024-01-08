import tkinter as tk
from app import TkApp
from home import HomeScreen
from data import LocalStorage
from request import send_request


class LoginScreen(TkApp):
    def __init__(self):
        super().__init__()
        self.root.title("Login Form")
        self.password_entry = None
        self.username_entry = None
        self.result_label = None
        self.render()

    def render(self):
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.login, width=15, height=2)
        login_button.pack(pady=10)

        # signup_button = tk.Button(self.root, text="Signup", command=self.navigate_to_signup, width=15, height=2)
        # signup_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", wraplength=200)
        self.result_label.pack()

    # def navigate_to_signup(self):
    #     self.root.destroy()
    #     from signup import SignupScreen
    #     SignupScreen()

    def do_login(self, response):
        LocalStorage.TOKEN = response.json().get('auth_token')
        self.root.destroy()
        HomeScreen()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        url = 'http://127.0.0.1:8000/api/auth/token/login/'

        data = {
            'username': username,
            'password': password,
        }

        send_request(
            'post',
            url,
            data,
            self.do_login,
            self.result_label,
        )
