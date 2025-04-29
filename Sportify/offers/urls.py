from django.urls import path
from . import views

app_name = 'offers'
urlpatterns = [
    path('offer/<int:offer_id>/', views.offer_details, name='offer_details'),
    path('offers/', views.all_offers, name='all_offers'),
    path('add/', views.add_offer, name='add_offer'),
    path('delete/<int:pk>/', views.delete_offer, name='delete_offer'),
    path('edit/<int:pk>/', views.edit_offer, name='edit_offer'),
    path('my_offers/', views.my_offers, name='my_offers'),

]

