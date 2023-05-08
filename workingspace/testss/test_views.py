from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
from django.core import mail
from ..forms import RegisterForm
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.paginator import Page
from ..models import URequest
from ..forms import ProjectForm


class test_HomeViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.url = reverse('home')

    def test_home_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()


class test_AboutViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.url = reverse('about')

    def test_about_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'about.html')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()


class ProjectViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('project')

    def test_project_view_with_valid_post_data(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        # Login the user
        self.client.force_login(user)
        data = {
            'request_text': 'test request text'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertEqual(response.context['response'], 'here we can do somethinghere we can do somethinghere ')
        self.assertEqual(URequest.objects.count(), 1)
        self.assertEqual(URequest.objects.first().request_text, data['request_text'])
        self.assertEqual(URequest.objects.first().response_text, response.context['response'])

    def test_project_view_with_invalid_post_data(self):
        data = {}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertNotIn('response', response.context)
        self.assertEqual(URequest.objects.count(), 0)

    def test_project_view_with_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertNotIn('response', response.context)
        self.assertEqual(URequest.objects.count(), 0)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()


class RegisterSIViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register\sign-up')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'check': True
        }
        self.invalid_data = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        }

    def test_get_register_s_i_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_s_i.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_post_valid_register_s_i_view(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Добро пожаловать на наш сайт!')
        self.assertEqual(mail.outbox[0].to, [self.valid_data['email']])

    def test_post_invalid_register_s_i_view(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_s_i.html')
        self.assertIsInstance(response.context['form'], RegisterForm)
        self.assertIn('This field is required.', str(response.content))
        self.assertNotEqual(len(mail.outbox), 1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()


class MyLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register\login')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='test1p2124as41s32421word'
        )

    def test_get_login_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_l_i.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_post_valid_login_view(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'test1p2124as41s32421word'
        })
        self.assertRedirects(response, reverse('home'))

    def test_post_invalid_login_view(self):
        response = self.client.post(self.url, {
            'username': 'wrongusername',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_l_i.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='test1p2124as41s32421word'
        )

    def test_get_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('register\login'))

    def test_logout(self):
        self.client.login(username='testuser', password='test1p2124as41s32421word')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()


class ProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.request = URequest.objects.create(user=self.user, request_text='Test request')

    def test_profile_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_requests_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('profile-req'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_requests.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertIsInstance(response.context['form'], ProjectForm)
        self.assertIsInstance(response.context['page_obj'], Page)

    def test_profile_requests_view_pagination(self):
        self.client.force_login(self.user)
        for i in range(6):
            URequest.objects.create(user=self.user, request_text=f'Test request {i}')
        response = self.client.get(reverse('profile-req') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(response.context['page_obj'].number, 2)
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)

    def test_create_request_view(self):
        self.client.force_login(self.user)
        data = {'request_text': 'New test request'}
        response = self.client.post(reverse('project'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(URequest.objects.count(), 2)
        request = URequest.objects.last()
        self.assertEqual(request.request_text, 'New test request')
        self.assertEqual(request.user, self.user)
        self.assertIsNotNone(request.response_text)
        self.assertIsInstance(request.request_date, datetime)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        connection.close()
