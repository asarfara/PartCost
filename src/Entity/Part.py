class Part:
    def __init__(self, name: str, price: float, supplier: str, type: str):
        """Create a part object.

        Args:
            name (str): Name of the part.
            price (float): Price of the part.
            supplier (str): Supplier name of the part.
            type (str): Type of the part.
        """

        self.name = name
        self.price = price
        self.supplier = supplier
        self.type = type
