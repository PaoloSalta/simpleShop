from injector import Injector, inject
from tabulate import tabulate
from products import ProductsRepository, ProductsService, ProductsController
from sales import SalesRepository, SalesService, SalesController

COMMANDS = [
    {
        "command": "help",
        "description": "Show available commands",
    },
    {
        "command": "add",
        "description": "Add a product to stock"
    },
    {
        "command": "list",
        "description": "List all products in stock"
    },
    {
        "command": "sell",
        "description": "Register a product sell",
    },
    {
        "command": "profits",
        "description": "Show the profits of the store"
    },
    {
        "command": "exit",
        "description": "Close the program"
    }
]


def _show_commands():
    print(tabulate(COMMANDS, headers='keys'))


@inject
def main(products_controller: ProductsController, sales_controller: SalesController):
    _show_commands()

    command = input("\nWhat would you like to do?\n")

    while command != 'exit':

        if command not in [sub_array["command"] for sub_array in COMMANDS]:
            # If the command is not in the list, notify the user and ask for a new input
            print("Invalid command")

        if command == 'help':
            _show_commands()

        if command == "list":
            products_controller.get_all_products()

        if command == "add":
            products_controller.add_product()

        if command == "sell":
            sales_controller.add_sale()

        if command == "profits":
            sales_controller.get_profits()

        command = input("\nWhat would you like to do?\n")

    print("Thank you for using me!")
    exit(0)


def start():
    """
    Set up of the dependency injection
    Using the the dependency injection in order have a singleton for each component and use the instance variable of
    the repositories for managing the data
    """
    injector = Injector()
    injector.binder.bind(ProductsRepository, to=ProductsRepository())
    injector.binder.bind(ProductsService, to=ProductsService(injector.get(ProductsRepository)))
    injector.binder.bind(ProductsController, to=ProductsController(injector.get(ProductsService)))
    injector.binder.bind(SalesRepository, to=SalesRepository())
    injector.binder.bind(SalesService, to=SalesService(injector.get(ProductsService), injector.get(SalesRepository)))
    injector.binder.bind(SalesController, to=SalesController(injector.get(SalesService)))

    injector.call_with_injection(main)


if __name__ == '__main__':
    start()

