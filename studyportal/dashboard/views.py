from django.shortcuts import render,redirect
from .models import Notes
from .forms import *
from youtubesearchpython import VideosSearch 
import requests
from wikipedia import summary,WikipediaException
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')
@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            Notes(user=request.user,title=request.POST['title'],description=request.POST['description']).save()
    notes_queryset=Notes.objects.filter(user=request.user)
    form=NotesForm()
    return render(request,'dashboard/notes.html',{'notesQuerySet':notes_queryset,'form':form})
@login_required
def notes_detail(request,id):
    model_instance=Notes.objects.get(id=id)
    return render(request,'dashboard/notes_detail.html',{'modelInstance':model_instance})

@login_required
def delete_notes(request,id):
    model_instance=Notes.objects.get(id=id)
    model_instance.delete()
    return redirect('notes')
@login_required
def homework(request):
    if request.method=="POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
            Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],due=request.POST['due']).save()
    form=HomeworkForm()
    queryset=Homework.objects.filter(user=request.user)
    if len(queryset)==0:
        homework_done=True
    else:
        homework_done=False
    return render(request,'dashboard/homework.html',{'queryset':queryset,'homework_done':homework_done,'form':form})
@login_required
def update_homework(request,id=None):
    h=Homework.objects.get(id=id)
    if h.status==False:
        h.status=True
    else:
        h.status=False
    h.save()
    return redirect('homework')
@login_required
def delete_homework(request,id=None):
    h=Homework.objects.get(id=id)
    h.delete()
    return redirect('homework')

def youtube(request):
    if request.method=="POST":
        query=request.POST.get('query','')
        if query:
            videos=VideosSearch(query,limit=10)
            result_list=[]
            for i in videos.result()['result']:
                result_dict={
                    'input':query,
                    'title':i['title'],
                    'duration':i['duration'],
                    'thumbnails':i['thumbnails'][0]['url'],
                    'channel':i['channel']['name'],
                    'link':i['link'],
                    'views':i['viewCount']['short'],
                    'published':i['publishedTime'],
                    
                }
                desc=""
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc+=j['text']
                result_dict['description']=desc
                result_list.append(result_dict)
            return render(request, 'dashboard/youtube.html',{'results':result_list,'query':query})
        else:
            return render(request, 'dashboard/youtube.html',{'error':"bhai kuchh search to kar"})

    return render(request, 'dashboard/youtube.html')
@login_required
def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                status=request.POST['status']
                if status=="on":
                    status=True
                else:
                    status=False
            except:
                status=False
            Todo(user=request.user,title=request.POST['title'],status=status).save()
    else:
        form=TodoForm()
    queryset=Todo.objects.filter(user=request.user)
    if len(queryset)==0:
        todo_done=True
    else:
        todo_done=False
    return render(request,'dashboard/todo.html',{'queryset':queryset,'form':form,'todo_done':todo_done})
@login_required
def update_todo(request,id=None):
    model_instance=Todo.objects.get(id=id)
    if model_instance.status:
        model_instance.status=False
    else:
        model_instance.status=True
    model_instance.save()
    return redirect('todo')
@login_required
def delete_todo(request,id=None):
    Todo.objects.get(id=id).delete()
    return redirect('todo')

