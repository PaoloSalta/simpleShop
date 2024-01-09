
class SalesService:
    """
    Layer to manage sales business logic
    """

    def __init__(self, product_service, repository):
        self.repository = repository
        self._product_service = product_service
        self._items = []
        self._total = 0
        self._net_total = 0

    def get_all_sales(self):
        """
        Get all sales
        :return: json containing all the sales
        """
        return self.repository.get_sales()

    def get_profits(self):
        """
        Calculate the gross and net profit of all sales
        :return: tuple with gross and net profit
        """
        sales = self.get_all_sales()
        net_total = 0
        total = 0
        for sale in sales:
            total += sale["total"]
            net_total += sale["netTotal"]

        return total, net_total

    def complete_sale(self):
        """
        Complete the current sale
        :return: sale dictionary or None if there are no items
        """
        if len(self._items) == 0:
            self._total = 0
            self._net_total = 0
            return

        sale = self.repository.add_sale({
            "items": self._items,
            "total": self._total,
            "netTotal": self._net_total
        })

        for item in self._items:
            product = self._product_service.get_product_by_name(item["name"])
            new_quantity = product["quantity"] - item["quantity"]
            self._product_service.update_product_quantity(product["name"], new_quantity)

        self._items = []
        self._total = 0
        self._net_total = 0

        return sale

    def add_item(self, item_name, quantity):
        """
        Adds an item to the current sale
        :param item_name: name of the product
        :param quantity: quantity to add to the sale
        """
        existing_product = self._product_service.get_product_by_name(item_name)

        if existing_product is None:
            print("This product does not exist")
            return

        sale_item = self._find_item_by_name(item_name)

        if sale_item is not None:
            if quantity + sale_item["quantity"] > existing_product["quantity"]:
                print(
                    f"Ordered quantity ({quantity + sale_item["quantity"]}) greater than stock ({existing_product['quantity']})"
                )
                return

            sale_item["quantity"] += quantity
        else:
            if quantity > existing_product["quantity"]:
                print(f"Ordered quantity ({quantity}) greater than stock ({existing_product['quantity']})")
                return

            self._items.append({
                "name": existing_product["name"],
                "quantity": quantity,
                "price": existing_product["sellingPrice"],
                "netPrice": existing_product["sellingPrice"] - existing_product["purchasePrice"]
            })

        self._net_total += quantity * (existing_product["sellingPrice"] - existing_product["purchasePrice"])
        self._total += quantity * existing_product["sellingPrice"]

    def _find_item_by_name(self, item_name):
        """
        Utility function to find an item by its name within the current sale
        :param item_name: name of the item
        :return: the matched item or None
        """
        for item in self._items:
            if item["name"] == item_name:
                return item

