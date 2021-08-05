
from datetime import datetime, timedelta
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from customers.models import Hotel, Room, Booking, PerDayBooking
from django.db.models import Min
from django.core.mail import send_mail
from django.conf import settings
from django.forms.models import model_to_dict
from .forms import BookingForm



def position_evaluater(function):
    def wraper(request, *args, **kwargs):
        if request.user.position == 'admin':
            return redirect('/admin/')
        elif request.user.position == 'customer':
            return function(request, *args, **kwargs)
        elif request.user.position == 'owner':
            return redirect('/hotel/')

    return wraper


# Create your views here.
@login_required
@position_evaluater
def home(request):
    print(request.is_secure())
    active_hotels = Hotel.objects.filter(status=True)
    data = []
    for hotel in active_hotels:
        min_price_ = hotel.room_set.aggregate(Min('price_for_adult'))
        if min_price_['price_for_adult__min']:
            temp_dict = {}
            temp_dict = model_to_dict(
                hotel, fields=['name', 'hotel_address', 'hotel_phone', 'star', 'owner'])
            temp_dict['min_price'] = min_price_['price_for_adult__min']
            data.append(temp_dict)

    pending_hotels = Hotel.objects.filter(status=False)

    return render(request, 'home.html', {'active_hotels': data, 'pending_hotels': pending_hotels, 'user': request.user})
    # return HttpResponse('ok')


@login_required
@position_evaluater
def detailed_view(request, pk):
    hotel = Hotel.objects.get(pk=pk)
    try:
        rooms = Room.objects.filter(hotel=hotel)
        return render(request, 'detail-hotel.html', {'hotel': hotel, 'rooms': rooms})
    except NameError:
        return render(request, 'detail-hotel.html', {'hotel': hotel})


