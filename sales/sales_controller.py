from tabulate import tabulate


class SalesController:
    """
    Layer to manage the user input for sales
    """

    def __init__(self, service,):
        self._service = service

    def get_profits(self):
        """
        Extracting the products and prompting them to the user
        """
        profits = self._service.get_profits()
        output = [{
            "Gross Profit": f"€{profits[0]:.2f}",
            "Net Profit": f"€{profits[1]:.2f}"
        }]

        print(tabulate(output, headers='keys', tablefmt='fancy_grid'))

    def add_sale(self):
        """
        Asking the user to insert the products he wants to buy and registering the sale
        """
        sale_completed = False
        while not sale_completed:
            name = input("Enter product name: ")
            quantity = None
            while quantity is None or quantity <= 0:
                try:
                    quantity = int(input("Enter product quantity: "))
                except ValueError as e:
                    print('Quantity must be an integer')
                    continue

                try:
                    assert quantity > 0, "Quantity must greater than 0."
                except AssertionError as e:
                    print(e)

            self._service.add_item(name, quantity)

            confirm = input("Do you want to add another item? (yes/[no]) ")

            sale_completed = confirm != "yes"

        sale = self._service.complete_sale()

        if sale is None:
            return

        print("Sale added successfully\n")
        for item in sale["items"]:
            print(f"{item["quantity"]} x {item['name']}: €{item['price']:.2f}")

        print(f"Total: €{sale['total']:.2f}")
