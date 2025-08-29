from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseServerError
)
from .models import Category,Carousel


# Create your views here.
# def home(request):
   
#    categories = Category.objects.all() 
#    carousels = Carousel.objects.all() 
#    context={"categories":categories,"carousels":carousels,}
#    return render(request,"home.html", context)

from django.views.generic import ListView
from .models import Category, Carousel

class HomeView(ListView):
    model = Category
    template_name = 'home.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousels'] = Carousel.objects.all()
        return context
    

def car_view(request):
    return render(request, 'car.html')


# views.py
from django.shortcuts import render, redirect
from .forms import PostForm

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace with your actual URL
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})