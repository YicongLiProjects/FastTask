from django.test import TestCase
from application.models import Profile
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpRequest
from application import views

class SignUpTest(TestCase):
    def setup_signup_test(self):
        req1 = HttpRequest()
        req1.method = "POST"
        req1.user = User.objects.create_user("SweatySWE",
                                             "michael.smith@gmail.com", "password")
        views.signup(req1)
    """
    User signing up with username, email and password. User should be created
    """
    def test_signup_1(self):
        self.assertEqual(1, Profile.objects.count())
        self.assertEqual("SweatySWE", Profile.objects.get(user__username="SweatySWE").user.username)

    """
    User signing up with username, email and password and first name, last name
    and date of birth. User should be created
    """
    def test_signup_2(self):
        pass

    """
    User signing up with missing username, email or password. User should not be created and
    a response will be shown on the signup page
    """
    def test_signup_3(self):
        pass

    """
    If the username is longer than 20 characters, password is not between 8 and 20 characters long
    and email is of invalid format, error should be raised, and user should not be created. This
    assumes that all 3 required fields (username, email, password) are present.
    """
    def test_signup_4(self):
        pass




class LoginTest(TestCase):
    def create_user(self):
        user = User.objects.create_user("SweatySWE", "fast@task.com", "password")

    """
    User enters correct email and password. Login successful
    """
    def test_login_1(self):
        pass

    """
    User enters wrong password for the input email. Return an error message and display it
    on the screen, do not log the user in. 
    """
    def test_login_2(self):
        pass

    """
    Email does not exist in the database. Return an error message and display it
    on the screen, instruct the user to create a new account
    """
    def test_login_3(self):
        pass


"""
Hash password correctly and add this value to the database when the user is created
"""
class PasswordHashTest(TestCase):
    pass