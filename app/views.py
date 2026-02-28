import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Interval
# Create your views here.
def home(request): 
    return render(request, "Home.html")


def settings(request): 
    if request.method == 'POST':
        num = request.POST.get('questions')
        request.session['num_questions']= int(num) if num != '' else 10
        request.session['direction'] = request.POST.get('direction', 'ascending')
        return redirect('exam')
    
    context = {
        'num_questions': request.session.get('num_questions', 10),
        'direction': request.session.get('direction', 'ascending')
    }
    return render(request, "settings.html", context)

def exam(request): 
    intervals = Interval.objects.all().order_by("semitones")

    direction = request.session.get('direction', 'ascending')

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

    direction = request.session.get('direction', 'ascending')
    print("DIRECTION DESDE SESIÓN:", direction)
    
    if direction == 'mixed':
        actual_direction = random.choice(['ascending', 'descending', 'harmonic'])
    else: 
        actual_direction = direction

    if actual_direction == 'descending':
        second_midi = root_midi - interval.semitones
    else:
        second_midi = root_midi + interval.semitones
 


    context = {
        "root_midi": root_midi,
        "second_midi": second_midi, 
        "intervals" : intervals,
        "feedback" : feedback,
        "prev_root": prev_root,       
        "prev_second": prev_second,
        "correct_interval_id" : interval.id, 
        "direction" : actual_direction, 
    }

    return render(request, "Exam.html", context)