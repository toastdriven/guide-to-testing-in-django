import datetime
from django.test import TestCase
from polls.models import Poll, Choice


class PollTestCase(TestCase):
    fixtures = ['polls_forms_testdata.json']
    
    def setUp(self):
        super(PollTestCase, self).setUp()
        self.poll_1 = Poll.objects.get(pk=1)
        self.poll_2 = Poll.objects.get(pk=2)
    
    def test_was_published_today(self):
        # Because unless you're timetraveling, they weren't.
        self.assertFalse(self.poll_1.was_published_today())
        self.assertFalse(self.poll_2.was_published_today())
        
        # Modify & check again.
        now = datetime.datetime.now()
        self.poll_1.pub_date = now
        self.poll_1.save()
        self.assertTrue(self.poll_1.was_published_today())


class ChoiceTestCase(TestCase):
    fixtures = ['polls_forms_testdata.json']
    
    def test_record_vote(self):
        choice_1 = Choice.objects.get(pk=1)
        choice_2 = Choice.objects.get(pk=2)
        
        self.assertEqual(Choice.objects.get(pk=1).votes, 1)
        self.assertEqual(Choice.objects.get(pk=2).votes, 0)
        
        choice_1.record_vote()
        self.assertEqual(Choice.objects.get(pk=1).votes, 2)
        self.assertEqual(Choice.objects.get(pk=2).votes, 0)
        
        choice_2.record_vote()
        self.assertEqual(Choice.objects.get(pk=1).votes, 2)
        self.assertEqual(Choice.objects.get(pk=2).votes, 1)
        
        choice_1.record_vote()
        self.assertEqual(Choice.objects.get(pk=1).votes, 3)
        self.assertEqual(Choice.objects.get(pk=2).votes, 1)
