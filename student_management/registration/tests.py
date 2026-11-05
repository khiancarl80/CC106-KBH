from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

<<<<<<< HEAD
from .models import Student


class StudentCrudMessageTests(TestCase):
    student_data = {
        'student_id': 'S1001',
        'first_name': 'Alex',
        'last_name': 'Morgan',
        'gender': 'Male',
        'date_of_birth': '2005-04-12',
        'contact_number': '555-0100',
    }

    def test_create_shows_success_message(self):
        response = self.client.post(
            reverse('student_create'),
            self.student_data,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            [str(message) for message in get_messages(response.wsgi_request)],
            ['Student record created successfully.'],
        )

    def test_update_shows_success_message(self):
        student = Student.objects.create(**self.student_data)
        updated_data = {**self.student_data, 'first_name': 'Jordan'}

        response = self.client.post(
            reverse('student_update', kwargs={'pk': student.pk}),
            updated_data,
        )

        student.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(student.first_name, 'Jordan')
        self.assertEqual(
            [str(message) for message in get_messages(response.wsgi_request)],
            ['Student record updated successfully.'],
        )

    def test_delete_shows_success_message(self):
        student = Student.objects.create(**self.student_data)

        response = self.client.post(
            reverse('student_delete', kwargs={'pk': student.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())
        self.assertEqual(
            [str(message) for message in get_messages(response.wsgi_request)],
            ['Student record deleted successfully.'],
        )

    def test_invalid_create_does_not_show_success_message(self):
        invalid_data = {**self.student_data, 'student_id': ''}

        response = self.client.post(reverse('student_create'), invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)
        self.assertEqual(list(get_messages(response.wsgi_request)), [])
=======
from django.urls import reverse

from .models import Student


class StudentViewsTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='S001',
            first_name='Ada',
            last_name='Lovelace',
            gender='Female',
            date_of_birth='1815-12-10',
            contact_number='123456789',
        )

    def test_registration_form_uses_model_field_names(self):
        response = self.client.get(reverse('student_registration'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="contact_no"')

    def test_registration_creates_student(self):
        response = self.client.post(
            reverse('student_registration'),
            {
                'student_id': 'S002',
                'first_name': 'Grace',
                'last_name': 'Hopper',
                'gender': 'Female',
                'date_of_birth': '1906-12-09',
                'contact_no': '987654321',
            },
        )

        self.assertRedirects(response, reverse('registration_success'))
        self.assertTrue(Student.objects.filter(student_id='S002').exists())

    def test_student_list_renders_directory(self):
        response = self.client.get(reverse('student_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student.student_id)

    def test_create_student(self):
        response = self.client.post(
            reverse('student_create'),
            {
                'student_id': 'S002',
                'first_name': 'Grace',
                'last_name': 'Hopper',
                'gender': 'Female',
                'date_of_birth': '1906-12-09',
                'contact_number': '987654321',
            },
            follow=True,
        )

        self.assertEqual(
            response.redirect_chain,
            [(reverse('student_list'), 302)],
        )
        self.assertTrue(Student.objects.filter(student_id='S002').exists())
        self.assertContains(response, 'Student record created successfully.')

    def test_update_student(self):
        response = self.client.post(
            reverse('student_update', args=[self.student.pk]),
            {
                'student_id': self.student.student_id,
                'first_name': 'Augusta',
                'last_name': self.student.last_name,
                'gender': self.student.gender,
                'date_of_birth': '1815-12-10',
                'contact_number': self.student.contact_number,
            },
        )

        self.assertRedirects(
            response,
            reverse('student_detail', args=[self.student.pk]),
        )
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Augusta')

    def test_delete_student(self):
        response = self.client.post(
            reverse('student_delete', args=[self.student.pk]),
        )

        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
