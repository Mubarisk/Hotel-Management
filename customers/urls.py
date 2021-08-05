from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home-page'),
    path('detail/<int:pk>/',views.detailed_view,name='detailed'),
    path('add_bookin/<int:pk>/', views.add_booking, name='add-booking'),
    path('my_booking/',views.my_booking,name='booking'),
    path('edit_booking/<int:pk>/',views.edit_booking,name='edit-booking'),
    path('delete_booking/<int:pk>/',views.delete_booking,name='delete-booking'),
    path('search/',views.search,name='search'),
]