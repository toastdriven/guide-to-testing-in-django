import datetime
from django.test import TestCase
from polls.models import Poll, Choice


class PollsViewsTestCase(TestCase):
    fixtures = ['polls_views_testdata.json']
    
    def test_index(self):
        resp = self.client.get('/polls/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('latest_poll_list' in resp.context)
        self.assertEqual([poll.pk for poll in resp.context['latest_poll_list']], [1])
        poll_1 = resp.context['latest_poll_list'][0]
        self.assertEqual(poll_1.question, 'Are you learning about testing in Django?')
        self.assertEqual(poll_1.choice_set.count(), 2)
        choices = poll_1.choice_set.all()
        self.assertEqual(choices[0].choice, 'Yes')
        self.assertEqual(choices[0].votes, 1)
        self.assertEqual(choices[1].choice, 'No')
        self.assertEqual(choices[1].votes, 0)
    
    def test_detail(self):
        resp = self.client.get('/polls/1/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['poll'].pk, 1)
        self.assertEqual(resp.context['poll'].question, 'Are you learning about testing in Django?')
        
        # Ensure that non-existent polls throw a 404.
        resp = self.client.get('/polls/2/')
        self.assertEqual(resp.status_code, 404)
