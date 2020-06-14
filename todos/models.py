from django.db import models

# Create your models here.
class todo(models.Model):
    username=models.CharField(max_length=50)
    title=models.CharField(max_length=30)
    description=models.CharField(max_length=500)
    date=models.DateTimeField(auto_now_add=True)