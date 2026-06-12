from django.urls import path
from user_auth.views import *
urlpatterns = [
     path('', createuser, name="createuser"),
     path('login/', login_page, name="login"),
    # path('contact/', sss, name="index"),
     path('forgot-password/', forgot_password, name="forgot_password"),
     path('reset-password/<uuid:token>/', reset_password, name="reset_password"),
     path('change-password/', change_password, name="change_password"),
    #  path('delete-contact/<int:id>/', delete_contact, name="delete_contact"),
    # path('edit-contact/<int:id>/', edit_contact, name="edit_contact"),
     path('logout/', logout_page, name="logout"),
]