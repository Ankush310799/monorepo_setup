from rest_framework import routers
from feed.views import ReportOnFeedViewSet

router = routers.DefaultRouter()

router.register(r'report_feed',ReportOnFeedViewSet,basename='report_on_post')
