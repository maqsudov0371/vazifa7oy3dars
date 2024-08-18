from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Course, User, Contact
from django.contrib.messages import warning, success
from .utils import send_verification_email
from django.contrib.auth import authenticate, login
from django.views.generic import ListView

class HomePageView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
    paginate_by = 3

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        phone = request.POST.get('phone')
        
        if password != password_confirm:
            warning(request, 'Password confirmation is incorrect')
            return redirect(reverse('main:register'))
        
        if User.objects.filter(username=username).exists():
            warning(request, 'User already registered')
            return redirect(reverse('main:register'))
        
        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password,
            phone=phone, 
            is_active=False
        )
        
        send_verification_email(user)
        
        success(request, 'User registered. Please check your email to verify your account.')
        return redirect(reverse("main:kirish"))

class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if not User.objects.filter(username=username).exists():
            warning(request, 'User does not exist')
            return redirect(reverse('main:kirish'))
        
        user = User.objects.get(username=username)
        
        if not user.check_password(password):
            warning(request, 'Password is incorrect')
            return redirect(reverse('main:kirish'))
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('main:home'))
        
        warning(request, 'Error')
        return redirect(reverse('main:kirish'))

class VerifyEmailView(View):
    def get(self, request, code):
        try:
            user = User.objects.get(verification_code=code)
            user.is_active = True
            user.verification_code = None
            user.save()
            success(request, 'Your email has been verified successfully. You can now log in.')
            return redirect(reverse('main:kirish'))
        except User.DoesNotExist:
            warning(request, 'Invalid verification code.')
            return redirect(reverse('main:register'))

class ContactView(View):
    def get(self, request):
        return render(request, 'contact_us.html')
    
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )
        contact.save()

        # Success message before redirecting
        success(request, 'Thank you for your message. We will get back to you soon.')
        return redirect(reverse('main:contact'))
