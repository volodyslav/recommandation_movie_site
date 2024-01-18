from django.urls import path
from . import views

url_name ="main"

urlpatterns = [
    path("predict", views.PredictAPIView.as_view(), name="predict-api")
]
