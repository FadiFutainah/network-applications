from cryptography.fernet import Fernet


class LocalStorage:
    STORAGE_PATH = 'secure_storage.env'
    KEY = Fernet.generate_key()
    TOKEN = ''

    def encrypt_token(self, token):
        cipher_suite = Fernet(self.KEY)
        cipher_text = cipher_suite.encrypt(token.encode())
        return cipher_text

    def decrypt_token(self, cipher_text):
        cipher_suite = Fernet(self.KEY)
        plain_text = cipher_suite.decrypt(cipher_text).decode()
        return plain_text

    def get_token(self):
        return self.TOKEN
        # with open(self.STORAGE_PATH, 'r') as file:
        #     token = file.read()
        # return self.decrypt_token(token)

    def store_token(self, token):
        self.TOKEN = token
        # with open(self.STORAGE_PATH, 'w') as file:
        #     file.write(str(self.encrypt_token(token)))
