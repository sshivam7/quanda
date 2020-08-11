from django.contrib import admin
from .models import Question, Answer, Topic


# Register the Admin Class for Question 
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_topic', 'quanda_votes', 'status', 'date_created')
    list_filter = ('date_created', 'status')

# Register the Admin Class for Answer
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'quanda_votes', 'date_created')

# Register the Admin Class for Topic 
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

