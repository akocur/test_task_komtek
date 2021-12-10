from rest_framework import generics

from services.terminology.models import Guide
from services.terminology.serializers import GuideSerializer


class GuideList(generics.ListAPIView):
    """List of guide."""

    queryset = Guide.objects.all()
    serializer_class = GuideSerializer
