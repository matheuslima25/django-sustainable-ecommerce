from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from .constants import (CLOTHING_SIZES, GENDER_CHOICES, PRODUCT_TYPES,
                        SHOE_SIZES)


class Product(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    shoe_size = models.CharField(max_length=2, choices=SHOE_SIZES, blank=True, null=True)
    clothing_size = models.CharField(max_length=2, choices=CLOTHING_SIZES, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    resale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse('core:product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name} ({self.code})"


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_items')
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def is_out_of_stock(self):
        return self.quantity == 0

    def __str__(self):
        return f"{self.product.name} - {self.size} - Qty: {self.quantity}"


class StockOut(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_outs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    note = models.TextField(blank=True, help_text="Venda, doação, perda, etc.")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saída: {self.quantity} de {self.stock.product.name} em {self.date.strftime('%d/%m/%Y')}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="De 1 a 5 estrelas"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # um review por usuário

    def __str__(self):
        return f"{self.product.name} - {self.rating}★"
