from django.urls import path
from assistant .views import *

urlpatterns = [
    path('',CHATBOT, name = "chatbot"),
    path('login',LOGIN, name = "login"),
    path('register',REGISTER, name = "register"),
    path('logout',LOGOUT, name = "logout"),
    path('doregister',DOREGISTER, name = "doregister"),
    path('dologin',DOLOGIN, name = "dologin")
]