def books(request):
    if request.method=="POST":
        query=request.POST.get('query','')
        if query:
            url="https://www.googleapis.com/books/v1/volumes?q="+query
            response=requests.get(url)
            json_data=response.json()
            result_list=[]
            for i in range(10):
                result_dict={
                    'title':json_data['items'][i]['volumeInfo']['title'],
                    'subtitle':json_data['items'][i]['volumeInfo'].get('subtitle'),
                    'description':json_data['items'][i]['volumeInfo'].get('description'),
                    'count':json_data['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':json_data['items'][i]['volumeInfo'].get('categories'),
                    'rating':json_data['items'][i]['volumeInfo'].get('averageRating'),
                    'thumbnail':json_data['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':json_data['items'][i]['volumeInfo'].get('previewLink'),
                }

                result_list.append(result_dict)
            return render(request, 'dashboard/books.html',{'results':result_list,'query':query})
        else:
            return render(request, 'dashboard/books.html',{'error':"bhai kuchh search to kar ",'query':query})


    return render(request,'dashboard/books.html')

def dictionary(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        if query:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{query}"
            response = requests.get(url)
            json_data = response.json()
            
            if response.status_code == 200 and isinstance(json_data, list):
                try:
                    phonetics = json_data[0]['phonetics'][0].get('text', 'N/A')
                    audio = json_data[0]['phonetics'][0].get('audio', '')
                    definition = json_data[0]['meanings'][0]['definitions'][0].get('definition', 'N/A')
                    example = json_data[0]['meanings'][0]['definitions'][0].get('example', 'N/A')
                    synonyms = json_data[0]['meanings'][0]['definitions'][0].get('synonyms', [])
                    
                    context = {
                        'query': query,
                        'phonetics': phonetics,
                        'audio': audio,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms
                    }
                    
                    return render(request, 'dashboard/dictionary.html', context)
                except (IndexError, KeyError) as e:
                    return render(request, 'dashboard/dictionary.html', {'query': query, 'error': 'Data not found'})
            else:
                return render(request, 'dashboard/dictionary.html', {'query': query, 'error': 'Invalid response from API'})
        else:
            return render(request, 'dashboard/dictionary.html', {'query': query, 'error': 'Bhai tu pakka pagal hai'})
    return render(request, 'dashboard/dictionary.html',{'query':""})

def wikipedia(request):
    if request.method == "POST":
        query = request.POST.get('query', '')
        if query:
            try:
                result = summary(query)
                context = {'result': result, 'title': query}
            except WikipediaException as e:
                context = {'error': str(e), 'title': query}
        else:
            context = {'error': 'Query cannot be empty'}
        return render(request, 'dashboard/wikipedia.html', context)
    
    return render(request, 'dashboard/wikipedia.html')

def conversion(request):
    if request.method=="POST":
        # form=ConversionForm(request.POST)
        form=ConversionForm(request.POST)
        if request.POST.get('measurement')=="length":
            m_form=ConversionLengthForm()
            context={
                "form":form,
                "m_form":m_form,
                "input":True
            }
            if 'input_length' in request.POST:
                l=request.POST.get("input_length")
                i=request.POST.get("input_unit")
                o=request.POST.get("output_unit")
                answer=" "
                if float(l)>0:
                    if i=="metre" and o=="centi":
                        answer=f'{l}{i}={float(l)*100}{o}{i}'
                    if o=="metre" and i=="centi":
                        answer=f'{l}{i}{o}={float(l)/100}{o}'
                context={
                    "form":form,
                    "m_form":m_form,
                    "input":True,
                    "answer":answer
                }

        else:
            m_form=ConversionMassForm()
            context={
                "form":form,
                "m_form":m_form,
                "input":True
            }
            if 'input_mass' in request.POST:
                l=request.POST.get("input_mass")
                i=request.POST.get("input_unit")
                o=request.POST.get("output_unit")
                answer=" "
                if float(l)>=0:
                    if i=="gram" and o=="centi":
                        answer=f'{l}{i}={float(l)*100}{o}{i}'
                    if o=="gram" and i=="centi":
                        answer=f'{l}{i}{o}={float(l)/100}{o}'
                        
                context={
                    "form":form,
                    "m_form":m_form,
                    "input":True,
                    "answer":answer
                }

        
    else:
        form=ConversionForm()
        context={"form":form,"input":False}
    return render(request,'dashboard/conversion.html',context)

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            # in case of built in model  directly form.save()
            user=form.save()
            print("ok")

            # in case of userdefined model we save data in a model like this
            # username=form.cleaned_data['username']
            # email=form.cleaned_data['email']
            # password=form.cleaned_data['password1']
            # User(username=username, email=email, password=password).save()
            login(request,user)
            return redirect('home')
    form=RegisterForm()
    return render(request,"dashboard/register.html",{"form":form})
@login_required
def profile(request):
    todo_queryset=Todo.objects.filter(status=False,user=request.user)
    homework_queryset=Homework.objects.filter(status=False,user=request.user)
    if len(todo_queryset)==0:
        todo_done=True
    else:
        todo_done=False
    if len(homework_queryset)==0:
        homework_done=True
    else:
        homework_done=False
    
    return render(request,'dashboard/profile.html',{'todo':todo_queryset,'homework':homework_queryset,'todo_done':todo_done,"homework_done":homework_done})
def logoutview(request):
    logout(request)
    return redirect('register')