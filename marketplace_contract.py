from pydoc import describe
from pyteal import *

# we create a product class in order to make this code reuseable
class Product:
    # subclass variables defines the keys for our global state variable
    class Variables:
        # name of the product
        name = Bytes("NAME")
        # image for the product
        image = Bytes("IMAGE")
        # description of a product
        description = Bytes("DESCRIPTION")
        # price of a product
        price = Bytes("PRICE")
        # has this product been sold?
        sold = Bytes("SOLD")
    # subclass app methods deines methods available for the product
    class AppMethods: