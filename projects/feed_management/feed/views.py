import csv
from io import StringIO
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse
from feed.serializers import FeedSerializer,GetFeedCountSerializer,ReportOnFeedSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from feed.models import Feed ,ReportOnFeed
from feed.permissions import UserPermissionForFeedAPI ,UserPermissionForReportFeedAPI



class FeedViewSet(generics.CreateAPIView):
    """ Create new feed """

    queryset = Feed.objects.filter()
    serializer_class = FeedSerializer
    permission_classes =(IsAuthenticated,)

    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['created_by']=request.user
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FeedsListViewSet(generics.ListAPIView):
    """ Get feeds of requested user """

    queryset = Feed.objects.all()
    serializer_class =GetFeedCountSerializer
    permission_classes =(IsAuthenticated,)

    def get_queryset(self,):

        if self.request.user.is_superuser:
            queryset =Feed.objects.all()
        elif self.request.user and self.request.user.is_authenticated:
            queryset = Feed.objects.filter(
                    created_by__id=self.request.user.id)
        else:
            queryset =  Feed.objects.none()
        return queryset


class FeedActionViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrive feed details of user.
        Update feed details of user.
        Delete feed details of user.
    """

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = (UserPermissionForFeedAPI,)


class DownloadFeedReportCSVViewSet(APIView):
    """
    API to Download report of feed.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        feed_id = request.query_params.get('feed_id')

        if request.user.is_superuser:
            feeds = Feed.objects.filter(id=feed_id).values(
                    'title','content','created_at','created_by__first_name',\
                    'created_by__last_name')
        elif request.user:
            feeds = Feed.objects.filter(
                        id=feed_id,created_by__username=request.user).values(
                        'title','content','created_at','created_by__first_name',
                        'created_by__last_name')
        else:
            feeds = Feed.objects.none()

        if feeds:
            buffer_ = StringIO()
            csv_writer = csv.writer(buffer_)
            csv_writer.writerow(['Title',' Content','Publish Date','Created_by']
            )
            for feed in feeds:
                first_name=feed['created_by__first_name'] \
                                    if feed['created_by__first_name'] else '-'
                last_name=feed['created_by__last_name'] \
                                    if feed['created_by__last_name'] else '-'
                csv_writer.writerow([
                        feed['title'] if feed['title'] else '-',
                        feed['content'] if feed['content'] else '-',
                        feed['created_at'] if feed['created_at'] else '-',
                        first_name +" "+ last_name
                    ])
            buffer_.seek(0)
            response = StreamingHttpResponse(buffer_, content_type='text/csv')
            response['Content-Disposition'] =\
                'attachment; filename=feed_report.csv'
            response.streaming = True
            return response
        else:
            return Response(
                "Feed details not available.",
                status.HTTP_404_NOT_FOUND
            )


class ReportOnFeedViewSet(viewsets.ModelViewSet):
    """ Create report on new feed """

    queryset = ReportOnFeed.objects.filter()
    serializer_class = ReportOnFeedSerializer
    permission_classes =(UserPermissionForReportFeedAPI,)
