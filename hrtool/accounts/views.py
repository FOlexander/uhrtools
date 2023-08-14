from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .forms import UserCreationForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .models import CustomUser
from .tokens import account_activation_token
from .decorators import user_not_authenticated

next_page = ''

def my_login(request):
    # try:
    #     next_page = request.GET['next']
    #     print(next_page)
    # except BaseException:
    #     next_page = '-------------next_page------------------'
    if request.method == 'POST':
        print(next_page)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.META.get('HTTP_REFERER').split('/')[-2] == 'datadownload':
                return redirect('dload')
            else:
                return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login or password.'})
    else:
        return render(request, 'login.html')


def my_logout(request):
    logout(request)
    return redirect('index')


def my_create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(form)
            # Log the user in
            login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'create.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    return redirect("homepage")
@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    print('Message sent')
                    # messages.success(request,
                    #     """
                    #     <h2>Password reset sent</h2><hr>
                    #     <p>
                    #         We've emailed you instructions for setting your password, if an account exists with the email you entered.
                    #         You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address
                    #         you registered with, and check your spam folder.
                    #     </p>
                    #     """
                    # )
                else:
                    print('Some issues occured')

                    # messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('index')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"form": form}
        )