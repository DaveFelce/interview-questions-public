from rest_framework import generics

from .models import Assignment, Listing
from .serializers import AssignmentSerializer, ListingSerializer


class ListingList(generics.ListAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.all().order_by("id")


class AssignmentList(generics.ListCreateAPIView):
    queryset = Assignment.objects.all().order_by("id")
    serializer_class = AssignmentSerializer
