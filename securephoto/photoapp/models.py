from django.db import models
from cryptography.fernet import Fernet

class EncryptedPhoto(models.Model):
    encrypted_data = models.BinaryField()
    key = models.BinaryField()

    @classmethod
    def encrypt_photo(cls, photo):
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(photo)
        return cls.objects.create(encrypted_data=encrypted_data, key=key)

    def decrypt_photo(self):
        cipher = Fernet(self.key)
        return cipher.decrypt(self.encrypted_data)
