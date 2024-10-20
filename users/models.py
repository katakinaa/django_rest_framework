from django.db import models
from django.contrib.auth.models import User
import random


class UserConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=6)

    def generate_code(self):
        self.confirmation_code = str(random.randint(100000, 999999))
        self.save()
