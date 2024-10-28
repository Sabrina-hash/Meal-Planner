class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name         # The name of the ingredient (e.g., "flour")
        self.quantity = quantity # The quantity of the ingredient (e.g., 2.5)
        self.unit = unit         # The unit of measurement (e.g., "cups")

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name}"
    
    def print(self):
        print("We have {self.quantity} {self.unit}s of {self.name}.")