import json


class SalesRepository:
    """
    Layer to manage sales persistent data
    Using a JSON file for persistent data, because it allows to keep track of the products within a sell in an easier way
    """
    def __init__(self):
        self.file_name = 'resources/sales.json'
        self._sales = []
        with open(self.file_name, 'r') as json_file:
            self._sales = json.load(json_file)

    def get_sales(self):
        """
        Get all sales
        :return: list of all sales in JSON format
        """
        return self._sales

    def add_sale(self, sale):
        """
        Saving a sale within the JSON file
        :param sale: JSON formatted sale
        :return: the sale saved
        """
        self._sales.append(sale)
        self._write_sales()
        return sale

    def _write_sales(self):
        """
        Utility function to write the sales in the JSON file
        """
        with open(self.file_name, 'w') as json_file:
            json_file.write(json.dumps(self._sales, indent=4, sort_keys=True))

