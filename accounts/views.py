from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from .forms import SignupForm
from .models import *


class Signup(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm

    # success_url = 'boards:home'
    # if success_url is given instead of the get_success_url() method, it'll raise an error of:-
    # "DisallowedRedirect at /signup/            Unsafe redirect to URL with protocol 'boards' "

    def get_success_url(self):
        return reverse('boards:home')

    # def form_valid(self, form):
    #
    # if not self.request.POST.get('tnc'):
    #     print('-------------andar to ayu----------------')
    #     messages.error(self.request, "You must agree to our Terms and Conditions..!!")
    #     return super().form_valid(form)
    #
    # else:
    #     super().form_valid(form)
    #     user = form.save()
    #     login(self.request, user)
    #     return redirect('boards:home')

    # raise ValueError('You must agree to our Terms and Conditions..!!')

    def form_valid(self, form):
        super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return redirect('boards:home')

    def form_invalid(self, form):
        return super().form_invalid(form)


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('accounts:my_account')

    def get_object(self):
        return self.request.user
