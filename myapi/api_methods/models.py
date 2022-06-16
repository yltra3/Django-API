from django.db import models


class DataBase(models.Model):
    id = models.primary_key = True
    encrypted_text = models.CharField(max_length=200)
    decrypted_text = models.CharField(max_length=200)
    create_at = models.DateTimeField('date published')

