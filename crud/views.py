from django.shortcuts import render, HttpResponse


# Create your views here.
def form(request):
    return render(request, 'crud/form.html')

