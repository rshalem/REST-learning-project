from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'restapp'

urlpatterns = [
    #path('questions/', views.questions_list, name='question-list'),
    #path('questions/<int:id>/', views.question_detail, name='question-detail'),
    path('questions/', views.QuestionAPIView.as_view(), name='question-list'),
    path('questions/<int:pk>/', views.QuestionDetailAPIView.as_view(), name='question-detail'),

]

#urlpatterns = format_suffix_patterns(urlpatterns)