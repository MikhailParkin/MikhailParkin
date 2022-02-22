from django.urls import reverse

from authors.models import Post, MyUser
from django.test import TestCase


class PostTest(TestCase):
    def setUp(self):
        self.author = MyUser.objects.create_user(username='TestUser',
                                                 email='author@blog.ru',
                                                 password='author@blog.ru')

        number_post = 25
        for post_num in range(number_post):
            Post.objects.create(name=MyUser.objects.get(username='TestUser'),
                                title=f'Test title {post_num}',
                                body=f'Test body {post_num}')

    def test_view_url(self):
        resp = self.client.get(reverse('authors:posts_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['post_list']) == 10)
        print(resp.context['is_paginated'])

    def test_view_posts_template(self):
        resp = self.client.get(reverse('authors:posts_list'))
        self.assertEqual(resp.status_code, 200)


class PostDetailTest(TestCase):

    def setUp(self):
        self.author = MyUser.objects.create_user(username='TestUser',
                                                 email='author@blog.ru',
                                                 password='author@blog.ru')

        self.post = Post.objects.create(name=MyUser.objects.get(username='TestUser'),
                                        title='Test title',
                                        body='Test body')

    def test_detail_author_posts(self):
        resp = self.client.get(reverse('authors:list_post_by_author',
                                       kwargs={'name_id': self.author.pk}))
        self.assertContains(resp, self.post.name)
        print(self.post.title)
        self.assertEqual(200, resp.status_code)
        print(resp.status_code)

