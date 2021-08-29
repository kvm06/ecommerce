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
        ('1mp', '1MP'),
        ('2mp', '2MP'),
        ('3mp', '3MP'),
        ('4mp', '4MP'),
        ('5mp', '5MP'),
        ('6mp', '6MP'),
        ('8mp', '8MP'),
    ]

    PLACE_CHOICES = [
        ('indoor', 'Внутренняя'),
        ('outdoor', 'Уличная'),
        ('universal', 'Универсальная'),
    ]

    ZOOM_CHOICES = [
        ('no', '1MP'),
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
        ('yes', 'Есть'),
        ('no', 'Нет'),
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
    SENSITIVITY_CHOICES = [
        ('0_01', '0.01л'),
        ('0_005', '0.005л'),
        ('0_0001', '0.0001лк'),
    ]

    VAND_PROT_CHOICES = [
        ('no', 'Нет'),
        ('ik08', 'IK08'),
        ('ik10', 'IK10'),
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

    resolution = models.CharField(max_length=250, choices=CheckboxChoices.RESOLUTION_CHOICES, default='0')
    corpus = models.CharField (max_length=250, choices=CheckboxChoices.CORPUS_CHOICES, default='0') 
    brand = models.CharField (max_length=250, choices=CheckboxChoices.CORPUS_CHOICES, default='0') 
    zoom = models.CharField (max_length=250, choices=CheckboxChoices.ZOOM_CHOICES, default='0') 
    sensor = models.CharField (max_length=250, choices=CheckboxChoices.SENSOR_CHOICES, default='0') 
    protection = models.CharField (max_length=250, choices=CheckboxChoices.PROTECTION_CHOICES, default='0') 
    ik = models.CharField (max_length=250, choices=CheckboxChoices.IK_CHOICES, default='0') 
    sensitivity = models.CharField (max_length=250, choices=CheckboxChoices.SENSITIVITY_CHOICES, default='0') 
    vand_protection = models.CharField (max_length=250, choices=CheckboxChoices.VAND_PROT_CHOICES, default='0') 

    has_audio_input = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0') 
    has_audio_output = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0') 
    has_wifi = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0') 
    has_microsd = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0') 
    has_alarm_input  = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0') 
    has_alarm_output  = models.BooleanField (choices=CheckboxChoices.YES_OR_NO_CHOICES, default='0') 

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
        return self.product
