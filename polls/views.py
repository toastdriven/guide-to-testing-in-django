from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from polls.forms import PollForm
from polls.models import Poll, Choice


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})


def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    form = PollForm(instance=p)
    return render_to_response('polls/detail.html', {'poll': p, 'form': form},
                               context_instance=RequestContext(request))


def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    
    if request.method == 'POST':
        form = PollForm(request.POST, instance=p)
        
        if form.is_valid():
            choice = form.cleaned_data['choice']
            choice.votes += 1
            choice.save()
            
            return HttpResponseRedirect(reverse('polls_results', kwargs={'poll_id': p.id}))
    else:
        form = PollForm(instance=p)
    
    return render_to_response('polls/detail.html', {
        'poll': p,
        'form': form,
    }, context_instance=RequestContext(request))
