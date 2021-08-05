from django.forms import ModelForm, fields,DateInput
from django.forms.models import ModelChoiceField
from .models import MyUser,Hotel, Room,Booking
# from django.forms import CharField, Form, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django import forms

class MyUserForm(UserCreationForm):
    
    class Meta:
        model=MyUser
        fields=['email','username','fullname','phone','address','image']
       

class HotelForm(ModelForm):
     class Meta:
        model=Hotel
        fields = "__all__"

class RoomForm(ModelForm):
    class Meta:
        model=Room
        exclude =['active_booking','total_booking','status','hotel']      
    
class HotelForm(ModelForm):
    class Meta:
        model=Hotel
        exclude=['status','owner']    

class EditUserForm(ModelForm):
    class Meta:
        model=MyUser
        fields=['email','username','fullname','phone','address','image']

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(ModelForm):
    
    class Meta:
        model=Booking
        fields=['date_from','date_to','number_of_adult','number_of_child']
        widgets = {
            'date_from': DateInput(),
            'date_to': DateInput(),
        }
