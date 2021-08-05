from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# from django import forms
# from django.forms import ModelForm


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    POSITION_SET = [('customer', 'customer'), ('owner', 'owner'), ('admin', 'admin')]
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, )
    position = models.CharField(choices=POSITION_SET, max_length=30, default='customer')
    fullname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='userimages',null=True,blank=True)
    username = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email + "--" + self.username + "--" + self.position

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Hotel(models.Model):
    owner = models.OneToOneField(MyUser, primary_key=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    hotel_phone = models.IntegerField()
    hotel_address = models.CharField(max_length=50)
    star = models.IntegerField()
    hotel_image = models.ImageField(upload_to='hotel-images')
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.name+'---'+str(self.pk) 
        



class Room(models.Model):
    STATUS_SET = [('active','active'),('open','open')]
    room_name = models.CharField(max_length=30)
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    price_for_adult = models.FloatField()
    price_for_child = models.FloatField(blank=True, null=True)
    occupancy_for_adult = models.IntegerField()
    occupancy_for_child = models.IntegerField(blank=True, null=True)
    status = models.CharField(choices=STATUS_SET,max_length=30,default='open')
    total_booking = models.IntegerField(blank=True, null=True)
    active_booking = models.IntegerField(blank=True, null=True)
    room_image=models.ImageField(upload_to='room-images',blank=True, null=True)
    def __str__(self):
        return self.room_name 

class Booking(models.Model):
    STATUS_SET = [('requested', 'requested'), ('booked', 'booked'), ('rejected', 'rejected'), ('completed', 'completed')]
    customer = models.ForeignKey(MyUser, blank=True, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    date_from = models.DateField()
    date_to = models.DateField()
    number_of_adult=models.IntegerField(null=True,blank=True)
    number_of_child=models.IntegerField(null=True,blank=True)
    status = models.CharField(choices=STATUS_SET, default='requested', max_length=30)
    total_price=models.FloatField(null=True,blank=True)
    def __str__(self):
        return self.status 

class PerDayBooking(models.Model):
   
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='perdaybooking')
    date=models.DateField()
    
    def __date__(self):
        return self.date

