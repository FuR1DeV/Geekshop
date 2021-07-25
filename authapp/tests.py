from django.test import TestCase
from django.test.client import Client
from authapp.models import User
from django.core.management import call_command
from geekshop import settings


class TestUserManagement(TestCase):
    status_code_success = 200
    status_code_redirect = 302
    username = 'django'
    email = 'django@gb.local'
    password = 'geekbrains'

    def setUp(self):
        self.superuser = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.user = User.objects.create_user('user2', 'user2@geekshop.local', 'geekbrains')
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'geekshop')
        self.assertNotContains(response, 'fa-user-circle', status_code=self.status_code_success)

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/users/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        response = self.client.get('/')
        self.assertContains(response, 'fa-user-circle', status_code=self.status_code_success)
        self.assertEqual(response.context['user'], self.superuser)

    def test_user_register(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertEqual(response.context['title'], 'GeekShop - Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'user1',
            'first_name': 'V',
            'last_name': 'H',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'user1@geekshop.local'}

        response = self.client.post('/users/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        new_user = User.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{new_user_data['email']}/{new_user.activation_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)

        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/')
        self.assertContains(response, text='fa-user-circle', status_code=self.status_code_success)

    def test_user_logout(self):
        self.client.login(username='user2', password='geekbrains')

        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, self.status_code_redirect)

        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)
