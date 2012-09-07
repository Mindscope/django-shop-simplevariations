# -*- coding: utf-8 -*-
from django.db import models
from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.fields import CurrencyField
from shop.util.loader import get_model_string

from shop_simplevariations.models.bases import OptionBase


#===============================================================================
# Multiple choice options
#===============================================================================


class Option(OptionBase):
    """
    Default model for Option
    """
    class Meta(object):
        abstract = False
        app_label = 'shop_optiongroups'

