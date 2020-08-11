from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('home/', views.index, name='index'),
    # displays question information
    path('questions/', views.QuestionListView.as_view(), name='questions'),
    path('questions/search/', views.SearchResults.as_view(), name='search-results'),
    path('questions/<int:pk>', views.question_details, name='question-detail'),
    # Change quanda votes
    path('question/<int:pk>/<int:change>',
         views.question_vote_change, name='question-vote-change'),
    path('answer/<int:qid>/<int:pk>/<int:change>',
         views.answer_vote_change, name='answer-vote-change'),
    # Load topics and search by topics
    path('topics/', views.TopicListView.as_view(), name='topics'),
    path('topics/<str:topic>', views.search_by_topic, name='search-by-topic'),
    # Holds all user created answers and questions
    path('myContent/', views.my_content, name='my-content'),
    # Create and change question properties
    path('questions/new/', views.QuestionCreate.as_view(), name='new-question'),
    path('questions/<int:pk>/delete/',
         views.QuestionDelete.as_view(), name='question-delete'),
    path('questions/<int:pk>/update/',
         views.QuestionUpdate.as_view(), name='question-update'),
    path('questions/<int:pk>/mark-resolved',
         views.mark_resolved, name='mark-resolved'),
    # Create, edit, and delete answers
    path('questions/<int:qid>/answer/',
         views.AnswerCreate.as_view(), name='new-answer'),
    path('questions/<int:pk>/answer-delete/',
         views.AnswerDelete.as_view(), name='answer-delete'),
    path('questions/<int:pk>/answer-update/',
         views.AnswerUpdate.as_view(), name='answer-update'),
    # create a new user
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
]
