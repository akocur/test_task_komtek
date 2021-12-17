import datetime

from django.test import TestCase
from django.utils import timezone

from services.terminology.models import Guide


class GuideModelTests(TestCase):
    """Test Guide model."""

    def test_current_version(self):
        """Test current version."""
        guide = Guide.objects.create(name='guide1')
        self.assertEqual(guide.current_version, None)

        last_date = timezone.now() - datetime.timedelta(days=30)
        last_version = guide.versions.create(
            version='last',
            start_date=last_date,
        )

        today = timezone.now().date()
        current_version = guide.versions.create(
            version='current',
            start_date=today,
        )

        future_date = timezone.now() + datetime.timedelta(days=30)
        future_version = guide.versions.create(
            version='future',
            start_date=future_date,
        )

        self.assertQuerysetEqual(
            guide.versions.order_by('id').all(),
            [last_version, current_version, future_version],
        )
        self.assertEqual(guide.current_version, current_version)
