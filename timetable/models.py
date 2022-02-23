from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class TimeTable(models.Model):
    name = models.CharField(max_length=64)
    days = models.IntegerField()
    slotsPerDay = models.IntegerField()
    slotOffset = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_shared = models.BooleanField()

    def __str__(self):
        return self.name


class Room(models.Model):
    tableRoom = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.description


class Section(models.Model):
    courseId = models.IntegerField()
    tableSec = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    currSec = models.IntegerField()
    totSection = models.IntegerField()
    description = models.CharField(max_length=1024)
    instructor = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.description


class Person(models.Model):
    name = models.CharField(max_length=64)
    is_instructor = models.BooleanField()
    sectionPer = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    tablePer = models.ForeignKey(TimeTable, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Event(models.Model):
    tableEvent = models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='table')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section')
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    length = models.IntegerField()
    description = models.CharField(max_length=1024)
    day = models.IntegerField()
    slot_number = models.IntegerField()

    def __str__(self):
        return self.description
