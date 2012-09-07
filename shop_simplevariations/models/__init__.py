from django.conf import settings

from shop.util.loader import load_class
from defaults import *
from bases import *

# Load the class specified by the user as the Option Model.
OPTION_MODEL = getattr(settings, 'SHOP_PRODUCTVARIATION_MODEL', 'shop_simplevariations.models.defaults.Option')

Option = load_class(OPTION_MODEL, 'SHOP_PRODUCTVARIATION_MODEL')