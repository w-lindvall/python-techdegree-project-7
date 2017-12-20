from django.contrib import messages
from django.contrib.auth import (authenticate, login,
                                 logout, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm,
                                       PasswordChangeForm)
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import ProfileForm, EmailForm


def sign_in(request):
    """View to sign in existing user"""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('home')
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    """View to create new user"""
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    """Sign user out"""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile(request):
    """Display user information if logged in."""
    profile = request.user.profile
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Edit user information if logged in."""
    form = ProfileForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'accounts/forms.html', {'form': form})


@login_required
def edit_email(request):
    """Edit user email if logged in."""
    form = EmailForm(instance=request.user.profile)
    if request.method == "POST":
        form = EmailForm(data=request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'accounts/forms.html', {'form': form})


@login_required
def change_password(request):
    """View allows user to change password if logged in."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Updated password!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/forms.html', {
        'form': form
    })
