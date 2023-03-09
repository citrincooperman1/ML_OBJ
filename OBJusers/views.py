from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Event, Team, TeamMember, Profile
from django.views import View
from django.contrib.auth import logout    

class LogoutView(View):

    template_name = 'registration/logged_out.html'

    def get(self, request):
        response = logout(request)

        return render(response, self.template_name)


# Create your views here.

@login_required(login_url="/login")
def home(request):
    # user_events = Profile.objects.filter(user=request.user)
    following = request.user.events.all() # I was thinking of sending a set of followed events
    events = Event.objects.all()
    if request.method == "POST":
        event_id = request.POST.get("event-id")
        follow_id = request.POST.get("follow-id")
        unfollow_id = request.POST.get("unfollow-id")
        print('follow_id:' + str(follow_id))
        print('unfollow_id:' + str(unfollow_id))
        current_user = request.user
        if event_id:
            event_del = Event.objects.filter(id=event_id).first()
            if event_del and (event_del.author == request.user ):
                event_del.delete()
        if follow_id:
            event_foll = Event.objects.filter(id=follow_id).first()
            print(event_foll)
            event_foll.user.add(current_user)
            #event_foll.events.add(user=request.user, followsEvent=event_foll)
            #event_foll.save()
        if unfollow_id:
            event_unfoll = Event.objects.get(id=unfollow_id)
            currentUserObj = User.objects.get(username=current_user)
            print(event_unfoll)
            print(currentUserObj)
            event_unfoll.user.remove(currentUserObj)
    return render(request, 'OBJusers/home.html', {"events": events,'following':following})

def team(request):
    teams = TeamMember.objects.all()
    return render(request, 'OBJusers/teams.html', {"teams": teams})

@login_required(login_url="/login")
def profile(request):
    current_user = request.user
    teams = TeamMember.objects.filter(member=current_user)
    choice_teams = Team.objects.all()
    events_followed_count = Event.objects.filter(user=current_user).count()
    if request.method == 'POST':
            event = Event()
            event.event = request.POST['event']
            team_id = request.POST['useroption']
            team_sel = Team.objects.get(id=team_id)
            event.team = team_sel
            event.author = request.user
            event.description = request.POST['desc']
            for key,value in request.FILES.items():
                print(key)
                print(value)
                event.file = value
            event.save()
            return render(request, 'OBJusers/profile.html',  {"teams": teams, "choice_teams": choice_teams, 'events_followed_count': events_followed_count})
    return render(request, 'OBJusers/profile.html',  {"teams": teams, "choice_teams": choice_teams, 'events_followed_count': events_followed_count})

@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'OBJusers/create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


# Onbjective Gaming
# Write to Profile on this App - Not additinal apps needed
# Add basic functionallity aka Change password, Forgot Password, and *lower priority* send emails for verification (added code in setting use gmail)
# Esports page
# Gioker - Admin User : can add events, and create teams on the page 1-*. Be able to add images to the logo
#       >> Each event page will display team + members
#       >> Members are able to join a team/or follow the event
# Feed Page - Events. If store clicked, the page will show details of the members and what is the event about
# Urls:
#       /Home - Index/Feed - see all events - available to everyone
#       /Teams - details of the teams - available to everyone
#       /Profile - User Profile - User can join teams, and follow events - Only available to user
#                   >> the feed by default will show the events of the team, and the followed ones
#       /Owner - add events, and create teams
