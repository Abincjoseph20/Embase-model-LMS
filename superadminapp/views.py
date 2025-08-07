from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, AdminRegistrationForm,UserAdminRegistrationForm
from .models import Account
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        print("Register POST:", request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = Account.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                roles='student'  # default role or handle later
            )
            
            user.is_verified = True
            user.is_approved = True
            user.is_active = True
            user.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
        else:
            print("Register form errors:", form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    print(f"[DEBUG] Request method: {request.method}")
    
    
    if request.method == 'POST':
        print(f"[DEBUG] POST data: {request.POST}")
        form = LoginForm(request.POST)
        
        
        if form.is_valid():
            print(f"[DEBUG] LoginForm is valid")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(f"[DEBUG] Cleaned Email: {email}, Password: {password}")

            user = authenticate(request, email=email, password=password)
            print(f"[DEBUG] Authenticate result: {user}")

            if user is not None:
                print(f"[DEBUG] Authenticated user: {user.email}, Role: {user.roles}")
                
                if not user.is_verified:
                    print("[DEBUG] User is not verified")
                    messages.error(request, 'Account is not verified.')
                    return redirect('login')

                if not user.is_approved:
                    print("[DEBUG] User is not approved")
                    messages.error(request, 'Account is not approved yet.')
                    return redirect('login')

                if not user.is_active:
                    print("[DEBUG] User is inactive")
                    messages.error(request, 'Account is inactive.')
                    return redirect('login')

                auth_login(request, user)
                print("[DEBUG] Login successful")
                
                # Role-based redirection
                print(f"[DEBUG] Redirecting based on role: {user.roles}")
                if user.is_superadmin:
                    print("[DEBUG] Redirecting to superadmin_dashboard")
                    return redirect('superadmin_dashboard')
                elif user.is_admin:
                    print("[DEBUG] Redirecting to admin_dashboard")
                    return redirect('admin_dashboard')
                elif user.roles == 'teacher':
                    print("[DEBUG] Redirecting to teacher_dashboard")
                    return redirect('teacher_dashboard')
                elif user.roles == 'student':
                    print("[DEBUG] Redirecting to student_dashboard")
                    return redirect('student_dashboard')
                elif user.roles == 'parent':
                    print("[DEBUG] Redirecting to parent_dashboard")
                    return redirect('parent_dashboard')
                elif user.roles == 'guest':
                    print("[DEBUG] Redirecting to guest_dashboard")
                    return redirect('guest_dashboard')
                else:
                    print("[DEBUG] Role not recognized")
                    messages.error(request, 'Role not recognized.')
                    return redirect('login')
            else:
                print("[DEBUG] Invalid credentials or user not found")
                messages.error(request, 'Invalid credentials.')
                return redirect('login')
        else:
            print(f"[DEBUG] LoginForm is invalid: {form.errors}")
    else:
        print("[DEBUG] GET request for login page")
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


def base_view(request):
    return render(request, 'base.html')

def a_Login(request):
    return render(request,'accounts/a_Login.html')


# Dashboards
def superadmin_dasboard_view(request):
    if request.user.is_authenticated and request.user.roles == 'superadmin':
        User = get_user_model()
        users = Account.objects.all().order_by('-date_joined')
        print("[DEBUG] Found users:", users)
        return render(request, 'dashboards/dashboard.html', {'users': users}) 
    else:
        return redirect('login')
    
def admin_dashboard_view(request):
    return render(request, 'dashboards/admin_dashboard.html')

def student_dashboard_view(request):
    return render(request, 'dashboards/student_dashboard.html')

def teacher_dashboard_view(request):
    return render(request, 'dashboards/teacher_dashboard.html')

def parent_dashboard_view(request):
    return render(request, 'dashboards/parent_dashboard.html')

def guest_dashboard_view(request):
    return render(request, 'dashboards/guest_dashboard.html')


def admin_register_view(request):
    print("Admin register method:", request.method)
    if request.method == 'POST':
        print("Admin Register POST:", request.POST)
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            print("Form valid:", form.cleaned_data)
            user = Account.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                roles=form.cleaned_data['roles']
            )

            # Role permissions
            if user.roles == 'admin':
                user.is_staff = True
                user.is_admin = True
                user.is_approved = True
                user.is_verified = True
            elif user.roles == 'superadmin':
                user.is_superuser = True
                user.is_staff = True
                user.is_admin = True
                user.is_approved = True
                user.is_verified = True
            elif user.roles in ['student', 'teacher', 'parent', 'guest']:
                user.is_verified = True
                user.is_approved = True

            user.is_active = True
            user.save()
            print("Admin registered:", user.email)
            messages.success(request, "Admin account registered successfully.")
            return redirect('login')
        else:
            print("Admin form errors:", form.errors)
    else:
        form = AdminRegistrationForm()

    return render(request, 'accounts/admin_register.html', {'form': form})

@login_required
def user_admin_register_view(request):
    print("Admin register method:", request.method)

    if request.method == 'POST':
        print("Admin Register POST:", request.POST)
        form = UserAdminRegistrationForm(request.POST)

        if form.is_valid():
            print("Form valid:", form.cleaned_data)

            # Create user with registered_by field
            user = Account.objects.create_user(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                roles=form.cleaned_data['roles'],
                registered_by=request.user 
            )

            # Set role-based flags
            if user.roles == 'admin':
                user.is_staff = True
                user.is_admin = True
                user.is_verified = True
                user.is_approved = True
            elif user.roles in ['student', 'teacher', 'parent', 'guest']:
                user.is_verified = True
                user.is_approved = True

            user.is_active = True
            user.save()
            print("Admin registered:", user.email)

            messages.success(request, "Admin account registered successfully.")
            return redirect('login')
        else:
            print("Admin form errors:", form.errors)
    else:
        form = UserAdminRegistrationForm()

    return render(request, 'accounts/User_admin_register.html', {'form': form})



@login_required
def my_registered_users(request):
    users = Account.objects.filter(registered_by=request.user)
    return render(request, 'tables/table.html', {'users': users})