from rest_framework.permissions import AllowAny,IsAuthenticated
from users.serializers import UserRegistrationSerializer,GetUserInformationSerializer,\
                            UserActionSerializer
from rest_framework import generics
from users.models import User,Group
from users.permissions import UserPermission



class UserRegistrationView(generics.CreateAPIView):
    """ Register new user """

    queryset = User.objects.filter()
    serializer_class = UserRegistrationSerializer
    permission_classes =(AllowAny,)


class UserViewSet(generics.ListAPIView):
    """ List of register users """

    queryset = User.objects.all()
    serializer_class = GetUserInformationSerializer
    permission_classes = (IsAuthenticated,)


    def get_queryset(self,):
        user_groups = Group.objects.filter(
            name="Admin"
        ).values_list('name', flat=True)

        if self.request.user.is_superuser:
            queryset = User.objects.all().values()
        elif self.request.user.is_authenticated and 'Admin'in user_groups :
            queryset = User.objects.filter(id=self.request.user.id).values()
        else:
            queryset = User.objects.none()
        return queryset


class UserActionViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrive user details.
        Update user details.
        Delete user from users list.
    """

    queryset = User.objects.all()
    serializer_class = UserActionSerializer
    permission_classes = (IsAuthenticated,UserPermission,)
