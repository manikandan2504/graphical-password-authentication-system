from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from .models import GraphicalUser

import random


def send_otp_email(email, otp):

    send_mail(
        'Your OTP Verification Code',
        f'Your OTP is: {otp}',
        None,
        [email],
        fail_silently=False,
    )


def register(request):

    message = ""

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        graphical = request.POST['graphical']

        otp = random.randint(100000, 999999)

        request.session['otp'] = str(otp)
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['graphical'] = graphical

        send_otp_email(email, otp)

        return redirect('/verify-otp/')

    return render(request, 'register.html', {
        'message': message
    })


def login_view(request):

    message = ""

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        graphical = request.POST.get('graphical')

        if username == "" or password == "" or graphical is None:

            message = "All fields are required ❌"

        else:

            user = GraphicalUser.objects.filter(
                username=username,
                graphical_password=graphical
            ).first()

            if user and check_password(password, user.password):

                request.session['username'] = username

                return redirect('/dashboard/')

            else:

                message = "Invalid Credentials ❌"

    return render(request, 'login.html', {
        'message': message
    })


def dashboard(request):

    username = request.session.get('username')

    if not username:

        return redirect('/login/')

    return render(request, 'dashboard.html', {
        'username': username
    })


def logout_view(request):

    request.session.flush()

    return redirect('/login/')


def verify_otp(request):

    message = ""

    if request.method == "POST":

        entered_otp = request.POST['otp']

        session_otp = request.session.get('otp')

        if entered_otp == session_otp:

            GraphicalUser.objects.create(

                username=request.session.get('username'),

                email=request.session.get('email'),

                password=make_password(
                    request.session.get('password')
                ),

                graphical_password=request.session.get('graphical')

            )

            request.session.flush()

            return redirect('/login/')

        else:

            message = "Invalid OTP ❌"

    return render(request, 'verify_otp.html', {
        'message': message
    })


def forgot_password(request):

    message = ""

    if request.method == "POST":

        username = request.POST['username']
        new_password = request.POST['new_password']
        graphical = request.POST['graphical']

        user = GraphicalUser.objects.filter(
            username=username,
            graphical_password=graphical
        ).first()

        if user:

            user.password = make_password(new_password)

            user.save()

            message = "Password changed successfully ✅"

        else:

            message = "Invalid Username or Graphical Password ❌"

    return render(request, 'forgot.html', {
        'message': message
    })