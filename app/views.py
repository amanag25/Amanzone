from ast import Or
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView

from .models import Customer,Cart,Product,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator





        

# class homeview(View):
# def get_name(request):
#         form = Searchform
#         return render(request, 'app/ex.html', {'form': form})
        
    # def post(self,request):
    #     form = Searchform(request.POST)
    #     if form.is_valid:
    #         text = form.cleaned_data('your_name')
    #         print(text)
    #     return render(request, 'app/ex.html', {'form': form})
        
class homeview(View):
    def get(self,request):

        form = Searchform()
        return render(request,'app/base.html',{'form':form})
    def post(self,request):
        
        form = Searchform(request.POST)
        if form.is_valid():
            data = form.cleaned_data['your_name']
            print(data)
        return render(request,'app/base.html',{'form':form})




class ProductView(View):
    def get(self,request):

        # The category here comes from models that is migrated into database and then comes here

        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        laptops = Product.objects.filter(category = 'L')
        

        # { the context is passed in these brakets and then rendered in the template}

        return render (request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops})


class ProductDetailView(View):
    def get(self,request,pk):
        
        product = Product.objects.get(pk = pk)
        item_already_in_cart = False
        if request.user.is_authenticated :
            item_already_in_cart = Cart.objects.filter(Q(product = product.id)
             &Q(user = request.user)).exists()

        return render(request , 'app/productdetail.html' , {'product':product,
         'item_already_in_cart':item_already_in_cart  })


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user,product= product).save()
    # return render(request, 'app/addtocart.html')

    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user = user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart , 'total_amount': total_amount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)




def minus_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id  = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))

        c.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            

        data = {
                
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)
@login_required
def buy_now(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    # add = Customer.objects.filter(user = request.user)
    Cart(user=user,product= product).save()
    # return render(request, 'app/addtocart.html')

    return redirect('/checkout')

@login_required
def address(request):
    add = Customer.objects.filter(user = request.user)
    return render(request,'app/address.html',{'add':add, 'active':'btn-primary'})



@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    return render (request, 'app/orders.html',{'order_placed':op})



def mobile(request ,data=None):

    # data default value is none if nothing is passed it wil show all the mobiles else it
    # will show mobiles according to the data passed
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'redmi' or data == 'samsung':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
        # lt is filter which filters and shows only the values lower than given value and 
        # similar behavior for gt
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt= 40000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt = 40000)
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request ,data=None):

    # data default value is none if nothing is passed it wil show all the mobiles else it
    # will show mobiles according to the data passed
    if data == None:
        laptops = Product.objects.filter(category = 'L')
    elif data == 'asus' or data == 'hp' or data == 'apple':
        laptops = Product.objects.filter(category = 'L').filter(brand = data)
    elif data == 'below':
        # lt is filter which filters and shows only the values lower than given value and 
        # similar behavior for gt
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__lt= 50000)
    elif data == 'above':
        laptops = Product.objects.filter(category = 'L').filter(discounted_price__gt = 50000)
    return render(request, 'app/laptop.html',{'laptops':laptops})


def topwear(request ,data=None):

    # data default value is none if nothing is passed it wil show all the mobiles else it
    # will show mobiles according to the data passed
    if data == None:
        topwears = Product.objects.filter(category = 'TW')
    elif data == 'allensolly' or data == 'coco' or data=='pepe':
        topwears = Product.objects.filter(category = 'TW').filter(brand = data)
    elif data == 'below':
        # lt is filter which filters and shows only the values lower than given value and 
        # similar behavior for gt
        topwears = Product.objects.filter(category = 'TW').filter(discounted_price__lt= 500)
    elif data == 'above':
        topwears = Product.objects.filter(category = 'TW').filter(discounted_price__gt = 500)
    return render(request, 'app/topwear.html',{'topwears':topwears})


def bottomwear(request ,data=None):

    # data default value is none if nothing is passed it wil show all the mobiles else it
    # will show mobiles according to the data passed
    if data == None:
        bottomwears = Product.objects.filter(category = 'BW')
    elif data == 'pepe' or data== 'levis' :
        bottomwears = Product.objects.filter(category = 'BW').filter(brand = data)
    elif data == 'below':
        # lt(lowerthan) is filter which filters and shows only the values lower than given value and 
        # similar behavior for gt
        bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__lt= 800)
    elif data == 'above':
        bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__gt = 800)
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self,request):

        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Conratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
    # print(total_amount)
    return render(request, 'app/checkout.html',{'add':add, 'totalamount': total_amount, 'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart =  Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user= user,customer =customer,product=c.product,quantity = c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form  = CustomerProfileForm()
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})


    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            # fetching current user from database
            user = request.user
            name  = form.cleaned_data['name']
            locality  = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state  = form.cleaned_data['state']
            zipcode  = form.cleaned_data['zipcode']
            reg  = Customer(user = user,name = name,locality = locality,city= city,state=state,zipcode= zipcode)
            reg.save()

            messages.success(request,'Congratulations!! Profile Updated Successfully')
#       active passes the btn-primary in the profile page
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
