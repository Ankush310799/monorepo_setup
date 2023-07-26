from rest_framework.test import APITestCase
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from users.models import User
from address.models import Address

class AddressAppTestData(APITestCase):

    @classmethod
    def setUpTestData(cls):

        # create superuser -
        cls.superuser = User.objects.create_superuser(
            username ='feed_superuser',
            email ='feed123@gmail.com',
            password = 'feed_super123@',
        )
        # create admin
        cls.admin = User.objects.create(
            username ='feed_admin',
            email ='admin23@gmail.com',
            password = 'feed_admin123@',
        )

        # Address data for superadmin
        cls.superuser_address = Address.objects.create(
            street = "B.R.Ambedkar Road",
            city = "Pune city",
            state = "Maharashtra",
            country = "India",
            user = cls.superuser,
        )

        # Address payload data for superuser
        cls.superuser_address_data={
            "street":'Mumbai-Goa Highway',
            "city":'Ratnagiri',
            "state":'Maharashtra',
            "country":"India",
            "user":cls.superuser.id,
        }

        cls.user = ContentType.objects.get(model='user')
        # Address data for Admin
        cls.admin_user_address = Address.objects.create(
            street = "Savitribai Phule Road",
            city = "Pune",
            state = "Maharashtra",
            country = "India",
            user = cls.admin
        )

        # Address payload data for admin
        cls.admin_user_address_data={
            "street":'Pune-Banglore Highway',
            "city":'Satara',
            "state":'Maharashtra',
            "country":'India',
            "user":cls.admin.id
        }

        # Update address details of admin user.
        cls.update_admin_user_address_data={
            "city":'Mumbai',
        }


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class TestCreateAddressAPI(AddressAppTestData):
    """ Test Address creation for users """

    def test_superuser_can_create_address(self):
        """ superuser create address """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(reverse('add_address'),
                                self.superuser_address_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_address(self):
        """ admin create address """

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('add_address'),
                                self.admin_user_address_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annonymous_user_can_not_create_address(self):
        """ annonymous user can not create address """

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('add_address'),
                                self.admin_user_address_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestReadAddressAPI(AddressAppTestData):
    """ Test Read user Address """

    def test_superuser_can_read_address_of_all_users(self):
        """ superuser can read all users address. """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('address-list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_read_address_in_detail_of_all_users(self):
        """ superuser can read all users addreses in detail """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_read_own_address(self):
        """ admin can read own address """

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('address-list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_read_own_address_in_detail(self):
        """ admin can read own address in detail """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annonymous_user_can_not_read_address(self):
        """ annonymous user can not read user address """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('address-list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteAddressAPI(AddressAppTestData):
    """ Test Delete Address API"""

    def test_superuser_can_delete_all_users_address(self):
        """ Superuser can delete all users address """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_Admin_cannot_delete_own_address(self):
        """ Admin cannot delete own address """

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_delete_user_address(self):
        """ Anonymous user cannot delete user address """

        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateAddressAPI(AddressAppTestData):
    """ Test Update Address API"""

    def test_superuser_can_update_all_users_address(self):
        """ Superuser can update all users address """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                self.update_admin_user_address_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Admin_can_update_own_address(self):
        """ Admin cannot delete own address """

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                self.update_admin_user_address_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_update_user_address(self):
        """ Anonymous user cannot update user address """

        self.client.force_authenticate(user=None)
        response = self.client.patch(reverse('address-details',
                                args=[self.admin_user_address.id]),
                                self.update_admin_user_address_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
