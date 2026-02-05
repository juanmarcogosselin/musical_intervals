import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Interval, Note

# Create your views here.
def home(request): 
    return render(request, "Home.html")


def settings(request): 
    return render(request, "settings.html")

def exam(request): 

    semitones = random.randint(1,12)

    correct_interval = Interval.objects.get(semitones = semitones)
    intervals = Interval.objects.all().order_by('semitones')

    return render(request, "Exam.html", { 
        "intervals": intervals,
        "correct_interval": correct_interval.id, 
    })

