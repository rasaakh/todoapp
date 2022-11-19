from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# from accounts.models import User
# Create your models here.
User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "user"