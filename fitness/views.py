from django.shortcuts import render,redirect
from . services import  FitnessServices
from django.views.decorators.cache import never_cache
def index(request):
    return render(request,"index.html")
def login(request):
    if request.method=="POST":
        nm=request.POST.get("userid")
        pw=request.POST.get("password")
        obj=FitnessServices()
        data=obj.authenticate(nm,pw)
        if data:
            request.session["authenticated"]=True
            request.session["userid"]=nm
            return redirect("dashboard")
        else:
            return render(request,"loginfailed.html")
@never_cache        
def dashboard(request):
    if not request.session.get("authenticated"):
        return redirect("index")
    nm=request.session.get("userid")
    return render(request,"dashboard.html",{"user":nm})
def addprofile(request):
    return render(request,"newprofile.html")
from django.shortcuts import render
from .services import FitnessServices

def newprofile(request):
    if request.method == "POST":
        nm = request.POST.get("name")
        age = request.POST.get("age")
        gen = request.POST.get("gender")
        ht = request.POST.get("height")
        wt = request.POST.get("weight")
        ft = request.POST.get("food_type")
        st = request.POST.get("steps")

        obj1 = FitnessServices()
        data = obj1.newprofile(nm, age, gen, ht, wt, ft, st)

        if data == True:
            return render(request, "profileadded.html", {"msg": "New profile added successfully ✅"})
        elif data == "duplicate":
            # Reopen the same page with an error message
            return render(request, "newprofile.html", {"error": "Profile already exists! Please use a different name."})
        else:
            return render(request, "profilefailed.html", {"error": "Something went wrong while adding the profile."})

    else:
        # When the page is loaded initially (GET request)
        return render(request, "newprofile.html")

def  logout(request):
    request.session["authenticated"]=False
    return render(request,"logout.html")
def viewreport(request):
    obj2=FitnessServices()
    aa=obj2.report()
    return render(request,"viewreport.html",{"report":aa})
def modify(request):
    return render(request,"modify.html")
def modisuccess(request):
    if request.method=="POST":
        nm=request.POST.get("name")
        ht=request.POST.get("height")
        wt=request.POST.get("weight")
        ft=request.POST.get("food_type")
        new=FitnessServices()
        ans=new.change(nm,ht,wt,ft)
        if ans:
         return render(request,"modisuccess.html",{"modify":"Data has been Successfully Modified "})
def deletepage(request):
    return render(request,"deletepage.html")        
def delete(request):
     if request.method=="POST":
        nm=request.POST.get("name")
        lm=FitnessServices()
        ml=lm.delete1(nm)
        if ml:
            return render(request,"deletesuccess.html",{"delete":"Data has been Deleted Successfully "})
def search(request):
    return render(request,"searchpro.html")
def searchpro(request):
    if request.method=="POST":
        nm=request.POST.get("name")
        search=FitnessServices()
        get_user=search.search_user(nm)
        if get_user:
            return render(request,"foundprofile.html",get_user)
        else:
            return render(request,"notfound.html")
def generate_ai_advice(request):
    return render(request,"generate_ai_advice.html")
        







































        
