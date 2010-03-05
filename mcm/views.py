from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import ItemForm
from cost_management.mcm.models import Item
import datetime

def index(request):
    return render_to_response('mcm/index.html')

def item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/mcm/item/')
    else:
        form = ItemForm()
    return render_to_response('mcm/item.html', {'form': form,})

def monthly(request, year, month):
    item_list = Item.objects.monthly_transaction(year, month)
    monthly_total = Item.objects.monthly_total(year, month)
    return render_to_response('mcm/item_list.html',{'item_list': item_list,'monthly_total': monthly_total})
