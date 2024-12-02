from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, RedirectView, TemplateView

from accounts.forms import UserRegistrationForm
from common.utils.token_generators import TokenGenerator


class IndexView(TemplateView):
    template_name = "index.html"


class UserRegistrationView(CreateView):
    template_name = "registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        return super().form_valid(form)


class UserLogin(LoginView):
    next_page = reverse_lazy("home")


class UserLogout(LogoutView):
    next_page = reverse_lazy("login")


class UserActivationView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            pk = force_str(urlsafe_base64_decode(uidb64))
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, ValueError, TypeError):
            render(request, "errors/wrong_data.html")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            login(request, current_user)

            return super().get(request, *args, **kwargs)

        render(request, "errors/wrong_data.html")
