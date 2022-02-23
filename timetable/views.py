
import json
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse 
from django.shortcuts import render, redirect

from django.core import serializers

from timetable.forms import *
from timetable.models import *
from timetable.models import Person
from .utilities.Event import Event as EventObject
from .utilities.Person import Person as PersonObject
from .utilities.Room import Room as RoomObject
from .utilities.RoomList import RoomList as RoomListObject
from .utilities.Section import Section as SectionObject
from .utilities.TimeSlot import TimeSlot as TimeSlotObject
from .utilities.TimeTable import TimeTable as TimeTableObject


DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Sunday","Saturday"]



def signup(request:HttpRequest):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home/')

    return render(request, 'registration/signin.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        raw_password = request.POST.get("password")
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'registration/signin.html')


@login_required(None, None, "/signin/")
def logout_req(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/home/")



@login_required(None, None, "/signin/")
def display_table(request: HttpRequest,tid):

    ttable = TimeTable.objects.get(id=tid)
    if(ttable.user == request.user or ttable.is_shared):
    
        rooms    = Room.objects.filter(tableRoom_id=tid)
        sections = Section.objects.filter(tableSec_id=tid)
        events   = Event.objects.filter(tableEvent=tid)
        people   = Person.objects.filter(tablePer=tid)

        room_list_object = RoomListObject()
        

        for room in rooms:
            room_object = RoomObject(room.id, room.capacity, room.description)
            room_list_object.room_list.append(room_object)

        event_object_list = []
        all_student_objects = []
        all_instructor_objects = []

        for event in events:
            curr_section = sections.filter(id=event.section.id)[0]
            curr_instr = people.filter(id=curr_section.instructor.id)[0]

            if len(list(filter(lambda i: i.name == curr_instr.name, all_instructor_objects))) > 0:
                instr_object = list(filter(lambda i: i.name == curr_instr.name, all_instructor_objects))[0]
            else:
                instr_object = PersonObject(curr_instr.id, curr_instr.name)
                all_instructor_objects.append(instr_object)

            section_object = SectionObject(curr_section.courseId, curr_section.currSec, curr_section.totSection,
                                            curr_section.description, instr_object)
            students = people.filter(is_instructor=False, sectionPer=curr_section.id)
            curr_student_object_list = []
            for student in students:
                if len(list(filter(lambda s: s.name == student.name, all_student_objects))) > 0:
                    curr_student_object_list.append(
                        list(filter(lambda s: s.name == student.name, all_student_objects))[0])
                else:
                    student_object = PersonObject(student.id, student.name)
                    curr_student_object_list.append(student_object)
                    all_student_objects.append(student_object)

            section_object.addStudent(curr_student_object_list)

            event_object = EventObject(section_object, event.length, event.description)
            curr_room_object = list(filter(lambda r: r.id == event.room.id, room_list_object.room_list))[0]
            event_object.schedule(TimeSlotObject(event.day, event.slot_number), curr_room_object)
            event_object_list.append(event_object)

        timeTableObject = TimeTableObject(ttable.days, ttable.slotsPerDay, room_list_object, ttable.slotOffset)
        timeTableObject.addEvents(event_object_list)

        conflictReport = [timeTableObject.getConflicts().__str__()]
        context = [conflictReport,timeTableObject.str_html()]
        contextJSON = json.dumps(context)

        return HttpResponse(contextJSON,content_type='application/json')
    else:
        return HttpResponse(None)

   
def copy_table(request,tid):
    # Copy table part
    cloneTable = TimeTable.objects.get(pk=tid)
    cloneTable.pk = None
    cloneTable.save()
    TimeTable.objects.filter(pk=cloneTable.pk).update(name=TimeTable.objects.get(pk=tid).name + "-"+str(cloneTable.pk),user=request.user)

    # Copy Rooms Part
    cloneRooms = Room.objects.filter(tableRoom_id = tid)
    for cloneRoom in cloneRooms:
        cloneRoom.pk = None
        cloneRoom.save()
        Room.objects.filter(pk=cloneRoom.pk).update(description=cloneRoom.description+'-'+str(cloneTable.pk),tableRoom_id = cloneTable.id)

    cloneSections = Section.objects.filter(tableSec_id = tid)
    for cloneSection in cloneSections:
        cloneSection.pk = None
        cloneSection.save()
        Section.objects.filter(pk=cloneSection.pk).update(description=cloneSection.description+'-'+str(cloneTable.pk),tableSec_id = cloneTable.id)
        cloneSections = Section.objects.filter(tableSec_id = tid)

    clonePeople = Person.objects.filter(tablePer_id = tid)
    for clonePerson in clonePeople:
        clonePerson.pk = None
        clonePerson.save()
        Person.objects.filter(pk=clonePerson.pk).update(description=clonePerson.description+'-'+str(cloneTable.pk),tableSec_id = cloneTable.id)


    tableJSON = serializers.serialize('json',TimeTable.objects.filter(pk=cloneTable.id))    
    return HttpResponse(tableJSON,content_type='application/json')
    


@login_required(None, None, "/signin/")
def home(request):
    return render(request,'ttable/time_tables.html')

@login_required(None, None, "/signin/")
def table_view(request:HttpRequest,tid):
    
    table = TimeTable.objects.get(id=tid)
    if(request.user == table.user or table.is_shared):
        return render(request,'ttable/view.html',context={'tid':tid,'is_shared':table.is_shared})
    else:
        return render(request,'ttable/time_tables.html')

@login_required(None, None, "/signin/")
def get_tables(request:HttpRequest):
        tableQueryResult = TimeTable.objects.filter(user=request.user) | TimeTable.objects.filter(is_shared=True)
        tablesJSON = serializers.serialize('json',tableQueryResult)
        return HttpResponse(tablesJSON,content_type='application/json')
    

@login_required(None, None, "/signin/")  
def get_rooms(request:HttpRequest,tid):
    table = TimeTable.objects.get(pk=tid)
    if request.user == table.user or table.is_shared:
        roomQueryResult = Room.objects.filter(tableRoom_id=tid)
        roomsJSON = serializers.serialize('json',roomQueryResult)
        return HttpResponse(roomsJSON,content_type='application/json')
    else:
        return render(request,'ttable/time_tables.html')

@login_required(None, None, "/signin/")
def get_sections(request:HttpRequest,tid):
    table = TimeTable.objects.get(pk=tid)
    if request.user == table.user or table.is_shared:
        sectionQueryResult = Section.objects.filter(tableSec_id=tid)
        sectionsJSON = serializers.serialize('json',sectionQueryResult)
        return HttpResponse(sectionsJSON,content_type='application/json')
    else:
        return render(request,'ttable/time_tables.html')

    
@login_required(None, None, "/signin/")
def add_room(request,tid):
    table = TimeTable.objects.get(pk=tid)
    rr = request.POST
    if request.user == table.user:
        room = Room.objects.create(
            tableRoom=TimeTable.objects.get(id=tid),
            capacity=rr['capacity'],
            description=rr['description']
        )
        roomJSON = serializers.serialize('json',Room.objects.filter(id=room.id))    
        return HttpResponse(roomJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
   
@login_required(None, None, "/signin/")   
def add_section(request,tid):
    table = TimeTable.objects.get(pk=tid)
    sr = request.POST
    if request.user == table.user:
        try:
            section = Section.objects.create(
                tableSec=TimeTable.objects.get(id=tid),
                courseId=sr['courseId'],
                currSec=sr['currSec'],
                totSection=sr['totSection'],
                description=sr['description'],
                instructor=Person.objects.get(id=sr['instructor_id'])
            )
        except:
            section = Section.objects.create(
                tableSec=TimeTable.objects.get(id=tid),
                courseId=sr['courseId'],
                currSec=sr['currSec'],
                totSection=sr['totSection'],
                description=sr['description'],
                instructor=None

            )
        sectionJSON = serializers.serialize('json',Section.objects.filter(id=section.id))    
        return HttpResponse(sectionJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def add_table(request:HttpRequest):
    tt = request.POST
    #add case
    if not 'tid' in request.POST:
        ttable = TimeTable.objects.create(
            name=tt['name'],
            days=tt['days'],
            slotsPerDay=tt['slotsPerDay'],
            slotOffset=tt['slotOffset'],
            user=request.user,
            is_shared=False
        )
        tableJSON = serializers.serialize('json',TimeTable.objects.filter(pk=ttable.id))    
        return HttpResponse(tableJSON,content_type='application/json')
    
@login_required(None, None, "/signin/")
def edit_room(request):
    
    rr = request.POST
    roomCheck = Room.objects.get(id=rr['pk'])
    if request.user == roomCheck.tableRoom.user:
        room = Room.objects.filter(id=rr['pk']).update(
                capacity=rr['capacity'],
                description=rr['description']
            )
        roomJSON = serializers.serialize('json',Room.objects.filter(pk=rr['pk']))    
        return HttpResponse(roomJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def edit_section(request):
    sr = request.POST
    pk = int(sr['pk'])
    sectionCheck = Section.objects.get(id=pk)
    if request.user == sectionCheck.tableSec.user:
        try:
            section = Section.objects.filter(id=pk).update(
                    courseId=sr['courseId'],
                    currSec=sr['currSec'],
                    totSection=sr['totSection'],
                    description=sr['description'],
                    instructor=Person.objects.get(id=sr['instructor_id'])
                )
        except:
            
            section = Section.objects.filter(id=pk).update(
                courseId=sr['courseId'],
                currSec=sr['currSec'],
                totSection=sr['totSection'],
                description=sr['description'],
                instructor= None
            )
        sectionJSON = serializers.serialize('json',Section.objects.filter(pk=pk))    
        return HttpResponse(sectionJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')   
    
@login_required(None, None, "/signin/")
def delete_section(request):
    sid = request.POST['pk']
    sectionCheck = Section.objects.get(id=sid)
    if request.user == sectionCheck.tableSec.user:
        Section.objects.filter(id=sid).delete()
        return HttpResponse('SUCC')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def delete_room(request):
    rid = request.POST['pk']
    roomCheck = Room.objects.get(id=rid)
    if request.user == roomCheck.tableRoom.user:
        Room.objects.filter(id=rid).delete()
        return HttpResponse('SUCC')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")        
def del_table(request:HttpRequest):
    tid = int(request.POST.get('pk'))
    table = TimeTable.objects.get(pk=tid)
    if request.user == table.user:
        TimeTable.objects.filter(id=tid).delete()
        return HttpResponse('SUCC')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def edit_table(request:HttpRequest):
    tt = request.POST
    table = TimeTable.objects.get(pk=tt['pk'])
    if table.user == request.user:
        try:
            ttable = TimeTable.objects.filter(id=tt['pk']).update(
                name=tt['name'],
                days=tt['days'],
                slotsPerDay=tt['slotsPerDay'],
                slotOffset=tt['slotOffset'],
                user=request.user,
            )
        except:
            ttable = TimeTable.objects.filter(id=tt['pk']).update(
                is_shared=tt['is_shared']
            )
        tableJSON = serializers.serialize('json',TimeTable.objects.filter(pk=tt['pk']))    
        return HttpResponse(tableJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def get_people(request:HttpRequest,tid,sid):
    table=TimeTable.objects.get(id=tid)
    if table.user == request.user or table.is_shared:
        peopleQueryResult = Person.objects.filter(tablePer_id=tid,sectionPer_id=sid)
        peopleJSON = serializers.serialize('json',peopleQueryResult)
        return HttpResponse(peopleJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def add_person(request:HttpRequest,tid,sid):
    table=TimeTable.objects.get(id=tid)
    if table.user == request.user:
        pr = request.POST
        person = Person.objects.create(
            tablePer = TimeTable.objects.get(id=tid),
            sectionPer = Section.objects.get(id=sid),
            name = pr['name'],
            is_instructor = pr['is_instructor'] == 'Yes' if True else False,
        )

        if(person.is_instructor):
            Section.objects.filter(id=sid).update(instructor=person)

        personJSON = serializers.serialize('json',Person.objects.filter(id=person.id))    
        return HttpResponse(personJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def edit_person(request:HttpRequest,sid):
    pr = request.POST
    personQuerySet = Person.objects.filter(id=int(pr['pk']))
    person = personQuerySet[0]
    if person.tablePer.user == request.user:
        personQuerySet.update(
            name = pr['name'],
            is_instructor = pr['is_instructor'] == 'Yes' if True else False,
        )
        personQuerySet = Person.objects.filter(id=int(pr['pk']))
        person = personQuerySet[0]
        if(person.is_instructor):
            Section.objects.filter(id=sid).update(instructor=person)
            instr = Section.objects.get(id=sid).instructor
            

        personJSON = serializers.serialize('json',Person.objects.filter(id=person.id))    
        return HttpResponse(personJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def delete_person(request:HttpRequest):
    pid = request.POST['pk']
    person = Person.objects.get(id=pid)
    if person.tablePer.user == request.user:
        Person.objects.filter(id=pid).delete()
        return HttpResponse('SUCC')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def add_event(request:HttpRequest,tid):
    er = request.POST
    table = TimeTable.objects.get(id=tid)
    if(table.user == request.user):
        event = Event.objects.create(
                tableEvent=TimeTable.objects.get(id=tid),
                section=Section.objects.get(description=er['section']),
                room=Room.objects.get(description=er['room']),
                length=er['length'],
                day=er['day'],
                slot_number=er['slot_number'],
                description=er['description']
            )

        eventJSON = serializers.serialize('json',Event.objects.filter(id=event.id))    
        return HttpResponse(eventJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')

    
@login_required(None, None, "/signin/")
def edit_event(request:HttpRequest):
    er = request.POST
    eventCheck = Event.objects.get(id=er['pk'])
    if eventCheck.tableEvent.user == request.user:
        Event.objects.filter(id=er['pk']).update(
                section = Section.objects.get(description=er['section']),
                room = Room.objects.get(description=er['room']),
                length = er['length'],
                description = er['description'],
            )
        eventJSON = serializers.serialize('json',Event.objects.filter(pk=er['pk']))    
        return HttpResponse(eventJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def delete_event(request:HttpRequest):
    eid = request.POST['pk']
    eventCheck = Event.objects.get(id=eid)
    if eventCheck.tableEvent.user == request.user:
        Event.objects.filter(id=eid).delete()
        return HttpResponse('SUCC')
    else:
        return HttpResponse(None,content_type='application/json')
    
@login_required(None, None, "/signin/")
def get_event(request:HttpRequest,tid):
    er = request.POST
    event=Event.objects.filter(description=er['description']).filter(tableEvent_id=tid)
    eventCheck = event[0]
    if eventCheck.tableEvent.user == request.user:
        eventJSON = serializers.serialize('json',Event.objects.filter(id=event[0].id))    
        return HttpResponse(eventJSON,content_type='application/json')
    else:
        return HttpResponse(None,content_type='application/json')









@login_required(None, None, "/signin/")
def person(request: HttpRequest, pid=None):
    if request.user:
        if request.POST:
            tid = request.POST.get('tid')
            sid = request.POST.get('sid')

            if request.POST.get('insert'):
                pForm = PersonForm()
                operation = 'insert'
                return render(request, 'person/update.html',
                              {'pid': pid, 'tid': tid, 'sid': sid, 'form': pForm, 'operation': operation})


            elif request.POST.get('update'):
                person = Person.objects.get(id=pid)
                pForm = PersonForm(
                    {
                        'name': person.name,
                        'is_instructor': person.is_instructor
                    }
                )
                operation = 'update'
                return render(request, 'person/update.html',
                              {'pid': pid, 'tid': tid, 'sid': sid, 'form': pForm, 'operation': operation})


            elif request.POST.get('delete'):
                Person.objects.filter(id=pid).delete()
                return redirect(f"/section/{sid}/")
        else:
            person = Person.objects.get(id=pid)
            return render(request, 'person/view.html', {'person': person, 'pid': pid})


@login_required(None, None, "/signin/")
def person_post(request, tid, sid):
    pr = request.POST
    if 'insert' in request.POST:
        try:
            person = Person.objects.create(
                tablePer=TimeTable.objects.get(id=tid),
                sectionPer=Section.objects.get(id=sid),
                name=pr['name'],
                is_instructor=pr['is_instructor'] == 'on'
            )
            Section.objects.filter(id=person.sectionPer_id).update(
                instructor = person
            )
        except:
            person = Person.objects.create(
                tablePer=TimeTable.objects.get(id=tid),
                sectionPer=Section.objects.get(id=sid),
                name=pr['name'],
                is_instructor=False)

        return redirect(f"/section/{sid}/")

    elif 'update' in request.POST:
        try:
            person = Person.objects.filter(id=pr['pid']).update(
                name=pr['name'],
                is_instructor=pr['is_instructor'] == 'on'
            )
            Section.objects.filter(id=person.sectionPer_id).update(
                instructor = person
            )
        except:
            person = Person.objects.filter(id=pr['pid']).update(
                name=pr['name'],
                is_instructor=False
            )
        return redirect(f"/section/{sid}/")

    else:
        return redirect(f"/section/{sid}/")


@login_required(None, None, "/signin/")
def event(request: HttpRequest, eid=None):
    if request.user:
        if request.POST:
            tid = request.POST.get('tid')
            if request.POST.get('insert'):

                evForm = EventForm()
                evForm.fields['section'].queryset = (Section.objects.filter(tableSec=tid))
                evForm.fields['room'].queryset = Room.objects.filter(tableRoom_id=tid)

                operation = 'insert'
                return render(request, 'event/update.html',
                              {'eid': eid, 'tid': tid, 'form': evForm, 'operation': operation})


            elif request.POST.get('update'):
                event = Event.objects.get(id=eid)
                evForm = EventForm(
                    {
                        'section': event.section,
                        'room': event.room,
                        'length': event.length,
                        'day': event.day,
                        'slot_number': event.slot_number,
                        'description': event.description

                    }
                )
                evForm.fields['section'].queryset = (Section.objects.filter(tableSec_id=tid))
                evForm.fields['room'].queryset = Room.objects.filter(tableRoom_id=tid)
                operation = 'update'
                return render(request, 'event/update.html',
                              {'eid': eid, 'tid': tid, 'form': evForm, 'operation': operation})


            elif request.POST.get('delete'):
                event = Event.objects.filter(id=eid).delete()
                return redirect(f"/ttable/{tid}/")
        else:
            event = Event.objects.get(id=eid)
            return render(request, 'event/view.html', {'event': event, 'eid': eid})


    else:
        print("eid error")


@login_required(None, None, "/signin/")
def event_post(request, tid):
    er = request.POST
    if 'insert' in request.POST:
        event = Event.objects.create(
            tableEvent=TimeTable.objects.get(id=tid),
            section=Section.objects.get(id=er['section']),
            room=Room.objects.get(id=er['room']),
            length=er['length'],
            day=er['day'],
            slot_number=er['slot_number'],
            description=er['description']
        )
        return redirect(f"/ttable/{tid}/")

    elif 'update' in request.POST:
        event = Event.objects.filter(id=er['eid']).update(
            tableEvent=TimeTable.objects.get(id=tid),
            section=Section.objects.get(id=er['section']),
            room=Room.objects.get(id=er['room']),
            length=er['length'],
            day=er['day'],
            slot_number=er['slot_number'],
            description=er['description']
        )
        return redirect(f"/ttable/{tid}/")

    else:
        return redirect(f"/ttable/{tid}/")


