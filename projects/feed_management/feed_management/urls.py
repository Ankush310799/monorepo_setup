from django.contrib import admin
from django.urls import path , include
from feed_management.routers import router
from users.views import UserRegistrationView,UserViewSet, UserActionViewSet
from address.views import AddressViewSet,AddressDetailViewSet,AddressActionViewSet
from feed.views import FeedViewSet,FeedsListViewSet,FeedActionViewSet,\
                    DownloadFeedReportCSVViewSet


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # User app
    path('api/register/',UserRegistrationView.as_view(),name='register'),
    path('api/user/',UserViewSet.as_view(),name='user_list'),
    path('api/user/<int:pk>/',UserActionViewSet.as_view(), name='useraction'),

    # Address app
    path('api/address/',AddressViewSet.as_view(),name='add_address'),
    path('api/address_list/',AddressDetailViewSet.as_view(),name='address-list'),
    path('api/address_list/<int:pk>/',AddressActionViewSet.as_view(),
        name='address-details'),

    # Feed app
    path('api/feed/',FeedViewSet.as_view(),name='add_feed'),
    path('api/feed_list/',FeedsListViewSet.as_view(),name='feeds_list'),
    path('api/feed_list/<int:pk>/',FeedActionViewSet.as_view(),name='feed_detail'),
    path('api/download_feed_report/',DownloadFeedReportCSVViewSet.as_view(),\
        name='download_feed_report'),

]
