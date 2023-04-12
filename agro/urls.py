from django.urls import path,include
from . import views
urlpatterns = [
    path('options/', views.options, name="options"),
    path('agrosection/', views.agrosection, name="agrosection"),
    path('cropresult/', views.cropresult, name="cropresult"),


]