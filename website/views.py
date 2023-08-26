from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Record


def home(request):
    #authenticate
    records = Record.objects.all()

    if request.method == 'POST':   #when user sends its credentials
        username=request.POST['username']
        password=request.POST['password']
        #authenticate
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Yoh have been logged in successfully..!")
            return redirect('home')
        else:
            messages.success(request,"There was an error logging you in. Please Check your credentials.")
            return redirect('home')
    else:                           #when user does nothing
        return render(request,'index.html',{'records':records})


def about(request):
    return render(request,'about.html',{})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out..!")
    return redirect('home')



def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirmPassword=request.POST.get('confirmPassword')
        if password==confirmPassword:
            myuser = User.objects.create_user(username,email,password)
            myuser.save
            messages.success(request,"successfull registered")
            return redirect('home')
        else:
            messages.success(request,"the two passwords doesn't match.!")
            return redirect('register')
            
    else:
        return render(request,'register.html')


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must be Logged in to view the records..")
        return redirect('home')


def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record Deleted successfully..")
        return redirect('home')
    else:
        messages.success(request,"You must be logged in to do that..")
        return redirect('home')
    

def add_record(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name=request.POST.get('name')
            email=request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            address=request.POST.get('address')
            city=request.POST.get('city')
            state=request.POST.get('state')
            zipcode=request.POST.get('zipcode')
            record = Record(first_name=name,email=email,phone_no=phone_no,address=address,state=state,city=city,zipcode=zipcode)
            record.save()
            messages.success(request,"Record added successfully")
            return redirect('home')
        else:
            return render(request,'add_record.html')
    else:
        messages.success(request,"You must be logged in to add records..")
        return redirect('home')
  
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)

        if request.method == 'POST':
            # Get the updated data from the form
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')

            # Update the record
            current_record.first_name = name
            current_record.email = email
            current_record.phone_no = phone_no
            current_record.address = address
            current_record.city = city
            current_record.state = state
            current_record.zipcode = zipcode

            # Save the updated record
            current_record.save()

            messages.success(request, "Record Has Been Updated!")
            return redirect('home')

        return render(request, 'update.html', {'current_record': current_record})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
        
# def update_record(request,pk):
#     return render(request,'update.html',{'id':pk})