"""
URL configuration for DSD400Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',views.homePage,name='homePage'),
    path('logout/',views.logoutUser,name='logoutUser'),
    path('about/',views.aboutPage,name='aboutPage'),
    path('register/',views.registerPage,name='registerPage'),
    path('reservation/',views.reservePage,name='reservePage'),
    path('delete/<int:pk>',views.deleteReservation,name='deleteReservation'),
    path('book/',views.bookPage,name='bookPage'),
    path('bookCar/<int:pk>',views.bookCar,name='bookCar'),
    path('select-dates/', views.selectDatesPage, name='selectDatesPage'),
    path('set-booking-dates/', views.setBookingDates, name='setBookingDates'),

]
