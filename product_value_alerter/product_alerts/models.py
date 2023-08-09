from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class URLs_Feed_Abstract(models.Model):
    url_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class URLs_Feed(URLs_Feed_Abstract):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    Url=models.TextField()
    product_name=models.TextField()
    Original_price=models.IntegerField()
    Current_price=models.IntegerField()
    # Expected_price=models.IntegerField(default=None)
    lowest_price=models.IntegerField()
    class Meta:
        ordering=('-created_at',)
    def __str__(self):
        return f"{self.user} : {self.product_name}"
