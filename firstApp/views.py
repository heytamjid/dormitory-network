from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from datetime import datetime
from .forms import *



def landing(request):
    return render(request, "firstApp/landing.html")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')  
    else:
        form = SignUpForm()
    return render(request, 'firstApp/signup.html', {'form': form})


def loginFunc(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace 'home' with the URL you want to redirect to after login
    else:
        form = LoginForm()
    return render(request, 'firstApp/login.html', {'form': form})

@login_required
def logoutFunc(request):
    logout(request)
    return redirect('landing') 

@login_required
def dashboard (request):
    context =  {
        'courses': Course.objects.filter(user = request.user).all(),
        'topics': Topic.objects.filter(user = request.user, course = None ).all(), #Note, not ==. also user & course are fields of Topic model
        'username' : request.user.username, 
    }
    return render (request, 'firstApp/dashboard.html', context)

@login_required
def getTopics (request):
    course = request.GET.get('courseSelect') #see how htmx also sends form/select data from frontend to backend #get the selected course id (most probably primary key number) from the request #courseSelect is the name of the select tag in the dashboard.html
    print("Selected Course:", course)
    topics = Topic.objects.filter(course=course) #note not ==. course is a field of Topic model.
    context = {'topics': topics}
    return render(request, 'partials/topics.html', context)

@login_required
def addCourse (request):
    if request.method == 'POST':
        form = CourseForm(request.POST) #initializes a CourseForm instance with the data contained in the POST request. It binds the form data to the form so that it can be validated.
        if form.is_valid(): # checks if the form data is valid based on the constraints defined in the CourseForm class
            course = form.save(commit=False) #If the form data is valid, this line creates a Course object using the form data, but it doesn't save it to the database yet (commit=False). This allows you to make any additional changes to the object before saving it.
            course.user = request.user  # Assign the logged-in user to the course
            course.save() #save it to db finally
            return redirect('dashboard')  
    else:
        form = CourseForm()
    return render(request, 'firstApp/newCourse.html', {'form': form})


@login_required
def addTopic (request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user 
            topic.save()
            return redirect('dashboard') #named url?
    else:
        form = TopicForm()
    return render(request, 'firstApp/newTopic.html', {'form': form}) #relative url? as settings.py has TEMPLATES = [ {'DIRS': [],'APP_DIRS': True ] so it will look for the template in the root/appFolder (as APP_DIRS is enabled)/templates (auto?)/appName (given)/ html file (given). 
    
    

    
@login_required
def start_timer(request):
    start_time = timezone.now()
    request.session['start_time'] = start_time.timestamp() #user refresh dile ki memory leak hobe??
    print("LETS PRINT ITTTTTTTTTTTTTT")
    print(request.session['start_time'])
    selectedCourse = request.GET.get('selectedCourse') 
    print("Selected Courseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee:", selectedCourse)
    return HttpResponse("<button type='submit' id='endTimerButton'  hx-vals='js:{selectedCourse : document.getElementById(&#39;storedata&#39;).dataset.selectedCourse}' hx-trigger='click' hx-get='/endTimerClicked/' hx-target='#endTimerButton' hx-swap='outerHTML'>  Stop Tracking </button>")
    #note the &#39; is used to escape the single quote in the string. It is used because the string is enclosed in single quotes. If the string was enclosed in double quotes, then we would have used &quot; to escape the double quote.
    #also single quote is typically  used inside doulbe quote
    #also json format must be in double quote. so we can't use double quote inside double quote. so we use single quote inside double quote.

@login_required
def stop_timer(request):
    end_time = timezone.now().timestamp()
    start_time = request.session['start_time']
    duration = (end_time - start_time)
    
    
    selectedCourse = request.GET.get('selectedCourse') 
    print("Selected Courseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee:", selectedCourse)

    #TrackedTimeDB te UTC+0 onujayi save ache time. User er timezoneinfo onujayi +- kore user ke show korte hobe
    TrackedTimeDB.objects.create(user=request.user, startTime=datetime.fromtimestamp(start_time), endTime=datetime.fromtimestamp(end_time), duration=timezone.timedelta(seconds=duration))
    del request.session['start_time']
    
    
    htmlcontent = "<button  type='submit' id='startTimerButton' hx-get='/startTimerClicked/' hx-target='#startTimerButton' hx-swap='outerHTML'> Start Tracking </button>"
    response = HttpResponse(htmlcontent)
    response['HX-Trigger'] = 'renderEntryzz' # upon receiving the response, it (the response) will trigger that [<div id = "trackedTime" hx-select="#onlyEntries2" hx-get="/endTimerClicked/renderEntry/" hx-trigger="renderEntryzz from:body">] in dashboard.html, which (that div) will then make a get request to /endTimerClicked/renderEntry/ and replace the content of itself with the response of that get request to the /endTimerClicked/renderEntry/ endpoint
    #https://chat.openai.com/share/873634e8-2731-47a5-af00-c9fb598beb2e


    return response


@login_required
def renderEntry (request):
    
    user = myUserDB.objects.get(username = request.user)
    last_10_entries = TrackedTimeDB.objects.filter(user=user).order_by('-startTime')[:10]
    
    # for entry in last_10_entries:
    #     localized_start_time = timezone.localtime(entry.startTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M')
    #     localized_end_time = timezone.localtime(entry.endTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M')
    #     duration_hours, duration_minutes = divmod(entry.duration.total_seconds() // 60, 60)   
             
    #     print("Start Time:", localized_start_time)
    #     print("End Time:", localized_end_time)
    #     print("Duration: {} hours {} minutes".format(int(duration_hours), int(duration_minutes)))
    #     print()
    #querying refference:  https://chat.openai.com/share/4eb58c3c-4539-404f-982b-75bb5b4d2900  
    
    entries_data_modified_from_backend = []
    for entry in last_10_entries:
        localized_start_time = timezone.localtime(entry.startTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')
        localized_end_time = timezone.localtime(entry.endTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')

        total_seconds = entry.duration.total_seconds()
        duration_hours, remaining_seconds = divmod(total_seconds, 3600)
        duration_minutes, duration_seconds = divmod(remaining_seconds, 60)        
        
        # Append entry data to the list
        entries_data_modified_from_backend.append({
            'start_time': localized_start_time,
            'end_time': localized_end_time,
            'duration_hours': int(duration_hours),
            'duration_minutes': int(duration_minutes),
            'duration_seconds' : int(duration_seconds)
        })

    context = {
        'readyEntries': entries_data_modified_from_backend
    }  
    
    
    return render(request, 'firstApp/entries.html', context)
