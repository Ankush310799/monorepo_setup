from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from address.models import Address
from users.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class GetUserAddressSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")

    def get_user(self,obj,*args,**kwargs):
        return User.objects.filter(id=obj['user_id']).values('username')

    class Meta:
        model = Address
        fields = ('id','street','city','state','country','user',)
