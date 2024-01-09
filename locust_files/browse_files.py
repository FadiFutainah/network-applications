from locust import HttpUser, task

class DesktopUser(HttpUser):
    @task
    def view_files(self):
        self.client.get('/api/files/file/', name='/files/file/')
