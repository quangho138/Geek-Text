from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class CartItem(models.Model):
    """
    Shopping cart item.
    Represents one book in a user's shopping cart.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        db_table = 'cart_item'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = [['user', 'book']]
    
    def __str__(self):
        return f"{self.user.username}: {self.quantity}x {self.book.name}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this cart item."""
        return self.quantity * self.unit_price
    
    def save(self, *args, **kwargs):
        """Auto-set unit_price from book if not provided."""
        if not self.unit_price:
            self.unit_price = self.book.price
        super().save(*args, **kwargs)