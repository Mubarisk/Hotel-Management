import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from customers.models import Hotel, PerDayBooking, Room, Booking
from django.core.mail import send_mail
from django.conf import settings
from customers.forms import RoomForm




def position_evaluater(function):
    def wraper(request, *args, **kwargs):
        if request.user.position == 'admin':
            return redirect('/admin/')
        elif request.user.position == 'customer':
            return redirect('/')
        elif request.user.position == 'owner':
            return function(request, *args, **kwargs)

    return wraper


@login_required
@position_evaluater
def dash(request):
    try:
        hotel = Hotel.objects.get(owner=request.user)
        try:
            rooms = Room.objects.filter(hotel=hotel)
            return render(request, 'dash.html', {'details': hotel, 'rooms': rooms})
        except:
            return render(request, 'dash.html', {'details': hotel})
    except:
        return render(request, 'dash.html')


@login_required
@position_evaluater
def add_room(request):
    hotel = Hotel.objects.get(pk=request.user)
    print(hotel)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            p=form.save(commit=False)
            p.hotel=hotel
            p.save()
            hotel.status = True
            hotel.save()

            return redirect('/hotel/')

    form = RoomForm()
    return render(request, 'add-room.html', {'form': form})


@login_required
@position_evaluater
def edit_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            
        return redirect('/hotel/')
       
    form=RoomForm(instance=room)

    return render(request, 'edit-room.html', {'form': form})


@login_required
@position_evaluater
def delete_room(request, pk):
    room = Room.objects.get(pk=pk)
    room.delete()
    return redirect('/hotel/')


@login_required
@position_evaluater
def bookings(request):
    pending_request = Booking.objects.filter(room__hotel__pk=request.user.id).filter(
        status='requested').order_by('date_from')
    accepted_request = Booking.objects.filter(
        room__hotel__pk=request.user.id).filter(status='booked').order_by('date_from')

    history_request = Booking.objects.filter(room__hotel__pk=request.user.id).filter(
        status='completed').order_by('date_from')
    rejected_request = Booking.objects.filter(
        room__hotel__pk=request.user.id).filter(status='rejected').order_by('date_from')
    return render(request, 'bookings.html', {'pending_request': pending_request, 'accepted': accepted_request, 'rejected': rejected_request, 'history': history_request})


@login_required
@position_evaluater
def accept_request(request, pk):
    booking = Booking.objects.get(pk=pk)
    booking.status = 'booked'
    booking.save()
    subject = ' booking accepted  '
    message = 'your booking accepted   \n your room is ' + \
        booking.room.room_name+' at '+booking.room.hotel.name + 'hotel'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [booking.customer.email]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('/hotel/view_booking/')


@login_required
@position_evaluater
def reject_request(request, pk):
    booking = Booking.objects.get(pk=pk)
    booking.status = 'rejected'
    booking.save()
    PerDayBooking.objects.filter(booking=booking).delete()
    subject = ' booking rejected  '
    message = 'your booking rejected'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [booking.customer.email]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('/hotel/view_booking/')


@login_required
@position_evaluater
def move_to_history(request):
    completed = Booking.objects.filter(room__hotel__pk=request.user.id).filter(
        date_to__lt=datetime.date.today()).filter(status='booked')
    for booking in completed:
        booking.status = 'completed'
        booking.save()
        PerDayBooking.objects.filter(booking=booking).delete()
    return redirect('/hotel/')
