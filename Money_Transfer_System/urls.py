"""
URL configuration for Money_Transfer_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Money_Transfer_System import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("",views.First_Page),
    path("money-transfer-system/",views.First_Page),
    path("user-login/",views.UserLogin_Page),
    path("user-registration/",views.NewUser_Registration),
    path("user-homepage/<user_id>/<unique_key>/<session_id>",views.User_HomePage),
    path("user-profile/<user_id>/<unique_key>/<session_id>",views.User_Profile),
    path("user-transfer-funds/<user_id>/<unique_key>/<session_id>",views.User_TransferFunds),
    path("user-messages/<user_id>/<unique_key>/<session_id>",views.User_Messages),
    path("user-balance/<user_id>/<unique_key>/<session_id>",views.User_Balance),
    path("user-payment-history/<user_id>/<unique_key>/<session_id>",views.User_PaymentHistory),
    path("user-query/<user_id>/<unique_key>/<session_id>",views.User_Query),
    path("user-logout/<user_id>/<unique_key>/<session_id>",views.User_Logout),
]
