from django.urls import path
from contacts.views import index, add_contacts, delete_contacts

urlpatterns = [
    path('', index, name="index"),
    path('add/', add_contacts, name="add-contacts"),
    path('delete/', delete_contacts, name="delete-contacts"),
]
