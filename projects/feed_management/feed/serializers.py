from rest_framework import serializers
from feed.models import Feed,ReportOnFeed
from users.models import User


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = ('title','content','image','created_by',)


class GetFeedSerializer(serializers.ModelSerializer):

    created_by = serializers.SerializerMethodField("get_user_information")

    def get_user_information(self,obj):
        return User.objects.filter(
                id=obj.created_by_id).values(
                'id', 'first_name', 'last_name','username', 'email','groups')

    class Meta:
        model = Feed
        fields = ('id','title','content','image','created_at',\
                    'updated_at','created_by')


class GetFeedCountSerializer(serializers.ModelSerializer):
    total_feed_count=serializers.SerializerMethodField("get_feed_count")
    get_feed_detail =serializers.SerializerMethodField("get_feed_details")

    def get_feed_count(self,obj):
        request= self.context.get('request', None)
        if request.user.is_superuser:
            count = Feed.objects.all().count()
        else:
            count = Feed.objects.filter(created_by=request.user).count()
        return count

    def get_feed_details(self,queryset):
        return GetFeedSerializer(queryset,read_only=True).data


    class Meta:
        model = Feed
        fields = ('total_feed_count','get_feed_detail',)


class ReportOnFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportOnFeed
        fields = '__all__'
