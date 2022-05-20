from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 64)
    description = models.TextField()
    begining_bid = models.FloatField(validators = [MinValueValidator(1)])
    final_bider = models.ForeignKey(User, blank = True, on_delete = models.CASCADE, related_name = "new_owner", null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "owner")
    category = models.CharField(blank = True, max_length = 64)
    active = models.BooleanField(blank = False, default = True)
    comments = models.ManyToManyField('Comment', related_name='comments_in_listing', blank=True)
    image = models.URLField(blank = True)

    def __str__(self):
        return (f"{self.title}; \t Begining Bid = ${self.begining_bid}")
    
class Bid(models.Model):
    current_price = models.FloatField(validators = [MinValueValidator(1)])
    listing = models.ForeignKey(Listing, verbose_name = "price", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    final_bider = models.BooleanField(default = False)
    
    def __str__(self):
        return (f"A bid of ${self.current_price} made for - \n{self.listing}\n by user - {self.user}")
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    textfield = models.TextField()
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)

    
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = False)
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, blank = False)
    watching = models.BooleanField(default=False)