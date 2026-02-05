from django.db import models

# Create your models here.
class Interval(models.Model): 
    name = models.CharField(max_length= 10, null=False) 
    semitones = models.IntegerField() 

class Note(models.Model): 
    name = models.CharField(max_length=5)
    pitch_class = models.PositiveSmallIntegerField()
    audio_file = models.FileField(upload_to="audio/intervals/", null=True)


class config(models.Model): 
    num_preguntas = models.IntegerField()
    direccion = models.CharField(max_length = 1, null = False)
