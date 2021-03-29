# Models to manage our data (independent of Kivy)
class Pizza:

    name = ""
    ingredients = ""
    price = 0.0
    vegetarian = False

    def __init__(self, name, ingredients, price, vegetarian=False):
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.vegetarian = vegetarian

    """ Get pizza in dictionary format """
    def get_data_dictionary(self):
        return { "name" : self.name , "ingredients" : self.ingredients , "price" : self.price , "vegetarian" : self.vegetarian }

    """
        Representation of a pizza  
        ref. https://stackoverflow.com/questions/4932438/how-to-create-a-custom-string-representation-for-a-class-object
    """
    def __repr__(self):
        return "Pizza: name={0}, ingredients={1}, price={2}, vegetarian={3}".format(self.name, self.ingredients, self.price,self.vegetarian)


    """ 
        Build a list of pizza objects (static method)
        Mapping:  name with nom, ingredients with ingredients, price with nom and vegetarienne with vegetarian
        due to differences of naming between DB and RW
    """
    @staticmethod
    def build_list_data_for_rw(data):
        list = []  # List of pizza objects
        for pizza in data:
            pf = pizza["fields"] # retrieve fields only!
            # print("pizza - fields: " + str(pf))
            p = Pizza(pf.get('nom'), pf.get('ingredients'), pf.get('prix'), pf.get('vegetarienne'))
            list.append(p)  # add object into list
        return [pizza.get_data_dictionary() for pizza in list]