from services.terminology.models import Guide, GuideItem


def populate_db():
    """Populate db with test data."""
    specialties = Guide.objects.create(name='specialties')
    facilities = Guide.objects.create(name='facilities')

    specialties.versions.create(version=1, start_date='2021-01-01')
    specialties.versions.create(version=2, start_date='2021-06-01')
    specialties.versions.create(version=3, start_date='2052-06-01')

    facilities.versions.create(version=1, start_date='2021-03-01')
    facilities.versions.create(version=2, start_date='2021-07-01')

    surgeon = GuideItem.objects.create(code=1, value='surgeon')
    therapist = GuideItem.objects.create(code=2, value='therapist')
    otolaryngologist = GuideItem.objects.create(
        code=3, value='otolaryngologist',
    )
    dentist = GuideItem.objects.create(code=4, value='dentist')

    specialties_v1 = specialties.versions.get(version=1)
    specialties_v2 = specialties.versions.get(version=2)
    specialties_v1.guide_item.add(surgeon, therapist, otolaryngologist)
    specialties_v2.guide_item.add(
        surgeon, therapist, dentist, otolaryngologist,
    )
