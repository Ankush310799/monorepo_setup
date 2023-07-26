import io
import shutil
import tempfile
from rest_framework.test import APITestCase
from PIL import Image as PilImage
from django.urls import reverse
from rest_framework import status
from users.models import User
from feed.models import Feed
from django.test import override_settings



class FeedAppTestData(APITestCase):

    @classmethod
    def generate_photo_file(cls):
        """ generate photo file funcion for create a tmp image. """
        image_file = io.BytesIO()
        image = PilImage.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(image_file, 'png')
        image_file.name = 'feed_image.png'
        image_file.seek(0)
        return image_file

    @classmethod
    def setUpTestData(cls):

        # fake image generate

        cls.photo_file = cls.generate_photo_file()
        cls.image_data = {
            'image': cls.photo_file,
            'deleted_at': ''
        }

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

        # Feed object for Superuser
        cls.feed_for_superuser = Feed.objects.create(
            title = "The story of superuser!",
            content	="In this article,you will get information about...",
            image = "https://www.shutterstock.com/image-photo/gradient-surface-agate-rock-2274918117",
            created_by = cls.superuser,
        )

        # Feed payload data for superuser
        cls.superuser_feed_data={
            "title":'Indian foods.',
            "content":'Your choice ...',
            "image":cls.photo_file,
            "created_by":cls.superuser.id,
        }

        # Feed object for Admin user
        cls.feed_for_admin = Feed.objects.create(
            title = "The story of admin!",
            content	="In this article,give you knowledge",
            image = "https://www.shutterstock.com/image-photo/gradient-surface-agate-rock-2274918117",
            created_by = cls.admin,
        )

        # Feed payload data for Admin user
        cls.admin_user_feed_data={
            "title":'Indian culture.',
            "content":'Your choice ...',
            "image":cls.photo_file,
            "created_by":cls.admin.id,
        }

        # Update feed details of admin user.
        cls.update_admin_user_feed_data={
            "content":'Hey......',
        }


    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)  # delete tmp dir.
        super().tearDownClass()




MEDIA_ROOT=tempfile.mkdtemp()
@override_settings(MEDIA_ROOT=MEDIA_ROOT)

class TestCreateFeedsAPI(FeedAppTestData):
    """ Test Feed creation of users """

    def test_superuser_can_create_feed(self):
        """ superuser can create feed """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(reverse('add_feed'),
                                self.superuser_feed_data,
                                format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_feed(self):
        """ admin can create feed """

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('add_feed'),
                                self.admin_user_feed_data,
                                format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_annonymous_user_can_not_create_feed(self):
        """ annonymous user can not create feed """

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('add_feed'),
                                self.admin_user_feed_data,
                                format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestReadFeedsAPI(FeedAppTestData):
    """ Test Read user Feeds """

    def test_superuser_can_read_all_feeds_of_users(self):
        """ superuser can read all feeds of users. """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('feeds_list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_superuser_can_read_all_feeds_in_detail_of_all_users(self):
        """ superuser can read all users feeds in detail """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_read_own_feed(self):
        """ admin can read own feed"""

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('feeds_list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_read_own_feed_detail(self):
        """ admin can read own address in detail """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_annonymous_user_can_not_read_feed_details(self):
        """ annonymous user can not read feed details """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('feeds_list'),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDeleteFeedsAPI(FeedAppTestData):
    """ Test Delete Feed API"""

    def test_superuser_can_delete_all_users_feeds(self):
        """ Superuser can delete all user feeds """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_Admin_can_delete_own_feed(self):
        """ Admin can delete own feeds """

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_user_cannot_delete_user_feed(self):
        """ Anonymous user cannot delete user feed """

        self.client.force_authenticate(user=None)
        response = self.client.delete(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUpdateFeedsDtailsAPI(FeedAppTestData):
    """ Test Update Feed API"""

    def test_superuser_can_update_all_Feeds(self):
        """ Superuser can update all user feeds """

        self.client.force_authenticate(user=self.superuser)
        response = self.client.patch(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                self.update_admin_user_feed_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Admin_can_update_own_feed(self):
        """ Admin can update own feed """

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                self.update_admin_user_feed_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_update_user_feed(self):
        """ Anonymous user cannot update user feed """

        self.client.force_authenticate(user=None)
        response = self.client.patch(reverse('feed_detail',
                                args=[self.feed_for_admin.id]),
                                self.update_admin_user_feed_data,
                                format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
