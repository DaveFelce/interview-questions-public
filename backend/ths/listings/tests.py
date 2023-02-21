from datetime import date

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from .models import Assignment, Listing


class ListingList(APITransactionTestCase):
    def setUp(self) -> None:
        self.listing_1 = Listing.objects.create(first_name="Ross", last_name="Geller")
        self.listing_2 = Listing.objects.create(first_name="Phoebe", last_name="Buffay")
        self.assignment_1 = Assignment.objects.create(
            start_date=date(2023, 2, 7),
            end_date=date(2023, 2, 15),
            listing=self.listing_1,
        )
        self.assignment_2 = Assignment.objects.create(
            start_date=date(2023, 4, 1),
            end_date=date(2023, 4, 4),
            listing=self.listing_2,
        )

    def test_get_200(self) -> None:
        response = self.client.get("/listings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_data(self) -> None:
        response = self.client.get("/listings/", {"page": 1})
        self.assertEqual(
            response.data["results"],  # listings are now paginated
            [
                {
                    "first_name": self.listing_1.first_name,
                    "last_name": self.listing_1.last_name,
                    "pets": [],
                    "assignments": [self.assignment_1.pk],
                },
                {
                    "first_name": self.listing_2.first_name,
                    "last_name": self.listing_2.last_name,
                    "pets": [],
                    "assignments": [self.assignment_2.pk],
                },
            ],
        )


class AssignmentList(APITransactionTestCase):
    def setUp(self) -> None:
        self.listing_1 = Listing.objects.create(first_name="Ross", last_name="Geller")

    def test_get_200(self) -> None:
        response = self.client.get("/listings/assignments")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_assignment_starts_tomorrow_or_later(self) -> None:
        test_assignment = {
            "start_date": date(2025, 2, 7),
            "end_date": date(2025, 2, 15),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_201_CREATED

    def test_assignment_start_date_is_in_past(self) -> None:
        test_assignment = {
            "start_date": date(2020, 2, 7),
            "end_date": date(2020, 2, 15),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["non_field_errors"][0]) == "Start date must be from tomorrow onwards"

    def test_assignment_end_date_is_after_start_date(self) -> None:
        test_assignment = {
            "start_date": date(2025, 2, 7),
            "end_date": date(2020, 2, 15),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert str(response.data["non_field_errors"][0]) == "End date must occur after start"

    def test_assignment_dates_do_not_overlap_existing(self) -> None:
        Assignment.objects.create(
            start_date=date(2025, 2, 7),
            end_date=date(2025, 2, 15),
            listing=self.listing_1,
        )
        test_assignment = {
            "start_date": date(2024, 2, 8),
            "end_date": date(2024, 2, 16),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_201_CREATED

    def test_assignment_dates_overlap_existing_end_date(self) -> None:
        Assignment.objects.create(
            start_date=date(2025, 2, 7),
            end_date=date(2025, 2, 15),
            listing=self.listing_1,
        )
        test_assignment = {
            "start_date": date(2025, 2, 8),
            "end_date": date(2025, 2, 16),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["non_field_errors"][0]) == "Your chosen dates have overlapped with an existing assignment"
        )

    def test_assignment_dates_overlap_existing_start_date(self) -> None:
        Assignment.objects.create(
            start_date=date(2025, 2, 7),
            end_date=date(2025, 2, 15),
            listing=self.listing_1,
        )
        test_assignment = {
            "start_date": date(2025, 2, 1),
            "end_date": date(2025, 2, 8),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["non_field_errors"][0]) == "Your chosen dates have overlapped with an existing assignment"
        )

    def test_assignment_dates_overlap_existing_dates_exactly(self) -> None:
        Assignment.objects.create(
            start_date=date(2025, 2, 7),
            end_date=date(2025, 2, 15),
            listing=self.listing_1,
        )
        test_assignment = {
            "start_date": date(2025, 2, 7),
            "end_date": date(2025, 2, 15),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["non_field_errors"][0]) == "Your chosen dates have overlapped with an existing assignment"
        )

    def test_assignment_starts_on_existing_end_date(self) -> None:
        Assignment.objects.create(
            start_date=date(2024, 2, 7),
            end_date=date(2024, 2, 15),
            listing=self.listing_1,
        )
        test_assignment = {
            "start_date": date(2024, 2, 15),
            "end_date": date(2024, 2, 28),
            "listing": self.listing_1.pk,
        }
        response = self.client.post("/listings/assignments", data=test_assignment)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(response.data["non_field_errors"][0]) == "Your chosen dates have overlapped with an existing assignment"
        )
