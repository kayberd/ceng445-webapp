from django import forms
from django.contrib.auth.forms import UserCreationForm

from timetable.models import Person, Room, Section


class TimeTableForm(forms.Form):
    name = forms.CharField(
        label='Table Name',
        max_length=64,
        required=True
    )

    days = forms.IntegerField(
        label='Days',
        min_value=1,
        required=True
    )
    slotsPerDay = forms.IntegerField(
        label='Slots Per Day',
        min_value=1,
        required=True
    )
    slotOffset = forms.IntegerField(
        label='Slot Offset',
        min_value=1,
        required=True
    )

    is_shared = forms.BooleanField(label='is_shared', required=False)


class RoomForm(forms.Form):
    capacity = forms.IntegerField(
        label='Capacity',
        min_value=1,
        required=True
    )
    description = forms.CharField(
        label='Description',
        max_length=1024,
        required=False
    )


class SectionForm(forms.Form):
    courseId = forms.IntegerField(
        label='Course ID',
        min_value=1,
        required=True
    )
    currSec = forms.IntegerField(
        label='Current Section',
        min_value=1,
        required=True
    )
    totSection = forms.IntegerField(
        label='Total Section',
        min_value=1,
        required=True
    )
    description = forms.CharField(
        label='Description',
        max_length=1024,
        required=False
    )
    instructor_id = forms.ModelChoiceField(queryset=Person.objects.all(), required=False)


class PersonForm(forms.Form):
    name = forms.CharField(
        label='Person Name',
        max_length=64,
        required=True
    )
    is_instructor = forms.BooleanField(label='is Instructor', required=False, initial=False)


class EventForm(forms.Form):
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=True)
    room = forms.ModelChoiceField(queryset=Room.objects.all(), required=True)
    length = forms.IntegerField(label="Length", required=True)
    day = forms.IntegerField(label="Day", required=True)
    slot_number = forms.IntegerField(label="Slot Number", required=True)
    description = forms.CharField(label='Description', max_length=1024, required=False)


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
