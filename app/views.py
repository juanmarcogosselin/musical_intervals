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
    intervals = Interval.objects.all().order_by("semitones")

#correcto/incorrecto
    feedback = None
    #si hubo una peticion con el metodo POST (post es un diccionario) y hay contenido del tipo "answer"
    if request.method == "POST" and "answer" in request.POST: 
        answer_id = int(request.POST["answer"])
        correct_id = int(request.POST["correct_interval_id"])
        if answer_id == correct_id: 
            feedback = "Correcto"
        else: 
            correct_name = Interval.objects.get(id = correct_id).name
            feedback = f"Incorrecto. {correct_name}"
        
    interval = random.choice(list(Interval.objects.all()))
    nota1 = random.choice(list(Note.objects.exclude(audio_file__isnull=True)))   

    pitch2 = (nota1.pitch_class + interval.semitones) % 12
    nota2 = Note.objects.get(pitch_class = pitch2)

    context = {
        "nota1_audio": nota1.audio_file.url, 
        "nota2_audio": nota2.audio_file.url,
        "intervals" : intervals,
        "feedback" : feedback,

        "correct_interval_id" : interval.id, 
    }

    return render(request, "Exam.html", context)