from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from cost_management.mcm.models import Category, User
from forms import ItemForm

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

def item_list(request):
    return render_to_response('mcm/item_list.html')