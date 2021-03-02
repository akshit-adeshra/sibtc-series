from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from .forms import NewTopicForm, PostForm
from .models import *


class Home(ListView):
    model = Board
    template_name = 'home.html'
    context_object_name = 'boards'
    # paginate_by = 10
    # if you give this pagination , then you'll have to access pending records by appending this code at the end of the
    # URL: ?page=1/2/3/4...

    # ALTERNATIVE code of the below get_context_data()
    # def get(self, request, *args, **kwargs):
    #     context = {'boards': Board.objects.all()}
    #     return render(request, 'home.html', context)


class BoardTopics(ListView):
    model = Topic
    template_name = 'topics.html'
    context_object_name = 'topics'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


@method_decorator(login_required, name='dispatch')
class NewTopic(CreateView):
    form_class = NewTopicForm  # If you don't need any additional functionality, you don't need to specify form_valid() method
    template_name = 'new_topic.html'
    model = Topic

    def get_success_url(self):
        return reverse('boards:board_topics', kwargs={'pk': self.kwargs.get("pk")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        super().form_valid(form)
        topic = form.save(commit=False)
        board = Board.objects.get(pk=self.kwargs.get('pk'))
        topic.board = board
        topic.starter = self.request.user
        topic.save()
        post = Post.objects.create(
            message=form.cleaned_data.get('message'),
            topic=topic,
            created_by=self.request.user
        )
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print('-------------------------- invalid form -------------------------------')
        return super().form_invalid(form)


class TopicPosts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Session is added for the view count
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))  
        # args in .get(' ') are fetched from url's kwargs and passed as arg in the model to fetch the obj
        
        queryset = self.topic.posts.order_by('-created_at')
        return queryset


@method_decorator(login_required, name='dispatch')
class ReplyTopic(CreateView):
    model = Topic
    template_name = 'reply_topic.html'
    form_class = PostForm
    success_url = 'reply/'

    # def get_success_url(self):
    #     return reverse('boards:reply_topic', kwargs={'pk': self.kwargs.get("pk"), 'topic_pk': self.kwargs.get("topic_pk")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = Topic.objects.get(board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        return context

    def form_valid(self, form):
        super().form_valid(form)
        msg = self.request.POST['message']
        post = form.save(commit=False)
        topic = Topic.objects.get(board__pk=self.kwargs.get("pk"), pk=self.kwargs.get("topic_pk"))
        post.topic = topic
        post.created_by = self.request.user
        post.save()

        # for updating the last_update field when someone replies to a post, and to correct ordering of the topics
        topic.last_updated = timezone.now()
        topic.save()

        # post_data = Post.objects.filter(message=msg).values()
        post_data = Post.objects.values_list('created_by__first_name', 'created_at', 'message').filter(message=msg)

        print(post_data)
        print("\n\n\n--------------------", type(post_data))
        post_data = list(post_data)
        return JsonResponse({'status': 'Save', 'post_data': post_data})
        # return redirect(self.get_success_url())

    def form_invalid(self, form):
        super(ReplyTopic, self).form_invalid(form)
        return HttpResponse({'status': 0})


@method_decorator(login_required, name='dispatch')
class EditPost(UpdateView):
    model = Post
    fields = ('message',)  
    # fields is the alternative of 'form_class'; it'll also generate the form on-the-fly. We've used it here coz we only need 'message' field
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
