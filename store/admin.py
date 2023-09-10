from django.contrib import admin
from .models import Product,Variation,ReviewRating,ProductGalery
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGaleryInline(admin.TabularInline):
    model=ProductGalery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','price','stock','modified_date','is_available','slug')
    inlines=[ProductGaleryInline]
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_filter=('product','variation_category','variation_value',)
    list_editable=('is_active',)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGalery)
