import datetime

from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from services.terminology.models import Guide, GuideItem
from services.terminology.serializers import (
    GuideItemSerializer,
    GuideSerializer,
)


@api_view(['GET'])
def api_root(request, format=None):  # noqa: WPS125
    """Return api root."""
    return Response({
        'guide': reverse('guide-list', request=request, format=format),
        'guide item': reverse(
            'guide-item-list', request=request, format=format,
        ),
    })


class GuideList(generics.ListAPIView):
    """List of guide."""

    serializer_class = GuideSerializer

    def get_queryset(self):  # noqa: WPS615
        """Get queryset.

        If start_date_lte is specified in the get method, only those guides
        whose start_date is less than or equal to start_date_lte will be
        selected.
        """
        queryset = Guide.objects.all()
        start_date_lte = self.request.query_params.get('start_date_lte')
        if start_date_lte:
            try:
                date = datetime.date.fromisoformat(start_date_lte)
            except ValueError:
                raise serializers.ValidationError(
                    {'start_date_lte': 'Please enter a valid start_date_lte'},
                )
            return queryset.filter(start_date__lte=date)
        return queryset


class GuideItemList(generics.ListAPIView):
    """List of guide item."""

    serializer_class = GuideItemSerializer

    def get_queryset(self):  # noqa: WPS615
        """Get queryset.

        If 'version' and 'guide_name' is specified in the get method, then
        queryset is change.
        Version can be either 'current' or specific.
        """
        queryset = GuideItem.objects.all()
        guide_name = self.request.query_params.get('guide_name')
        version = self.request.query_params.get('version')
        if version and guide_name:
            if version == 'current':
                return queryset.filter(
                    guide=Guide.current_version(guide_name),
                )
            return queryset.filter(
                guide__version=version, guide__name=guide_name,
            )
        return queryset
