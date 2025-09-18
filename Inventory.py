class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity=1):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity

    def remove_item(self, item, quantity=1):
        if item in self.items:
            self.items[item] = max(0, self.items[item] - quantity)

    def display_inventory(self):
        print("Inventory:")
        for item, quantity in self.items.items():
            print(f"{item}: {quantity}")