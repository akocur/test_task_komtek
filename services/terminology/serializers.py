from rest_framework.serializers import ModelSerializer

from services.terminology.models import Guide


class GuideSerializer(ModelSerializer):
    """Serializer of Guide."""

    class Meta(object):
        model = Guide
        fields = [
            'id', 'name', 'short_name', 'description', 'version', 'start_date',
        ]
