from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from address.serializers import AddressSerializer,GetUserAddressSerializer
from rest_framework import generics
from address.models import Address
from address.permissions import UserPermissionForAddressAPI



class AddressViewSet(generics.CreateAPIView):
    """ Add address to requested user """

    serializer_class = AddressSerializer
    permission_classes =(IsAuthenticated,)

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if Address.objects.filter(user__id=self.request.data['user']).exists():
                return Response({"error": "Address is already exists."})
            else:
                serializer.save(user=request.user)
                return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AddressDetailViewSet(generics.ListAPIView):
    """ Get address of requested user """

    queryset = Address.objects.all()
    serializer_class = GetUserAddressSerializer
    permission_classes =(IsAuthenticated,)

    def get_queryset(self,):

        if self.request.user.is_superuser:
            queryset = Address.objects.all().values()

        elif self.request.user and self.request.user.is_authenticated:
            queryset = Address.objects.filter(user__id=self.request.user.id).values()

        else:
            queryset =  Address.objects.none()
        return queryset


class AddressActionViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
        Retrive address details of user.
        Update address details of user.
        Delete address details of user.
    """

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (UserPermissionForAddressAPI,)
