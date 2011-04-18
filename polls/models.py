import datetime
from django.db import models


class PollManager(models.Manager):
    def get_query_set(self):
        now = datetime.datetime.now()
        return super(PollManager, self).get_query_set().filter(pub_date__lte=now)


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now)
    
    objects = models.Manager()
    published = PollManager()
    
    def __unicode__(self):
        return self.question
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.choice
    
    def record_vote(self):
        self.votes += 1
        self.save()
