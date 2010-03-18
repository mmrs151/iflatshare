from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, Context, loader
from forms import ItemForm
from cost_management.mcm.models import *
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render_to_response('base.html',{},context_instance=RequestContext(request))

@login_required
def item(request):
    user = request.user
    if request.method == 'POST':
        form = ItemForm(user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/mcm/item/')
    else:
        form = ItemForm(user)
    return render_to_response('mcm/item.html', {'form': form,}, context_instance=RequestContext(request))

@login_required
def monthly(request, year, month):
    user = request.user
    address = user.profile.address
    item_list = address.monthly_transaction(year, month)
    monthly_total = address.monthly_total(year, month)
    return render_to_response('mcm/monthly.html',{'item_list': item_list,'monthly_total': monthly_total, 'year':year, 'month':month},context_instance=RequestContext(request))

@login_required
def avg_diff(request, year, month):
    user = request.user
    address = user.profile.address
    total = address.monthly_total(year, month)
    avg = address.monthly_avg(year, month)
    users = user.profile.get_housemates()
    avg_diff =dict((usr.username, {'total': usr.profile.monthly_total(year, month), 'diff': usr.profile.monthly_total(year,month)-address.monthly_avg(year,month)}) for usr in users) 
    return render_to_response('mcm/avg_diff.html', {'avg_diff': avg_diff, 'avg': avg, 'total': total},context_instance=RequestContext(request))

@login_required
def user_transaction(request, user_name, year, month):
    user = User.objects.get(username__iexact=user_name)
    logged_in_user = request.user
    if not logged_in_user.profile.is_housemate_of(user):
        return HttpResponseForbidden("<h1>You are not authorised to view this page</h1>")
    item_list = user.profile.monthly_transaction(year, month)
    monthly_total = user.profile.monthly_total(year, month)
    return render_to_response('mcm/user_transaction.html',{'item_list': item_list, 'monthly_total':monthly_total, 'user_name':user_name},context_instance=RequestContext(request))

@login_required
def monthly_category(request, year, month):
    user = request.user
    address = user.address
    summery = address.category_summery(year, month)
    return render_to_response('mcm/monthly_category.html',{'summery':summery},context_instance=RequestContext(request))


@login_required
def category_transaction(request, category_name, year, month):
    user = request.user
    address = user.profile.address
    category_transaction = address.category_transaction(category_name, year, month)
    summery = address.category_summary(year, month)
    return render_to_response('mcm/category_transaction.html',{'year':year, 'month':month, 'summery':summery,'category':category_name,'category_transaction':category_transaction},context_instance=RequestContext(request))
