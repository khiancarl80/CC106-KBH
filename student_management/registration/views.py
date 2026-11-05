from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student

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
    )


def registration_success(request):
    return render(
        request,
        'registration/success.html'
    )

<<<<<<< HEAD
=======

>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
def student_list(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.all().order_by('last_name', 'first_name')
    if query:
<<<<<<< HEAD
       students = students.filter(
           Q(student_id__icontains=query) |
           Q(first_name__icontains=query) |
           Q(last_name__icontains=query)
      )
=======
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
        )
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
    return render(
        request,
        'registration/student_list.html',
        {'students': students, 'query': query},
    )

<<<<<<< HEAD
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
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
        {
            'form': form,
            'page_title': 'Update Student',
            'student': student,
        },
    )

<<<<<<< HEAD
=======

>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student record deleted successfully.')
        return redirect('student_list')

    return render(
        request,
        'registration/student_confirm_delete.html',
        {'student': student},
    )