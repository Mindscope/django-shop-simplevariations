# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.fields import CurrencyField
from shop.util.loader import get_model_string, load_class

OPTION_MODEL = getattr(settings, 'SHOP_PRODUCTVARIATION_MODEL', 'shop_simplevariations.models.defaults.Option')

#===============================================================================
# Text options
#===============================================================================

class TextOption(models.Model):
    """
    This part of the option is selected by the merchant - it lets him/her "flag"
    a product as being able to receive some text as an option, and sets its
    price.
    """
    name = models.CharField(max_length=255, help_text="A name for this option - this will be displayed to the user")
    description = models.CharField(max_length=255, null=True, blank=True, help_text='A longer description for this option')
    price = CurrencyField(help_text='The price for this custom text') # The price
    #length = models.IntegerField() # TODO: make this limiting in the form
    products = models.ManyToManyField(Product, related_name='text_options')
    
    class Meta:
        app_label = 'shop_simplevariations'
    
    def __unicode__(self):
        return self.name

class CartItemTextOption(models.Model):
    """
    An option representing a bit of custom text a customer can define, i.e.
    for engraving or custom printing etc...
    The text is stored on the cart item because we assume we will not engrave or
    print many times the same bit of text. 
    
    If your use case is different, you should probably make a "text bit" Model
    """
    text = models.CharField(max_length=255) # The actual text the client input
    
    text_option = models.ForeignKey(TextOption)
    cartitem = models.ForeignKey(CartItem, related_name='text_option')
    
    class Meta:
        app_label = 'shop_simplevariations'
    
    def __unicode__(self):
        return self.text


#===============================================================================
# Multiple choice options
#===============================================================================


class OptionGroup(models.Model):
    '''
    A logical group of options
    Example:

    "Colors"
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField() # Used in forms for example
    description = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product, related_name="option_groups",
                                      blank=True, null=True)
    
    class Meta:
        app_label = 'shop_simplevariations'

    def __unicode__(self):
        return self.name

    def get_options(self):
        Option = load_class(OPTION_MODEL, 'SHOP_PRODUCTVARIATION_MODEL')
        options = Option.objects.filter(group=self)
        return options


class OptionBase(models.Model):
    '''
    A product option. Example: Red, 10.0; Green: 20.0; Blue, 30.0;
    '''
    name = models.CharField(max_length=255)
    price = CurrencyField() # Can be negative
    group = models.ForeignKey(OptionGroup)
                              
    class Meta:
        abstract = True
        verbose_name = _('Group Option')
        verbose_name_plural = _('Group Options')

    def __unicode__(self):
        return self.name


class CartItemOption(models.Model):
    '''
    This holds the relation to product options from the cart item.
    It allows to know which options where selected for what cartItem.

    Generally, this is used by
    shop.cart.modifiers.product_options.ProductOptionsModifier
    '''
    cartitem = models.ForeignKey(CartItem)
    option = models.ForeignKey(load_class(OPTION_MODEL))
    
    class Meta:
        app_label = 'shop_simplevariations'
