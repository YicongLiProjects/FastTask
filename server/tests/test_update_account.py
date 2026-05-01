from django.test import TestCase
from application.models import Profile
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
import io

class UpdateFieldsTest(TestCase):
    def test_update_fn_and_ln(self):
        # Create user
        # With RequestFactory, you have to call the function manually (e.g. signup)
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1985-02-05",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )

        # Update first and last name
        # With Client, the function (e.g. update profile here) is automatically called
        login_response = c.post(
        '/login/submit/',
        {
                "email": "christianoronaldo@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1985-02-05",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            }
        )
        status = update_response.status_code
        self.assertEqual(200, status)

        profile = Profile.objects.get(user__username="christianoronaldo@yahoo.com")
        self.assertEqual(profile.user.first_name, "Lionel")
        self.assertEqual(profile.user.last_name, "Messi")


    def test_update_email_and_password(self):
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1985-02-05",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )

        login_response = c.post(
            '/login/submit/',
            {
                "email": "christianoronaldo@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        profile = Profile.objects.get(user__username="christianoronaldo@yahoo.com")

        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1985-02-05",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_Euros_2016"
            }
        )
        status = update_response.status_code
        self.assertEqual(200, status)

        profile_updated = Profile.objects.get(user_id=profile.user_id_primary)

        self.assertIsNotNone(profile_updated)

        self.assertEqual(profile_updated.user.email, "lionelmessi@yahoo.com")
        self.assertTrue(profile_updated.user.check_password("i_won_Euros_2016"))


    def test_update_display_name(self):
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1985-02-05",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )

        login_response = c.post(
            '/login/submit/',
            {
                "email": "christianoronaldo@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1985-02-05",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "IAmCR7TheGoat",
                "password": "i_won_WC_2022"
            }
        )
        status = update_response.status_code
        self.assertEqual(200, status)
        profile = Profile.objects.get(user__username="christianoronaldo@yahoo.com")
        self.assertEqual(profile.display_name, "IAmCR7TheGoat")


    def test_update_date_of_birth(self):
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1985-02-05",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )

        login_response = c.post(
            '/login/submit/',
            {
                "email": "christianoronaldo@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)
        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Christiano",
                "last_name": "Ronaldo",
                "dob": "1987-06-24",
                "email": "christianoronaldo@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            }
        )
        status = update_response.status_code
        self.assertEqual(200, status)
        profile = Profile.objects.get(user__username="christianoronaldo@yahoo.com")
        self.assertEqual(str(profile.dob), "1987-06-24")


class UploadProfilePictureTest(TestCase):
    # Upload JPEG (success)
    @override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
    def test_upload_picture_file1(self):
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1987-06-24",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        login_response = c.post(
            '/login/submit/',
            {
                "email": "lionelmessi@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(200, login_response.status_code)

        # Use PIL and io module to create images for testing
        f = io.BytesIO()
        img = Image.new("RGB", (8, 8))
        img.save(f, "JPEG")
        # Use this module to simulate uploading files to a server
        test_file = SimpleUploadedFile(
            'test.jpg',
            f.read(),
            content_type='image/jpeg'
        )
        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1987-06-24",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022",
                "pfp": test_file
            }
        )
        self.assertEqual(200, update_response.status_code)
        self.assertIn("test", Profile.objects.get(user__username="lionelmessi@yahoo.com").pfp.name)


    # Upload PNG (success)
    @override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
    def test_upload_picture_file2(self):
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1987-06-24",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        login_response = c.post(
            '/login/submit/',
            {
                "email": "lionelmessi@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(login_response.status_code, 200)

        # Use PIL and io module to create images for testing
        f = io.BytesIO()
        img = Image.new("RGB", (8, 8))
        img.save(f, "PNG")
        # Use this module to simulate uploading files to a server
        test_file = SimpleUploadedFile(
            'test.png',
            f.read(),
            content_type='image/png'
        )
        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1987-06-24",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022",
                "pfp": test_file
            }
        )
        self.assertEqual(200, update_response.status_code)
        self.assertIn("test", Profile.objects.get(user__username="lionelmessi@yahoo.com").pfp.name)


    # Upload any other file format than JPG, JPEG or PNG (fail)
    @override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
    def test_upload_non_picture_file(self):
        c = Client()
        c.post(
        '/signup/submit/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1987-06-24",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        c = Client()
        login_response = c.post(
            '/login/submit/',
            {
                "email": "lionelmessi@yahoo.com",
                "password": "i_won_WC_2022"
            },
            content_type='application/json'
        )
        self.assertEqual(200, login_response.status_code)

        # Use this module to simulate uploading files to a server
        test_file = SimpleUploadedFile(
            'test.pdf',
            b'My best selfie ever!',
            content_type='image/pdf'
        )
        update_response = c.post(
            '/update_profile/',
            {
                "first_name": "Lionel",
                "last_name": "Messi",
                "dob": "1987-06-24",
                "email": "lionelmessi@yahoo.com",
                "display_name": "TheGoat123",
                "password": "i_won_WC_2022",
                "pfp": test_file
            }
        )
        self.assertEqual(400, update_response.status_code)
