from django.urls import path
from . import views
urlpatterns=[
    path('',views.admin_panel,name='admin-panel'),
    path('addhotel/',views.add_hotel,name='add-hotel'),
    path('logout/',views.logout_view,name='logout'),
    path('delete_hotel/<int:pk>/',views.delete_hotel,name='delete-hotel'),
    path('view_hotel/<int:pk>/',views.view_hotel,name='view-hotel'),
    # path('edit_owner_details/<int:pk>/',views.edit_owner_details,name='edit-owner'),
    path('edit_hotel/<int:pk>/',views.edit_hotel,name='edit-hotel'),
    path('reset_password/<int:pk>/',views.reset_password,name='reset-password'),
]