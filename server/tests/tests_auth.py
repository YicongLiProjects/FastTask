from django.test import TestCase
from application.models import Profile
import json
from application import views
from django.test import RequestFactory
from django.test import Client
from django.contrib.auth.hashers import make_password, check_password

class SignUpTest(TestCase):
    """
    User signing up with valid username, email and password. User should be created
    """
    def test_signup_1(self):
        rf = RequestFactory()
        data = {
            "display_name": "SweatySWE",
            "email": "michael.smith@gmail.com",
            "password": "password"
        }
        req = rf.post(
            'fasttask/signup',
            data=json.dumps(data),
            content_type='application/json'
        )
        status = views.signup(req).status_code
        created_profile = Profile.objects.get(user__username="michael.smith@gmail.com")
        self.assertEqual(1, Profile.objects.count())
        self.assertEqual("SweatySWE", created_profile.display_name)
        self.assertEqual("michael.smith@gmail.com", created_profile.user.email)
        self.assertEqual("1900-01-01", str(created_profile.dob))
        self.assertEqual(201, status)

    """
    User signing up with display name, email, password, first name, last name
    and date of birth. User should be created
    """
    def test_signup_2(self):
        rf = RequestFactory()
        data = {
            "display_name": "SweatySWE",
            "email": "michael.smith@gmail.com",
            "password": "password",
            "first_name": "Michael",
            "last_name": "Smith",
            "dob": "2000-01-01"
        }
        req = rf.post(
            'fasttask/signup',
            data=json.dumps(data),
            content_type='application/json'
        )
        status = views.signup(req).status_code
        created_profile = Profile.objects.get(user__username="michael.smith@gmail.com")
        self.assertEqual(1, Profile.objects.count())
        self.assertEqual("SweatySWE", created_profile.display_name)
        self.assertEqual("michael.smith@gmail.com", created_profile.user.email)
        self.assertEqual("2000-01-01", str(created_profile.dob))
        self.assertEqual(201, status)

    """
    User signing up with missing display name, email or password. User should not be created and
    a response will be shown on the signup page
    """
    def test_signup_3(self):
        rf = RequestFactory()
        data = {
            "email": "michael.smith@gmail.com",
            "password": "password",
            "first_name": "Michael",
            "last_name": "Smith",
            "dob": "2000-01-01"
        }
        req = rf.post(
            'fasttask/signup',
            data=json.dumps(data),
            content_type='application/json'
        )
        status = views.signup(req).status_code
        self.assertEqual(0, Profile.objects.count())
        self.assertEqual(400, status)

    """
    If the display name is longer than 20 characters, password is not between 8 and 20 characters long
    and email is of invalid format, error should be raised, and user should not be created. 
    This assumes that all 3 required fields (username, email, password) are present.
    """
    def test_signup_4(self):
        rf = RequestFactory()
        data1 = {
            "display_name": "SweatySWE",
            "email": "michael.smith@gmail.com",
            "password": "passwd",
            "first_name": "Michael",
            "last_name": "Smith",
            "dob": "2000-01-01"
        }
        req1 = rf.post(
            'fasttask/signup',
            data=json.dumps(data1),
            content_type='application/json'
        )

        data2 = {
            "display_name": "SweatySWE",
            "email": "michael.smith@gmail.com",
            "password": "password",
            "first_name": "Michael",
            "last_name": "Smith",
            "dob": "2099-01-01"
        }
        req2 = rf.post(
            'fasttask/signup',
            data=json.dumps(data2),
            content_type='application/json'
        )

        status1 = views.signup(req1).status_code
        status2 = views.signup(req2).status_code

        self.assertEqual(0, Profile.objects.count())
        self.assertEqual(400, status1)
        self.assertEqual(400, status2)

    """
    If a user with the same email already exists in the database, don't create the user
    """
    def test_signup_5(self):
        rf = RequestFactory()
        data1 = {
            "display_name": "SweatySWE",
            "email": "michael.smith@gmail.com",
            "password": "password",
            "first_name": "Michael",
            "last_name": "Smith",
            "dob": "2000-01-01"
        }
        req1 = rf.post(
            'fasttask/signup',
            data=json.dumps(data1),
            content_type='application/json'
        )

        data2 = {
            "display_name": "SweatySWE",
            "email": "michael.smith@gmail.com",
            "password": "password",
            "first_name": "Michael",
            "last_name": "Smith",
            "dob": "2000-01-01"
        }
        req2 = rf.post(
            'fasttask/signup',
            data=json.dumps(data2),
            content_type='application/json'
        )
        status1 = views.signup(req1).status_code
        status2 = views.signup(req2).status_code
        self.assertEqual(1, Profile.objects.count())
        self.assertEqual(201, status1)
        self.assertEqual(409, status2)



class LoginTest(TestCase):
    """
    User enters correct email and password. Login successful
    """
    def test_login_1(self):
        c = Client()
        signup_response = c.post(
            '/signup/submit/',
            {
                "display_name": "SweatySWE",
                "email": "michael.smith@gmail.com",
                "password": "password"
            },
            content_type='application/json'
        )
        self.assertEqual(201, signup_response.status_code)
        login_response = c.post(
            '/login/submit/',
            {
                "email": "michael.smith@gmail.com",
                "password": "password"
            },
            content_type='application/json'
        )
        self.assertEqual(200, login_response.status_code)


    """
    User enters wrong password for the input email. Return an error message and display it
    on the screen, do not log the user in. 
    """
    def test_login_2(self):
        c = Client()
        signup_response = c.post(
            '/signup/submit/',
            {
                "display_name": "SweatySWE",
                "email": "michael.smith@gmail.com",
                "password": "passwords"
            },
            content_type='application/json'
        )
        self.assertEqual(201, signup_response.status_code)
        login_response = c.post(
            '/login/submit/',
            {
                "email": "michael.smith@gmail.com",
                "password": "pass1234"
            },
            content_type='application/json'
        )
        self.assertEqual(401, login_response.status_code)

    """
    Email does not exist in the database. Return an error message and display it
    on the screen, instruct the user to create a new account
    """
    def test_login_3(self):
        c = Client()
        login_response = c.post(
            '/login/submit/',
            {
                "email": "alicia.miller@gmail.com",
                "password": "password"
            },
            content_type='application/json'
        )
        self.assertEqual(409, login_response.status_code)


"""
Hash password correctly and add this value to the database when the user is created
"""
class PasswordHashTest(TestCase):
    def hash_test(self):
        password = 'password'
        hashed_password = make_password(password)
        self.assertTrue(check_password(password, hashed_password))