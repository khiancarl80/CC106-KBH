from django import forms
<<<<<<< HEAD
=======
<<<<<<< HEAD
from .models import Student

=======
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f

from .models import Student


<<<<<<< HEAD
=======
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
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
<<<<<<< HEAD
        }
=======
        }
>>>>>>> 9f40c6e4b841a32b9b0c81a60ce855e211056d99
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
