from django.shortcuts import render


def index(request):
    """ View for index """
    return render(request, 'home/index.html')
