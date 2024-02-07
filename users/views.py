from django.urls import reverse
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User


class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('main:survey_list')
