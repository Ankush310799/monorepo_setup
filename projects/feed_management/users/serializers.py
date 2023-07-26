from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import User
from address.models import Address


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password','first_name','last_name','groups',)

        read_only_fields=['groups',]


    def validate_password(self, password: str) -> str:
        """
            Validate password method is used for hashing the raw password
            before saving into the db
        """
        return make_password(password)


class GetUserInformationSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField("get_address_of_user")

    def get_address_of_user(self,obj,*args,**kwargs):

        return Address.objects.filter(
                        user__id=obj['id']).values()

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','groups','address')


class UserActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields ='__all__'
