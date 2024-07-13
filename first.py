import pandas as pd

# Load data from CSV
dat = pd.read_csv("data.csv")
df = pd.DataFrame(dat)
a = df.to_numpy()
print(a)

class Shop:
    def __init__(self, SI_no, Item_name, Rate):
        self.SI_no = SI_no
        self.Item_name = Item_name
        self.Rate = Rate
        self.Quantity_Available = self.get_quantity_available()

    def get_quantity_available(self):
        quantities = [x[2] for x in a if self.Item_name == x[1]]
        if quantities:
            return quantities[0]
        else:
            return 0

    def quantity_check(self):
        if self.Quantity_Available == 0:
            print(f"{self.Item_name} has run out.")
        return self.Quantity_Available

class Customer(Shop):
    def __init__(self, Item_name, Quantity, total=0):
        self.Item_name = Item_name
        self.Quantity = Quantity
        self.total = total
        super().__init__(SI_no=None, Item_name=Item_name, Rate=self.get_rate())

    def get_rate(self):
        rates = [x[3] for x in a if self.Item_name == x[1]]
        if rates:
            return rates[0]
        else:
            return 0

    def purchase(self):
        if self.Quantity_Available is None:
            self.Quantity_Available = self.get_quantity_available()
        self.Quantity_Available -= self.Quantity
        
    def bill(self):
        for i in a:
            if self.Item_name == i[1]:
                self.total += self.Quantity * i[3]

    def display_total(self):
        print(f"Total bill for {self.Quantity} {self.Item_name}(s): {self.total}")

# Example usage
s = Shop(2, "soap", 40)
print(s.quantity_check())
c = Customer("soap", 2)
c.bill()
c.purchase()
c.display_total()
