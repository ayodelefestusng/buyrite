from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseServerError
)
from .models import Category


# Create your views here.
def home(request):
   
   categories = Category.objects.all() 
   context={"categories":categories}
   return render(request,"home.html", context)


def car_view(request):
    return render(request, 'car.html')
