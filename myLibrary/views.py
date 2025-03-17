from django.shortcuts import render 
def homepage(request):
    return render(request, "home.html")
def dashboard(request):
    return render(request,'customadmin/dashboard.html')



def get_student(request):
    return render(request,'customadmin/students.html')

def get_plan(request):
    return render(request,'customadmin/plans.html')


def get_trans(request):
    return render(request,'customadmin/transaction.html')