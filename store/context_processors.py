from django.db.models import F
from store.models import Category

def categories_processor(request):
    categories = (
        Category.objects
        .filter(display_at_bar=True)  # Only categories marked for the bar
        .order_by(F('serial').asc(nulls_last=True))  # Order by serial, nulls go last
        .prefetch_related('subcategory_set__brandsortypesofsubcategory_set')
    )
    return {'categories': categories}
