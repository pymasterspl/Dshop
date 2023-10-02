# from django.shortcuts import render
# use class based views.
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView, View, TemplateView, RedirectView

from .forms import CustomUserForm, UpdateUserForm, UpdateCustomUserForm
from .models import CustomUser


class RegistrationView(CreateView):
    redirect_authenticated_user = True
    form_class = CustomUserForm
    success_url = reverse_lazy('login')
    template_name = 'users/registration.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super(RegistrationView, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        CustomUser.objects.create(user_id=new_user.id)
        login(self.request, new_user)
        return valid


class LoginUserView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password !')
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class RemoveUserView(LoginRequiredMixin, View):
    login_url = 'login/'

    def post(self, request):
        user = request.user
        user.is_active = False
        logout(user)
        return redirect('home')


class UpdateUserView(LoginRequiredMixin, View):
    template_name = 'users/update_user.html'

    def get(self, request):
        user = CustomUser.objects.get(user=self.request.user)
        form = UpdateCustomUserForm(instance=user)
        form_s = UpdateUserForm(instance=self.request.user)
        context = {'form': form, 'form_s': form_s, 'user': user}
        return render(request, self.template_name, context)

    def post(self, request):
        user = CustomUser.objects.get(user=self.request.user)
        form = UpdateCustomUserForm(request.POST, instance=user)
        form_s = UpdateUserForm(request.POST, instance=self.request.user)
        if form.is_valid() & form_s.is_valid():
            form.save()
            form_s.save()
            return redirect('update_user')
        context = {'form': form, 'form_s': form_s, 'user': user}
        return render(request, self.template_name, context)


class HomeView(TemplateView):
    template_name = 'users/home.html'
