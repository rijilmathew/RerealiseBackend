

from django.urls import path
from . import views
from .views import Last50MessagesView,ProviderChatRoomsView,UnseenMessagesCountView,MarkMessagesAsSeenView,TotalMessageCountView

urlpatterns = [
    path('rooms/', views.CreateRoomView.as_view(), name='room-list'),
    path('messages/', views.MessageList.as_view(), name='message-list'),
    path('last-50-messages/<str:room_name>/', Last50MessagesView.as_view(), name='last-50-messages'),
    path('provider-chat-rooms/<int:provider_id>/', ProviderChatRoomsView.as_view(), name='provider-chat-rooms'),
    path('unseen-messages-count/<int:room_id>/', UnseenMessagesCountView.as_view(), name='unseen_messages_count'),
    path('mark-messages-as-seen/<int:room_id>/', MarkMessagesAsSeenView.as_view(), name='mark_messages_as_seen'),
    path('total-message-count/<int:provider_id>/', TotalMessageCountView.as_view(), name='total_message_count'),
]
