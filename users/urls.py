from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name="land"),

    path('register/',views.register,name="register"),
    # path('register1/',views.login_view,name="login_view"),
    # path('logout/',views.logout_view,name="logout_view"),


]


