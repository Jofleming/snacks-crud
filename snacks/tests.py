from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Snack


# Create your tests here.

class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='tester', email='tester@email.com', password='tester')
        
        self.snack = Snack.objects.create(title='test sandwhich', description='Test Description', purchaser=self.user)


    def test_snack_list_page(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "test sandwhich")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "test sandwhich")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(self.snack.description, 'Test Description')

    def test_snack_list_template(self):
        url = reverse('snack_list')
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_list_page_context(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        snacks = response.context['object_list']
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0].title, 'test sandwhich')
        self.assertEqual(snacks[0].purchaser.username, 'tester')
        self.assertEqual(snacks[0].description, 'Test Description')

    def test_detail_page_status_code(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_page_context(self):
        url = reverse('snack_detail',args=(1,))
        response = self.client.get(url)
        snack = response.context['snack']
        self.assertEqual(snack.title, 'test sandwhich')
        self.assertEqual(snack.description, 'Test Description')
        self.assertEqual(snack.purchaser.username, 'tester')

    def test_update_page_template(self):
        url = reverse('snack_update',args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_update.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_delete_page_template(self):
        url = reverse('snack_delete',args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snack_delete.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_create_page(self):
        url = reverse('snack_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_404(self):
        url = 'missing/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)