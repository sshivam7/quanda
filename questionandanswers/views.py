from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from questionandanswers.models import Question, Answer, Topic
from django.contrib.auth import login, authenticate
from questionandanswers.forms import UserEmailCreationForm

def index(request):
    """ Load the Site Homepage """
    return render(request, 'index.html')


class SearchResults(generic.ListView):
    """ Search for questions based on a GET request """
    model = Question
    template_name = 'question_list.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        return Question.objects.filter(title__contains=query)


class QuestionListView(generic.ListView):
    """ List all questions """
    model = Question 
    paginate_by = 10


def question_details(request, pk):
    """ Load the question details page """
    question = get_object_or_404(Question, pk=pk)
    answers_list = Answer.objects.filter(qid=pk)

    # answers for a given question along with the question are passed to the template 
    context = {
        'question': question,
        'answer_list': answers_list,
    }

    return render(request, 'questionandanswers/question_detail.html', context)


@login_required
def question_vote_change(request, pk, change):
    """ Change quanda votes for a given question """
    question = get_object_or_404(Question, pk=pk)
    # 0 as the change parameter results in a decrease to the quanda vote counter
    if change == 0:
        change = -1
    question.quanda_votes = F('quanda_votes') + change
    question.save()

    return redirect(question.get_absolute_url())


@login_required
def answer_vote_change(request, qid, pk, change):
    """ Change quanda votes for a given answer """
    answer = get_object_or_404(Answer, pk=pk)
    # 0 as the change parameter results in a decrease to the quanda vote counter
    if change == 0:
        change = -1 
    answer.quanda_votes = F('quanda_votes') + change
    answer.save()

    question = get_object_or_404(Question, pk=qid)
    return redirect(question.get_absolute_url())


class TopicListView(generic.ListView):
    """ List all topics """
    model = Topic

 
def search_by_topic(request, topic):
    """ Load all questions "tagged" with a specific topic """
    question_list = Question.objects.filter(topic__name__contains=topic)
    context = {'question_list': question_list}
    return render(request, 'questionandanswers/question_list.html', context)


@login_required
def my_content(request): 
    """ 
    Loads the my content page where users can view the questions and answers
    that they have created
    """

    question_list = Question.objects.filter(author=request.user)
    answer_list = Answer.objects.filter(author=request.user)

    context = {
        'question_list': question_list,
        'answer_list': answer_list,
    }

    return render(request, 'questionandanswers/my_content.html', context)


class QuestionCreate(LoginRequiredMixin, CreateView):
    """ View for creating a question """
    model = Question
    fields = ['title', 'description', 'topic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(QuestionCreate, self).form_valid(form)


class QuestionDelete(LoginRequiredMixin, DeleteView):
    """ View for deleting a question """
    model = Question
    success_url = reverse_lazy('my-content')


class QuestionUpdate(LoginRequiredMixin, UpdateView):
    """ View for updating a question """
    model = Question
    fields = ['title', 'description', 'topic']


@login_required
def mark_resolved(request, pk):
    """ Marks a given question as resolved """
    question = get_object_or_404(Question, pk=pk)
    # updates question status
    question.status = 'r'
    question.save()
    return redirect(reverse_lazy('my-content'))


class AnswerCreate(LoginRequiredMixin, CreateView):
    """ View for creating an answer """
    model = Answer
    fields = ['description']

    # Redirect back to question page after an answer has been posted 
    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk': self.question.qid})

    # get the corresponding question for the given answer
    def dispatch(self, request, *args, **kwargs):
        # Get question instance
        self.question = get_object_or_404(Question, pk=kwargs['qid'])
        return super().dispatch(request, *args, **kwargs)

    # Set default fields for 
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.qid = self.question
        return super(AnswerCreate, self).form_valid(form)


class AnswerUpdate(LoginRequiredMixin, UpdateView):
    """ View for updating an answer """
    model = Answer
    fields = ['description']

    # Get question object to 
    def dispatch(self, request, *args, **kwargs):
        # Get question instance
        self.answer = get_object_or_404(Answer, pk=kwargs['pk'])
        self.question = self.answer.qid
        return super().dispatch(request, *args, **kwargs)
    
    # Redirect back to question page after an answer has been updated
    def get_success_url(self):
        return reverse_lazy('question-detail', kwargs={'pk': self.question.qid})


class AnswerDelete(LoginRequiredMixin, DeleteView):
    """ View for deleting an answer """
    model = Answer
    success_url = reverse_lazy('my-content')


class SignUp(CreateView):
    """ Loads signup page allowing a guest to create a user account """
    form_class = UserEmailCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'