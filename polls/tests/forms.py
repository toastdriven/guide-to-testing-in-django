from django.test import TestCase
from polls.forms import PollForm
from polls.models import Poll, Choice


class PollFormTestCase(TestCase):
    fixtures = ['polls_forms_testdata.json']
    
    def setUp(self):
        super(PollFormTestCase, self).setUp()
        self.poll_1 = Poll.objects.get(pk=1)
        self.poll_2 = Poll.objects.get(pk=2)
    
    def test_init(self):
        # Test successful init without data.
        form = PollForm(instance=self.poll_1)
        self.assertTrue(isinstance(form.instance, Poll))
        self.assertEqual(form.instance.pk, self.poll_1.pk)
        self.assertEqual([c for c in form.fields['choice'].choices], [(1, u'Yes'), (2, u'No')])
        
        # Test successful init with data.
        form = PollForm({'choice': 3}, instance=self.poll_2)
        self.assertTrue(isinstance(form.instance, Poll))
        self.assertEqual(form.instance.pk, self.poll_2.pk)
        self.assertEqual([c for c in form.fields['choice'].choices], [(3, u'Alright.'), (4, u'Meh.'), (5, u'Not so good.')])
        
        # Test a failed init without data.
        self.assertRaises(KeyError, PollForm)
        
        # Test a failed init with data.
        self.assertRaises(KeyError, PollForm, {})
    
    def test_save(self):
        self.assertEqual(self.poll_1.choice_set.get(pk=1).votes, 1)
        self.assertEqual(self.poll_1.choice_set.get(pk=2).votes, 0)
        
        # Test the first choice.
        form_1 = PollForm({'choice': 1}, instance=self.poll_1)
        form_1.save()
        self.assertEqual(self.poll_1.choice_set.get(pk=1).votes, 2)
        self.assertEqual(self.poll_1.choice_set.get(pk=2).votes, 0)
        
        # Test the second choice.
        form_2 = PollForm({'choice': 2}, instance=self.poll_1)
        form_2.save()
        self.assertEqual(self.poll_1.choice_set.get(pk=1).votes, 2)
        self.assertEqual(self.poll_1.choice_set.get(pk=2).votes, 1)
        
        # Test the other poll.
        self.assertEqual(self.poll_2.choice_set.get(pk=3).votes, 1)
        self.assertEqual(self.poll_2.choice_set.get(pk=4).votes, 0)
        self.assertEqual(self.poll_2.choice_set.get(pk=5).votes, 0)
        
        form_3 = PollForm({'choice': 5}, instance=self.poll_2)
        form_3.save()
        self.assertEqual(self.poll_2.choice_set.get(pk=3).votes, 1)
        self.assertEqual(self.poll_2.choice_set.get(pk=4).votes, 0)
        self.assertEqual(self.poll_2.choice_set.get(pk=5).votes, 1)
