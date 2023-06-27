from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render


from catalogue.models import *


def product_list(request):
    products = Product.objects.all()
    context = dict()
    context["products"] = products
    return render(request, 'catalogue/product_list.html', context=context)


def product_detail(request, upc):
    products = Product.objects.filter(upc=upc)
    if products.exists():
        product = products.first()
        return render(
            request, "catalogue/product_detail.html", {"product": product}
        )
    return HttpResponse(f"product not is active to this id.{upc}")


def products_search(request):
    title = request.GET.get('q')
    products = Product.objects.filter(
        Q(title__icontains=title) | Q(category__name__icontains=title),
    )
    if products.exists():
        return render(
            request, 'catalogue/product_list.html', {"products": products}
        )
    return HttpResponse(f"Products not found to title: {title}")


def category_list(request):
    categories = Category.objects.all()
    if categories.exists():
        return render(
            request, 'catalogue/category_list.html', {"categories": categories}
        )
    return HttpResponse("No categories found.")


def category_products(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse("Category dose not exist.")
    products = Product.objects.filter(
        Q(category=category) | Q(category__pattern__name=category.name)
    )

    if products.exists():
        return render(
            request, 'catalogue/product_list.html', {"products": products}
        )
    return HttpResponse("No products were found with this category.")


def table_list(request):
    tables = Table.objects.all()
    if tables.exists():
        return render(
            request, 'catalogue/table_list.html', {"tables": tables}
        )

    return HttpResponse("Not exist any table.")


def table_detail(request, upc):
    table = Table.objects.filter(upc=upc).first()
    if table:
        return render(
            request, 'catalogue/table_detail.html', {"table": table}
        )
    return HttpResponse("Table dose not exist.")


def hall_list(request):
    halls = Hall.objects.all()
    if halls.exists():
        return render(
            request, "catalogue/hall_list.html", {"halls": halls}
        )

    return HttpResponse("There is no hall.")


def hall_detail(request, pk):
    hall = Hall.objects.filter(Q(id=pk) or Q(pk=pk) or Q(upc=pk)).first()
    if hall:
        return render(
            request, "catalogue/hall_detail.html", {"hall": hall}
        )
    return HttpResponse("hall dose not exist.")
