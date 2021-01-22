from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import CreateView, ListView
from .models import *
from .forms import NewTopicForm


class Home(ListView):
    model = Board
    template_name = 'home.html'
    context_object_name = 'boards'

    # ALTERNATIVE code of the below get_context_data()
    # def get(self, request, *args, **kwargs):
    #     context = {'boards': Board.objects.all()}
    #     return render(request, 'home.html', context)

class BoardTopics(ListView):
    model = Topic
    template_name = 'topics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(pk=self.kwargs.get('pk'))
        return context

class NewTopic(CreateView):
    form_class = NewTopicForm               # If you don't need any additional functionality, you don't need to specify form_valid() method
    template_name = 'new_topic.html'
    model = Topic

    def get_success_url(self):
        return reverse('boards:board_topics', kwargs={'pk': self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        context = super(NewTopic, self).get_context_data(**kwargs)
        context['board'] = Board.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        topic = form.save(commit=False)
        board = Board.objects.get(pk=self.kwargs.get('pk'))
        user = User.objects.first()
        topic.board = board
        topic.starter = user
        topic.save()
        post = Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=user
        )
        super().form_valid(form)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)