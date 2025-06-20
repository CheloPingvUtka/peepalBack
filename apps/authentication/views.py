from django.shortcuts import redirect, render
from apps.user.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from . tokens import generate_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def current_user_view(request):
    user = request.user
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_authenticated': True,
    })

@login_required
def protected_view(request):
    return render(request, 'protected.html')


def home(request):
    if request.user.is_authenticated:
        return render(request, "authentication/index.html", {'username': request.user.username})
    else:
        return render(request, "authentication/index.html")


def auth(request, form_type):
    if form_type == 'signup':
        return render(request, "authentication/auth.html", {'form_type': 'signup'})
    elif form_type == 'login':
        return render(request, "authentication/auth.html", {'form_type': 'login'})
    else:
        return render(request, "authentication/index.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        # Check if the username already exists
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        # Check if the username is longer than 20 characters
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('home')
        
        # Check if the passwords match
        if password1 != password2:
            messages.error(request, "Passwords didn't match!!")
            return redirect('home')
        
        # Check if the username is alphanumeric
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        # If the passwords match, create a new user
        if password1 == password2:
            myuser = User.objects.create_user(username, email, password1)
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Your account has been successfully created! Please check your email to confirm your email address and activate your account.")
  
            # Send confirmation email
            subject = "Welcome to PeePal!"
            message = f"Hello {myuser.username}!\nThank you for visiting our website. We have also sent you a confirmation email, please confirm your email address."
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            
            current_site = get_current_site(request)
            email_subject = "Confirm your Email - Django Login!"
            message2 = render_to_string('authentication/email_confirmation.html', {
                'name': myuser.username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            # Add print statement for debugging before redirect
            print("Redirecting to home page...")
            next_param = request.GET.get('next', '')
            return redirect(f'http://localhost:5173/auth-success?next={next_param}')

        else:
            messages.error(request, "Passwords do not match.")
            return redirect('auth', form_type='signup')
    else:
        return render(request, "authentication/auth.html", {'form_type': 'signup'})


def login_view(request):
    # Get the username and password from the request
    if request.method == "POST":
        username = request.POST['user-login']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)

        # If the user is authenticated
        if user is not None:
            # Log in the user
            login(request, user)
            username = user.username
            request.session['is_authenticated'] = True
            request.session['username'] = username
            next_param = request.GET.get('next', '')
            return redirect(f'http://localhost:5173/auth-success?next={next_param}')
        else:
            # If authentication fails, display an error message and redirect to the home page
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    
    # If the request method is not POST, render the login template
    return render(request, 'authentication/auth.html', {'form_type': 'login'})


def signout(request):
    # Log out the user
    logout(request)

    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


def forgot(request):
    if request.method == "POST":
        email = request.POST.get('pass-forgot')
        
        if email:
            try:
                user = User.objects.get(email=email)

                # Генерируем ссылку для сброса пароля
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                reset_url = reverse('change', kwargs={'uidb64': uid, 'token': token})
                reset_link = f'http://{current_site.domain}{reset_url}'

                # Отправка email с ссылкой для сброса пароля
                mail_subject = 'Password Reset'
                message = render_to_string('authentication/reset_password_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                user.email_user(mail_subject, message)

                messages.success(request, "The password reset email has been sent successfully.")
                return redirect('home')

            except User.DoesNotExist:
                messages.error(request, "Sorry, the user with this email address is not registered.")
                return redirect('home')
        else:
            messages.error(request, "Please try to enter a valid email address next time.")
            return redirect('home')
    
    return render(request, "authentication/forgot.html")


def change(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if password1 and password2 and password1 == password2:
                    # Устанавливаем новый пароль для пользователя
                    user.password = make_password(password1)
                    user.save()
                    messages.success(request, f"Password changed successfully for user: {user.username}")
                    return redirect('home')
                else:
                    messages.error(request, "Passwords do not match or some fields are empty. Please try again.")
                    return redirect('home')
            else:
                return render(request, "authentication/change_password.html", {'user': user, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "The password reset link is no longer valid.")
            return redirect('home')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "The password reset link is no longer valid.")
        return redirect('home')


def activate(request, uidb64, token):
    try:
        # Декодируем id и проверяем токен
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('home')  # Возвращаем на главную, если активация не удалась

    if generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Your account has been activated!")
        return redirect('home')  # Перенаправление на главную страницу после успешной активации
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('home')  # Возвращаем на главную, если токен неверный

@login_required
def dashboard_home(request):
    return render(request, 'home.html')
    
