from django.urls import path
from .views import TicketListView, TicketDetailView, TicketCreateView, TicketUpdateView, TicketDeleteView, UserTicketListView, TicketReplieView, FilterListView
from . import views

urlpatterns = [
    path('', FilterListView.as_view(), name='ticket-home'),
    path('tickets/<str:status>/', FilterListView.as_view(), name='filtered-tickets'),
    path('user/<str:username>/', UserTicketListView.as_view(), name='user-tickets'),
    path('ticket/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/replie/', TicketReplieView.as_view(), name='add-replie'),
    path('ticket/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]