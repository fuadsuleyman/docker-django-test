from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from account.models import Customer
from django import template
from amdtelecom.utils import unique_slug_generator
from django.db.models.signals import pre_save
from .common import slugify

register = template.Library()


class Tag(models.Model):

    title = models.CharField('Title', max_length=100, db_index=True)

    # moderations
    is_published = models.BooleanField('is published', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tag'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ('-created_at', 'title')

    def __str__(self):
        return self.title


# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     parent_id = models.IntegerField(default=0)
#     description = models.TextField()
#     image = models.ImageField(upload_to='uploads/')

#     def __str__(self):
#         return f'{self.name}'

class Marka(models.Model):  
    # adidasin alt marka-lari saxlanilacaq
    
    # informations
    title = models.CharField('Title', max_length=100, db_index=True)
    image = models.ImageField('Image', blank=True, upload_to='marka_images')
    description = models.CharField(max_length=255, blank=True)
    slug = models.SlugField('Slug', editable=False, default='',  max_length=110, unique = True)

    # moderations
    status = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'marka'
        verbose_name = 'Marka'
        verbose_name_plural = 'Markas'
        ordering = ('-created_at', 'title')

    def __str__(self):
        return self.title 
    
    def save(self, *args, **kwargs):        
        super(Marka, self).save(*args, **kwargs)        
        self.slug = f'{slugify(self.title)}'       
        super(Marka, self).save(*args, **kwargs)


class Category(models.Model):

    # relation
    parent = models.ManyToManyField('self', related_name='children', blank=True)

    # information
    title = models.CharField('Title', max_length=100, db_index=True)
    image = models.ImageField('Image', blank=True, upload_to='categories_images')
    description = models.CharField(max_length=255, blank=True)
    slug = models.SlugField('Slug', max_length=110, editable=False, default='', unique = True)
    is_main = models.BooleanField('is_main', default=False)
    is_second = models.BooleanField('is_second', default=False)
    is_third = models.BooleanField('is_third', default=False)

    # moderations
    status = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('created_at', 'title')
        unique_together = ('slug',)

    def __str__(self):
        if self.is_main:
            s = f'{self.title}'
        elif self.is_second:
            s = f'{self.title}'
        else:
            s = f'{self.parent.all().first()} {self.title} '
        return s 

    def save(self, *args, **kwargs):        
        super(Category, self).save(*args, **kwargs)
        self.slug = f'{slugify(self.title)} {self.id}'       
             

        super(Category, self).save(*args, **kwargs)


# class Brand(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=400)
#     image = models.ImageField(upload_to='uploads/')

#     def __str__(self):
#         return f'{self.name}'




# class Color_p(models.Model):
#     color_name = models.CharField(max_length=50, blank=True, null=True, default=None)
#     color_code = models.CharField(max_length=50, blank=True, null=True, default=None)

#     def __str__(self):
#         return f'{self.color_name}'


class Product(models.Model):
    """
    very important table
    """
    # relations
    tags = models.ManyToManyField(Tag, related_name='products')
    same_product = models.ManyToManyField('self', related_name='same_products', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product_categories')
    # who_like = models.ManyToManyField(Customer, related_name='liked_products', blank=True)
    marka = models.ManyToManyField("Marka", related_name='marka')


    # informations
    color_title = models.CharField('Color Name', max_length=50, blank=True, null=True)
    color_code = models.CharField('Color code', max_length=50, blank=True, null=True)
    title = models.CharField('Title', max_length=100, db_index=True)
    slug = models.SlugField('Slug', max_length=110, unique = True, blank=True)
    sku = models.CharField('SKU', max_length=50, db_index=True)
    description = models.TextField('Description', null=True, blank=True)
    sale_count = models.IntegerField('Sale Count', default=0)
    is_new = models.BooleanField('is_new', default=True)
    is_featured = models.BooleanField('is_featured', default=False)
    is_discount = models.BooleanField('is_discount', default=False)

    # price info
    CHOICES = (
        (1, 'Not'),
        (2, 'Percent'),
        (3, 'Unit'),
    )
    price = models.DecimalField('Price', max_digits=7, decimal_places=2)
    discount_type = models.PositiveIntegerField("Discount Type", choices=CHOICES, default=1)
    discount_value = models.IntegerField('Discount Value', null=True, blank=True)

    # moderations
    status = models.BooleanField('is_active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def Marka(self):
        return ", ".join([str(p) for p in self.marka.all()])

    class Meta:
        unique_together = ('title', 'slug')
        # slug unique
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('-created_at', 'title')
    

    def get_price(self):
        if self.discount_type == 1:
            return self.price
        elif self.discount_type == 2:
            return self.price - (self.price * self.discount_value / 100)
        else:
            return self.price - self.discount_value
    
    def get_is_discount(self):
        if self.get_price() < self.price:
             is_discount = True
    
    def get_is_new(self):
        delta = datetime.now().date() - self.created_at
        if delta.days <= 30:
             is_new = True

    def __str__(self):
        return f'{self.title} {self.color_title}'


class Detail_name(models.Model):
    title = models.CharField('title', max_length=50)
    category = models.ManyToManyField('Category', related_name='detail_name')

    def get_categories(self):
        return ", ".join([str(p) for p in self.category.all()])

    class Meta:
        db_table = 'detail_name'
        verbose_name = 'Detail Name'
        verbose_name_plural = 'Detail Names'

    def __str__(self):
        return f'{self.title}'

class Detail(models.Model):
    value = models.CharField("Value", max_length=50)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product', blank=True, null=True)
    detail_name = models.ForeignKey('Detail_name', on_delete=models.CASCADE, db_index=True, related_name='detail')

    class Meta:
        db_table = 'detail'
        verbose_name = 'Detail'
        verbose_name_plural = 'Details'

    def __str__(self):
        return f'{self.value}'

class Product_detail_rel(models.Model):
    # in_stock = models.BinaryField(default=True)
    detail = models.ForeignKey('Detail', on_delete=models.CASCADE, db_index=True, related_name='product_detail_rel')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, db_index=True, related_name='product_detail_rel')


class Detail_value_name(models.Model):
    # in_stock = models.BinaryField(default=True)
    detail_name = models.ForeignKey('Detail_name', on_delete=models.CASCADE, db_index=True, related_name='_detail_name')
    detail_value = models.ForeignKey('Detail', on_delete=models.CASCADE, db_index=True, related_name='_detail_value')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, db_index=True, related_name='product_detail')




# slug 
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# herdefe Product-un instance-i yarandiqda asagidaki funqsiya ishe dushur
pre_save.connect(slug_generator, sender=Product)
# pre_save.connect(slug_generator, sender=Category)

# class Product(models.Model):
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='uploads/', blank=True, null=True)
#     sku = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=7, decimal_places=2, default=1)
#     price_old = models.DecimalField(max_digits=7, decimal_places=2, default=1)
#     description = models.TextField()
#     status = models.BooleanField(default=False)
#     date_posted = models.DateTimeField(auto_now_add=True)
#     internal_storage = models.CharField(max_length=50, blank=True, null=True, default=None)
#     ram = models.CharField(max_length=50, blank=True, null=True, default=None)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     color_pro = models.ForeignKey(Color_p, on_delete=models.CASCADE, default=1)

