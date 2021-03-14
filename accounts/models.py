from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import UserManager

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    profile_pic = models.ImageField(upload_to='profiles/',default ='profiles/avatar.png')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    objects = UserManager()

class Instructor(models.Model):
  name = models.CharField(max_length=100)
  brief_info = models.TextField()

  def __str__(self):
    return self.name