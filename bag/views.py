from django.shortcuts import render, redirect, reverse, HttpResponse


def view_bag(request):
    """ View that renders the shopping bag contents """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # session temporarily saves data, i.e users shopping bag contents.
    # Allows users to carry on shopping, deletes data once browser is closed.
    """ Collecting 'bag', if exists within the session, or create one if not. 
    (empty curly brackets {})"""
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
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


# Editing shopping bag quantity.
def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        # If quantity is greater then 0,
        if quantity > 0:
            # Get item id, drill into items by size dic. find the size of item,
            # Set it's quantity to the updated one, if adding quantity.
            bag[item_id]['items_by_size'][size] = quantity
        else:
            # This removes item quantity if quantity is 0.
            del bag[item_id]['items_by_size'][size]
            # If the only size in bag, remove item_id entirely.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            # pop method removes item from bag via item_id.
            bag.pop[item_id]
    # Overwriting 'bag' in the session with the updated one.
    request.session['bag'] = bag
    # Redirect to 'view_bag' url.
    return redirect(reverse('view_bag'))


# Removing items from shopping bag.
def remove_from_bag(request, item_id):
    """ Remove item from shopping bag """

    # try, tests block of code for errors.
    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            # If the only size in bag, remove item_id entirely.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        # Overwriting 'bag' in the session with the updated one.
        request.session['bag'] = bag
        # Returns a successful response, code 200.
        return HttpResponse(status=200)

    # except, handles errors.
    except Exception as e:
        # Returns error code 500.
        return HttpResponse(status=500) 
