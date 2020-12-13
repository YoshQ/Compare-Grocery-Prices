class Product:
    
    def __init__(self):
        self.name = ""
        self.rating = ""
        self.number_of_reviews: ""
        self.price = ""
        self.price_per = ""
        self.earliest_arrival = ""
        self.availability = ""
        self.website = ""
        self.shipping_cost = ""
        self.size = ""
        self.url = ""

    def printProduct(self):
        if self.website == "Amazon":
            print("Name:", end = " ")
            print(self.name) 
            print("Rating:", end = " ")
            print(self.rating)
            print("Price:", end = " ")
            print(self.price)
        elif self.website == "PickNSave":
            print("Name:", end = " ")
            print(self.name)
            print("Price:", end = " ")
            print(self.price)
            print("Size:", end = " ")
            print(self.size)
        elif self.website == "FestivalFoods":
            print("Name:", end = " ")
            print(self.name)
            print("Price:", end = " ")
            print(self.price)
            print("Size:", end = " ")
            print(self.size)
            print("Price per unit:", end = " ")
            print(self.price_per)
            print("URL:", end = " ")
            print(self.url)            