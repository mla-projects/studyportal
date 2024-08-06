from . import views
from django.urls import path
urlpatterns = [
    path('', views.home,name="home"),
    path('notes', views.notes, name='notes'),
    path('notes_detail/<int:id>', views.notes_detail, name='notes_detail'),
    path('delete_notes/<int:id>', views.delete_notes, name='delete_notes'),
    path('homework',views.homework,name='homework'),
    path('update_homework/<int:id>',views.update_homework,name='update_homework'),
    path('delete_homework/<int:id>',views.delete_homework,name='delete_homework'),
    path('youtube/',views.youtube,name='youtube'),
    path('todo/',views.todo,name='todo'),
    path('update_todo/<int:id>',views.update_todo,name='update_todo'),
    path('delete_todo/<int:id>',views.delete_todo,name='delete_todo'),
    path('books',views.books,name='books'),
    path('dictionary',views.dictionary,name='dictionary'),
    path('wikipedia',views.wikipedia,name='wikipedia'),
    path('conversion',views.conversion,name='conversion'),

]