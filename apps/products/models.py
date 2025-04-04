from django.db import models
from slugify import slugify

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        """  автоматическое создание слаг """
        if not self.slug:
            self.slug = slugify(self.name) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

        
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    article = models.CharField(max_length=5, unique=True, editable=False) 
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ForeignKey('ProductImage', null=True, blank=True, related_name='main_image',
                                   on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        
        """ каждый новый продукт получит уникальный артикул """
        if not self.article:
            self.article = str(Product.objects.count() + 1).zfill(5)

        super().save(*args, **kwargs)

        if not self.main_image and self.images.exists():
            self.main_image = self.images.filter(is_main=True).first() or self.images.first()
            super().save(update_fields=['main_image'])

    def __str__(self):
        return self.name

    @property
    def images(self):
        return self.images.all()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    is_main = models.BooleanField(default=False)  

    def save(self, *args, **kwargs):
        
        """  проверка основного изображения и дополн """
        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Image for {self.product.name}'

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: {self.value}'

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        """ сначала сохраняется сам объект отзыва, затем пересчитывается средний рейтинг товара """
        self.product.rating = self.product.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        self.product.save()

