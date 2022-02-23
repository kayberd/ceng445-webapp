"""phase3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')) 
"""
from django.contrib import admin
from django.urls import path, include, re_path
from timetable import views

urlpatterns = [

    path('admin/', admin.site.urls),
    re_path(r'^signup/$', views.signup),
    re_path(r'^signin/$', views.signin),
    re_path(r'^logout/$', views.logout_req),

    # path('chat/', views.index, name='index'),
    # path('chat/<str:room_name>/', views.room, name='room'),

    path('', views.home),
    path('home/', views.home),
    

    re_path(r'get_tables/',views.get_tables),
    re_path(r'add_table/',views.add_table),
    re_path(r'del_table/',views.del_table),
    re_path(r'edit_table/',views.edit_table),
    re_path(r'copy_table/(?P<tid>[0-9]+)?',views.copy_table),


    re_path(r'get_rooms/(?P<tid>[0-9]+)?',views.get_rooms),
    re_path(r'add_room/(?P<tid>[0-9]+)?',views.add_room),
    re_path(r'delete_room/',views.delete_room),
    re_path(r'edit_room/',views.edit_room),

    re_path(r'get_sections/(?P<tid>[0-9]+)?',views.get_sections),
    re_path(r'add_section/(?P<tid>[0-9]+)?',views.add_section),
    re_path(r'delete_section/',views.delete_section),
    re_path(r'edit_section/',views.edit_section),

    re_path(r'get_people/(?P<tid>[0-9]+)?/(?P<sid>[0-9]+)/',views.get_people),
    re_path(r'add_person/(?P<tid>[0-9]+)?/(?P<sid>[0-9]+)/',views.add_person),
    re_path(r'delete_person/',views.delete_person),
    re_path(r'edit_person/(?P<sid>[0-9]+)/',views.edit_person),

    re_path(r'add_event/(?P<tid>[0-9]+)?',views.add_event),
    re_path(r'get_event/(?P<tid>[0-9]+)?',views.get_event),
    re_path(r'edit_event/',views.edit_event),
    re_path(r'delete_event/',views.delete_event),


    re_path(r'display_table/(?P<tid>[0-9]+)?/',views.display_table),
    re_path(r'table_view/(?P<tid>[0-9]+)?/',views.table_view),


]
