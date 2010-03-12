from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext, Context, loader
from forms import ItemForm
from cost_management.mcm.models import *
import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    return render_to_response('mcm/index.html')

@login_required
def item(request):
    user = User.objects.get_from_auth_user(request.user)
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
    user = User.objects.get_from_auth_user(request.user)
    address = user.address
    item_list = address.monthly_transaction(year, month)
    monthly_total = address.monthly_total(year, month)
    return render_to_response('mcm/item_list.html',{'item_list': item_list,'monthly_total': monthly_total, 'year':year, 'month':month},context_instance=RequestContext(request))

@login_required
def avg_diff(request, year, month):
    user = User.objects.get_from_auth_user(request.user)
    address = user.address
    total = address.monthly_total(year, month)
    avg = address.monthly_avg(year, month)
    users = address.user_set.all()
    avg_diff =dict((usr.username, {'total': usr.monthly_total(year, month), 'diff': usr.monthly_total(year,month)-address.monthly_avg(year,month)}) for usr in users) 
    return render_to_response('mcm/avg_diff.html', {'avg_diff': avg_diff, 'avg': avg, 'total': total},context_instance=RequestContext(request))

@login_required
def user_transaction(request, user_name, year, month):
    user = User.objects.get(username__iexact=user_name)
    logged_in_user = User.objects.get_from_auth_user(request.user)
    if not logged_in_user.is_housemate_of(user):
        return HttpResponseForbidden("<h1>You are not authorised to view this page</h1>")
    item_list = user.monthly_transaction(year, month)
    monthly_total = user.monthly_total(year, month)
    return render_to_response('mcm/monthly_transaction.html',{'item_list': item_list, 'monthly_total':monthly_total, 'user_name':user_name},context_instance=RequestContext(request))

@login_required
def monthly_category(request, year, month):
    user = User.objects.get_from_auth_user(request.user)
    address = user.address
    summery = address.category_summery(year, month)
    return render_to_response('mcm/monthly_category.html',{'summery':summery},context_instance=RequestContext(request))
