# store/forms.py
from django import forms
from store.models import Category, unique_slugify, subCategory, typesOfSubCategory


class CategoryBulkAddForm(forms.ModelForm):
    bulk_names = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Enter comma-separated category names"}),
        required=False,
        help_text="Add multiple categories at once, separated by commas."
    )

    class Meta:
        model = Category
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Save the single instance first if it has a name
        if instance.name and not instance.pk:
            if not instance.slug:
                instance.slug = unique_slugify(instance, instance.name)
            instance.save()

        # Handle bulk_names
        bulk_names = self.cleaned_data.get("bulk_names")
        if bulk_names:
            names = [name.strip() for name in bulk_names.split(",") if name.strip()]
            categories = []
            for name in names:
                cat = Category(name=name)
                cat.slug = unique_slugify(cat, name)
                categories.append(cat)
            Category.objects.bulk_create(categories)

        return instance


class SubCategoryBulkAddForm(forms.ModelForm):
    bulk_names = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Enter comma-separated sub-category names"}),
        required=False,
        help_text="Add multiple sub-categories at once, separated by commas."
    )

    class Meta:
        model = subCategory
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Save the single sub-category first if it has a name
        if instance.name and not instance.pk:
            if not instance.slug:
                instance.slug = unique_slugify(instance, instance.name)
            instance.save()

        # Handle bulk_names
        bulk_names = self.cleaned_data.get("bulk_names")
        if bulk_names:
            names = [name.strip() for name in bulk_names.split(",") if name.strip()]
            subcategories = []
            for name in names:
                subcat = subCategory(category=instance.category, name=name)
                subcat.slug = unique_slugify(subcat, name)
                subcategories.append(subcat)
            subCategory.objects.bulk_create(subcategories)

        return instance


class TypesOfSubCategoryBulkAddForm(forms.ModelForm):
    bulk_names = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Enter comma-separated type names"}),
        required=False,
        help_text="Add multiple types at once, separated by commas."
    )

    class Meta:
        model = typesOfSubCategory
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Save the single type first if it has a name
        if instance.name and not instance.pk:
            if not instance.slug:
                instance.slug = unique_slugify(instance, instance.name)
            instance.save()

        # Handle bulk_names
        bulk_names = self.cleaned_data.get("bulk_names")
        if bulk_names:
            names = [name.strip() for name in bulk_names.split(",") if name.strip()]
            types_list = []
            for name in names:
                type_obj = typesOfSubCategory(
                    category=instance.category,
                    sub_category=instance.sub_category,
                    name=name
                )
                type_obj.slug = unique_slugify(type_obj, name)
                types_list.append(type_obj)
            typesOfSubCategory.objects.bulk_create(types_list)

        return instance

