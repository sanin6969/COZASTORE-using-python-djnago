from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class MyaccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('invalid email address')
        if not username:
            raise ValueError('invalid username')
        user=self.model(
            email       =self.normalize_email(email),
            username    =username,
            first_name  =first_name,
            last_name   =last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(
            email       =self.normalize_email(email),
            username    =username,
            first_name  =first_name,
            last_name   =last_name,
            password    =password
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
        
        
        
class Account(AbstractBaseUser):
    first_name      =models.CharField(max_length=50)
    last_name       =models.CharField(max_length=50)
    username        =models.CharField(max_length=50,unique=True)
    email           =models.EmailField(max_length=254,unique=True)
    phone_number    =models.CharField(max_length=50,null=True)
    
    # required
    date_joined     =models.DateTimeField(auto_now_add=True)
    last_logined     =models.DateTimeField(auto_now_add=True)
    is_admin        =models.BooleanField(default=False)
    is_staff        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=False)
    is_superadmin   =models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    #To change username into email for using login
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']
    
    objects=MyaccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
class UserProfile(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    address_line_1=models.CharField(blank=True,max_length=200)
    address_line_2=models.CharField(blank=True,max_length=200)
    profile_picture=models.ImageField(blank=True,upload_to='photos/user')
    city=models.CharField(blank=True,max_length=20)
    state=models.CharField(blank=True,max_length=20)
    country=models.CharField(blank=True,max_length=20)
    def __str__(self) -> str:
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'