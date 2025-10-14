class Product:
    """Product model representing an inventory item."""

    def __init__(self, product_id, name, sku, purchase_price, selling_price, quantity):
        self.product_id = product_id
        self.name = name
        self.sku = sku
        self.purchase_price = purchase_price
        self.selling_price = selling_price
        self.quantity = quantity
