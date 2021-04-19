from django.shortcuts import render, redirect
import random
from django.http import HttpResponse
from classicmodels.models import *
from django.contrib import messages
from .forms import *
from django.core.exceptions import ValidationError
from datetime import datetime,timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import decimal


# Create your views here.

    
@login_required(login_url = 'userLogin')
def conversion(request):
    current_user = request.user
    obj = MonetaryInfo.objects.get(auth_user_id = current_user.id) #monetary_id = 1
    usdtocad = ConversionRate.objects.get(conversion_rate_id = 1)
    cadtousd = ConversionRate.objects.get(conversion_rate_id = 2)
    conrateusdtocad = usdtocad.value
    conratecadtousd = cadtousd.value
    print(conratecadtousd)

    usdsum = obj.usd_sum
    cadsum = obj.cad_sum

    if request.method == 'POST':
            form = DepositForm(request.POST)
            if form.is_valid():
                my_model = MonetaryInfo.objects.get(auth_user_id = current_user.id)
                print('hello')
                # TRY TO DO SOME ERROR CLEANING UP LATER
                # if form.cleaned_data.get('depositCAD') < 0 or form.cleaned_data.get('depositUSD') < 0:
                #     messages.add_message(request, messages.INFO, 'Hello world.')

                usd = form.cleaned_data.get('depositUSD')
                cad = form.cleaned_data.get('depositCAD')
                
                # DJANGO DOESNT TAKE IN BLANK VALUES SO YOU HAVE TO CHECK FOR IT MANUALLY
                if usd is None:
                    usd = 0;
                if cad is None:
                    cad = 0;

                my_model.usd_sum += decimal.Decimal(float(cad) * conratecadtousd)
                my_model.usd_sum -= decimal.Decimal(float(usd))
                my_model.cad_sum += decimal.Decimal(float(usd) * conrateusdtocad)
                my_model.cad_sum -= decimal.Decimal(float(cad))
                # MAKE SURE IT TAKES IN THE FORM.DEPOSITCAD AND NOT THE NAME OF THE SUBMIT BUTTONS
                my_model.save()
                messages.success(request, f'Deposit successful!')
                return redirect('homepage')
    else:      
        form = DepositForm()



    context = {
        'usdtocadrate' : conrateusdtocad,
        'cadtousdrate' : conratecadtousd,
        'usdsum': usdsum,
        'cadsum': cadsum,
        'form' : form
    }

    return render(request, 'classicmodels/conversion.html', context)

@login_required(login_url = 'userLogin')
def deposit(request):
    current_user = request.user
    # DEBUGGING PRINT STMNT
    print(str(current_user.id) + " " +current_user.username +" ")
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

                usd = form.cleaned_data.get('depositUSD')
                cad = form.cleaned_data.get('depositCAD') 
                
                # DJANGO DOESNT TAKE IN BLANK VALUES SO YOU HAVE TO CHECK FOR IT MANUALLY
                if usd is None:
                    usd = 0;
                if cad is None:
                    cad = 0;

                my_model.usd_sum += usd
                my_model.cad_sum += cad 
                # MAKE SURE IT TAKES IN THE FORM.DEPOSITCAD AND NOT THE NAME OF THE SUBMIT BUTTONS
                my_model.save()
                messages.success(request, f'Deposit successful!')
                return redirect('homepage')
    else:      
        form = DepositForm()

    context = {
        'usdsum': usdsum,
        'cadsum': cadsum,
        'form' : form
    }
    return render(request, 'classicmodels/deposit.html', context )

@login_required(login_url = 'userLogin')
def homepage(request):
    current_user = request.user
    obj = MonetaryInfo.objects.get(auth_user_id = current_user.id) #monetary_id = 1
    usdsum = obj.usd_sum
    cadsum = obj.cad_sum

    context = {
        'usdsum': usdsum,
        'cadsum': cadsum
    }

    return render(request, 'classicmodels/homepage.html', context)

@login_required(login_url = 'userLogin')
def logoutUser(request):
    logout(request)
    return redirect('userLogin')
    return render(request, 'classicmodels/userLogin.html')

@login_required(login_url = 'userLogin')
def deactivate(request):
    current_user = request.user
    u = User.objects.get(username = current_user.username)
    u.delete()
    return redirect('userLogin')
    return render(request, 'classicmodels/userLogin.html')

@login_required(login_url = 'userLogin')
def transfer(request):
    return render(request, 'classicmodels/transfer.html')

def userLogin(request):
    form = LoginForm(request.POST)
    if request.user.is_authenticated:
        form = LoginForm(request.POST)
        print('hello')
        return redirect('homepage')
    if form.is_valid():
        cleandata=form.cleaned_data
        print('hello5')
        #authenticate checks if credentials exists in db
        user=authenticate(username=cleandata['username'],
                          password=cleandata['password'])
        if user is not None:
            if user.is_active:
                print('hello3')
                login(request, user)
                return redirect('homepage')
            else:
                print('hello2')
                return redirect('userLogin')
        else:
            return HttpResponse("Invalid login")
    else:
        form=LoginForm()

    context = {
        'form':form
    }
    return render(request, 'classicmodels/userLogin.html', context)
    

@login_required(login_url = 'userLogin')
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

@login_required(login_url = 'userLogin')
def details(request):
    current_user = request.user
    username = current_user.username
    
    money = MonetaryInfo.objects.get(auth_user_id = current_user.id)
    bankAcct = money.bank_account_number
    debitcard = DebitCards.objects.get(fk_debit_cards_monetary_info1 = money.monetary_id).debit_card_num
    context = {
        'username': username,
        'bankAcct': bankAcct,
        'debitcard' : debitcard
    }
    return render(request, 'classicmodels/details.html', context)
    

def signup(request):
    debitcard = random.randint(1000000000000000,9999999999999999)
    cvv1 = random.randint(100, 999)
    bankacct = random.randint(100000000000,999999999999)
    #ADDING TWO YEARS FROM CURRENT TIME AND THEN PUTTING IT IN AN EXPIRATION FORMAT
    date = datetime.now() + timedelta(days=720)
    twoYearsFromNow= date.strftime('%m/%y')
    
    if request.user.is_authenticated:
        return redirect('homepage')

    else:
        if request.method =='POST':
            form = UserRegisterForm(request.POST)
            
            if form.is_valid():
                newuser = form.save()
                print(newuser.pk)

                new_entry = MonetaryInfo(bank_account_number = bankacct, usd_sum = 0,cad_sum = 0, auth_user_id = newuser.pk)
                new_entry.save()


                new_entry2 = DebitCards(debit_card_num = debitcard, cvv = cvv1, expiration_date = twoYearsFromNow, fk_debit_cards_monetary_info1_id = new_entry.pk)
                new_entry2.save()
                
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')

                new_user = authenticate(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        )
                login(request, new_user)
                
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