from django.urls import path

from frontend.views import HomeView, ChainActionView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chain-action/', ChainActionView.as_view(), name='chain_action')
]
