from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from functools import wraps

from .forms import StudentForm
from .models import Student


def staff_check(user):
    return user.is_authenticated and user.is_staff


def staff_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), reverse('login'))
        if not staff_check(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped_view


@staff_required
def staff_dashboard(request):
    total_students = Student.objects.count()
    male_students = Student.objects.filter(gender='Male').count()
    female_students = Student.objects.filter(gender='Female').count()

    male_percent = (
        male_students / total_students * 100
        if total_students > 0 else 0
    )
    female_percent = (
        female_students / total_students * 100
        if total_students > 0 else 0
    )

    query = request.GET.get('q', '').strip()
    students = Student.objects.all().order_by('last_name', 'first_name')
    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )

    context = {
        'total_students': total_students,
        'male_students': male_students,
        'female_students': female_students,
        'male_percent': male_percent,
        'female_percent': female_percent,
        'students': students,
        'query': query,
    }
    return render(request, 'registrations/dashboard.html', context)


def student_registration(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        contact_number = request.POST.get('contact_number') or request.POST.get('contact_no')

        student = Student(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            contact_number=contact_number
        )

        try:
            student.full_clean()
            student.save()
            return redirect('registration_success')
        except ValidationError as error:
            return render(
                request,
                'registrations/registration.html',
                {
                    'errors': error.message_dict,
                    'student': request.POST,
                },
            )

    return render(
        request,
        'registrations/registration.html',
    )


def registration_success(request):
    return render(
        request,
        'registrations/success.html'
    )


@staff_required
def student_list(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.all().order_by('last_name', 'first_name')
    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
    return render(
        request,
        'registrations/student_list.html',
        {'students': students, 'query': query},
    )


@staff_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(
        request,
        'registrations/student_detail.html',
        {'student': student},
    )


@staff_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record created successfully.')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(
        request,
        'registrations/student_form.html',
        {'form': form, 'page_title': 'Register Student'},
    )


@staff_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record updated successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(
        request,
        'registrations/student_form.html',
        {
            'form': form,
            'page_title': 'Update Student',
            'student': student,
        },
    )


@staff_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student record deleted successfully.')
        return redirect('student_list')
    return render(
        request,
        'registrations/student_confirm_delete.html',
        {'student': student},
    )