#     def __str__(self):
#         return f'{self.title}, {self.description}'
    
#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except:
#             url = ''
#         return url
    
    # @property
    # def sorted_image_set(self):
    #     return self.images.last().image

    # def get_last_image(self):
    #     try:
    #         last_image = self.images.last().image
    #     except AttributeError:
    #         last_image = self.image


# class Product_image(models.Model):
#     image = models.ImageField(upload_to='uploads/')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

#     def __str__(self):
#         return f'{self.product.title} image'


# class Product_details(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
#     size = models.CharField(max_length=50, blank=True, null=True, default=None)
#     # color = models.CharField(max_length=50, blank=True, null=True, default=None)
#     video = models.CharField(max_length=200, blank=True, null=True, default=None)
#     # internal_storage = models.CharField(max_length=50, blank=True, null=True, default=None)
#     external_storage = models.CharField(max_length=50, blank=True, null=True, default=None)
#     # ram = models.CharField(max_length=50, blank=True, null=True, default=None)
#     production_year = models.CharField(max_length=50, blank=True, null=True, default=None)
#     sim_count = models.CharField(max_length=50, blank=True, null=True, default=None)
#     sim_type = models.CharField(max_length=50, blank=True, null=True, default=None)
#     operation_system = models.CharField(max_length=100, blank=True, null=True, default=None)
#     operation_system_version = models.CharField(max_length=100, blank=True, null=True, default=None)
#     screen_size = models.CharField(max_length=50, blank=True, null=True, default=None)
#     resolution = models.CharField(max_length=50, blank=True, null=True, default=None)
#     back_camera = models.CharField(max_length=50, blank=True, null=True, default=None)
#     front_camera = models.CharField(max_length=50, blank=True, null=True, default=None)
#     battery = models.CharField(max_length=50, blank=True, null=True, default=None)
#     weigth = models.CharField(max_length=50, blank=True, null=True, default=None)
#     prosessor = models.CharField(max_length=50, blank=True, null=True, default=None)
#     security = models.CharField(max_length=50, blank=True, null=True, default=None)
#     guarantee = models.CharField(max_length=50, blank=True, null=True, default=None)
#     operator_prefix = models.CharField(max_length=50, blank=True, null=True, default=None)
#     wifi = models.BooleanField(blank=True, null=True, default=None)
#     allow_3G = models.BooleanField(blank=True, null=True, default=None)
#     allow_4G = models.BooleanField(blank=True, null=True, default=None)
#     nfc = models.BooleanField(blank=True, null=True, default=None)
#     gps = models.BooleanField(blank=True, null=True, default=None)
#     eye_recognition = models.BooleanField(blank=True, null=True, default=None)
#     waterproof = models.BooleanField(blank=True, null=True, default=None)
#     faceID = models.BooleanField(blank=True, null=True, default=None)
#     shockproof = models.BooleanField(blank=True, null=True, default=None)

#     def __str__(self):
#         return f'{self.product.title} details'


class Product_images(models.Model):
    # product-un butun sekilleri burda saxlanacaq
    # is_main true olan esas shekildi
    # is_second_main olan shekil coxlu product sehifesinde hover edende gelen sekildi

    # relations
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    # informations
    image = models.ImageField('Image', upload_to='product_images')
    is_main = models.BooleanField('Main Image', default=False) 
    is_second_main = models.BooleanField('Second Main Image', default=False) 

    # moderations
    status = models.BooleanField('Status', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        db_table = 'image'
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.image}'



class Product_colors(models.Model):
    # eyni bir product bir nece renge sahib ola bildiyi ucun yaratdim    
    # relations
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')

    # informations
    # coler_title = models.CharField('Title', max_length=50, db_index=True, blank=True, null=True)
    # color_code = models.CharField('Title', max_length=50, db_index=True, blank=True, null=True)

    # moderations
    status = models.BooleanField('Status', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_colors'
        verbose_name = 'Product_color'
        verbose_name_plural = 'Product_colors'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.title}'

