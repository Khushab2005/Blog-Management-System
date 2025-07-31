from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from myapp.models import *
from myapp.utils.email_varify import is_valid_email
from myapp.utils.password_varify import password_valid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username_ = request.POST['username']
        email_ = request.POST['email']
        password_ = request.POST['password']
        confirm_password_ = request.POST['confirm_password']
        
        if not  is_valid_email(email_):
            messages.error(request,'Invalid email address.')
            return redirect('register')
        
        if not password_valid(password_)[0]:
            messages.error(request, password_valid(password_)[1])
            return redirect('register')
            
        
        if password_ != confirm_password_:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if User.objects.filter(email=email_).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        
        data = User.objects.create(
            username = username_,
            email = email_,
            password = password_,
        )
        messages.success(request, "Registration successful! Please log in.")
        data.save()
        return redirect('login')    
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username_ = request.POST['username']
        password_ = request.POST['password']
        
        if not User.objects.filter(username=username_).exists():
            messages.error(request, "Invalid username.")
            return redirect('login')
        elif not User.objects.filter(password=password_).exists():
            messages.error(request, "Invalid  password.")
            return redirect('login')
        else:
            
            user = authenticate(username=username_, password=password_)
            user = User.objects.get(username = username_)
            if not user.is_active:
                messages.error(request, "Your account is inactive. Please contact support.")
                return redirect('login')
            request.session['user_id'] = str(user.id)
            request.session['username'] = user.username
            print(request.session['username'])
            print(request.session['user_id'])
            messages.success(request, "Login successful!")
            return redirect('dashboard')
    
        
    return render(request, 'login.html')

# @login_required(login_url='login')
def dashboard(request):
    query_ = request.GET.get('query')
    blogs = Blog.objects.all()
    
    comment = Comment.objects.all()
    if query_:
        blogs = blogs.filter(
            Q(title__icontains=query_) |
            Q(author__username__icontains=query_)
        )
        
    paginator = Paginator(blogs, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = User.objects.all()
    context = {
        'comment': comment,
        'blogs': page_obj,
        'user': user,
        'query':query_,
        'page_obj':page_obj,
    }
    if request.method == "POST":
        if "title" in request.POST:
            title_ = request.POST['title']
            content_ = request.POST['content']
            username_ = request.session['username']
            images_ = request.FILES.get('images') 
        
            author_instance = User.objects.get(username = username_)
            Blog.objects.create(
                title = title_,
                content = content_,
                author = author_instance,
                images = images_,
            )
        elif "comment" in request.POST:
            

            comment_ = request.POST['comment']
            blog_id = request.POST.get('blog_id') 
            username_ = request.session['username']
            author_instance = User.objects.get(username = username_)
            blog_instance = Blog.objects.get(id = blog_id)
            
            Comment.objects.create(
                comment = comment_,
                author = author_instance,
                blog = blog_instance,
                
                
            )
    
    

        
        
    return render(request, 'dashboard.html',context)


def logout(request):
    request.session.flush() 
    messages.success(request, "Logout successful!")
    return redirect('thank_you')


def thank_you(request):
    return render(request, 'thankyou.html')


def updateblog(request,id):
    data = get_object_or_404(Blog,id=id)
    if request.method == 'POST':
        data.title = request.POST['title']
        data.content = request.POST['content']
        data.images = request.FILES.get('images')
        data.save()
        return redirect('dashboard')
        
    return render(request,'dashboard.html')

def deleteblog(request,id):
    data = get_object_or_404(Blog,id=id)
    data.delete()
    return redirect('dashboard')
