from django.contrib.auth import get_user_model
from django.test import TestCase


class DetailLoginTest(TestCase):
    def setUp(self):
        self.super_user_data = {
            'username': 'TestUser',
            'email': 'admin@blog.ru',
            'password': 'TestUser',
        }
        self.super_user = get_user_model().objects.create_superuser(
            **self.super_user_data
        )

    def test_not_logged(self):
        response = self.client.get('/')
        print(response.status_code)
        print(response.content.decode())
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertContains(response, 'Login')

    def test_force_login(self):
        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.super_user_data['username'],
                          password=self.super_user_data['password'])

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        print('ok')
