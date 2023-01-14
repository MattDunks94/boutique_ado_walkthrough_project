from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Q is for making queries in one or two areas.(product name or description)
from django.db.models.functions import Lower
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # Sorting products via price, rating
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                # Double underscore 'drills' into model 'Category'.
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    # Sorting products in descending order
                    sortkey = f'-{sortkey}'

            # Sorts the products
            products = products.order_by(sortkey)

        # Filters by category name. (For the main nav links)
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
        # Search bar queries.
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!"
                    )
                return redirect(reverse('products'))
            # the '|' is the or argument, 'i' in front of 'contains'
            # makes the queries case insensitive.
            queries = Q(name__icontains=query) | Q(
                description__icontains=query
                )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    # pk = primary key
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add product to the store (admin use only) """
    # If user is not admin user.
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can add products.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        # New instance of the product form.
        # .FILES captures images if one was submitted.
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # Display success message if form is valid.
            messages.success(request, 'Successfully added product!')
            # Redirect to product detail via it's id.
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Display error message if form is not valid.
            messages.error(request, 'Failed to add product.\
                Please ensure the form is valid.')
    # Return empty form.
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit product in the store """
    # If user is not admin user.
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can edit products.')
        return redirect(reverse('home'))
        
    # Getting a product
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {product.name}')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product. \
                Please ensure the form is valid.'
                )
    else:
        # Instantiating the product form using the product.
        form = ProductForm(instance=product)
        # Display an info message.
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete product from the store. """
    # If user is not admin user.
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only store owners can delete products.'
            )
        return redirect(reverse('home'))

    # Getting the product.
    product = get_object_or_404(Product, pk=product_id)
    # Deleting the product.
    product.delete()
    # Display success message.
    messages.success(request, 'Product deleted!')
    # Redirect back to 'products' page.
    return redirect(reverse('products'))
