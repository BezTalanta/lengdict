import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class MUser(AbstractUser):
    is_email_confirmed = models.BooleanField('Has user confirmed email',
                                             default=False)
    is_user_premium = models.BooleanField('Has user premium',
                                          default=False)

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ['email']
        ordering = ['is_user_premium']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserEmailConfirmation(models.Model):
    token = models.UUIDField('Confirmation token',
                             primary_key=True,
                             default=uuid.uuid4,
                             unique=True)
    user = models.OneToOneField(MUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user}'s token to email confirm and his email {self.user.is_email_confirmed}"
