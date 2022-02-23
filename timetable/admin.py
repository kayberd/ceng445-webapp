from django.contrib import admin

from timetable.models import *

# Register your models here.
admin.site.register(TimeTable)
admin.site.register(Room)
admin.site.register(Section)
admin.site.register(Person)
admin.site.register(Event)
