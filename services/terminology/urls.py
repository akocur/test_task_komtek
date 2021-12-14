from rest_framework.urls import path

from services.terminology.views import GuideItemList, GuideList, api_root

urlpatterns = [
    path('', api_root),
    path('guides/data', GuideList.as_view(), name='guide-list'),
    path(
        'guides/<int:pk>/guide-items/data',
        GuideItemList.as_view(),
        name='guide-item-list',
    ),
]
