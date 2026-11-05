from django import forms
<<<<<<< HEAD
from .models import Student

=======

from .models import Student


>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'gender',
            'date_of_birth',
            'contact_number',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
<<<<<<< HEAD
        }
=======
        }
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
