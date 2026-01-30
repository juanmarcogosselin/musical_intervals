from django.db import models

# Create your models here.
class Interval(models.Model): 
    name = models.CharField(max_length= 4, null=False) 
    semitones = models.IntegerField() 

class AudioSample(models.Model):
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE)
    base_note = models.CharField(max_length=5)  
    audio_file = models.FileField(upload_to="audios/")
    