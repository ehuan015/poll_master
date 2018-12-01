from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Poll, Choice

# Create your views here.
def polls_list(request):
    """
        renders polls_list.html which lists all available polls
    """
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls_list.html', context)

def poll_detail(request, poll_id):
    """
        render poll
    """
    #poll = Poll.objects.get(id=poll_id)
    poll = get_object_or_404(Poll, id=poll_id)
    context = {'poll': poll}
    return render(request, 'poll_detail.html', context)

def poll_vote(request, poll_id):
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=poll_id)
        poll = choice.question
        choice.votes += 1
        choice.save()
        return render(request, 'poll_results.html', {'poll': poll})
    return render(request, 'poll_results.html', {'error': True})
