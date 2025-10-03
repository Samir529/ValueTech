from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.http import JsonResponse
from core.forms import productForm, ProductColorForm
from store.models import ProductColor, subCategory


ProductColorFormSet = modelformset_factory(
    ProductColor,
    form=ProductColorForm,
    extra=1,
    can_delete=True
)


@login_required
def staffPanel(request):
    return render(request, 'core/staff_panel.html')


@login_required
def add_product(request):
    if request.method == "POST":
        form = productForm(request.POST, request.FILES)
        formset = ProductColorFormSet(request.POST, queryset=ProductColor.objects.none())

        if form.is_valid() and formset.is_valid():
            product = form.save()     # category logic is handled inside the form

            # save product colors
            for color_form in formset:
                if color_form.cleaned_data and not color_form.cleaned_data.get("DELETE"):
                    color = color_form.save(commit=False)
                    color.product = product
                    color.save()

            return redirect("product_list")
    else:
        form = productForm()
        formset = ProductColorFormSet(queryset=ProductColor.objects.none())

    return render(request, "core/add_product.html", {
        "form": form,
        "formset": formset,
    })


def admin_get_categories_and_subcategories(request):
    cat_id = request.GET.get('cat_id')
    if not cat_id:
        return JsonResponse({'results': []})
    subs = list(subCategory.objects.filter(category_id=cat_id).values('id', 'name'))
    return JsonResponse({'results': subs})

