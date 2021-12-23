from rest_framework import serializers

from services.terminology.models import GuideItem, GuideVersion


class GuideSerializer(serializers.ModelSerializer):
    """Serializer of Guide."""

    id = serializers.IntegerField(
        read_only=True, label='ID', source='guide.id',
    )
    name = serializers.CharField(
        allow_blank=True, max_length=200, source='guide.name',  # noqa: WPS432
    )
    short_name = serializers.CharField(
        allow_blank=True, max_length=100, source='guide.short_name',
    )
    description = serializers.CharField(
        allow_blank=True, source='guide.description',
    )

    class Meta(object):
        model = GuideVersion
        fields = [
            'id', 'name', 'short_name', 'description', 'version', 'start_date',
        ]


class GuideItemSerializer(serializers.ModelSerializer):
    """Serializer of GuideItem."""

    id = serializers.IntegerField()
    guide_id = serializers.IntegerField()

    class Meta(object):
        model = GuideItem
        fields = [
            'id', 'guide_id', 'code', 'value',
        ]

    def validate_id(self, value):  # noqa: WPS110
        """Raise ValidationError if GuideItem does not exist."""
        try:
            GuideItem.objects.get(pk=value)
        except GuideItem.DoesNotExist:
            raise serializers.ValidationError({value: 'does not exist'})
        return value

    def validate(self, data):  # noqa: WPS110
        """Validate code, value."""
        guide_item = GuideItem.objects.get(pk=data['id'])
        errors = []
        fields = ['code', 'value']
        for field in fields:
            if getattr(guide_item, field) != data[field]:
                errors.append(f'{field} is incorrect')
        if errors:
            raise serializers.ValidationError({data['id']: errors})
        return data
