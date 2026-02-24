import random
from django.shortcuts import render
from django.http import HttpResponse
from .models import Interval
# Create your views here.
def home(request): 
    return render(request, "Home.html")


def settings(request): 
    return render(request, "settings.html")

def exam(request): 
    intervals = Interval.objects.all().order_by("semitones")

#correcto/incorrecto
    feedback = None

    # intervalo anterior para el boton de repetir
    prev_root = None
    prev_second = None

    #si hubo una peticion con el metodo POST (post es un diccionario) y hay contenido del tipo "answer"
    if request.method == "POST" and "answer" in request.POST: 
        answer_id = int(request.POST["answer"])
        correct_id = int(request.POST["correct_interval_id"])
        if answer_id == correct_id: 
            feedback = "Correcto"
        else: 
            correct_name = Interval.objects.get(id = correct_id).name
            feedback = f"Incorrecto. {correct_name}"
            
        prev_root = request.POST.get("root_midi")
        prev_second = request.POST.get("second_midi")
    
        
    interval = random.choice(list(intervals))

    root_midi = random.randint(48, 72)
    
    second_midi = root_midi + interval.semitones


    context = {
        "root_midi": root_midi,
        "second_midi": second_midi, 
        "intervals" : intervals,
        "feedback" : feedback,
        "prev_root": prev_root,       
        "prev_second": prev_second,
        "correct_interval_id" : interval.id, 
    }

    return render(request, "Exam.html", context)