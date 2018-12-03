import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import  Choice, Poll, Vote
from .forms import ChoiceForm, PollForm, EditPollForm

# Create your views here.
@login_required
def polls_list(request):
    """
        renders polls_list.html which lists all available polls
    """
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls_list.html', context)

@login_required
def user_polls(request):
    curr_user = request.user
    polls = Poll.objects.filter(owner=curr_user)
    context = {'polls': polls}
    return render(request, 'user_polls.html', context)

@login_required
def add_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()
            new_choice1 = Choice(poll = new_poll,
                                 choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(poll = new_poll,
                                 choice_text=form.cleaned_data['choice2']).save()
            messages.success(request,
                             'New poll added!',
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:list')
    else:
        form = PollForm()
    form = PollForm()
    context = {'form': form}
    return render(request, 'add_poll.html', context)

@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        redirect('/')

    if request.method == "POST":
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Changes saved!',
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)

    return render(request, 'edit_poll.html', {'form': form, 'poll': poll})

@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        poll.delete()
        messages.success(request,
                         'Poll deleted!',
                         extra_tags='alert alert-success alert-dismissible fade show')
        return redirect('polls:list')
    return render(request, 'delete_poll_confirm.html', {'poll': poll})

@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
        return redirect('polls:edit_poll', poll_id=poll_id)
    else:
        form = ChoiceForm()
    return render(request, 'add_choice.html', {'form': form})

@login_required
def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
        return redirect('polls:edit_poll', poll_id=choice.poll.id)
    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'add_choice.html', {'form': form, 'edit_mode': True, 'choice': choice})

@login_required
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('/')
    if request.method == "POST":
        curr_poll = choice.poll.id
        choice.delete()
        return redirect('polls:edit_poll', poll_id=curr_poll)
    return render(request, 'delete_choice_confirm.html', {'choice': choice})

@login_required
def poll_detail(request, poll_id):
    """
        render poll
    """
    #poll = Poll.objects.get(id=poll_id)
    poll = get_object_or_404(Poll, id=poll_id)
    user_can_vote = poll.user_can_vote(request.user)
    results = poll.get_results_dict()
    context = {'poll': poll, 'user_can_vote': user_can_vote, 'results': results}
    return render(request, 'poll_detail.html', context)

@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.user_can_vote(request.user):
        messages.error(request, 'User already voted.')
        return redirect('polls:detail', poll_id=poll_id)

    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user, poll=poll, choice=choice)
        new_vote.save()
    else:
        messages.error(request, 'No choice was made.')
        return redirect('polls:detail', poll_id=poll_id)
    return redirect('polls:detail', poll_id=poll_id)
