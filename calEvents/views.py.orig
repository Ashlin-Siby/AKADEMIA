from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Entry
from .forms import EntryForm
import datetime

# Create your views here.


def getMonth():
    today = str(datetime.date.today())
    monthList = today.split('-')
    month_int = int(monthList[1])
    month = datetime.date(1900, month_int, 1).strftime('%B')
    return month[:3]




def index(request):
    month = getMonth()
    entries = Entry.objects.all()
    return render(request, 'calEvents.html', {'entries': entries, 'month': month})

def calEvents(request, month):
    entries = Entry.objects.all()

    return render(request, 'calEvents.html', {'entries': entries, 'month': month})


def details(request, pk):
    entry = Entry.objects.get(id=pk)
    return render(request, 'details.html', {'entry': entry})

def eventsToday(request, date, month):
    entries = Entry.objects.all()
    dateToday = date
    currentMonth = month
    return render(request, 'eventsToday.html', {'entries': entries, 'dateToday': dateToday, 'currentMonth': currentMonth})

def add(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']

            Entry.objects.create(
            name=name,
            date=date,
            description=description,
            ).save()
            return HttpResponseRedirect('/akademia/calEvents/')


    else:
        form = EntryForm()

    return render(request, 'form.html', {'form': form})


def delete(request, pk):

    if request.method == 'DELETE':
        entry = get_object_or_404(Entry, pk=pk)
        entry.delete()

    return HttpResponseRedirect('/')
