from rest_framework.urls import path

from services.terminology.views import GuideList

urlpatterns = [
    path('', GuideList.as_view(), name='guide-list'),
]
