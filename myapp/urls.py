from django.urls import path
from .views import ItineraryView

urlpatterns = [
    path('generate-itinerary/', ItineraryView.as_view(), name='generate_itinerary'),
]
