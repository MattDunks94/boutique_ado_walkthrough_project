from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ View that renders the shopping bag contents """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
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
                # Adding new size of product already in the bag. 
                messages.success(
                    request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}'
                    )
                
            else:
                bag[item_id]['items_by_size'][size] = quantity
                # Added size success message.
                messages.success(
                    request, f'Added size {size.upper()} {product.name} to your bag'
                    )
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            # Added size success message.
            messages.success(
                request, f'Added size {size.upper()} {product.name} to your bag'
                )
    else:
        """ Adding items to bag or updating the quantity """
        if item_id in list(bag.keys()):
            # Updating quantity in bag.
            bag[item_id] += quantity
            # Updated quantity success message.
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_id]}'
                )
        else:
            # Adding to empty bag.
            bag[item_id] = quantity
            # Adding item to bag success message.
            messages.success(request, f'Added {product.name} to your bag')
    # Overwriting 'bag' in the session with the updated one.
    request.session['bag'] = bag
    return redirect(redirect_url)


# Editing shopping bag quantity.
def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
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
            # Adding new size of product already in the bag.
            messages.success(
                request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}'
                )
        else:
            # This removes item quantity if quantity is 0.
            del bag[item_id]['items_by_size'][size]
            # If the only size in bag, remove item_id entirely.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
                # Remove product size success message.
                messages.success(
                    request, f'Removed size {size.upper()} {product.name} from your bag'
                    )
    else:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            # Updating quantity success message.
            messages.success(
                request, f'Updated {product.name} quantity to {bag[item_id]}'
                )
        else:
            # pop method removes item from bag via item_id.
            bag.pop[item_id]
            # Removed product success message.
            messages.success(request, f'Removed {product.name} from your bag')
    # Overwriting 'bag' in the session with the updated one.
    request.session['bag'] = bag
    # Redirect to 'view_bag' url.
    return redirect(reverse('view_bag'))


# Removing items from shopping bag.
def remove_from_bag(request, item_id):
    """ Remove item from shopping bag """

    # try, tests block of code for errors.
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            # If the only size in bag, remove item_id entirely.
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(
                request, f'Removed size {size.upper()} {product.name} from your bag'
                )
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        # Overwriting 'bag' in the session with the updated one.
        request.session['bag'] = bag
        # Returns a successful response, code 200.
        return HttpResponse(status=200)

    # except, handles errors.
    except Exception as e:
        # Error message.
        messages.error(request, f'Error removing item {e}')
        # Returns error code 500.
        return HttpResponse(status=500) 
