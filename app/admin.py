from django.contrib import admin
from .models import Interval, Note, config

admin.site.register(Interval)
admin.site.register(Note)
admin.site.register(config)
# Register your models here.
