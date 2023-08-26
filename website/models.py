from django.db import models

# Create your models here.
class Record(models.Model):
    
    created_at = models.DateTimeField(  auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    phone_no = models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    zipcode=models.CharField(max_length=20 , default=0)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
    