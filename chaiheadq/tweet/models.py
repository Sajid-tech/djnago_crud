from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tweet(models.Model):
    # without tweet user will not be done for this use foreign key , one to one
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    #  auto now add means jaise add hoga wese cerate hoga
    create_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    #  integrate with admin
    def __str__(self):
        return f"{self.user.username} - {self.text[:10]}"
