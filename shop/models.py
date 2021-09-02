from django.db import models
from django.urls import reverse

# Create your models here.
class CheckboxChoices:
    BRAND_CHOICES = [
        ('dahua', 'Dahua'),
        ('hikvision', 'Hikvision'),
        ('hiwatch', 'HiWatch'),
    ]
    CORPUS_CHOICES = [
        ('dome', 'Купольная'),
        ('bullet', 'Цилиндрическая'),
        ('ptz', 'Поворотная'),
    ]
    RESOLUTION_CHOICES = [
        ('1mp', '1Мп'),
        ('2mp', '2Мп'),
        ('3mp', '3Мп'),
        ('4mp', '4Мп'),
        ('5mp', '5Мп'),
        ('6mp', '6Мп'),
        ('8mp', '8Мп'),
    ]

    PLACE_CHOICES = [
        ('indoor', 'Внутренняя'),
        ('outdoor', 'Уличная'),
        ('universal', 'Универсальная'),
    ]

    ZOOM_CHOICES = [
        ('no', 'Нет'),
        ('4x', '4x'),
        ('10x', '10x'),
        ('15x', '15x'),
        ('20x', '20x'),
        ('23x', '23x'),
        ('25x', '25x'),
    ]

    SENSOR_CHOICES = [
        ('cmos1_2', 'CMOS 1/2"'),
        ('cmos1_25', 'CMOS 1/2.5"'),
        ('cmos1_27', 'CMOS 1/2.7"'),
        ('cmos1_28', 'CMOS 1/2.8"'),
        ('cmos1_29', 'CMOS 1/2.9"'),
        ('cmos1_3', 'CMOS 1/3"'),
        ('cmos1_4', 'CMOS 1/4"'),
    ]

    YES_OR_NO_CHOICES = [
        (True, 'Есть'),
        (False, 'Нет'),
    ]

    PROTECTION_CHOICES = [
        ('no', 'Нет'),
        ('IP66', 'IP66'),
        ('IP67', 'IP67'),
    ]
    IK_CHOICES = [
        ('no', 'Нет'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
        ('30', '30'),
        ('40', '40'),
        ('50', '50'),
        ('60', '60'),
        ('70', '70'),
        ('80', '80'),
        ('100', '100'),
    ] 

    CATEGORY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    LENS_TYPE_CHOCIES = [
        ('fixed', 'Фиксированный'),
        ('motorized', 'Моторизированный')
    ]

    FOCAL_LENGTH = [
        ('2mm', '2мм'),
        ('2.7-8.1mm', '2.7-8.1мм'),
        ('2.7-13.5mm', '2.7-13.5мм'),
        ('2.8mm', '2.8мм'),
        ('2.8-12mm', '2.8-12мм'),
        ('3.6mm', '3.6мм'),
        ('4.8-120mm', '4.8-120мм'),
        ('5-75mm', '5-75мм'),
        ('6mm', '6мм'),
    ]
    
class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="category", blank=True)

    class Meta:
            ordering = ('name',)
            verbose_name = 'category'
            verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('product_by_category', args=[self.slug])
        
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product", blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    camera_category = models.CharField(max_length=250, choices=CheckboxChoices.CATEGORY_CHOICES, default='0', blank=True)
    resolution = models.CharField(max_length=250, choices=CheckboxChoices.RESOLUTION_CHOICES, default='0', blank=True)
    corpus = models.CharField (max_length=250, choices=CheckboxChoices.CORPUS_CHOICES, default='0', blank=True) 
    brand = models.CharField (max_length=250, choices=CheckboxChoices.BRAND_CHOICES, default='0', blank=True) 
    zoom = models.CharField (max_length=250, choices=CheckboxChoices.ZOOM_CHOICES, default='0', blank=True) 
    sensor = models.CharField (max_length=250, choices=CheckboxChoices.SENSOR_CHOICES, default='0', blank=True) 
    protection = models.CharField (max_length=250, choices=CheckboxChoices.PROTECTION_CHOICES, default='0', blank=True) 
    ik = models.CharField (max_length=250, choices=CheckboxChoices.IK_CHOICES, default='0', blank=True) 
    sensitivity = models.CharField (max_length=250, default='0', blank=True, null=True) 
    focal_length = models.CharField(max_length=250, choices=CheckboxChoices.FOCAL_LENGTH, default='0', blank=True)
    lens_type = models.CharField(max_length=250, choices=CheckboxChoices.LENS_TYPE_CHOCIES, default='0', blank=True)
    has_micro = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0', blank=True) 
    has_wifi = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0', blank=True) 
    has_microsd = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0', blank=True) 
    short_descr = models.CharField (max_length=100, default='0', blank=True) 
    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'product'

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']
        db_table = 'Cart'

    def __str__(self):
            return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['product']
        db_table = 'CartItem'

    def sum_total(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return str(self.product)
