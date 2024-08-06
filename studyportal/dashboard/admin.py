from django.contrib import admin
from . import models

# # Register your models here.
@admin.register(models.Notes)
class NotesAdmin(admin.ModelAdmin):
    display_lst=['user','title','description']
@admin.register(models.Homework)
class HomeworkAdmin(admin.ModelAdmin):
    display_lst=['user','subject','title','description','due','status']
@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    display_lst=['user','title','status']
