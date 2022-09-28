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
        # allows a user to buy a product
        buy = Bytes("buy")
    # add function for creating the application which is the product in this case
    def application_creation(self):
        # this function returns a sequence
        return Seq([
            # assertions have to be true for the global puts to execute
            # asserts the application has five arguments
            Assert(Txn.application_args.length() == Int(4)),
            # asserts that the application has a specific note attached to it
            Assert(Txn.note() == Bytes("tutorial-markeplace:uv1")),
            # asserts that the price is greater than zero
            Assert(Btoi(Txn.application_args[3]) > Int(0)),
            # puts the name variable into the first application argument for the transaction
            App.globalPut(self.Variable.name, Txn.application_args[0]),
            # puts the image variable into the second application argument for the transaction
            App.globalPut(self.Variable.image, Txn.application_args[1]),
            # puts the description variable into the third application argument for the transaction
            App.globalPut(self.Variable.description, Txn.application_args[2]),
            # puts the price variable into the fourth application argument for the transaction
            App.globalPut(self.Variable.price, Btoi(Txn.application_args[3])),
            # puts the sold variable into the fifth application argument for the transaction
            App.globalPut(self.Variable.sold, Int(0)),
            # approve leaves a one at the top of the stack
            Approve()
        ])

    # adding a method which is a handler for buying a product
    # a handler is a callback routine which operates asynch when an event takes place
    def buy(self):
        # count is the number of products being purchases
        count = Txn.application_args[1]
        # the number of transaction in the group must be exactly two
        valid_number_of_transactions = Global.group_size() == Int(2)

        # performs validity checks
        valid_payment_to_seller = And(
            # the second transaction in the group must be the payment transaction
            Gtxn[1].type_enum() == TxnType.Payment,
            # the receiver of the payment should be the creator of the smart contract for the product
            Gtxn[1].receiver() == Global.creator_address(),
            # the total payment should be the cost of the product times the number being purchased
            Gtxn[1].amount() == App.globalGet(self.Variable.price) * Btoi(count),
            # makes sure that the sender of the transaction matches the address making the smart contract call
            Gtxn[1].sender() == Gtxn[0].sender(),
        )
