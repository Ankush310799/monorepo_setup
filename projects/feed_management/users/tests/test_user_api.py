from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class UserAppTestData(APITestCase):

    @classmethod
    def setUpTestData(cls):

        # create superuser -
        cls.superuser = User.objects.create_superuser(
            username ='feed_superuser',
            email ='feed123@gmail.com',
            password = 'feed_super123@',
            first_name ="Sam",
            last_name ="Dean",
        )
        # create admin
        cls.admin = User.objects.create(
            username ='feed_admin',
            email ='admin23@gmail.com',
            password = 'feed_admin123@',
            first_name ='Daniel',
            last_name = 'Head',
        )

        # Address payload data for superuser
        cls.superuser_payload_data={
            "username" : 'feed_super_user',
            "email" :'superman23@gmail.com',
            "password" : 'feed_hdsdsf123@',
            "first_name" : 'Daniel',
            "last_name" : 'Brain',
        }

        # user creatation payload data for admin
        cls.admin_user_payload_data={
            "username" : 'feed_admin_user',
            "email" :'admin1223@gmail.com',
            "password" : 'feed_admin1233@',
            "first_name" : 'Daniel',
            "last_name" : 'Head',
        }

        # Anonymous user payload data
        cls.anonymous_user_payload_data={
            "username" : 'anonymous_admin',
            "email" :'anonymous23@gmail.com',
            "password" : 'feed_anonymous123@',
            "first_name" : 'Marshal',
            "last_name" : 'King',
        }

        # Update user details for admin user.
        cls.update_admin_user_payload_data={
            "last_name":'Marsh',
        }


    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class TestCreateUserAPI(UserAppTestData):
    """ Test creation of new user """

    def test_superuser_can_create_address(self):
        """ Superuser can create user account """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(reverse('register'),
                                self.superuser_payload_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_user_account(self):
        """ Admin can create user account  """

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('register'),
                                self.admin_user_payload_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_annonymous_user_can_create_user_account(self):
        """ annonymous user can create user account """

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('register'),
                                self.anonymous_user_payload_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestReadUsersListAPI(UserAppTestData):
    """ Test Read Users Details """

    def test_superuser_can_read_list_of_users(self):
        """ superuser can read list of users """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('user_list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_read_user_details_of_all_users(self):
        """ superuser can read all users addreses in detail """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('useraction',
                                args=[self.admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_read_own_details(self):
        """ admin can read own address """

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user_list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_cannot_read_other_users_detail(self):
        """ admin cannot read other users  details """

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('useraction',
                                args=[self.superuser.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_annonymous_user_can_not_read_address(self):
        """ annonymous user can not read user address """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('user_list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteUsersAPI(UserAppTestData):
    """ Delete User Details Test """

    def test_superuser_can_delete_all_users_detail(self):
        """ superuser can delete all users detail """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(reverse('useraction',
                                args=[self.admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_admin_cannot_delete_own_and_other_users_detail(self):
        """ admin cannot delete own and  other user details """

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse('useraction',
                                args=[self.superuser.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_annonymous_user_can_not_delete_user_details(self):
        """ annonymous user can not delete user details """

        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse('useraction',
                                args=[self.superuser.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateUserDetailsAPI(UserAppTestData):
    """ Update Users Details API"""

    def test_superuser_can_update_all_users_detail(self):
        """ Superuser can update all users details """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(reverse('useraction',
                                args=[self.admin.id]),
                                self.update_admin_user_payload_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_own_user_details(self):
        """ Admin can update own details """

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(reverse('useraction',
                                args=[self.admin.id]),
                                self.update_admin_user_payload_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_update_user_details(self):
        """ Anonymous user cannot update user details """

        self.client.force_authenticate(user=None)
        response = self.client.patch(reverse('useraction',
                                args=[self.admin.id]),
                                self.update_admin_user_payload_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
