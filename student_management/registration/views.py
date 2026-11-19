<<<<<<< HEAD
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from functools import wraps
=======
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f

from .forms import StudentForm
from .models import Student

<<<<<<< HEAD

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
    return render(request, 'registrations/dashboard.html')


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
=======
def student_registration(request):
    if request.method == 'POST':
        Student.objects.create(
            student_id=request.POST.get('student_id'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            contact_number=request.POST.get('contact_no'),
        )
        return redirect('registration_success')

    return render(
        request,
        'registration/registration.html',
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
    )


def registration_success(request):
    return render(
        request,
<<<<<<< HEAD
        'registrations/success.html'
    )


@staff_required
=======
        'registration/success.html'
    )

<<<<<<< HEAD
=======

>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
def student_list(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.all().order_by('last_name', 'first_name')
    if query:
<<<<<<< HEAD
=======
<<<<<<< HEAD
       students = students.filter(
           Q(student_id__icontains=query) |
           Q(first_name__icontains=query) |
           Q(last_name__icontains=query)
      )
=======
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
<<<<<<< HEAD
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
=======
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
    return render(
        request,
        'registration/student_list.html',
        {'students': students, 'query': query},
    )

<<<<<<< HEAD
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
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
=======
            student = form.save()
            messages.success(request, 'Student record created successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
=======

def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student record created successfully.')
        return redirect('student_list')
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99

    return render(
        request,
        'registration/student_form.html',
        {'form': form, 'page_title': 'Register Student'},
    )

<<<<<<< HEAD
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'registration/student_detail.html', {'student': student})

>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
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
<<<<<<< HEAD
    return render(
        request,
        'registrations/student_form.html',
=======
=======

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(
        request,
        'registration/student_detail.html',
        {'student': student},
    )


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student record updated successfully.')
        return redirect('student_detail', pk=student.pk)
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99

    return render(
        request,
        'registration/student_form.html',
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
        {
            'form': form,
            'page_title': 'Update Student',
            'student': student,
        },
    )

<<<<<<< HEAD

@staff_required
=======
<<<<<<< HEAD
=======

>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student record deleted successfully.')
        return redirect('student_list')
<<<<<<< HEAD
    return render(
        request,
        'registrations/student_confirm_delete.html',
=======

    return render(
        request,
        'registration/student_confirm_delete.html',
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
        {'student': student},
    )