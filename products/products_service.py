
class ProductsService:
    """
    Layer to manage products business logic
    """

    def __init__(self, repository):
        self.repository = repository

    def get_all_products(self):
        """
        Get all products
        :return: list of all products JSON formatted
        """
        return self.repository.get_products()

    def get_product_by_name(self, name):
        """
        Get product by name
        :param name: name of the product
        :return: the product JSON formatted or None if the product does not exist
        """
        return self.repository.get_by_name(name)

    def add_product(self, product):
        """
        Add a product to the inventory
        :param product: product to add JSON formatted
        :return: product added JSON formatted
        """
        return self.repository.add_product(product)

    def update_product_quantity(self, name, quantity):
        """
        Update product quantity by product name
        :param name: name of the product
        :param quantity: new quantity
        :return: product updated JSON formatted or None if the product does not exist
        """
        return self.repository.update_quantity(name, quantity)
