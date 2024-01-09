from tabulate import tabulate


class ProductsController:
    """
    Layer to manage the user input for products
    """

    def __init__(self, service):
        self.service = service

    def get_all_products(self):
        """
        Retrieve all the products and prompting them to the user
        """
        products = self.service.get_all_products()

        output = []
        for product in products:
            output.append({
                "Name": product["name"],
                "Quantity": product["quantity"],
                "Selling Price": f"€{product["sellingPrice"]:.2f}",
                "Purchase Price": f"€{product["purchasePrice"]:.2f}"
            })

        if len(products) > 0:
            print(tabulate(output, headers='keys', tablefmt='fancy_grid'))
        else:
            print("No products available")

    def add_product(self):
        """
        Asking the user to enter the data to insert or update a product
        """
        name = input("Enter product name: ")
        quantity = None
        while quantity is None or quantity < 0:
            try:
                quantity = int(input("Enter product quantity: "))
            except ValueError as e:
                print('Quantity must be an integer')
                continue

            try:
                assert quantity >= 0, "Quantity must be positive."
            except AssertionError as e:
                print(e)

        existing_product = self.service.get_product_by_name(name)

        if existing_product is not None:
            product = self.service.update_product_quantity(name, existing_product["quantity"] + quantity)
            print(f"Product added successfully: {quantity} x {product["name"]}")
            return

        purchase_price = None
        while purchase_price is None or purchase_price < 0:
            try:
                purchase_price = float(input("Enter product purchase price: "))
            except ValueError as e:
                print('Purchase price must be a float')
                continue

            try:
                assert purchase_price >= 0, "Purchase price must be positive."
            except AssertionError as e:
                print(e)

        selling_price = None
        while selling_price is None or selling_price <= 0:
            try:
                selling_price = float(input("Enter product selling price: "))
            except ValueError as e:
                print('Selling price must be a float')
                continue

            try:
                assert selling_price >= 0, "Selling price must be greater than 0."
            except AssertionError as e:
                print(e)

        product = self.service.add_product({
            "name": name,
            "quantity": quantity,
            "sellingPrice": round(selling_price, 2),
            "purchasePrice": round(purchase_price, 2)
        })

        print(f"Product added successfully: {product["quantity"]} x {product["name"]}")
