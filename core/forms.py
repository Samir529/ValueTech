from django import forms
from store.models import Category, Product


class productForm(forms.ModelForm):
    # Select existing category
    existing_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Select from Existing Category",
        widget=forms.Select(
            attrs={"class": "form-control select-category"}
        ),
    )
    # Add new category
    new_category = forms.CharField(
        required=False,
        label="Add New Category",
        widget=forms.TextInput(
            attrs={
                "class": "form-control new-category",
                "placeholder": "Type a new category name",
            }
        ),
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "brand",
            "model",
            "color",
            "specification",
            "description",
            "regular_price",
            "special_price",
            "stock",
            "status",
            "product_code",
            "warranty",
            "warranty_details",
            "product_image",
        )
        labels = {
            "name": "Product Name",
            "slug": "Custom Slug",
            "brand": "Brand",
            "model": "Model",
            "color": "Color",
            "specification": "Specifications",
            "description": "Description",
            "regular_price": "Regular Price",
            "special_price": "Special Price",
            "stock": "Stock Quantity",
            "status": "Availability Status",
            "product_code": "Product Code",
            "warranty": "Warranty",
            "warranty_details": "Warranty Details",
            "product_image": "Product Image",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter product name", "class": "form-control"}),
            "slug": forms.TextInput(attrs={"placeholder": "Auto-generated if left empty", "class": "form-control"}),
            "brand": forms.TextInput(attrs={"placeholder": "Enter brand name", "class": "form-control"}),
            "model": forms.TextInput(attrs={"placeholder": "Enter model number/name", "class": "form-control"}),
            "color": forms.TextInput(attrs={"placeholder": "e.g. Black, Blue, Gray", "class": "form-control"}),
            "specification": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter specifications", "class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter product description", "class": "form-control"}),
            "regular_price": forms.NumberInput(attrs={"placeholder": "Enter regular price", "class": "form-control"}),
            "special_price": forms.NumberInput(attrs={"placeholder": "Enter special/discounted price", "class": "form-control"}),
            "stock": forms.NumberInput(attrs={"placeholder": "Enter available stock", "class": "form-control"}),
            "product_code": forms.TextInput(attrs={"placeholder": "Unique product code (SKU)", "class": "form-control"}),
            "warranty": forms.TextInput(attrs={"placeholder": "e.g. 1 Year", "class": "form-control"}),
            "warranty_details": forms.Textarea(attrs={"rows": 2, "placeholder": "Warranty details", "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        existing_category = cleaned_data.get("existing_category")
        new_category = cleaned_data.get("new_category")

        # Category validation
        if not existing_category and not new_category:
            raise forms.ValidationError("Please select from existing category OR add a new category.")

        if existing_category and new_category:
            raise forms.ValidationError("Choose either existing category OR add a new category, not both.")

        if new_category:
            # Check if category already exists
            category = Category.objects.filter(name__iexact=new_category).first()
            if category:
                raise forms.ValidationError(
                    f"Category '{new_category}' already exists. Please select it from existing categories."
                )
            category = Category.objects.create(name=new_category)
            cleaned_data["category"] = category
        else:
            cleaned_data["category"] = existing_category

        # --- Price validation (attach to field) ---
        regular_price = cleaned_data.get("regular_price")
        special_price = cleaned_data.get("special_price")

        if special_price is not None and regular_price is not None:
            if special_price >= regular_price:
                self.add_error("special_price", "Special price must be less than the regular price.")

        return cleaned_data

    def save(self, commit=True):
        product = super().save(commit=False)
        product.category = self.cleaned_data["category"]
        if commit:
            product.save()

        return product

