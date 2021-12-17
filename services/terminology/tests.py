import datetime

from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from services.terminology.models import Guide, GuideItem

DEFAULT_GUIDE_NAME = 'guide1'


class GuideModelTests(TestCase):
    """Test Guide model."""

    def setUp(self):
        """Set up."""
        Guide.objects.create(name=DEFAULT_GUIDE_NAME)
        GuideItem.objects.create(code=1, value='surgeon')
        GuideItem.objects.create(code=2, value='therapist')
        GuideItem.objects.create(code=3, value='otolaryngologist')
        GuideItem.objects.create(code=4, value='dentist')

    def test_current_version(self):
        """Test current version."""
        guide = Guide.objects.get(name=DEFAULT_GUIDE_NAME)
        self.assertEqual(guide.current_version, None)

        last_version = self._create_last_version(guide)
        current_version = self._create_current_version(guide)
        future_version = self._create_future_version(guide)

        self.assertQuerysetEqual(
            guide.versions.order_by('id').all(),
            sorted(
                [last_version, current_version, future_version],
                key=lambda version: version.id,
            ),
        )
        self.assertEqual(guide.current_version, current_version)

    def test_get_guide_items(self):
        """Test get_guide_items."""
        guide = Guide.objects.get(name=DEFAULT_GUIDE_NAME)
        self.assertQuerysetEqual(guide.get_guide_items(), [])
        self.assertQuerysetEqual(guide.get_guide_items('last'), [])

        last_version = self._create_last_version(guide)
        self._create_current_version(guide)

        surgeon = GuideItem.objects.get(value='surgeon')
        therapist = GuideItem.objects.get(value='therapist')

        last_version.guide_items.add(surgeon, therapist)
        self.assertQuerysetEqual(
            guide.get_guide_items(), [],  # current version
        )
        self.assertQuerysetEqual(
            guide.get_guide_items('last').order_by('id'),
            sorted([surgeon, therapist], key=lambda guide_item: guide_item.id),
        )

    def _create_version(self, guide, version, start_date):
        return guide.versions.create(version=version, start_date=start_date)

    def _create_last_version(self, guide):
        now = timezone.now()
        last_date = now - datetime.timedelta(days=30)  # noqa: WPS432
        return self._create_version(guide, 'last', last_date)

    def _create_current_version(self, guide):
        today = timezone.now().date()
        return self._create_version(guide, 'current', today)

    def _create_future_version(self, guide):
        now = timezone.now()
        future_date = now + datetime.timedelta(days=30)  # noqa: WPS432
        return self._create_version(guide, 'future', future_date)


class GuideVersionModelTests(TestCase):
    """Test GuideVersion model."""

    def test_unique_version_for_specific_guide(self):
        """Identical versions cannot be created for a particular guide."""
        guide = Guide.objects.create(name=DEFAULT_GUIDE_NAME)
        guide.versions.create(version='1', start_date='2021-12-01')
        raise_text = 'duplicate key value violates unique constraint'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            guide.versions.create(version='1', start_date='2021-12-02')

    def test_version_cannot_be_empty(self):
        """Version cannot be empty."""
        guide = Guide.objects.create(name=DEFAULT_GUIDE_NAME)
        raise_text = 'constraint "non_empty_version"'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            guide.versions.create(version='', start_date='2021-12-01')


class GuideItemModelTests(TestCase):
    """Test GuideItem model."""

    def test_code_cannot_be_empty(self):
        """Code cannot be empty."""
        raise_text = 'constraint "non_empty_code"'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            GuideItem.objects.create(code='', value='value1')
