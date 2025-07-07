from django.shortcuts import redirect, render
from apps.user.models import User

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import generate_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.review.models import Review
from apps.location.models import Location

User = get_user_model()

@api_view(['GET'])
def public_user_info(request, user_id):
    try:
        user = User.objects.get(id=user_id)

        # Количество отзывов, кроме автоматических (где location.user = сам пользователь)
        reviews_count = Review.objects.filter(user_id=user.id).exclude(location__user_id=user.id).count()

        # Только вручную добавленные локации
        locations_count = Location.objects.filter(user_id=user.id).count()

        return Response({
            'username': user.username,
            'email': user.email,
            'phone': getattr(user, 'phone', None),
            'reviews_count': reviews_count,
            'locations_count': locations_count,
        })

    except User.DoesNotExist:
        return Response({'detail': 'Пользователь не найден'}, status=404)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'detail': 'Внутренняя ошибка сервера'}, status=500)


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

        if User.objects.filter(username=username):
            messages.error(request, "Имя пользователя уже существует! Попробуйте другое.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Этот email уже зарегистрирован!")
            return redirect('home')
        
        if len(username) > 20:
            messages.error(request, "Имя пользователя не должно превышать 20 символов!")
            return redirect('home')
        
        if password1 != password2:
            messages.error(request, "Пароли не совпадают!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Имя пользователя должно состоять только из букв и цифр!")
            return redirect('home')

        if password1 == password2:
            myuser = User.objects.create_user(username, email, password1)
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Аккаунт успешно создан! Проверьте почту для активации.")

            current_site = get_current_site(request)
            email_subject = "Подтверждение регистрации на PeePal"
            message2 = render_to_string('authentication/email_confirmation.html', {
                'name': myuser.username,
                'domain': 'peepal.ru',
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.DEFAULT_FROM_EMAIL,
                [myuser.email],
            )
            email.fail_silently = False
            email.send()

            next_param = request.GET.get('next', '')
            return redirect(f'https://peepal.ru/auth-success?next={next_param}')

        else:
            messages.error(request, "Пароли не совпадают.")
            return redirect('auth', form_type='signup')
    else:
        return render(request, "authentication/auth.html", {'form_type': 'signup'})


def login_view(request):
    if request.method == "POST":
        username = request.POST['user-login']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            username = user.username
            request.session['is_authenticated'] = True
            request.session['username'] = username
            next_param = request.GET.get('next', '')
            return redirect(f'https://peepal.ru/auth-success?next={next_param}')
        else:
            messages.error(request, "Неверные данные для входа!")
            return redirect('home')
    
    return render(request, 'authentication/auth.html', {'form_type': 'login'})


def signout(request):
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect('home')


def forgot(request):
    if request.method == "POST":
        email = request.POST.get('pass-forgot')
        
        if email:
            try:
                user = User.objects.get(email=email)

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                reset_url = reverse('change', kwargs={'uidb64': uid, 'token': token})
                reset_link = f'http://{current_site.domain}{reset_url}'

                mail_subject = 'Сброс пароля'
                message = render_to_string('authentication/reset_password_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                user.email_user(mail_subject, message)

                messages.success(request, "Письмо для сброса пароля успешно отправлено.")
                return redirect('home')

            except User.DoesNotExist:
                messages.error(request, "Пользователь с таким email не зарегистрирован.")
                return redirect('home')
        else:
            messages.error(request, "Введите корректный адрес электронной почты.")
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
                    user.password = make_password(password1)
                    user.save()
                    messages.success(request, f"Пароль успешно изменён для пользователя: {user.username}")
                    return redirect('home')
                else:
                    messages.error(request, "Пароли не совпадают или поля не заполнены.")
                    return redirect('home')
            else:
                return render(request, "authentication/change_password.html", {'user': user, 'uidb64': uidb64, 'token': token})
        else:
            messages.error(request, "Ссылка для сброса пароля недействительна.")
            return redirect('home')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Ссылка для сброса пароля недействительна.")
        return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Недопустимая ссылка активации.")
        return redirect('home')

    if generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Ваш аккаунт был успешно активирован!")
        return redirect('home')
    else:
        messages.error(request, "Ссылка активации недействительна или устарела.")
        return redirect('home')


@login_required
def dashboard_home(request):
    return render(request, 'home.html')