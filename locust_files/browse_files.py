from locust import HttpUser, task, between


class DesktopUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post('api/auth/token/login/', data={'username': 'test', 'password': '123'})
        self.token = response.json().get('auth_token')

    @task
    def view_files(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Token {self.token}'
        }

        self.client.get('/api/files/file/', headers=headers)
