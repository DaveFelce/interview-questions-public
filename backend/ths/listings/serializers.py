import datetime
from collections import OrderedDict

from django.db.models import Q
from rest_framework import serializers

from .models import Assignment, Listing


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ["start_date", "end_date", "listing"]

    def validate(self, data: OrderedDict) -> OrderedDict:
        if data["start_date"] > data["end_date"]:
            raise serializers.ValidationError("End date must occur after start")

        # validate that the assignment starts tomorrow or later
        if data["start_date"] < (datetime.date.today() + datetime.timedelta(days=1)):
            raise serializers.ValidationError("Start date must be from tomorrow onwards")

        # validate that the assignment does not overlap with any existing assignments for this listing.
        count_overlapping_dates = Assignment.objects.filter(
            Q(listing=data["listing"])
            & (
                Q(start_date__range=(data["start_date"], data["end_date"]))
                | Q(end_date__range=(data["start_date"], data["end_date"]))
            )
        ).count()  # might want to return all records to user in a real app, but count is most efficient check
        if count_overlapping_dates > 0:
            raise serializers.ValidationError("Your chosen dates have overlapped with an existing assignment")

        return data


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["first_name", "last_name", "pets", "assignments"]
