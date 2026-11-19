from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Student


class RegistrationTests(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_user(
            username='staff',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(self.staff_user)

    def create_student(self, student_id='S-100', first_name='Juan', last_name='Dela Cruz'):
        return Student.objects.create(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            gender='Male',
            date_of_birth='2005-01-15',
            contact_number='09171234567',
        )

    def test_registration_page_loads(self):
        self.client.logout()
        response = self.client.get(reverse('student_registration'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registrations/registration.html')
        self.assertContains(response, reverse('student_list'))
        self.assertContains(response, 'Back to Home')

    def test_registration_creates_student_and_redirects(self):
        self.client.logout()
        response = self.client.post(reverse('student_registration'), {
            'student_id': 'S-100',
            'first_name': 'Juan',
            'last_name': 'Dela Cruz',
            'gender': 'Male',
            'date_of_birth': '2005-01-15',
            'contact_number': '09171234567',
        })

        self.assertRedirects(response, reverse('registration_success'))
        self.assertTrue(Student.objects.filter(student_id='S-100').exists())

    def test_registration_rejects_missing_required_fields(self):
        self.client.logout()
        response = self.client.post(reverse('student_registration'), {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 0)

    def test_student_list_searches_id_and_names(self):
        matching = self.create_student()
        self.create_student(student_id='S-200', first_name='Maria', last_name='Reyes')

        response = self.client.get(reverse('student_list'), {'q': 'dela'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, matching.student_id)
        self.assertNotContains(response, 'S-200')
        self.assertContains(response, 'Back to Home')

    def test_student_create_and_update(self):
        create_response = self.client.post(reverse('student_create'), {
            'student_id': 'S-300',
            'first_name': 'Ana',
            'last_name': 'Santos',
            'gender': 'Female',
            'date_of_birth': '2004-02-15',
            'contact_number': '09170000001',
        })

        student = Student.objects.get(student_id='S-300')
        self.assertRedirects(create_response, reverse('student_list'))

        update_response = self.client.post(
            reverse('student_update', args=[student.pk]),
            {
                'student_id': 'S-300',
                'first_name': 'Anna',
                'last_name': 'Santos',
                'gender': 'Female',
                'date_of_birth': '2004-02-15',
                'contact_number': '09170000001',
            },
        )

        student.refresh_from_db()
        self.assertRedirects(
            update_response,
            reverse('student_detail', args=[student.pk]),
        )
        self.assertEqual(student.first_name, 'Anna')

    def test_student_delete_requires_post(self):
        student = self.create_student()

        response = self.client.get(reverse('student_delete', args=[student.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Student.objects.filter(pk=student.pk).exists())

        response = self.client.post(reverse('student_delete', args=[student.pk]))
        self.assertRedirects(response, reverse('student_list'))
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())

    def test_staff_login_redirects_to_dashboard(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'staff',
            'password': 'test-password',
        })

        self.assertRedirects(response, reverse('staff_dashboard'))
        dashboard_response = self.client.get(reverse('staff_dashboard'))
        self.assertContains(dashboard_response, 'Welcome, staff!')

    def test_dashboard_summary_and_search_report(self):
        male = self.create_student()
        female = self.create_student(
            student_id='S-200',
            first_name='Maria',
            last_name='Reyes',
        )
        female.gender = 'Female'
        female.save()

        response = self.client.get(reverse('staff_dashboard'))

        self.assertEqual(response.context['total_students'], 2)
        self.assertEqual(response.context['male_students'], 1)
        self.assertEqual(response.context['female_students'], 1)
        self.assertEqual(response.context['male_percent'], 50)
        self.assertEqual(response.context['female_percent'], 50)

        search_response = self.client.get(
            reverse('staff_dashboard'),
            {'q': 'Maria'},
        )
        self.assertContains(search_response, female.student_id)
        self.assertNotContains(search_response, male.student_id)
        self.assertEqual(search_response.context['total_students'], 2)

    def test_invalid_login_displays_error(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'staff',
            'password': 'incorrect-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_non_staff_user_cannot_login_through_staff_login(self):
        get_user_model().objects.create_user(
            username='regular',
            password='test-password',
            is_staff=False,
        )
        self.client.logout()

        response = self.client.post(reverse('login'), {
            'username': 'regular',
            'password': 'test-password',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
        self.assertNotContains(response, 'Forbidden')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_anonymous_users_are_redirected_from_management_pages(self):
        student = self.create_student()
        self.client.logout()
        protected_urls = [
            reverse('staff_dashboard'),
            reverse('student_list'),
            reverse('student_create'),
            reverse('student_detail', args=[student.pk]),
            reverse('student_update', args=[student.pk]),
            reverse('student_delete', args=[student.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f'{reverse("login")}?next={url}',
                    fetch_redirect_response=False,
                )

    def test_non_staff_users_cannot_access_management_pages(self):
        student = self.create_student()
        non_staff_user = get_user_model().objects.create_user(
            username='regular',
            password='test-password',
            is_staff=False,
        )
        self.client.force_login(non_staff_user)
        protected_urls = [
            reverse('staff_dashboard'),
            reverse('student_list'),
            reverse('student_create'),
            reverse('student_detail', args=[student.pk]),
            reverse('student_update', args=[student.pk]),
            reverse('student_delete', args=[student.pk]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def test_logout_ends_staff_session_and_redirects_to_login(self):
        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
        dashboard_response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(dashboard_response.status_code, 302)
        self.assertTrue(dashboard_response.url.startswith(reverse('login')))


class StudentAdminTests(TestCase):
    def setUp(self):
        admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(admin_user)

    def test_admin_can_create_staff_user_and_staff_can_edit_student_directory(self):
        add_user_response = self.client.post(
            reverse('admin:auth_user_add'),
            {
                'username': 'directory-editor',
                'password1': 'test-password',
                'password2': 'test-password',
                'is_staff': 'on',
                '_save': 'Save',
            },
        )

        self.assertEqual(add_user_response.status_code, 302)
        staff_user = get_user_model().objects.get(username='directory-editor')
        self.assertTrue(staff_user.is_staff)

        student = Student.objects.create(
            student_id='STAFF-100',
            first_name='Alex',
            last_name='Santos',
            gender='Male',
            date_of_birth='2004-02-15',
            contact_number='09170000001',
        )
        self.client.force_login(staff_user)
        change_url = reverse('admin:registration_student_change', args=[student.pk])
        response = self.client.post(change_url, {
            'student_id': 'STAFF-100',
            'first_name': 'Alexandra',
            'last_name': 'Santos',
            'gender': 'Female',
            'date_of_birth': '2004-02-15',
            'contact_number': '09170000001',
            '_save': 'Save',
        })

        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.first_name, 'Alexandra')

    def test_admin_add_user_defaults_staff_status_to_off(self):
        self.client.post(
            reverse('admin:auth_user_add'),
            {
                'username': 'directory-viewer',
                'password1': 'test-password',
                'password2': 'test-password',
                '_save': 'Save',
            },
        )

        user = get_user_model().objects.get(username='directory-viewer')
        self.assertFalse(user.is_staff)

    def test_admin_can_create_and_edit_students(self):
        changelist_url = reverse('admin:registration_student_changelist')
        add_url = reverse('admin:registration_student_add')
        add_response = self.client.post(add_url, {
            'student_id': 'ADMIN-100',
            'first_name': 'Alex',
            'last_name': 'Santos',
            'gender': 'Male',
            'date_of_birth': '2004-02-15',
            'contact_number': '09170000001',
            '_save': 'Save',
        })

        self.assertRedirects(add_response, changelist_url)
        student = Student.objects.get(student_id='ADMIN-100')
        self.assertContains(self.client.get(changelist_url), student.student_id)

        change_url = reverse('admin:registration_student_change', args=[student.pk])
        change_response = self.client.post(change_url, {
            'student_id': 'ADMIN-100',
            'first_name': 'Alexandra',
            'last_name': 'Santos',
            'gender': 'Female',
            'date_of_birth': '2004-02-15',
            'contact_number': '09170000001',
            '_save': 'Save',
        })

        self.assertRedirects(change_response, changelist_url)
        student.refresh_from_db()
        self.assertEqual(student.first_name, 'Alexandra')
        self.assertEqual(student.gender, 'Female')

    def test_admin_can_edit_student_fields_from_the_changelist(self):
        student = Student.objects.create(
            student_id='ADMIN-200',
            first_name='Taylor',
            last_name='Cruz',
            gender='Female',
            date_of_birth='2004-06-21',
            contact_number='09170000003',
        )

        response = self.client.post(
            reverse('admin:registration_student_changelist'),
            {
                'form-TOTAL_FORMS': '1',
                'form-INITIAL_FORMS': '1',
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '1000',
                'form-0-id': str(student.pk),
                'form-0-first_name': 'Taylor Anne',
                'form-0-last_name': 'Reyes',
                'form-0-gender': 'Female',
                'form-0-date_of_birth': '2004-06-21',
                'form-0-contact_number': '09170000004',
                '_save': 'Save',
            },
        )

        student.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(student.first_name, 'Taylor Anne')
        self.assertEqual(student.last_name, 'Reyes')
        self.assertEqual(student.contact_number, '09170000004')
