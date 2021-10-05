from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import MyUserCreationForm


class SignUpView(FormView):
    form_class = MyUserCreationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("blog:all_posts")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)
