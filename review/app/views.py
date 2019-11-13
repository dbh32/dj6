from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    reviews = Review.objects.all().filter(product=product)

    if request.session['reviewed_products'] is None:
        request.session['reviewed_products'] = []

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()

        request.session['reviewed_products'].append(pk)
        request.session.modified = True

        ire = True  # is_review_exist

    elif request.method == 'GET':
        if pk in request.session['reviewed_products'] and reviews:
            ire = True
            form = None
        else:
            ire = False
            form = ReviewForm()

    for item in reviews:
        print(item)

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
        'is_review_exist': ire
    }

    return render(request, template, context)
