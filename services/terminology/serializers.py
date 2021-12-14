from rest_framework import serializers

from services.terminology.models import GuideItem, GuideVersion


class GuideSerializer(serializers.ModelSerializer):
    """Serializer of Guide."""

    id = serializers.IntegerField(
        read_only=True, label='ID', source='guide.id',
    )
    name = serializers.CharField(
        allow_blank=True, max_length=200, source='guide.name',
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

    guide = serializers.IntegerField(
        read_only=True, label='ID',
    )

    class Meta(object):
        model = GuideItem
        fields = [
            'id', 'guide', 'code', 'value',
        ]
