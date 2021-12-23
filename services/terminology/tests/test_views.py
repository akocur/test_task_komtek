from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .mixins import (  # noqa: WPS300
    GuideItemMixin,
    GuideMixin,
    GuideVersionMixin,
)


class GuideListApiViewTests(GuideMixin, GuideVersionMixin, APITestCase):
    """Test GuideList view."""

    def test_get_empty_guide_list(self):
        """Test getting empty guide list."""
        url = reverse('guide-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_get_guide_list(self):
        """Test getting guide list."""
        guide1 = self.create_guide(
            self.default_guide_name,
            self.default_guide_short_name,
            self.default_guide_description,
        )
        last_version_g1 = self.create_last_version(guide1)
        current_version_g1 = self.create_current_version(guide1)
        future_version_g1 = self.create_future_version(guide1)
        guide2 = self.create_guide('guide2')
        current_version_g2 = self.create_current_version(guide2)
        url = reverse('guide-list')
        response = self.client.get(url, format='json')
        expected_data = [
            {
                'id': guide1.id,
                'name': self.default_guide_name,
                'short_name': self.default_guide_short_name,
                'description': self.default_guide_description,
                'version': self.last_version_name,
                'start_date': last_version_g1.start_date.isoformat(),
            },
            {
                'id': guide1.id,
                'name': self.default_guide_name,
                'short_name': self.default_guide_short_name,
                'description': self.default_guide_description,
                'version': self.current_version_name,
                'start_date': current_version_g1.start_date.isoformat(),
            },
            {
                'id': guide1.id,
                'name': self.default_guide_name,
                'short_name': self.default_guide_short_name,
                'description': self.default_guide_description,
                'version': self.future_version_name,
                'start_date': future_version_g1.start_date.isoformat(),
            },
            {
                'id': guide2.id,
                'name': 'guide2',
                'short_name': '',
                'description': '',
                'version': self.current_version_name,
                'start_date': current_version_g2.start_date.isoformat(),
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], expected_data)

    def test_get_guide_list_on_actual_date(self):
        """Test getting guide list on the actual date."""
        guide1 = self.create_guide(
            self.default_guide_name,
            self.default_guide_short_name,
            self.default_guide_description,
        )
        self.create_last_version(guide1)
        current_version_g1 = self.create_current_version(guide1)
        self.create_future_version(guide1)
        guide2 = self.create_guide('guide2')
        current_version_g2 = self.create_current_version(guide2)
        url = reverse('guide-list')
        today = timezone.now().date()
        query_string = {'start_date_lte': today.isoformat()}
        response = self.client.get(url, query_string, format='json')
        expected_data = [
            {
                'id': guide1.id,
                'name': self.default_guide_name,
                'short_name': self.default_guide_short_name,
                'description': self.default_guide_description,
                'version': self.current_version_name,
                'start_date': current_version_g1.start_date.isoformat(),
            },
            {
                'id': guide2.id,
                'name': 'guide2',
                'short_name': '',
                'description': '',
                'version': self.current_version_name,
                'start_date': current_version_g2.start_date.isoformat(),
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], expected_data)

    def test_start_date_lte_is_valid(self):
        """Test that start_date_lte is valid."""
        url = reverse('guide-list')
        query_string = {'start_date_lte': 'invalid'}
        response = self.client.get(url, query_string, format='json')
        expected_data = {
            'start_date_lte': 'Please enter a valid start_date_lte',
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_data)


class GuideItemListApiViewTests(  # noqa: WPS215
    GuideMixin, GuideVersionMixin, GuideItemMixin, APITestCase,
):
    """Test GuideItemList api."""

    def setUp(self):
        """Set up."""
        self.guide1 = self.create_guide(self.default_guide_name)
        self.pk = self.guide1.id
        self.last_version_g1 = self.create_last_version(self.guide1)
        self.current_version_g1 = self.create_current_version(self.guide1)
        self.future_version_g1 = self.create_future_version(self.guide1)
        guide2 = self.create_guide('guide2')
        self.create_current_version(guide2)
        self.surgeon = self.create_guide_item(code='1', value='surgeon')
        self.therapist = self.create_guide_item(code='2', value='therapist')
        self.dentist = self.create_guide_item(code='3', value='dentist')

    @property
    def url(self):
        """Return url."""
        return reverse('guide-item-list', kwargs={"pk": self.pk})

    def test_guide_id_dont_exist(self):
        """Test case guide_id don't exist."""
        self.pk = 1000000
        response = self.client.get(self.url, pk=self.pk, format='json')
        expected_data = {f'{self.pk}': 'guide_id does not exist'}
        self.assertEqual(response.json(), expected_data)

    def test_get_empty_list_of_guide_items_of_current_guide_version(self):
        """Test case when current guide version don't any guide items."""
        response = self.client.get(self.url, pk=self.pk, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_get_guide_items_of_current_guide_version(self):
        """Test getting guide items of current guide version."""
        self.last_version_g1.guide_items.add(self.surgeon)
        self.current_version_g1.guide_items.add(self.surgeon, self.therapist)
        self.future_version_g1.guide_items.add(self.surgeon, self.dentist)
        response = self.client.get(self.url, pk=self.pk, format='json')
        expected_data = [
            {
                'id': self.surgeon.id,
                'guide_id': self.guide1.id,
                'code': self.surgeon.code,
                'value': self.surgeon.value,
            },
            {
                'id': self.therapist.id,
                'guide_id': self.guide1.id,
                'code': self.therapist.code,
                'value': self.therapist.value,
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], expected_data)

    def test_get_guide_items_of_specific_guide_version(self):
        """Test getting guide items of specific guide version."""
        self.last_version_g1.guide_items.add(self.surgeon)
        self.current_version_g1.guide_items.add(self.surgeon, self.therapist)
        self.future_version_g1.guide_items.add(self.surgeon, self.dentist)
        query_string = {'version': self.future_version_name}
        response = self.client.get(
            self.url, query_string, pk=self.pk, format='json',
        )
        expected_data = [
            {
                'id': self.surgeon.id,
                'guide_id': self.guide1.id,
                'code': self.surgeon.code,
                'value': self.surgeon.value,
            },
            {
                'id': self.dentist.id,
                'guide_id': self.guide1.id,
                'code': self.dentist.code,
                'value': self.dentist.value,
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], expected_data)
