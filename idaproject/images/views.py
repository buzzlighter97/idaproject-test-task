from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from api.models import Image
from .forms import ImageForm


def index(request):
    template = 'images/index.html'
    images_list = Image.objects.all()
    context = {
        'images_list': images_list,
    }
    
    return render(request, template, context)

def add_image(request):
    template = 'images/add-image.html'
    if request.method == 'POST':
        form = ImageForm(data=request.data)
        if form.is_valid():
            form.save()
            form = ImageForm()
            context = {'form': form}
            return render(request, template, form)
        return render(request, template, context)
    form = ImageForm()
    context = {'form': form}
    return render(request, template, context)