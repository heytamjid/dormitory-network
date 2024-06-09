from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from datetime import datetime
from .forms import *
import plotly.express as px
import pandas as pd
from datetime import timedelta
import plotly.graph_objects as go
from django.db.models import F, Sum, DurationField, ExpressionWrapper
from django.db.models.functions import TruncDate




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
    course = request.GET.get('courseSelect') #see how htmx also sends form/select key-values automatically from frontend to backend #course will store the selected course id (primary key number) (not sure as int or str) #courseSelect is the name of the select tag in the dashboard.html
    print("SSSSelected Course:", course)
    if (course != ''):
        topics = Topic.objects.filter(course=course).all() #note not ==. # LHS course is a field of the Topic model, RHS course is the selected course's primary key. #https://pastebin.com/zqQeXv84
    else:
        topics = Topic.objects.filter(user = request.user, course = None ).all() #Note querying on multiple conditions #in many cases omitting .all() will still work because Django will 'lazily' evaluate the queryset when necessary
    #topics is defined in both the if and else branches of the if-else statement. Therefore, it can be accessed outside the if-else block without any issues.
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
    return HttpResponse("<button type='submit' id='endTimerButton'  hx-vals='js:{selectedCourse : document.getElementById(&#39;courseSelect&#39;).value, selectedTopic : document.getElementById(&#39;topicSelect&#39;).value, selectedDescription : document.getElementById(&#39;sessionDescription&#39;).value}' hx-trigger='click' hx-get='/endTimerClicked/' hx-target='#endTimerButton' hx-swap='outerHTML' class='text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l focus:ring-4 focus:outline-none focus:ring-purple-200 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2'>  Stop Tracking </button>")
    #note the &#39; is used to escape the single quote in the string. It is used because the string is enclosed in single quotes. If the string was enclosed in double quotes, then we would have used &quot; to escape the double quote.
    #also single quote is typically  used inside doulbe quote
    #also json format must be in double quote. so we can't use double quote inside double quote. so we use single quote inside double quote.
    # JSON could be string, number, object, array, true, false, null. But it can't be a function or evaluatable variable. To evaluate them use js as mentioned here https://htmx.org/attributes/hx-vals/ or use https://htmx.org/attributes/hx-vars/ that is dynamically computed.

