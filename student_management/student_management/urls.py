"""
URL configuration for student_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.urls import path, include


class StaffAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                "Invalid username or password.",
                code="invalid_login",
            )


class StaffAwareLoginView(auth_views.LoginView):
    template_name = 'login.html'
    authentication_form = StaffAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path(
        'login/',
        StaffAwareLoginView.as_view(),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
=======
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
>>>>>>> 8334cfc5afb2a58983832eac19673caa1666c81f
    path('registration/', include('registration.urls')),
]
