from django.shortcuts import render, redirect


def view_bag(request):
    """ View that renders the shopping bag contents """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # session temporarily saves data, i.e users shopping bag contents.
    # Allows users to carry on shopping, deletes data once browser is closed.
    """ Collecting 'bag', if exists within the session, or create one if not. 
    (empty curly brackets {})"""
    bag = request.session.get('bag', {})
    """ Adding items to bag or updating the quantity """
    if item_id in list(bag.keys()):
        # Updating quantity in bag.
        bag[item_id] += quantity
    else:
        # Adding to empty bag.
        bag[item_id] = quantity
    # Overwriting 'bag' in the session with the updated one.
    request.session['bag'] = bag
    return redirect(redirect_url)
