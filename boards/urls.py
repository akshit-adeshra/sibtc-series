from django.urls import path

from boards import views

app_name = 'boards'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('boards/<int:pk>/', views.BoardTopics.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.NewTopic.as_view(), name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.TopicPosts.as_view(), name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply', views.ReplyTopic.as_view(), name='reply_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit', views.EditPost.as_view(), name='edit_post'),
]
