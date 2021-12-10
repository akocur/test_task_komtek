import datetime

from rest_framework import generics, serializers

from services.terminology.models import Guide
from services.terminology.serializers import GuideSerializer


class GuideList(generics.ListAPIView):
    """List of guide."""

    serializer_class = GuideSerializer

    def get_queryset(self):  # noqa: WPS615
        """Get queryset."""
        queryset = Guide.objects.all()
        start_date_lte = self.request.query_params.get('start_date_lte')
        if start_date_lte:
            try:
                date = datetime.date.fromisoformat(start_date_lte)
            except ValueError:
                raise serializers.ValidationError(
                    {'start_date_lte': 'Please enter a valid start_date_lte'},
                )
            queryset = Guide.objects.filter(start_date__lte=date)
        return queryset
