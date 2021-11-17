from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField('性',max_length=20)
    last_name = models.CharField('名',max_length=20)
    age = models.IntegerField('年齢',default=0)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent",verbose_name="代理", null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category",verbose_name="カテゴリー", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField('説明')
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField('携帯',max_length=20)
    email = models.EmailField('メール')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email

class Category(models.Model):
    name = models.CharField('カテゴリ名',max_length=30)
    organisation = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def post_user_created_signal(sender,instance,created,**kwargs):
    print(instance,created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal,sender=User)