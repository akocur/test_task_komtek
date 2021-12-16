import datetime

from django.db import models
from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from services.terminology.models import Guide, GuideItem, GuideVersion
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
        queryset = GuideVersion.objects.all()
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
        """Get queryset."""
        pk = self.kwargs.get('pk')
        guide = Guide.objects.get(id=pk)
        version = self.request.query_params.get('version')
        guide_id_field = models.Value(
            pk, output_field=models.IntegerField(),
        )
        try:
            guide_items = guide.get_guide_items(version).annotate(
                guide_id=guide_id_field,
            )
        except GuideVersion.DoesNotExist:
            raise serializers.ValidationError(
                {'version': f'No data for the {version} version'},
            )

        return guide_items


class GuideItemValidate(APIView):
    """Validate guide item."""

    def post(self, request, pk, format=None):  # noqa: WPS125
        """Validate data."""
        try:
            guide = Guide.objects.get(pk=pk)
        except GuideVersion.DoesNotExist:
            raise serializers.ValidationError({'guide_id': 'does not exist.'})

        serializer = GuideItemSerializer(many=True, data=request.data)
        serializer.is_valid(raise_exception=True)

        version = self.request.query_params.get('version')
        guide_items_of_version = guide.get_guide_items(version)

        guide_item_ids = [
            guide_item['id'] for guide_item in serializer.validated_data
        ]
        expected_guide_items = GuideItem.objects.filter(id__in=guide_item_ids)
        invalid_guide_items = expected_guide_items.difference(
            guide_items_of_version,
        ).order_by('id')

        errors = list(map(
            lambda invalid_guide_item: {invalid_guide_item.id: False},
            invalid_guide_items,
        ))

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'all': True})
