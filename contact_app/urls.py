from django.urls import path
from contact_app.views import *


urlpatterns = [
    # path('', login_page, name="login"),
    # path('login/', login_page, name="login"),
    path('contact/', sss, name="index"),
    # path('forgot-password/', forgot_password, name="forgot_password"),
    # path('reset-password/<uuid:token>/', reset_password, name="reset_password"),
    # path('change-password/', change_password, name="change_password"),
    path('delete-contact/<int:id>/', delete_contact, name="delete_contact"),
    path('edit-contact/<int:id>/', edit_contact, name="edit_contact"),
    path("profile/", profile, name="profile"),
    path("about/", about, name="about"),
    path('categories/', category_page, name="categories"),
    path("delete-category/<int:id>/",delete_category,name="delete_category"),
    path('category_contacts/<int:id>/', category_contacts, name="category_contacts")
]
