
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST["uname"]
        upass=request.POST["upass"]
        ucpass=request.POST["ucpass"]
        if uname=="" or upass=="" or ucpass=="":
            context["errmsg"]="Fields cannot be Empty"
            return render (request,"register.html",context)
        elif upass!=ucpass:
            context["errmsg"]="password and confirm password didnt match"
            return render (request,"register.html",context)
        else:
            try:
                u=User.objects.create(username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context["success"]="User Created SuccessFully"
                return render (request,"register.html",context)
                """return HttpResponse("User Created SuccessFully")"""
            except Exception:
                context["errmsg"]="user with same username already exist "
                return render (request,"register.html",context)
    else:
        return render (request,"register.html",context)

def loginuser(request):
       context={}
       if request.method=='POST':
           uname=request.POST.get('uname')
           upass=request.POST.get('upass')
           if uname=="" or upass=="":
               context["errmsg"]="Fields cannot be empty"
               return render(request,"login.html",context)
           else:
               user=authenticate(request , username=uname , password=upass)
               if user is not None:
                   login(request,user)
                   return redirect("/index")
               else:
                   context["errmsg"]="Credientials are incorrect"
                   return render(request,"login.html",context)
       else:
           return render(request,"login.html",context)

def logout(request):
    logout(request)
    #return redirect("home/")
    return redirect('login')


def catfilter(request,cv):#cv-catrgory value
    q1=Q(is_active=True)#Q- it is used for defining the conditions
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)#q1 and q2 are conditions.
    print(p)
    context={}
    context['Products']=p
    return render(request,'index.html',context)


def home(request):
    context={}
    p=Product.objects.filter(is_active=True)#This line will print all the products which are in active state
    context['Products']=p # Here products means the table which is in Admin side
    # print(p)
    return render(request,'index.html',context)


def sort(request,sv):#sv=sorting value
    print(type(sv))#This will print the type of product whether it is int,str,etc
    if sv == "0":
        col="-pcost"#ascending
    else:
        col="pcost"#descending
    p=Product.objects.filter(is_active=True).order_by(col)# This line will filter all the products which are in the active state
    context={}
    context["Products"]=p
    return render(request,"index.html",context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(pcost__gte=min)
    q2=Q(pcost__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context["Products"]=p
    return render(request,'index.html',context)

def product_details(request,pid):
    context={}
    context["Products"]=Product.objects.filter(id=pid)
    return render(request,"pdetails.html",context)


def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u)
        p=Product.objects.filter(id=pid)
        print(p)
        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        return HttpResponse("<p style='color: blue; font-weight: bold;'>Product added in the cart</p><img src='C:\django_project\petstoreproject\media\success.jpeg' alt='Success Image'><br><br><a href='/home'><button>Back to Home</button></a>&nbsp;&nbsp;<a href='/placeorder'><button>Proceed to Pay</button></a>")
    else:
        return redirect("/login")
    #return render(request,"cart.html")
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect("/viewcart")

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np =len(c)    #no of products
    for x in c:
        s=s+x.pid.pcost*x.qty
    context={}
    context['n']=np
    context['Products']=c
    context['total']=s
    return render(request,"viewcart.html",context)
def updateqty(request,qv,cid):
    #print(type(qv))
    c=Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    return redirect("/viewcart")

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print(c)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np =len(orders)    #no of products
    for x in orders:
        s=s+x.pid.pcost*x.qty
    context={}
    context['Products']=orders
    context['total']=s
    context['n']=np
    return render(request,'place_order.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np =len(orders)    #no of products
    for x in orders:
        s=s+x.pid.pcost*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_zdLBYxuK3Df0nN", "EoumSuSCNCWACMksHl3pTzD1"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    #print(payment)
    context={}
    context['data']=payment
    context['amt']=payment['amount']*100
    return render(request,"pay.html",context)

"""from django.shortcuts import get_object_or_404
from django.http import HttpResponse

def confirm_payment(request, order_id):
    # Assuming you have a way to confirm the payment status, and `order_id` is passed here

    # Your existing code to confirm payment...
    # ...

    # Assuming the payment is successful, now delete the associated orders
    orders_to_delete = Order.objects.filter(order_id=order_id)

    for order in orders_to_delete:
        order.delete()

    # Redirect or respond accordingly after successful payment and order deletion
    return HttpResponse("Payment successful. Orders deleted.")"""


def sendusermail(request):
        uemail=request.user.email
        print(uemail)
        msg="order details are:"
        send_mail(
        "Ekart order placed successfully!",
        msg,
        "anshusayare@gmail.com",
        [uemail],
        fail_silently=False,
        )
        return HttpResponse("mail send successfully")




def about(request):
    return render(request,'aboutus.html')

def contact(request):
    return render(request,'contact.html')

def indexpage(request):
    return render(request,"index.html")





def navbar(request):
    return render(request,"navbar.html")

def footer(request):
    return render(request,'footer.html')
