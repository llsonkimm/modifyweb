import json
from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import PersonalForm, BusinessForm, NeedsForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group, Permission
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect, reverse, get_object_or_404
from guardian.conf import settings as guardian_settings
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm, get_objects_for_user

from .tokens import user_tokenizer
from .forms import RegistrationForm, PersonalForm, BusinessForm, NeedsForm
from django.http.response import HttpResponseRedirect


class HomeView(FormView):
    def get(self, request):
        return render(request, 'home.html')


class SuccessView(TemplateView):
    template_name = 'success.html'

class TestEmail(View):
    def get(self, request):
        user = User.objects.get(pk=9)
        token = user_tokenizer.make_token(user)
        user_id = urlsafe_base64_encode(force_bytes(user.id))
        url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
        message = get_template('survey/register_email.html').render({
          'confirm_url': url
        })
        mail = EmailMessage('Django Survey Email Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
        mail.content_subtype = 'html'
        mail.send()
        return HttpResponse(f'email sent user_id = {user_id}, token = {token}')


class ConfirmRegistrationView(View):
    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        
        user = User.objects.get(pk=user_id)

        context = {
          'form': AuthenticationForm(),
          'message': 'Registration confirmation error . Please click the reset password to generate a new confirmation email.'
        }
        if user and user_tokenizer.check_token(user, token):
            user.is_valid = True
            user.save()
            context['message'] = 'Registration complete. Please login'

        return render(request, 'login.html', context)

class CustomFieldFormView(FormView):
    def get(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = PersonalForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('trial2/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = PersonalForm()

        return render(request, 'trial1.html', {'form': PersonalForm()})





class CustomBusinessFieldFormView(FormView):
    def get(self, request):
         # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = BusinessForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('trial3/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = BusinessForm()
        return render(request, 'trial2.html', { 'form': BusinessForm() })

class CustomNeedsFieldFormView(FormView):
    def get(self, request):
         # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = NeedsForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('/success/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = NeedsForm()
        return render(request, 'trial3.html', { 'form': NeedsForm() })


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html', { 'form': RegistrationForm() })

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
            message = get_template('register_email.html').render({
              'confirm_url': url
            })
            mail = EmailMessage('Confirmation', message, to=[user.email], from_email=settings.EMAIL_HOST_USER)
            mail.content_subtype = 'html'
            mail.send()

            return render(request, 'login.html', {
              'form': AuthenticationForm(),
              'message': f'A confirmation email has been sent to {user.email}. Please confirm to finish registering'
            })

        return render(request, 'register.html', { 'form': form })



class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', { 'form':  AuthenticationForm() })


    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            try:
                form.clean()
            except ValidationError:
                return render(
                    request,
                    'login.html',
                    { 'form': form, 'invalid_creds': True }
                )

            login(request, form.get_user())

            return redirect(reverse('profile'))

        return render(request, 'login.html', { 'form': form })
