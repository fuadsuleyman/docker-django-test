from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import Detail, Detail_name, Product, Marka, Category, Product_colors, Product_detail_rel, Product_images, Tag, Detail_value_name

admin.site.register(Product_colors)
# admin.site.register(Detail_value_name)
# admin.site.register(Detail_name)
admin.site.register(Product_detail_rel)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "is_main", "status")
    list_display_links = ("title",)
    readonly_fields = ('slug',)
    list_filter = ("title", "status")
    search_fields = ('title',)

@admin.register(Marka)
class MarkaAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    list_display_links = ("title",)



# @admin.register(Product_colors)
# class ColorpAdmin(admin.ModelAdmin):
#     list_display = ("id", "color_name", "color_code")
#     list_display_links = ("color_name",)

class ImageInline(admin.TabularInline):
    model = Product_images
    extra = 0

@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ("value", "detail_name", "product")

@admin.register(Detail_name)
class DetailNameAdmin(admin.ModelAdmin):
    list_display = ("title", "get_categories")

@admin.register(Detail_value_name)
class DetailValueAdmin(admin.ModelAdmin):
    list_display = ("detail_name", "detail_value", "product")
    list_display_links = ("detail_name",)
    
    # def get_categories(self, obj):
    #     return "\n".join([p.category for p in obj.category.all()])


# class DetailsInline(admin.TabularInline):
#     model = Detail
#     extra = 0

class DetailsInline(admin.TabularInline):
    model = Detail_value_name
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "Marka", "category", "price", "is_new", "get_image") #"get_image"
    list_display_links = ("title",)
    list_filter = ("price", "category")
    search_fields = ('title', "category__title", "Marka")
    inlines = [ImageInline, DetailsInline]
    lest_per_page = 20
    save_on_top = True
    save_as = True #create new product easy way

    fieldsets = (
        ('Relations', {
            'fields': ('category','marka', 'tags', 'same_product'),
        }),
        ('Informations', {
            'fields': (('title', 'slug'), 'sku', ('color_title', 'color_code',), 'description', 'sale_count', ('is_new', 'is_featured', 'is_discount'), 'status')
        }),
        ('Price Info', {
            'fields': ('price', 'discount_type', 'discount_value'),
        }),
    )


    def get_image(self, obj):
        return mark_safe(f'<img src={obj.images.get(is_main=True).imageURL} width="50" height="60"')


    get_image.short_description = "Image"
    
# admin.site.register(Product)
admin.site.register(Tag)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product_images)

@admin.register(Product_images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("image", "product")

# admin.site.register(Detail)