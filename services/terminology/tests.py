import datetime

from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from services.terminology.models import Guide, GuideItem


class GuideMixin(object):
    """Provide methods for working with guide."""

    default_guide_name = 'guide1'

    def create_guide(self, name, short_name='', description=''):
        """Create guide."""
        return Guide.objects.create(
            name=name, short_name=short_name, description=description,
        )

    def get_guide(self, **kwargs):
        """Get guide."""
        return Guide.objects.get(**kwargs)


class GuideVersionMixin(object):
    """Provide methods for working with guide version."""

    last_version_name = 'last'
    current_version_name = 'current'
    future_version_name = 'future'

    def create_version(self, guide, version, start_date, guide_items=None):
        """Create guide version."""
        if guide_items is None:
            guide_items = []
        guide_version = guide.versions.create(
            version=version, start_date=start_date,
        )
        if guide_items:
            guide_version.guide_items.add(guide_items)
        return guide_version

    def create_last_version(self, guide):
        """Create last guide version."""
        now = timezone.now()
        last_date = now - datetime.timedelta(days=30)  # noqa: WPS432
        return self.create_version(guide, self.last_version_name, last_date)

    def create_current_version(self, guide):
        """Create last guide version."""
        today = timezone.now().date()
        return self.create_version(guide, self.current_version_name, today)

    def create_future_version(self, guide):
        """Create last guide version."""
        now = timezone.now()
        future_date = now + datetime.timedelta(days=30)  # noqa: WPS432
        return self.create_version(
            guide, self.future_version_name, future_date,
        )


class GuideItemMixin(object):
    """Provide methods for working with guide item."""

    def create_guide_item(self, code, value):  # noqa: WPS110
        """Create guide item."""
        return GuideItem.objects.create(code=code, value=value)


class GuideModelTests(  # noqa: WPS215
    GuideMixin, GuideVersionMixin, GuideItemMixin, TestCase,
):
    """Test Guide model."""

    def setUp(self):
        """Set up."""
        self.create_guide(name=self.default_guide_name)
        self.create_guide_item(code=1, value='surgeon')
        self.create_guide_item(code=2, value='therapist')

    def test_current_version(self):
        """Test current version."""
        guide = self.get_guide(name=self.default_guide_name)
        self.assertEqual(guide.current_version, None)

        last_version = self.create_last_version(guide)
        current_version = self.create_current_version(guide)
        future_version = self.create_future_version(guide)

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
        guide = self.get_guide(name=self.default_guide_name)
        self.assertQuerysetEqual(guide.get_guide_items(), [])
        self.assertQuerysetEqual(
            guide.get_guide_items(self.last_version_name), [],
        )

        last_version = self.create_last_version(guide)
        self.create_current_version(guide)

        surgeon = self.create_guide_item(code='1', value='surgeon')
        therapist = self.create_guide_item(code='2', value='therapist')

        last_version.guide_items.add(surgeon, therapist)
        self.assertQuerysetEqual(
            guide.get_guide_items(), [],  # current version
        )
        self.assertQuerysetEqual(
            guide.get_guide_items(self.last_version_name).order_by('id'),
            sorted([surgeon, therapist], key=lambda guide_item: guide_item.id),
        )


class GuideVersionModelTests(GuideMixin, GuideVersionMixin, TestCase):
    """Test GuideVersion model."""

    def test_unique_version_for_specific_guide(self):
        """Identical versions cannot be created for a particular guide."""
        guide = self.create_guide(name=self.default_guide_name)
        guide.versions.create(version='1', start_date='2021-12-01')
        raise_text = 'duplicate key value violates unique constraint'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            guide.versions.create(version='1', start_date='2021-12-02')

    def test_version_cannot_be_empty(self):
        """Version cannot be empty."""
        guide = self.create_guide(name=self.default_guide_name)
        raise_text = 'constraint "non_empty_version"'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            guide.versions.create(version='', start_date='2021-12-01')


class GuideItemModelTests(GuideItemMixin, TestCase):
    """Test GuideItem model."""

    def test_code_cannot_be_empty(self):
        """Code cannot be empty."""
        raise_text = 'constraint "non_empty_code"'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            self.create_guide_item(code='', value='value1')

    def test_value_cannot_be_empty(self):
        """Value cannot be empty."""
        raise_text = 'constraint "non_empty_value"'
        with self.assertRaisesMessage(IntegrityError, raise_text):
            self.create_guide_item(code='1', value='')
