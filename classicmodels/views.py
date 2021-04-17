from django.shortcuts import render
from django.shortcuts import redirect
import random

# Create your views here.
from django.http import HttpResponse

from classicmodels.models import *
from django.contrib import messages
from .forms import *
from django.core.exceptions import ValidationError


# Create your views here.

#def index(request):
#    return HttpResponse('Hello, welcome to the index page.')

def index(request):
    return render(request, 'classicmodels/home.html')
    #create a folder called templates inside of classicmodels
    
def conversion(request):
    return render(request, 'classicmodels/conversion.html')
    
def deposit(request):
    #current_user_id = current_user.id
    current_user = request.user
    # money = MonetaryInfo.objects.get(MonetaryInfo = current_user.monetary_id)
    # money.usd_sum = 500
    # money.save()
    print(str(current_user.id) + " " +current_user.username +" ")
    here = request.POST.get('depositUSD')
    print(here)
    obj = MonetaryInfo.objects.get(auth_user_id = current_user.id) #monetary_id = 1
    usdsum = obj.usd_sum
    cadsum = obj.cad_sum


    form = DepositForm(request.POST)
    if request.method == 'POST':
            form = DepositForm(request.POST)
            if form.is_valid():
                my_model = MonetaryInfo.objects.get(auth_user_id = current_user.id)

                
                
                
                # TRY TO DO SOME ERROR CLEANING UP LATER
                # if form.cleaned_data.get('depositCAD') < 0 or form.cleaned_data.get('depositUSD') < 0:
                #     messages.add_message(request, messages.INFO, 'Hello world.')

                cad = form.cleaned_data.get('depositCAD') 
                usd = form.cleaned_data.get('depositUSD')
                
                # DJANGO DOESNT TAKE IN BLANK VALUES SO YOU HAVE TO CHECK FOR IT MANUALLY
                if cad is None or cad > my_model.cad_sum:
                    cad = 0;
                if usd is None or usd > my_model.usd_sum:
                    usd = 0;


                my_model.cad_sum += cad # MAKE SURE IT TAKES IN THE FORM.DEPOSITCAD AND NOT THE NAME OF THE SUBMIT BUTTONS
                my_model.usd_sum += usd
                
                my_model.save()
                messages.success(request, f'Deposit successful!')
                return redirect('homepage')
    else:    
        print('i stg')    
        form = DepositForm()
    # obj.usd_sum = 534.343
    # obj.save()
    context = {
        'usdsum': usdsum,
        'cadsum': cadsum,
        'form' : form
    }
    return render(request, 'classicmodels/deposit.html', context )

def homepage(request):
    current_user = request.user
    user_id = current_user.id

    obj = MonetaryInfo.objects.get(auth_user_id = current_user.id) #monetary_id = 1
    usdsum = obj.usd_sum
    cadsum = obj.cad_sum

    context = {
        'usdsum': usdsum,
        'cadsum': cadsum
    }

    return render(request, 'classicmodels/homepage.html', context)

def logout(request):
    return render(request, 'classicmodels/logout.html')

def transfer(request):
    return render(request, 'classicmodels/transfer.html')

def userLogin(request):
        if request.user.is_authenticated():
            return  redirect('homepage')
        else:
            return render(request, 'classicmodels/userLogin.html')
    

def withdraw(request):
    current_user = request.user
    obj = MonetaryInfo.objects.get(auth_user_id = current_user.id) #monetary_id = 1
    usdsum = obj.usd_sum
    cadsum = obj.cad_sum

    form = WithdrawForm(request.POST)
    if request.method == 'POST':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                my_model = MonetaryInfo.objects.get(auth_user_id = current_user.id)
                cad = form.cleaned_data.get('withdrawCAD') 
                usd = form.cleaned_data.get('withdrawUSD')
                if cad is None or cad > my_model.cad_sum:
                    cad = 0;
                if usd is None or usd > my_model.usd_sum:
                    usd = 0;
                my_model.cad_sum -= cad 
                my_model.usd_sum -= usd
                
                my_model.save()
                messages.success(request, f'Deposit successful!')
                return redirect('homepage')
    else:    
        print('i stg')    
        form = WithdrawForm()
    # obj.usd_sum = 534.343
    # obj.save()
    context = {
        'usdsum': usdsum,
        'cadsum': cadsum,
        'form' : form
    }
    return render(request, 'classicmodels/withdraw.html', context)
    
def details(request):
    return render(request, 'classicmodels/details.html')
    
def product_details_view(request):
    #alt to below
    #query_set = Products.objects.all() #raw(use SQL syntax here, 'SELECT * FROM Products...') || use the cursorobject
    #context = {
    #   'object_instance' : query_set,
    #}

    #obj = Products.objects.get(productcode = 'S10_4757')
    obj = AuthUser.objects.get(id = 1)
    #context = {
    #    'title' : obj.productname,
    #    'price' : obj.msrp,
    #}
    context = {
        'username' : obj.username,
        'email' : obj.email
    }
    return render(request, 'classicmodels/productdetails.html', context)
    
def user_product_query_view(request):
    return render(request, 'classicmodels/userProductQuery.html')
    
def user_product_details_view(request):
    # current_user = request.user
    # minPrice = request.GET['minprice']
    # y = MonetaryInfo.objects.get(monetary_id = 1)
    # x = AuthUser.objects.get(id = current_user.id)
    # x.somenum = minPrice
    # x.save()
    new_entry = AuthUser(username='testUserr', password='test1234!', email = 'endrit@gmail.com', is_superuser = 0, is_staff = 0, is_active= 1, first_name = 'endrit', last_name = 'zenuni', date_joined = '2021-01-04')
    new_entry.save()

    # y.monetary_id = 1
    # y.save
    # maxPrice = request.GET['maxprice']
    #create a filtered list
    # query_set_product_price_filtered = []
    # #run the query : extract all results
    # query_set_product_price = Products.objects.all()
    # for object in query_set_product_price:
    #     if (object.msrp >= float(minPrice) and object.msrp <= float(maxPrice)):
    #         query_set_product_price_filtered.append(object)
            
    # context = {
    #     'object_instance' : query_set_product_price_filtered
    # }
    
    return render(request, 'classicmodels/userProductDetails.html')

def signup(request):
    debitcard = random.randint(1000000000000000,9999999999999999)
    cvv1 = random.randint(100, 999)
    bankacct = random.randint(100000000000,999999999999)


    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            newuser = form.save()
            print(newuser.pk)

            new_entry = MonetaryInfo(bank_account_number = bankacct, usd_sum = 0,cad_sum = 0, auth_user_id = newuser.pk)
            new_entry.save()


            new_entry2 = DebitCards(debit_card_id = 3,debit_card_num = debitcard, cvv = cvv1, expiration_date = '2021-01-04', fk_debit_cards_monetary_info1_id = new_entry.pk)
            new_entry2.save()
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            return redirect('homepage')
    else:
        form = UserRegisterForm()

    # x = AuthUser.objects.get(id)
    # print(x)
        
        

    
    # THIS IS HOW YOU DELTE STUFF, NOT THROUGH MY SQL \/ \/ \/ \/ \/
        # instance = MonetaryInfo.objects.get(monetary_id=7)
        # instance.delete()
    
    
    # new_entry = AuthUser(name='testUserr', password='test1234!', email = 'endrit@gmail.com')
    # new_entry.save()

    return render(request, 'classicmodels/signup.html', {'form':form})