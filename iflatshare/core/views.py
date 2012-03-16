from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.mail import send_mail

from datetime import date
from iflatshare.core.models import *
from forms import ItemForm, AddressForm, CalendarForm, FlatmateCreateForm

@login_required
def index(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    return HttpResponseRedirect('/avg_diff')

@login_required
def item(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = request.user
    if user.check_password(settings.DEFAULT_PASSWORD):
        return HttpResponseRedirect('/accounts/password/change/')    
    if user.profile.has_address():
        if request.method == 'POST':
            form = ItemForm(user, request.POST)
            if form.is_valid():
                form.save()
                when = date.today()
                year = when.strftime("%Y")
                month = when.strftime("%m")
                return monthly(request, year, month)
        else:
            form = ItemForm(user)
        return render_to_response('item.html', {'form': form,}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/profile/address/edit/')

@login_required
def monthly(request, year, month):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = request.user
    address = user.profile.address
    item_list = address.monthly_transaction(year, month)
    monthly_total = address.monthly_total(year, month)
    return render_to_response('monthly.html',{'item_list': item_list,'monthly_total': monthly_total, 'year':year, 'month':month},context_instance=RequestContext(request))

@login_required
def avg_diff(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = request.user
    if not user.profile.has_address():
        return HttpResponseRedirect('/profile/address/edit/')
    form = CalendarForm(request.POST or None)
    if form.is_valid():
        year = request.POST.get('year')
        month = request.POST.get('month')
    else:
        year = date.today().year 
        month = date.today().month
    user = request.user
    address = user.profile.address
    total = address.monthly_total(year, month)
    avg = address.monthly_avg(year, month)
    users = user.profile.get_housemates()
    when = date.today()
    today = when.strftime("%A %d, %B %Y")
    avg_diff =dict((usr.username, {'total': usr.profile.monthly_total(year, month), 'diff': usr.profile.monthly_total(year,month)-address.monthly_avg(year,month)}) for usr in users) 
    return render_to_response('avg_diff.html', {'form': form, 'avg_diff': avg_diff, 'avg': avg, 'total': total,'year':year, 'month':month, 'today':today},context_instance=RequestContext(request))

@login_required
def user_transaction(request, user_name, year, month):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = User.objects.get(username__iexact=user_name)
    logged_in_user = request.user
    if not logged_in_user.profile.is_housemate_of(user):
        return HttpResponseForbidden("<h1>You are not authorised to view this page</h1>")
    item_list = user.profile.monthly_transaction(year, month)
    monthly_total = user.profile.monthly_total(year, month)
    housemates = user.profile.get_housemates()
    return render_to_response('user_transaction.html',{'item_list': item_list, 'monthly_total':monthly_total, 'user_name':user_name,'year':year, 'month':month, 'housemates':housemates},context_instance=RequestContext(request))

@login_required
def monthly_category(request, year, month):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = request.user
    address = user.profile.address
    summary = address.category_summary(year, month)
    return render_to_response('monthly_category.html',{'summary':summary, \
            'year':year, 'month':month,
        },context_instance=RequestContext(request))


@login_required
def category_transaction(request, category_name, year, month):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = request.user
    address = user.profile.address
    category_transaction = address.category_transaction(category_name, year, month)
    summary = address.category_summary(year, month)
    return render_to_response('category_transaction.html',{'year':year, 'month':month, 'summary':summary,'category':category_name,'category_transaction':category_transaction},context_instance=RequestContext(request))

@csrf_protect
@login_required
def edit_address(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    profile = request.user.profile
    if profile.has_address():
        address = profile.address
    else:
        address = Address()
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save()
            if not profile.has_address():
                profile.address = address
                profile.status = 'present'
                profile.is_admin = True
                profile.user.is_staff = True
                profile.user.groups.add(Group.objects.get(name='Flat Admin'))
                profile.save()
                profile.user.save()
                return HttpResponseRedirect('/item/')
    else:
        form = AddressForm(instance=address)
    return render_to_response('address.html', {'form': form}, context_instance=RequestContext(request))

def thanks(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    return render_to_response('envelope/thanks.html', RequestContext(request))

def create_flatmate(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin')
    user = request.user
    admin = user.profile.get_admin()
    if request.method == 'POST':
        form = FlatmateCreateForm(request.POST)
        if form.is_valid():            
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            newuser = User.objects.create_user(name, email, password)
            profile = Profile(user=newuser)
            admin_address = user.profile.address
            profile.address = admin_address
            profile.status = 'present'
            profile.save()
            context = {'user': str(newuser).title(),
                       'admin': str(admin).title(),
                       'url': 'http://iflatshare.co.uk',
                       'password': settings.DEFAULT_PASSWORD }
            mailbody = render_to_string(\
                            'registration/confirm_flatmate.txt', context)
            send_mail('Welcome to iFlatshare', \
                      mailbody, \
                      settings.DEFAULT_FROM_EMAIL, [email,], \
                      fail_silently=False)
            return HttpResponseRedirect('/avg_diff/')
    else:
        form = FlatmateCreateForm()
    return render_to_response('create-flatmate.html', \
		    {'form':form, 'admin':admin}, context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html')
