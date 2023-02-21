from django.urls import path

from .views import AssignmentList, ListingList

urlpatterns = [
    path("", ListingList.as_view()),
    path("assignments", AssignmentList.as_view()),
]
