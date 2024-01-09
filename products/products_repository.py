import csv


class ProductsRepository:
    """
    Layer to manage products persistent data
    Using a CSV file for persistent data in order to have a tabular representation of the data
    """
    def __init__(self):
        self.file_name = 'resources/products.csv'
        self._products = []
        with open(self.file_name, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                for key, value in row.items():
                    if key in ["sellingPrice", "purchasePrice"]:
                        row[key] = float(value)
                    if key == "quantity":
                        row[key] = int(value)

                self._products.append(row)

    def get_products(self):
        """
        Returns a list of all the products JSON formatted
        :return: list of products
        """
        return self._products

    def get_by_name(self, product_name):
        """
        Returns the product with the given name
        :param product_name: name of the product
        :return: product with the given name or None if the product does exists
        """
        for product in self._products:
            if product['name'] == product_name:
                return product

        return None

    def update_quantity(self, product_name, quantity):
        """
        Updates the product with the given quantity
        :param product_name: product name
        :param quantity: new quantity to insert
        :return: updated product or None if the product does exists
        """
        product = next((item for item in self._products if item["name"] == product_name), None)

        if product is None:
            raise Exception("Product does not exists")

        product['quantity'] = quantity
        self._write_products()
        return product

    def add_product(self, product):
        """
        Adds a product to the inventory
        :param product: product to add JSON formatted
        :return: product inserted
        """
        self._products.append(product)
        self._write_products()
        return product

    def _write_products(self):
        """
        Utility function to write the products in the CSV file
        """

        with open(self.file_name, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self._products[0].keys())

            csv_writer.writeheader()
            csv_writer.writerows(self._products)

