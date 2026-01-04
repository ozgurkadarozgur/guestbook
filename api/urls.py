from django.urls import path
from api.views.entry import EntryAPIView
from api.views.user import UserAPIView

urlpatterns = [
    path("users/", UserAPIView.as_view(), name="user"),
    path("entry/", EntryAPIView.as_view(), name="entry"),
]
