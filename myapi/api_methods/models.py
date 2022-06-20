from django.db import models


class DataBase(models.Model):
    encrypted_text = models.CharField(max_length=200)
    decrypted_text = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)

