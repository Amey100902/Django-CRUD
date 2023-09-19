from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Record
import requests,json,copy
import pyrebase,os
import firebase_admin

from firebase_admin import credentials

# cred = credentials.Certificate("C:/Users/ameya/OneDrive/Desktop/CRUD/dcrm/website/serviceAccount.json")
# firebase_admin.initialize_app(cred)
# firebase setup 

firebaseConfig  = {
  "apiKey": "AIzaSyCzcx8F7Vf26Lj1WTCtCwjrWPc-iWN2-Rc",
  "authDomain": "crud-59e02.firebaseapp.com",
  "projectId": "crud-59e02",
  "databaseURL" : "https://crud-59e02-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "crud-59e02.appspot.com",
  "messagingSenderId": "230843205578",
  "appId": "1:230843205578:web:771c48609c29d02d663133"
  
}

firebase=pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
storage.child("profile_photo.jpg").put("media/images/profile_photo.jpg")


def bojerom(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            job_type = request.POST.get('job_type')
            job_location=request.POST.get('job_location')
            url = "https://jsearch.p.rapidapi.com/search"
            if not job_type or not job_location:
                # Handle the case where one or both fields are empty
                return render(request, 'view_jobs.html')
            
            else:
                querystring = {"query":"{} in {}".format(job_type,job_location),"page":"1","num_pages":"1"}

                headers = {
                    "X-RapidAPI-Key": "54dead1671mshdf45e261fbccb66p1c7870jsnc6860a8d0e72",
                    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
                }

                response = requests.get(url, headers=headers, params=querystring)
                response=response.json()
                modified_data = copy.deepcopy(response)

                # Retrieve the job description from the JSON data
                for i in range(0,10):
                    job_description = modified_data["data"][i]["job_description"]

                    # Split the description into words and take the first 20 words
                    words = job_description.split()[:25]
                    truncated_description = " ".join(words)

                    # Update the job description in the modified data
                    modified_data["data"][i]["job_description"] = truncated_description+"..."
                
                return render(request, 'view_jobs.html',{'response':modified_data})
        
        else:
            return render(request, 'view_jobs.html', {'response': None})
        
    else:
        messages.success(request,"You must be Logged in to search jobs..")
        return redirect('home')

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
            profile_pic = request.FILES.get('profile_pic') 
            storage.child(name).put(profile_pic)
            # file_name = f"media/images/{os.path.basename(profile_pic.name)}"
            # print("filename= "+file_name)
            download_url = storage.child(name).get_url(None)
            # print("url= "+download_url)
            profile_pic=download_url
            record = Record(first_name=name,email=email,phone_no=phone_no,address=address,state=state,city=city,zipcode=zipcode,profile_pic=download_url)
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
            profile_pic = request.FILES.get('profile_pic')
            # print("profile_pic= " , profile_pic)
            storage.child(name).put(profile_pic)
            # file_name = f"media/images/{os.path.basename(profile_pic.name)}"
            # print("filename= "+file_name)
            download_url = storage.child(name).get_url(None)
            # print("url= "+download_url)
            profile_pic=download_url
            # Update the record
            current_record.first_name = name
            current_record.email = email
            current_record.phone_no = phone_no
            current_record.address = address
            current_record.city = city
            current_record.state = state
            current_record.zipcode = zipcode
            current_record.profile_pic = profile_pic

            # Save the updated record
            current_record.save()

            messages.success(request, "Record Has Been Updated!")
            return redirect('home')

        return render(request, 'update.html', {'current_record': current_record})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')
        
