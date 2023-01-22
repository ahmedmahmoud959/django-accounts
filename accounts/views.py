from django.shortcuts import render ,redirect
from .models import Profile
from .forms import SignupForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate , login

# Create your views here.
def signup(request):
   
   if request.method == 'POST' :
      form = SignupForm(request.POST)
      if form.is_valid():
         form.save()
         # username = request.POST["username"]
         # password = request.POST["password"]
         username = form.cleaned_data['username']
         password = form.cleaned_data['password1']
         user = authenticate(username=username , password=password)
         login(request, user)
         return redirect('/accounts/profile')
   else :
      form = SignupForm()
   context = {
      'form' : form
   }
   return render(request, 'registration/signup.html',context)


def profile (request):
   
   profile = Profile.objects.get(user=request.user)
   
   return render(request, 'profile/profile.html' , {'profile':profile})


def profile_edit (request):
   profile = Profile.objects.get(user= request.user)
   if request.method == 'POST':
      user_form = UserEditForm(request.POST, instance=request.user)
      profile_form = ProfileEditForm(request.POST , instance=profile)
      if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         myprofile = profile_form.save(commit=False)
         myprofile.user = request.user
         myprofile.save()
         return redirect('/accounts/profile')
   else:
      user_form = UserEditForm(instance=request.user)
      profile_form = ProfileEditForm(instance=profile)
   
   context = {
      'user_form' : user_form,
      'profile_form' : profile_form,
   }
   return render(request, 'profile/profile_edit.html' , context)