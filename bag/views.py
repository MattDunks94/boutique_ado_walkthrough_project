from django.shortcuts import render


def view_bag(request):
    """ View that renders the shopping bag contents """
    return render(request, 'bag/bag.html')

