from django.test import TestCase
from django.test import Client
from django.urls import reverse


class BlogViewsTestCase(TestCase):

    def test_index_pages(self):
        for n in range(100):
            resp = self.client.get('/?page=' + str(n * 100))
            self.assertEqual(resp.status_code, 200)

    def test_admin_access(self):
        resp = self.client.get(reverse('admin'))
        self.assertNotAlmostEquals(resp.status_code, 200, delta=6)

    def test_redirect_add_post_if_not_logged(self):
        resp = self.client.get(reverse('add_post'))
        self.assertRedirects(resp, "/login/?next=/post/add/")

    def test_redirect_edit_post_if_not_logged(self):
        post_id = 1
        resp = self.client.get(reverse('edit_post', kwargs={"id": post_id}))
        self.assertRedirects(resp, "/login/?next=/post/" + str(post_id) + "/edit/")

    def test_redirect_delete_post_if_not_logged(self):
        post_id = 1
        resp = self.client.get(reverse('delete_post', kwargs={"id": post_id}))
        self.assertRedirects(resp, "/login/?next=/post/" + str(post_id) + "/delete/")

    def test_redirect_edit_author_if_not_logged(self):
        username = "author"
        resp = self.client.get(reverse('edit_author', kwargs={"username": username}))
        self.assertRedirects(resp, "/login/?next=/author/" + username + "/edit/")

    def test_redirect_add_user_if_not_staff(self):
        resp = self.client.get(reverse('admin_add_user'))
        self.assertRedirects(resp, "/django/admin/login/?next=/admin/user/add/")

    def test_redirect_admin_if_not_staff(self):
        resp = self.client.get(reverse('admin'))
        self.assertRedirects(resp, "/django/admin/login/?next=/admin/")

    def test_redirect_admin_authors_if_not_staff(self):
        resp = self.client.get(reverse('admin_all_users'))
        self.assertRedirects(resp, "/django/admin/login/?next=/admin/users/")

    def test_redirect_admin_posts_if_not_staff(self):
        resp = self.client.get(reverse("admin_all_posts"))
        self.assertRedirects(resp, "/django/admin/login/?next=/admin/posts/")

    def test_redirect_admin_reset_password_not_staff(self):
        username = "username"
        resp = self.client.get(reverse('admin_reset_password', kwargs={"username": username}))
        self.assertRedirects(resp, "/django/admin/login/?next=/admin/user/" + username + "/resetpassword/")

    def test_redirect_admin_delete_user_if_not_staff(self):
        username = "username"
        resp = self.client.get(reverse('admin_delete_user', kwargs={"username": username}))
        self.assertRedirects(resp, "/django/admin/login/?next=/admin/user/" + username + "/delete/")

    











