from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'basic': 'Hello World'
    }

    return render(request, 'Article/index.html', context)