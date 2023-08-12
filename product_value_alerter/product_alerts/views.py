from django.shortcuts import render,redirect
from .forms import NewUserForm
from django.contrib import messages
from .serializers import ProductSerializer
from .models import userList,URLs_Feed
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
import requests as req
from bs4 import BeautifulSoup
import time

# Create your views here.
def userregister(request):
    if request.user.is_authenticated:
        return redirect(f"/product_list/{request.user.id}")
    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('user created')
            return redirect("/login/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={"register_form": form})

def userlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)   
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(f'/product_list/{request.user.id}')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def userlogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

def product_list(request,userid):
    if request.user.is_authenticated:
        try:
            user=userList.objects.get(user_id=userid)
        except:
            user_data=User.objects.get(id=userid)
            userList.objects.create(user=user_data)
            user=userList.objects.get(user_id=userid)
        products=user.Urls.all() # objects.filter(user_id=userid).order_by('-created_at')
        return render(request=request,template_name='productList.html',context={"products":products,"user":request.user})
    else:
        return redirect("/login/")

def fetch_data(amazon_base_url):
    r=req.get(amazon_base_url)
    # limit=7
    time.sleep(2)
    while r.status_code==503:
        r=req.get(amazon_base_url)
        time.sleep(3)
        # limit-=1
    if r.status_code==200:
        soup=BeautifulSoup(r.content,'lxml')
        product_name=soup.find('h1',class_="a-size-large a-spacing-none").get_text()
        Original_price=soup.find('div',class_="a-section a-spacing-small aok-align-center").find('span',class_="a-offscreen").get_text()[1:]
        str_price=Original_price.split(',')
        Str=''
        for x in str_price:
            Str+=x
        Original_price=int(Str)
        Current_price=soup.find('span',class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay").find('span',class_="a-price-whole").get_text()
        Current_price=Current_price.split(',')
        Str=''
        for x in Current_price:
            Str+=x
        Current_price=int(Str)

        return product_name,Original_price,Current_price
    else:
        print('site '+ f'{amazon_base_url}' + ' was not hit. Code:',r.status_code)
    
def add_product(request,userid):
    if request.method=="POST":
        if request.user.is_authenticated:
            data={'Url':request.POST['Url'],}
            if URLs_Feed.objects.filter(Url=data['Url']).exists():
                print('url probably added by some user')
                URL=URLs_Feed.objects.get(Url=data['Url'])
                if URL.users.filter(id=userid).exists():
                    print('user trying to add same url again!!')
                    pass
                else:
                    print('Mapping url to the current user..!')
                    URL.users.add(request.user)
                    user_data=userList.objects.get(id=userid)
                    user_data.Urls.add(URL)
                    print('Success')
                return redirect(f"/product_list/{userid}")
            else:       
                print('fetching data...!')
                product_name,Original_price,Current_price=fetch_data(data['Url'])
                data['product_name']=product_name
                data['Original_price']=Original_price
                data['Current_price']=Current_price
                # data['user']=str(request.user.id)
                data['lowest_price']=Current_price
                data['status']='No price Change..!'
                print('data',data)
                serializer = ProductSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    print('product is scheduled')
                    URL=URLs_Feed.objects.get(Url=data['Url'])
                    URL.users.add(request.user)
                    user_data=userList.objects.get(id=userid)
                    user_data.Urls.add(URL)
                    return redirect(f"/product_list/{userid}")
                else:
                    print("product is not scheduled")
                    return render(request=request,template_name="addproduct.html")
        else:
            return redirect('/')
    else:
        return render(request=request,template_name="addproduct.html")
