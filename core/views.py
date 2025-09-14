from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.forms import productForm


@login_required
def staffPanel(request):
    return render(request, 'core/staff_panel.html')


@login_required
def add_product(request):
    if request.method == "POST":
        form = productForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()     # category logic is handled inside the form
            return redirect("product_list")
    else:
        form = productForm()

    return render(request, "core/add_product.html", {"form": form})