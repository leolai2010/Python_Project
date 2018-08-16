from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.conf import settings 
from .models import *
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
from django.core import serializers
import json
from django.db.models import Sum
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    return render(request, 'users/login.html')
def current_user(request):
	return User.objects.get(id=request.session['user_id'])
def registration(request):
    if request.method == "POST":
        result = User.objects.valdiate_info(request.POST)
        if 'errors' in result:
            for key,value in result['errors'].items():
                messages.error(request, value)
        else:
            messages.success(request, 'Registration Successful! Welcome!')
        return redirect('/')
    return redirect('/')
def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['user_email'])
        if len(users_with_email) > 0:
            print('user with the email exists! checking passswords now....')
            the_user = users_with_email.first()
            print('PW FROM DB:', the_user.password.encode('utf-8'))
            if bcrypt.checkpw(request.POST['password'].encode('utf-8'), the_user.password.encode('utf-8')):
                print('the passwords match! adding to session')
                request.session['user_id'] = the_user.id
                request.session['user_name'] = the_user.first_name
                return redirect('/dashboard')
            else:
                print('passwords do not match')
                messages.error(request, "invalid info")
                return redirect('/')
        else:
            messages.error(request, "Invalid Info, No Users with that Email")
            return redirect('/')
def logout(request):
    request.session.clear()
    return redirect('/')
def dashboard(request):
    user = current_user(request)
    context = {
        'user_info': user,
        'nervous_system': Ailment.objects.filter(system_ailment_id=1),
        'endocrine_system': Ailment.objects.filter(system_ailment_id=3),
        'circulation_system': Ailment.objects.filter(system_ailment_id=2),
        'lymphatic_system': Ailment.objects.filter(system_ailment_id=4),
        'respiratory_system': Ailment.objects.filter(system_ailment_id=5),
        'digestive_system': Ailment.objects.filter(system_ailment_id=6),
        'renal_system': Ailment.objects.filter(system_ailment_id=7),
        'reproductive_system': Ailment.objects.filter(system_ailment_id=8),
        'integumentary_system': Ailment.objects.filter(system_ailment_id=11),
        'muscular_system': Ailment.objects.filter(system_ailment_id=10),
        'skeletal_system': Ailment.objects.filter(system_ailment_id=9),
    }
    return render(request, 'users/dashboard.html', context)
def ailmentherb(request, ailmentid):
    ailment = Ailment.objects.get(id=ailmentid)
    context = {
        'ailment_info':ailment,
        'ailmentherbs':ailment.herb_ailments.all()
    }
    return render(request, 'users/ailmentherb.html', context)
def allherbs(request):
    context = {
        'allherbs':Herb.objects.all()
    }
    return render(request, 'users/allherbs.html', context)
def consult(request):
    user = current_user(request)
    context = {
        'user_info': User.objects.all(),
        'job_info': Job.objects.all(),
        'sol_info': Solution.objects.filter(comment_by = user),
        'my_job': user.users_job.all(),
        'user_name': user
    }
    return render(request, 'users/consult.html', context)
def addJob(request):
    return render(request, 'users/addJob.html')
def addJobfunction(request):
    if request.method == 'POST':
        errorms = Job.objects.validate_info(request.POST)
        if 'errors' in errorms:
            for key,value in errorms['errors'].items():
                messages.error(request,value)
            return redirect('/addJob')
        else:
            messages.success(request, "Consult has been successfully added!")
            return redirect('/consult')
def addSol(request, number):
    job = Job.objects.get(id=number)
    sol = Solution.objects.filter(id=job.id)
    context = { 
        'job_info': job,
        'sol_info': sol,
        'all_sol': Solution.objects.all()
    }
    return render(request, 'users/addSol.html', context)
def addSolfunction(request):
    if request.method == 'POST':
        errorms = Solution.objects.validate_info(request.POST)
        if 'errors' in errorms:
            for key,value in errorms['errors'].items():
                messages.error(request,value)
            return redirect('/addSol')
        else:
            messages.success(request, "Solution has been successfully added!")
            return redirect('/consult')            
def editJob(request, number):
    job = Job.objects.get(id=number)
    context = { 'job_info':job }
    return render(request, 'users/editJob.html', context)
def editJobfunction(request):
    if request.method == 'POST':
        update = Job.objects.validate_edit(request.POST)
        if 'errors' in update:
            for key,value in update['errors'].items():
                messages.error(request,value)
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.success(request, "Consult has been successfully updated!")
            return redirect('/consult')
def editSol(request, number):
    sol = Solution.objects.get(id=number)
    context = { 'sol_info':sol }
    return render(request, 'users/editSol.html', context)
def editSolfunction(request):
    if request.method == 'POST':
        update = Solution.objects.validate_edit(request.POST)
        if 'errors' in update:
            for key,value in update['errors'].items():
                messages.error(request,value)
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.success(request, "Consult has been successfully updated!")
            return redirect('/consult')
def destroy(request, number):
    deleter = Job.objects.get(id=number)
    deleter.delete()
    return redirect('/consult')
def deletesol(request, number):
    deleter = Solution.objects.get(id=number)
    deleter.delete()
    return redirect('/consult')
def cart(request):
    user = current_user(request)
    context = {
        'user_info': user,
        'item_info': Cart.objects.filter(purchase_by_id=user),
        'total': Cart.objects.filter(purchase_by_id=user).aggregate(Sum('item_added__price')),
        'key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'users/cart.html', context)
def addcart(request):
    if request.method == 'POST':
        Cart.objects.add_product(request.POST)
        return redirect('/cart')
def deletecart(request, number):
    deleter = Cart.objects.get(id=number)
    deleter.delete()
    return redirect('/cart')
def checkout(request):
    if request.method == 'POST':
        amountcharged = request.POST.get("amountcharged")
        print(amountcharged)
        charge = stripe.Charge.create(
            amount=amountcharged,
            currency='usd',
            description='Charge for Herbs',
            source=request.POST['stripeToken']
        )
        deleter = Cart.objects.all()
        deleter.delete()
        messages.success(request, "Thank you for shopping with us! You will receive a Confirmation E-mail shortly")
    return redirect('/cart')
def about(request):
    return render(request, 'users/about.html')
def contact(request):
    return render(request, 'users/contact.html')