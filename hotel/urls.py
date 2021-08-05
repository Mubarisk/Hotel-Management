from django.urls import path
from . import views
urlpatterns=[
    path('',views.dash,name='dash'),
    # path('add_hotel_details/',views.add_hotel_details,name='add-hotel-details'),
    # path('edit_hotel_details/', views.edit_hotel_details, name='edit-hotel-details'),
    path('add_room',views.add_room,name='add-room'),
    path('edit_room/<int:pk>/',views.edit_room,name='edit-room'),
    path('delete_room/<int:pk>/',views.delete_room,name='delete-room'),
    path('view_booking/',views.bookings,name='view-booking'),
    path('accept_request/<int:pk>/',views.accept_request,name='accept_request'),
    path('reject_request/<int:pk>/',views.reject_request,name='reject_request'),
    path('move_to_history/',views.move_to_history,name='move_to_history'),
    

]