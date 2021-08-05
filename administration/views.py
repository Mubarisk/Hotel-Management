from django.core.exceptions import ObjectDoesNotExist
from django.db.models.expressions import F
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from customers.models import Booking, MyUser, Hotel, Room
from django.contrib.auth import logout
from django.conf import settings
from django.db.models import Avg, Count, Min, Sum
from django.core import serializers
import datetime
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from customers.forms import HotelForm, MyUserForm,EditUserForm


def position_evaluater(function):
    def wraper(request, *args, **kwargs):
        if request.user.position == 'admin':
            return function(request, *args, **kwargs)
        elif request.user.position == 'customer':
            return redirect('/')
        elif request.user.position == 'owner':
            return redirect('/hotel/')

    return wraper


@login_required
@position_evaluater
def admin_panel(request):
    data = []
    try:
        active_hotels = Hotel.objects.order_by('name').filter(status=True)
        for hotel in active_hotels:
            total_oc = hotel.room_set.aggregate(
                oc=Sum('occupancy_for_adult') + Sum('occupancy_for_child'))
            temp_data = {}

            temp_data = model_to_dict(
                hotel, fields=['name', 'hotel_phone', 'star', 'owner'])
            temp_data['room_count'] = hotel.room_set.count()
            temp_data['oc'] = total_oc['oc']
            data.append(temp_data)

        # print(data)
        try:
            pending_hotels = Hotel.objects.order_by(
                'name').filter(status=False)
            # print(pending_hotels)

            return render(request, 'admin.html', {'active_hotels': data, 'pending_hotels': pending_hotels})
        except ObjectDoesNotExist:

            return render(request, 'admin.html', {'active_hotels': active_hotels})
    except ObjectDoesNotExist:

        return render(request, 'admin.html')


@login_required
@position_evaluater
def add_hotel(request):
    if request.method == 'POST':
        user_form = MyUserForm(request.POST, request.FILES)
        hotel_form = HotelForm(request.POST, request.FILES)

        if user_form.is_valid() and hotel_form.is_valid():

            user = user_form.save(commit=False)
            user.position='owner'
            user.save()
            hotel = hotel_form.save(commit=False)
            hotel.owner = user
            hotel.save()
        # email send to the owner about the login cdentials
            subject = 'welcome '
            message = 'youre registered  your username : ' + user_form.cleaned_data['email'] + '\n your password :' + \
                    user_form.cleaned_data['password1']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_form.cleaned_data['email']]
            send_mail(subject, message, email_from, recipient_list)
    
            return redirect('/admin/')
    user_form = MyUserForm()
    hotel_form = HotelForm()
    return render(request, 'add-hotel.html', {'user_form': user_form, 'hotel_form': hotel_form})
            


@position_evaluater
def edit_hotel(request, pk):
    owner = MyUser.objects.get(pk=pk)
    hotel = Hotel.objects.get(pk=pk)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, request.FILES,instance=owner)
        hotel_form=HotelForm(request.POST, request.FILES,instance=hotel)
        if user_form.is_valid():
            user_form.save()
            if hotel_form.is_valid():
                hotel_form.save()
        
        return redirect('/admin/')
    user_form = EditUserForm()
    hotel_form = HotelForm()
    return render(request, 'edit-hotel.html',  {'user_form': user_form, 'hotel_form': hotel_form})


@position_evaluater
def delete_hotel(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    user = MyUser.objects.get(pk=pk)
    hotel.delete()
    user.delete()
    return redirect('/admin/')


@position_evaluater
def view_hotel(request, pk):
    hotel = Hotel.objects.get(pk=pk)

    try:
        rooms = Room.objects.filter(hotel_id=hotel.pk)
        try:
            today_booking = 0
            total_booking = 0
            # date = datetime.datetime.now()
            # print(date)
            for room in rooms:
                active_booking = Booking.objects.filter(
                    room__pk=room.id).filter(date_from=datetime.date.today())
                if active_booking:
                    today_booking = today_booking+1

            for room in rooms:
                upcoming_booking = Booking.objects.filter(
                    room__pk=room.id).filter(date_from__gt=datetime.date.today())
                if upcoming_booking:
                    total_booking = total_booking+1

            return render(request, 'view-hotel.html', {'details': hotel, 'rooms': rooms, 'booking_today': today_booking, 'total_booking': today_booking+today_booking})
        except ObjectDoesNotExist:
            return render(request, 'view-hotel.html', {'details': hotel, 'rooms': rooms})

    except ObjectDoesNotExist:
        return render(request, 'view-hotel.html', {'details': hotel})




# @login_required
# @user_passes_test(admincheck)
def logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('/accounts/login/')

# @login_required
# @user_passes_test(admincheck)


def reset_password(request, pk):
    owner = MyUser.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST['pass1'] == request.POST['pass2']:
            owner.set_password(request.POST['pass1'])
            owner.save()
            print(owner.email)
            subject = 'your password  changed  '
            message = 'youre new password : ' + request.POST['pass1']
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [owner.email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('/admin/')

    return render(request, 'reset.html')
