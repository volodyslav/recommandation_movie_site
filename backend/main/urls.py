from django.urls import path
from . import views

url_name ="main"

urlpatterns = [
    path("", views.hello, name="hello"),
    path("predict", views.predict, name="predict")
]
