# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
# class Role(models.Model):
#     ROLE_CHOICES = (
#         ('user', 'User'),
#         ('admin', 'Admin'),
#     )
#     role_name = models.CharField(max_length=50, choices=ROLE_CHOICES)
#     role_desc = models.CharField(max_length=200, null=True, blank=True)
#
#     def __str__(self):
#         return self.role_name
#
# # def get_user_role():
# #     return Role.objects.get_or_create(role_name='user')[0].id
#
# class CustomUser(AbstractUser):
#     username = models.CharField(max_length=255, unique=False, blank=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=20)
#     role = models.ForeignKey(Role, on_delete=models.SET("user"), default="user")
#
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"