@login_required
def stop_timer(request):
    end_time = timezone.now().timestamp()
    start_time = request.session['start_time']
    duration = (end_time - start_time)
    
    
    selectedCourse = request.GET.get('selectedCourse') 
    print("Selected Course:", selectedCourse)
    selectedTopic = request.GET.get('selectedTopic') #so we just got the value - which is defined as primary key or '' in the html file. #selectedTopic is the name of the select tag in the dashboard.html
    
    
    print("Selected Topic:", selectedTopic)
    #so primary key for each table or model is started from 1 to infinity at its own table. So, if we want to save the selected course and topic in the TrackedTimeDB model, we need to get the primary key of the selected course and topic.
    #problem: deal with unselected course that should show up as None in the database. Also deal with unselected topic that should show up as None in the database..
    #problem: when course is back to unselected in frontend, topics NOT associated with any course should show up in the topic dropdown.
    selectedDescription = request.GET.get('selectedDescription')
    print("Selected Description:", selectedDescription)   
    
    
    #TrackedTimeDB te UTC+0 onujayi save ache time. User er timezoneinfo onujayi +- kore user ke show korte hobe
    newTrackedTimeInstance = TrackedTimeDB(
        user=request.user, 
        startTime=datetime.fromtimestamp(start_time), 
        endTime=datetime.fromtimestamp(end_time), 
        duration=timezone.timedelta(seconds=duration), 
        course = Course.objects.get(pk = selectedCourse) if (selectedCourse!='') else None,
        topic = Topic.objects.get(pk = selectedTopic) if (selectedTopic!='') else None,  #ternary operator. #RHS e both are topic instances.
        #modelName.objects.get(pk) gets you an instance whereas modelName.objects.filter(pk) gets you a queryset 
        session = selectedDescription
    )
    newTrackedTimeInstance.save()

    #Oldline of code with modelName.objects.create() #TrackedTimeDB.objects.create(user=request.user, startTime=datetime.fromtimestamp(start_time), endTime=datetime.fromtimestamp(end_time), duration=timezone.timedelta(seconds=duration), topic = Topic.objects.get(pk = selectedTopic) if (selectedTopic!='NONE') else None, session = selectedDescription) 
    
    del request.session['start_time']
    
    
    htmlcontent = "<button  type='submit' id='startTimerButton' hx-get='/startTimerClicked/' hx-target='#startTimerButton' hx-swap='outerHTML' class='text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-2'> Start Tracking </button>"
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
    
    entries_data_modified_from_backend = [] #list. ordered list. indexing. mutable. different types of data. []
    for entry in last_10_entries:
        localized_start_time = timezone.localtime(entry.startTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')
        localized_end_time = timezone.localtime(entry.endTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')

        total_seconds = entry.duration.total_seconds()
        duration_hours, remaining_seconds = divmod(total_seconds, 3600)
        duration_minutes, duration_seconds = divmod(remaining_seconds, 60)  
                
        # Append entry data to the list
        entries_data_modified_from_backend.append ({ #so it is a list of dictionary!
            'start_time': localized_start_time,
            'end_time': localized_end_time,
            'duration_hours': int(duration_hours),
            'duration_minutes': int(duration_minutes),
            'duration_seconds' : int(duration_seconds),
            'course_id': 0 if entry.course is None else entry.course.id,
            'topic_id': 0 if entry.topic is None else entry.topic.id,
            'course' : 'Unselected Course' if entry.course is None else entry.course.name, #Old code when trackedtimedb used to have only topic foreign key, and course was evaluated according to topic #'Unselected Course' if (entry.topic is None) else      'Unselected Course' if (entry.topic.course is None) else entry.topic.course.name, #condition validating.
            'topic': 'Unselected Topic' if entry.topic is None else entry.topic.name, #condition validating
            'session': entry.session,
        })

    context = { #dictionary. unordered. key-value pairs. immutable. same type of data. {} 
               #so we passed a list (of dictionaries) that is turned into value of a dictionary key (namely 'renderEntries')
               #so in the front end, we have to loop through the list (the dictionary value) to get the data of each entry. Note that each value itself will be a dictionary. 
        'readyEntries': entries_data_modified_from_backend
    }  
    
    
    return render(request, 'firstApp/entries.html', context)


@login_required
def renderEntrybyCourse (request, pk):
    
    user = myUserDB.objects.get(username = request.user)
    last_10_entries = TrackedTimeDB.objects.filter(user=user, course=pk).order_by('-startTime')[:10]
    
    entries_data_modified_from_backend = [] #list. ordered list. indexing. mutable. different types of data. []
    for entry in last_10_entries:
        localized_start_time = timezone.localtime(entry.startTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')
        localized_end_time = timezone.localtime(entry.endTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')

        total_seconds = entry.duration.total_seconds()
        duration_hours, remaining_seconds = divmod(total_seconds, 3600)
        duration_minutes, duration_seconds = divmod(remaining_seconds, 60)  
                
        # Append entry data to the list
        entries_data_modified_from_backend.append ({ #so it is a list of dictionary!
            'start_time': localized_start_time,
            'end_time': localized_end_time,
            'duration_hours': int(duration_hours),
            'duration_minutes': int(duration_minutes),
            'duration_seconds' : int(duration_seconds),
            'course' : 'Unselected Course' if entry.course is None else entry.course.name, #Old code when trackedtimedb used to have only topic foreign key, and course was evaluated according to topic #'Unselected Course' if (entry.topic is None) else      'Unselected Course' if (entry.topic.course is None) else entry.topic.course.name, #condition validating.
            'course_id': 0 if entry.course is None else entry.course.id,
            'topic_id': 0 if entry.topic is None else entry.topic.id,
            'topic': 'Unselected Topic' if entry.topic is None else entry.topic.name, #condition validating
            'session': entry.session,
        })

    context = { #dictionary. unordered. key-value pairs. immutable. same type of data. {} 
               #so we passed a list (of dictionaries) that is turned into value of a dictionary key (namely 'renderEntries')
               #so in the front end, we have to loop through the list (the dictionary value) to get the data of each entry. Note that each value itself will be a dictionary. 
        'readyEntries': entries_data_modified_from_backend
    }  
    
    
    return render(request, 'firstApp/entries.html', context)



@login_required
def renderEntrybyTopic (request, pk):
    
    user = myUserDB.objects.get(username = request.user)
    last_10_entries = TrackedTimeDB.objects.filter(user=user, topic=pk).order_by('-startTime')[:10]
    
    entries_data_modified_from_backend = [] #list. ordered list. indexing. mutable. different types of data. []
    for entry in last_10_entries:
        localized_start_time = timezone.localtime(entry.startTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')
        localized_end_time = timezone.localtime(entry.endTime, timezone=user.timezone).strftime('%Y-%m-%d %H:%M:%S')

        total_seconds = entry.duration.total_seconds()
        duration_hours, remaining_seconds = divmod(total_seconds, 3600)
        duration_minutes, duration_seconds = divmod(remaining_seconds, 60)  
                
        # Append entry data to the list
        entries_data_modified_from_backend.append ({ #so it is a list of dictionary!
            'start_time': localized_start_time,
            'end_time': localized_end_time,
            'duration_hours': int(duration_hours),
            'duration_minutes': int(duration_minutes),
            'duration_seconds' : int(duration_seconds),
            'course' : 'Unselected Course' if entry.course is None else entry.course.name, #Old code when trackedtimedb used to have only topic foreign key, and course was evaluated according to topic #'Unselected Course' if (entry.topic is None) else      'Unselected Course' if (entry.topic.course is None) else entry.topic.course.name, #condition validating.
            'course_id': 0 if entry.course is None else entry.course.id,
            'topic_id': 0 if entry.topic is None else entry.topic.id,
            'topic': 'Unselected Topic' if entry.topic is None else entry.topic.name, #condition validating
            'session': entry.session,
        })

    context = { #dictionary. unordered. key-value pairs. immutable. same type of data. {} 
               #so we passed a list (of dictionaries) that is turned into value of a dictionary key (namely 'renderEntries')
               #so in the front end, we have to loop through the list (the dictionary value) to get the data of each entry. Note that each value itself will be a dictionary. 
        'readyEntries': entries_data_modified_from_backend
    }  
    
    
    return render(request, 'firstApp/entries.html', context)


def active_users(request):
    #to work on later: https://chat.openai.com/share/6dce5375-0b7a-4c29-b301-92e6cb04f535 Title: Active Users
    active_sessions = Session.objects.filter(expire_date__gte=datetime.now())
    active_usernames = []
    for session in active_sessions:
        session_data = session.get_decoded()
        if 'start_time' in session_data:
            user_id = session_data['_auth_user_id']
            user = myUserDB.objects.get(pk=user_id)
            active_usernames.append(user.username)
    return render(request, 'partials/active_users.html', {'active_usernames': active_usernames})

##new days ahead

def edit_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic) #This initializes a form instance with the POST data (request.POST contains the data submitted through the form via POST request upon clicking on submit button) and binds it to the topic instance. 
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = TopicForm(instance=topic) #The instance=topic argument is used to bind the form to the existing instance of the Topic model and prefill the form with the existing data upon rendering. 
    return render(request, 'firstApp/editTopic.html', {'form': form})

def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = CourseForm(instance=course)
    return render(request, 'firstApp/editCourse.html', {'form': form})


def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = CourseForm(instance=course)
    return render(request, 'firstApp/editCourse.html', {'form': form})


def edit_trackedtime(request, pk): #this function works but is faulty because duration is needed to be calculated accordingly.. time should be userfriendly. course/topic relation should be accordingly. 
    tracked_time = get_object_or_404(TrackedTimeDB, pk=pk)
    if request.method == 'POST':
        form = TrackedTimeForm(request.POST, instance=tracked_time)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = TrackedTimeForm(instance=tracked_time)
    return render(request, 'firstApp/editTrackedTime.html', {'form': form})


def edit_user(request, username):
    user = get_object_or_404(myUserDB, username=username)
    if request.method == 'POST':
        form = myUserDBForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard') #redirect to userprofile later 
    else:
        form = myUserDBForm(instance=user)
    return render(request, 'firstApp/edit_user.html', {'form': form})



#data visualization part goes here
def reportView(request):
    return render(request, 'firstApp/report.html')


def format_duration_to_hhmm(hours):
    """Convert duration from hours to hh:mm format."""
    total_minutes = int(hours * 60)
    hh = total_minutes // 60
    mm = total_minutes % 60
    return f"{hh:02}:{mm:02}"


@login_required
def get_bar_chart_data(request):
    # for future reff: https://chatgpt.com/share/914d2657-75b0-4a26-bf93-28ca64ec38f1
    # for future reff: https://chatgpt.com/share/701af340-a3c2-4603-9ab4-8d66104743f9
    user = request.user
    start_date = request.POST.get('start_date') #so we are getting the start date from the frontend. #start_date is the NAME of the INPUT TAG in the report.html. The request method must be POST in HTMX
    #print(start_date)
    end_date = request.POST.get('end_date')
    #print(end_date)
    #print("TESTing if start date & end date working")

    if start_date and end_date:
        tracked_times = TrackedTimeDB.objects.filter(
            user=user,
            startTime__date__gte=start_date, #syntax
            endTime__date__lte=end_date
        )
    else:
        tracked_times = TrackedTimeDB.objects.filter(user=user) #so taking the entire tracked times of the user
        
        
    # First, annotate the queryset to add the total duration for each course on each day as that will be shown on hover
    #https://docs.djangoproject.com/en/5.0/topics/db/aggregation/
    annotated_tracked_times = (
        TrackedTimeDB.objects
        .annotate(date=TruncDate('startTime')) #TruncDate is a function that truncates the datetime field to the date part only. #so we are adding a new field 'date' to the queryset.
        .values('date', 'course') #.values('date', 'course') changes the queryset to a valuesqueryset containing date & course #When you call values(), the resulting queryset contains QUERYSETS OF DICTIONARies (which is a subclass of querysets) instead of model instances.
        .annotate( #.values(): when combined with .annotate(), it groups the data by the specified fields specified in the arguments and allows aggregation functions to be applied to each group.
            total_course_duration=Sum(  # so the new field gonna be total_course_duration. The other two fiels are date and course. # it calculates the sum of durations for each GROUP of records defined by the unique combinations of date and course.
                ExpressionWrapper( 
                    F('duration'), #F() is used to reference a field value in the database. It is used to avoid hardcoding field values in queries. #Also note, 'duration' feild is not there in the valuesqueryset but being validly referenced here.
                    output_field=DurationField() #DurationField() is used to specify the output field type for the expression. It might be unnecessary as the field type is already DurationField.
                )
            )
        )
    )
    #print(TrackedTimeDB.objects.annotate(date=TruncDate('startTime')).values('date', 'course'))
    
    #we can not aggregate i.e. sum on another aggregation i.e. sum values btw in django ORM
    # Another annotation. Calculating the total tracked duration per day
    total_tracked_duration_per_day = (
    TrackedTimeDB.objects
    .annotate(date=TruncDate('startTime')) 
    .values('date')  # Group by date only
    .annotate(
        total_tracked_duration_per_day=Sum('duration', output_field=DurationField())  # Sum the duration for each date
        )
    )  
    print(total_tracked_duration_per_day)  

    # Create a dictionary to lookup
    total_duration_per_course_per_day = {
        (entry['date'], entry['course']): entry['total_course_duration'].total_seconds() / 3600 #key is a tuple of date and course. value is the total duration in hours
        for entry in annotated_tracked_times
    }
    
    #Creating another dictioanry for the second annotation
    total_tracked_duration_per_day = {
        entry['date']: entry['total_tracked_duration_per_day'].total_seconds() / 3600
        for entry in total_tracked_duration_per_day
    }

    #preparing the data for the plot
    data = [] #empty list
    for track in tracked_times:
        track_date = track.startTime.date() 
        data.append({ 
            'date': track_date, # which will be plotted in x axis
            'course': track.course.name if track.course else 'Uncategorized', #which will be divided into colors
            'duration': track.duration.total_seconds() / 3600, # will be plotted in the y axis
            'totalDurationForThisDay': format_duration_to_hhmm(total_tracked_duration_per_day.get(track_date, 0)), 
            'totalCourseDurationForThisDay': format_duration_to_hhmm(total_duration_per_course_per_day.get((track_date, track.course_id), 0)) #will be shown on hover # #looking up the dictioanry, default to 0 if not found
        })

    df = pd.DataFrame(data) #converting the list of dictionaries to a pandas dataframe as that's convenient #dataframe is a 2D labeled DS with columns of potentially different types.
    #print(df)

    # As we want to show ALL THE DATES in the range on the x axis, even if corresponding y axis value is 0, creating a date range from start_date to end_date
    if start_date and end_date:
        all_dates = pd.date_range(start=start_date, end=end_date).date #.date is used to get the date part only #pd.date_range() is used to generate a range of dates
    elif start_date:
        all_dates = pd.date_range(start=start_date, end=df['date'].max()).date
    elif end_date:       
        all_dates = pd.date_range(start=df['date'].min(), end=end_date).date    
    else:
        if not df.empty:
            all_dates = pd.date_range(start=df['date'].min(), end=df['date'].max()).date
        else:
            all_dates = [] #safety

    #print(all_dates)
    all_dates_df = pd.DataFrame({'date': all_dates}) #so currently only one column exists named 'date'
    #print(all_dates_df)

    # Merge the all dates range stored in all_dates_df we just created with the tracked times data stored in df (where x exists only if y exists)
    if not df.empty:
        df = all_dates_df.merge(df, on='date', how='left') #left is all_dates_df, right is df. # merged data gonna be stored in df. #left join is used to keep all the dates in all_dates_df even if there is no corresponding data in df.
        df['duration'] = df['duration'].fillna(0) # Fill missing duration values with 0
        df['course'] = df['course'].fillna('Uncategorized') # Fill missing course values with 'No Data'
    else: #safety
        df = all_dates_df
        df['duration'] = 0
        df['course'] = 'Uncategorized'
        
    
    
    df['this_session_hours'] = df['duration'].apply(format_duration_to_hhmm) #adding a new column to the dataframe #note .apply() on a dataframe column # the result of the apply function does not get stored in df['duration'], it gets stored in the lhs i.e. the new column
    # print(df['duration'])
    
        
    #now let's feeeeed into it, fianllyyyy
    fig = px.bar(
        df,
        x='date',
        y='duration',
        color='course', #the bars will be colored according to the course
        labels={'duration': 'Hours You Grinded', 'date': 'Days Gone', 'course': 'Courses You Aspired'},
        title='Your Learning Journey in Hours', 
        #hover_data={'date':True, 'course':True, 'duration':False, 'totalCourseDurationForThisDay':True},
        custom_data=['course', 'totalCourseDurationForThisDay', 'totalDurationForThisDay', 'this_session_hours'] #custom_data is used to add additional data to the hovertemplate #the custom data must be in the dataframe i.e. df here
    )
    
    #hovertemplate is used to customize the hover text that appears when you hover over the trace in the plot #Note syntax
    fig.update_traces(hovertemplate= 
        '<b>%{x} </b> -- Total Recorded <b>%{customdata[2]}</b> hours<br><br>' +
        'Studied <b>%{customdata[0]}  %{customdata[1]} </b>hours. <br>'+
        'This session comprises of %{customdata[3]} hours.<br>'+
        '<extra></extra>' #empty extra tag removes the trace name. note that.
    )


    # Sort the dates
    sorted_dates = sorted(all_dates)

    # Update the x-axis with sorted dates
    fig.update_xaxes(
        tickangle=45,
        tickmode='array',
        tickvals=[str(date) for i, date in enumerate(sorted_dates) if i % (len(sorted_dates) // 20 + 1) == 0]
    )

    
    
    chart_html = fig.to_html(full_html=False)

    response = HttpResponse(chart_html)

    return response