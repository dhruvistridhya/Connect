from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):

	name = models.CharField(max_length=50)
	mobileno = models.CharField(max_length=10, blank=True)
	image = models.ImageField(default='/profile_pics/default.jpg',upload_to='profile_pics')
	user = models.ForeignKey(User,on_delete=models.CASCADE)