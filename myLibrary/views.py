from django.shortcuts import render

from myLibrary.decorators import role_required 

def homepage(request):
    return render(request, "home.html")

def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

@role_required("Vendor")
def vendor_dashboard(request):
    return render(request, "vendor_dashboard.html")

@role_required("Student")
def student_dashboard(request):
    return render(request, "student_dashboard.html")

@role_required("Vendor")
def dashboard(request):
    return render(request,'vender/index.html')



# def get_student(request):
#     return render(request,'customadmin/students.html')

# def get_plan(request):
#     return render(request,'customadmin/plans.html')


def get_trans(request):
    return render(request,'vender/transaction.html')