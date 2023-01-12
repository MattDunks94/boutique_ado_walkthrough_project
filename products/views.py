from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
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


def add_product(request):
    """ Add product to the store (admin use only) """

    if request.method == 'POST':
        # New instance of the product form.
        # .FILES captures images if one was submitted.
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Display success message if form is valid.
            messages.success(request, 'Successfully added product!')
            # Return to add_product view.
            return redirect(reverse('add_product'))
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
