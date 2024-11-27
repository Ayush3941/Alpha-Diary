from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import contactM,Task,Budget
from django.utils import timezone
from . import smssender
from .check import process_unvisited_records,mark_as_visited, delete_record
from django.http import JsonResponse
from .sql_saver import process_emails

def add_budget(request):
	if request.method == 'POST':
		name = request.POST['budget_name']
		test = request.POST['status']
		if test == "credited":
			num = int(float(request.POST['amount']))
		else:
			num = -int(float(request.POST['amount']))
		try:
			task = Budget.objects.get(name=name)
			task.number += num  # Adjust the value of the 'number' field
			task.save() 

			return redirect("track")
		except:
			task = Budget(name = name,number = num)
			task.save()
			return redirect("track")

	return render(request,"add_budget.html")









def budget(request):
    if request.method == 'POST':
        # Get the form data for the budget name and balance to be added
        budget_name = request.POST.get('budget_name')
        add_balance = request.POST.get('balance')

        # Get the corresponding budget instance by name
        try:
            budget = Budget.objects.get(name=budget_name)
            # Add the balance to the existing budget number
            budget.number += int(add_balance)  # Assuming 'add_balance' is a valid number
            budget.save()  # Save the updated budget
        except Budget.DoesNotExist:
            # Handle the case where the budget doesn't exist
            pass
        
        return redirect('budget')  # Redirect to the same page after updating

    # Fetch all budgets to display on the page
    budgets = Budget.objects.all()
    return render(request, "budget.html", {'budgets': budgets})







def re_load(request):
	if request.method == 'POST':
		sender_email = "alerts@hdfcbank.net"
		process_emails(sender_email)
	return redirect('track')


def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)

        task.delete()

        return redirect("index")
    except Task.DoesNotExist:
        print(f"Task with ID {task_id} does not exist.")
        return redirect("index")

def toggle_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
        return JsonResponse({"status": "success"})
def add_task(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            Task.objects.create(text=text)
    return redirect('index')


def add_record(request,ID,AMOUNT,STATUS,REF):
    if request.method == 'POST': # For debugging
        mark_as_visited(ID) # Call function from check.py
        return render(request,"add_budget.html",{"ID":ID,"AMOUNT":AMOUNT,"STATUS":STATUS,"REF":REF})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

# Delete record function using check.py
def delete_record_view(request, record_id):
    if request.method == 'POST':
        if mark_as_visited(record_id):  # Call function from check.py
            return redirect('track')
        else:
            return render(request, 'error.html', {'message': 'Failed to mark record as visited.'})
def index(request):
	tasks = Task.objects.all()
	return render(request, 'index.html', {'tasks': tasks})
def track(request):
	unvisited_records = process_unvisited_records()
	return render(request, 'track.html', {'records': unvisited_records})

def invest(request):
	return render(request,"invest.html")
def sponser(request):
	return render(request,"sponser.html")
def contact(request):
	if request.method == "POST":
		Name = request.POST["name"]
		email = request.POST["email"]
		contactno = request.POST["contactno"]
		enqtxt = request.POST["enqtxt"]
		regdate = timezone.now()
		x = contactM(name=Name,email=email,contactno = contactno,enqtxt = enqtxt,regdate = regdate)
		x.save()
		smssender.sendsms(contactno)
		messages.success(request,"Enquiry is saved")
		return redirect('contact')

	return render(request,"contact.html")
def help_(request):
	return render(request,"help.html")
def login_(request):
    return render(request,"login.html")
def logcode(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_staff:

				return redirect("index")
			else:
				messages.error(request, "Sry the access is denied")
				return redirect("contact")
		else:
			messages.error(request, "Invalid username or password")
			return redirect("login")
	return render(request, "login.html")
def planner(request):
	return render(request,"planner.html")
