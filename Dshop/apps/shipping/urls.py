from django.urls import path

from .views import InPostSendingMethodView, InPostPointsView

urlpatterns = [
    path('points/', InPostPointsView.as_view(), name='inpost-points'),
    path('sending-methods/', InPostSendingMethodView.as_view(), name='sending-methods'),
]
