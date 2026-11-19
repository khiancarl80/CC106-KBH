from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import Student


class StaffUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(
        required=False,
        label='Staff status',
        help_text='Allows this user to edit the student directory.',
    )

    class Meta(UserCreationForm.Meta):
        fields = (*UserCreationForm.Meta.fields, 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data['is_staff']
        if commit:
            user.save()
        return user


User = get_user_model()
admin.site.unregister(User)


@admin.register(User)
class StaffUserAdmin(UserAdmin):
    add_form = StaffUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff'),
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'contact_number',
    )
    list_display_links = ('student_id',)
    list_editable = (
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'contact_number',
    )
    search_fields = ('student_id', 'first_name', 'last_name')
    list_filter = ('gender',)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff
=======

# Register your models here.
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
