from rest_framework.urls import path

from services.terminology.views import GuideItemList, GuideList, api_root

urlpatterns = [
    path('', api_root),
    path('guide/', GuideList.as_view(), name='guide-list'),
    path('guide-item/', GuideItemList.as_view(), name='guide-item-list'),
]
