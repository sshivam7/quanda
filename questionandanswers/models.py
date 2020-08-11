from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """ Model representing question topic """
    name = models.CharField(
        max_length=200, help_text="Enter a question topic (e.g. Programming)")

    def __str__(self):
        """String for representing the Model Object"""
        return self.name


class Question(models.Model):
    """ Model representing a question asked by a user """
    qid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(
        max_length=2000, help_text="A detailed description explaining the problem and attempted solutions")
    quanda_votes = models.IntegerField(
        help_text="Amount of Quanda votes (used to sort good and bad questions)", default=0)

    # Foregin Key used to represent an author (User model)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Many to Many field used to represent topics the current question falls under
    topic = models.ManyToManyField(
        Topic, help_text="Select a topic (or topics) for this question")

    QUESTION_STATUS = (
        ('r', 'Resolved'),
        ('u', 'Unresolved'),
    )

    status = models.CharField(
        max_length=1,
        choices=QUESTION_STATUS,
        default='u',
        help_text="Question Resolution",
    )

    date_created = models.DateField(editable=False)

    class Meta:
        """ Order questions by newest first and then look at the most quanda votes """
        ordering = ['-date_created', '-quanda_votes']

    def save(self, *args, **kwargs):
        """ On save, set timestamp to store the date the question was created """
        # check if the question has not already been created
        if not self.qid:
            self.date_created = timezone.now()
        return super(Question, self).save(*args, **kwargs)

    def display_topic(self):
        """ Create a string to display (up to 3) topics """
        return ', '.join(topic.name for topic in self.topic.all()[:3])

    def get_absolute_url(self):
        """ Returns the url to access a particular question instance """
        return reverse("question-detail", args=[str(self.qid)])

    def __str__(self):
        """ String for representing the model object """
        return self.title


class Answer(models.Model):
    """ Model representing answers that a question can have """
    aid = models.AutoField(primary_key=True)
    qid = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(
        max_length=2000, help_text="A detailed description providing the solution to a given question")
    quanda_votes = models.IntegerField(
        help_text="Amount of Quanda votes (used to sort good and bad answers)", default=0)

    # Foregin Key used to represent answer author (User model)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    date_created = models.DateField(editable=False)

    class Meta:
        # sort based on most votes and then by most recent
        ordering = ['-quanda_votes', '-date_created']

    def save(self, *args, **kwargs):
        """ On save, update timestamp """
        if not self.aid:
            self.date_created = timezone.now()
        return super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        """ String for representing the model object """
        return f'{self.author}: {self.description}'
