from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

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
    poll = get_object_or_404(Poll, id=poll_id)
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=poll_id)
        choice.votes += 1
        choice.save()
    else:
        messages.error(request, 'No choice was made.')
        return HttpResponseRedirect(reverse("polls:detail", args=(poll_id,)))
    return render(request, 'poll_results.html', {'poll': poll})
