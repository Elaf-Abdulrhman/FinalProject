from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserSignupForm, AthleteSignupForm, ClubSignupForm, ClubUserSignupForm
from .models import User, Athlete, Club
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def sign_up_as_view(request:HttpRequest):

    return render(request,"account/sign_up_as.html")

def profile_view(request:HttpRequest, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request,"account/profile.html", {'user': user})


def signup_athlete_view(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        athlete_form = AthleteSignupForm(request.POST, request.FILES)

        if user_form.is_valid() and athlete_form.is_valid():
            user = user_form.save()
            athlete = athlete_form.save(commit=False)
            athlete.user = user
            athlete.save()

            messages.success(request, "Athlete account created successfully! Please log in.")
            return redirect('account:login_view')
        else:
            messages.error(request, "There was an error with your form.")
    else:
        user_form = UserSignupForm()
        athlete_form = AthleteSignupForm()

    return render(request, 'account/signup_athlete.html', {
        'user_form': user_form,
        'athlete_form': athlete_form
    })




def signup_club_view(request):
    if request.method == 'POST':
        user_form = ClubUserSignupForm(request.POST)
        club_form = ClubSignupForm(request.POST, request.FILES)

        if user_form.is_valid() and club_form.is_valid():
            user = user_form.save()
            club = club_form.save(commit=False)
            club.user = user
            club.is_approved = False
            club.save()

            messages.info(request, "Club account created! Awaiting admin approval.")
            return redirect('account:login_view')
        else:


            messages.error(request, "There was an error with your form.")
    else:
        user_form = ClubUserSignupForm()
        club_form = ClubSignupForm()

    return render(request, 'account/signup_club.html', {
        'user_form': user_form,
        'club_form': club_form
    })



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            try:
                club = Club.objects.get(user=user)
                if not club.is_approved:
                    messages.error(request, "Club account not approved yet by admin.")
                    return redirect('account:login_view')
            except Club.DoesNotExist:
                pass

            login(request, user)
            return redirect('main:main_page_view')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main:main_page_view')




@login_required
def Edit_Profile_view(request: HttpRequest, user_id):
    print("Logged in user ID:", request.user.id)
    print("URL user ID:", user_id)

    if request.user.id != user_id:
        messages.warning(request, "You cannot edit this profile.", "alert-warning")
        return redirect("main:main_page_view")

    user = request.user
    try:
        athlete = Athlete.objects.get(user=user)
    except Athlete.DoesNotExist:
        messages.error(request, "Athlete profile not found.", "alert-danger")
        return redirect("main:main_page_view")

    if request.method == "POST":
        user_form = UserSignupForm(request.POST, instance=user)
        athlete_form = AthleteSignupForm(request.POST, request.FILES, instance=athlete)

        if user_form.is_valid() and athlete_form.is_valid():
            user_form.save()
            athlete_form.save()
            messages.success(request, "Profile updated successfully!", "alert-success")
            login(request, user)
            return redirect("account:profile_view", user_id=request.user.id)
        else:
            print("User Form Errors:", user_form.errors)
            print("Athlete Form Errors:", athlete_form.errors)
            messages.error(request, "There was an error with your form.", "alert-danger")
    else:
        user_form = UserSignupForm(instance=user)
        athlete_form = AthleteSignupForm(instance=athlete)

    return render(request, "account/Edit_Profile.html", {
        "user_form": user_form,
        "athlete_form": athlete_form,
        "user": user,
        "athlete": athlete,
    })
    
    


@login_required
def Edit_profile_club_view(request: HttpRequest, user_id):
    # Check if the logged-in user matches the user_id in the URL
    print("Logged in user ID:", request.user.id)
    print("URL user ID:", user_id)

    if request.user.id != user_id:
        messages.warning(request, "You cannot edit this profile.", "alert-warning")
        return redirect("main:main_page_view")

    user = request.user
    club = get_object_or_404(Club, user=user)

    # Handle the form submission on POST request
    if request.method == 'POST':
        user_form = ClubUserSignupForm(request.POST, instance=user)
        club_form = ClubSignupForm(request.POST, request.FILES, instance=club)

        if user_form.is_valid() and club_form.is_valid():
            user_form.save()
            club_form.save()
            messages.success(request, "Profile updated successfully!", "alert-success")
            login(request, user)
            return redirect("account:profile_view", user_id=request.user.id)
        else:
            print("User Form Errors:", user_form.errors)
            print("Club Form Errors:", club_form.errors)
            messages.error(request, "There was an error with your form.", "alert-danger")
    else:
        # Pre-fill the forms with current user and club data
        user_form = ClubUserSignupForm(instance=user)
        club_form = ClubSignupForm(instance=club)

    return render(request, 'account/Edit_profile_club.html', {
        'user_form': user_form,
        'club_form': club_form,
        'user': user,
        'club': club,
    })