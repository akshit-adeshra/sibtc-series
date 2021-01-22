from django.urls import path
from boards import views

app_name = 'boards'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('boards/<int:pk>/', views.BoardTopics.as_view(), name='board_topics'),
    path('boards/<int:pk>/new/', views.NewTopic.as_view(), name='new_topic'),
]
