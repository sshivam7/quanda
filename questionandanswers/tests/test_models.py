from django.test import TestCase
from questionandanswers.models import Topic, Question, Answer


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Setup data to be used in tests 
        Topic.objects.create(name="Books")

    def test_name_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')


