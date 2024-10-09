from django.urls import path
from .views import *

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path('calculator/', calculator, name='calculator'),
    path('guess/', guess_the_number, name='guess'),
    path('hello/', hello, name='hello'),
]