@login_required
@position_evaluater
def add_booking(request, pk):
    room = Room.objects.get(pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():

            date_check1 = PerDayBooking.objects.filter(
                booking__room=pk).filter(date__gte=form.cleaned_data['date_from']).filter(date__lte=form.cleaned_data['date_to'])
            print(date_check1)
            # date_check2 = PerDayBooking.objects.filter(
            #     booking__room=pk).filter(date=form.cleaned_data['date_to'])

            if not date_check1 :

                if int(form.cleaned_data['number_of_adult']) <= int(room.occupancy_for_adult):
                    c_form = form.save(commit=False)
                    c_form.customer = request.user
                    c_form.room = room

                    if form.cleaned_data['number_of_child']:
                        if int(form.cleaned_data['number_of_child']) <= int(room.occupancy_for_child):

                            number_of_days = form.cleaned_data['date_to'] - \
                                form.cleaned_data['date_from']
                            total_price = number_of_days.days*int(form.cleaned_data['number_of_child'])*room.price_for_child+int(
                                form.cleaned_data['number_of_adult'])*room.price_for_adult
                            c_form.total_price = total_price
                            c_form.save()
                            print(c_form)

                            print(number_of_days)
                            for i in range(number_of_days.days):
                                perday_booking = PerDayBooking.objects.create(
                                    booking=c_form, date=(form.cleaned_data['date_from']+timedelta(i)))
                                perday_booking.save()

                            # sendMail(room, booking)
                            return redirect('/')
                        else:
                            return render(request, 'add-booking.html', {'form': form, 'err': 'booking not addedd maximum child occupancy exceed'})
                    number_of_days = form.cleaned_data['date_to'] - \
                        form.cleaned_data['date_from']
                    c_form.total_price = number_of_days.days*int(
                        form.cleaned_data['number_of_adult'])*room.price_for_adult
                    c_form.save()

                    for i in range(number_of_days.days):
                        perday_booking = PerDayBooking.objects.create(
                            booking=c_form, date=(form.cleaned_data['date_from']+timedelta(i)))
                        perday_booking.save()
                    # sendMail(room, booking)
                else:
                    return render(request, 'add-booking.html', {'form': form, 'err': 'booking not addedd maximum occupancy exceed '})
            else:
                return render(request, 'add-booking.html', {'form': form, 'err': 'booking not addedd choose diffrent date or room '})
    form = BookingForm()
    return render(request, 'add-booking.html', {'form': form})


@login_required
@position_evaluater
def my_booking(request):
    pending_request = Booking.objects.filter(customer=request.user.id).filter(
        status='requested').order_by('date_from')
    accepted_request = Booking.objects.filter(
        customer=request.user.id).filter(status='booked').order_by('date_from')
    history_request = Booking.objects.filter(customer=request.user.id).filter(
        status='completed').order_by('date_from')
    rejected_request = Booking.objects.filter(customer=request.user.id).filter(
        status='rejected').order_by('date_from')

    return render(request, 'my-booking.html', {'request': pending_request, 'accepted': accepted_request, 'rejected': rejected_request, 'history': history_request})


@login_required
@position_evaluater
def edit_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    room = Room.objects.get(pk=booking.room.id)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            date_check1 = PerDayBooking.objects.exclude(booking__customer=request.user).filter(
                date__gte=form.cleaned_data['date_from']).filter(
                date__lte=form.cleaned_data['date_to']).filter(booking__room=room)
            # date_check2 = PerDayBooking.objects.exclude(booking__customer=request.user).filter(
            #     date=form.cleaned_data['date_to']).filter(booking__room=room)

            if not date_check1:

                if int(form.cleaned_data['number_of_adult']) <= int(room.occupancy_for_adult):
                    c_form = form.save(commit=False)
                    if form.cleaned_data['number_of_child']:
                        if int(form.cleaned_data['number_of_child']) <= int(room.occupancy_for_child):
                            PerDayBooking.objects.filter(
                                booking=booking).delete()
                            number_of_days = form.cleaned_data['date_to'] - \
                                form.cleaned_data['date_from']
                            c_form.total_price = number_of_days.days*int(
                                form.cleaned_data['number_of_child'])*room.price_for_child+int(form.cleaned_data['number_of_adult'])*room.price_for_adult

                            c_form.save()

                            for i in range(number_of_days.days):
                                perday_booking = PerDayBooking.objects.create(
                                    booking=c_form, date=(form.cleaned_data['date_from']+timedelta(i)))
                                perday_booking.save()

                            return redirect('/')
                        else:
                            return render(request, 'edit-booking.html', {'form': form, 'err': 'cannot edit , exceed child limit'})
                    PerDayBooking.objects.filter(booking=booking).delete()
                    number_of_days = form.cleaned_data['date_to'] - \
                        form.cleaned_data['date_from']
                    c_form.total_price = number_of_days.days*int(
                        form.cleaned_data['number_of_adult'])*room.price_for_adult

                    c_form.save()
                    for i in range(number_of_days.days):
                        perday_booking = PerDayBooking.objects.create(
                            booking=c_form, date=(form.cleaned_data['date_from']+timedelta(i)))
                        perday_booking.save()

                    return redirect('/')
                else:
                    return render(request, 'edit-booking.html', {'form': form, 'err': 'cannot edit exceed adult number '})
            else:
                return render(request, 'edit-booking.html', {'form': form, 'err': 'this date is already booked '})
    form = BookingForm(instance=booking)
    return render(request, 'edit-booking.html', {'form': form})


@login_required
@position_evaluater
def delete_booking(request, pk):
    booking = Booking.objects.get(pk=pk)
    if booking.status == 'requested':
        booking.delete()
        return redirect('/')
    else:
        print('cant delete booked bookings')


@login_required
@position_evaluater
def search(request):
    active_hotels = Hotel.objects.filter(
        status=True, name__contains=request.GET['key'])
    if active_hotels:
        data = []
        for hotel in active_hotels:
            min_price_ = hotel.room_set.aggregate(Min('price_for_adult'))
            if min_price_['price_for_adult__min']:
                temp_dict = {}
                temp_dict = model_to_dict(
                    hotel, fields=['name', 'hotel_address', 'hotel_phone', 'star', 'owner'])
                temp_dict['min_price'] = min_price_['price_for_adult__min']
                data.append(temp_dict)
        return render(request, 'home.html', {'active_hotels': data,  'user': request.user})
    else:
        return render(request, 'home.html', {'err': 'not found'})


@login_required
@position_evaluater
def sendMail(room, booking):
    subject = ' booking request  '
    message = 'new booking request for the room ' + \
        room.room_name+'\n by the '+booking.customer.username
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [room.hotel.owner.email]
    send_mail(subject, message, email_from, recipient_list)
    return True
