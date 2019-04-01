from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.db.models import Sum

from .models import Candidate, Poll, Choice

# import datetime
from django.utils import timezone

# Create your views here.
def index(request):
    candidates = Candidate.objects.all()
    """
    str = ''
    for candidate in candidates:
        str += "<p>{} 기호 {}번 ({})<br>".format(candidate.name,
                                       candidate.party_number,
                                       candidate.area)

        str += candidate.introduction + "</p>"
    """

    context = {'candidates': candidates}

    # return HttpResponse(str)
    return render(request, 'elections/index.html', context)


def candidates(request, name):
    candidate = get_object_or_404(Candidate, name=name)
    # try:
    #     candidate = Candidate.objects.get(name=name)
    # except:
    #     # return HttpResponseNotFound("없는 페이지입니다.")
    #     raise Http404

    return HttpResponse(candidate.name)


def areas(request, area):
    today = timezone.now()
    try:
        poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today)
        candidates = Candidate.objects.filter(area=area)
    except:
        poll = None
        candidates = None

    context = {'candidates': candidates,
               'area': area,
               'poll': poll}

    # return HttpResponse(area)
    return render(request, 'elections/area.html', context)


def polls(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id=poll_id, candidate_id=selection)
        choice.votes += 1
        choice.save()
    except:
        choice = Choice(poll_id=poll_id, candidate_id=selection, votes=1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))


def results(request, area):
    candidates = Candidate.objects.filter(area=area)

    polls = Poll.objects.filter(area=area)
    poll_result = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']

        rates = []
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll_id=poll.id, candidate_id=candidate)
                rates.append(
                    round(choice.votes * 100 / result['total_votes'], 1))
            except:
                rates.append(0)
        result['rates'] = rates

        poll_result.append(result)

    context = {'candidates': candidates, 'area': area, 'poll_results': poll_result}

    return render(request, 'elections/result.html', context)
