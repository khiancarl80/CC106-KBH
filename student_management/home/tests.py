from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_landing_page_links_to_registration_and_directory(self):
        response = self.client.get(reverse('landing'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('student_registration'))
        self.assertContains(response, reverse('student_list'))

    def test_home_page_links_to_registration_and_directory(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('student_registration'))
        self.assertContains(response, reverse('student_list'))
