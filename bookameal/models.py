from .basemodel import Model,data

class User(Model):

    # def before_persist(self):
    #     self.isAdmin = False
    #     del self.password_conf

    def before_save(self):
        user = User().where("email", self.email)
        if user != []:
            return False
        else:
            return True

    def check_email_existence(self,email):
        if User().where("email",email) == []:
            return "emailNotUsed"
        return "emailUsed"


    @staticmethod
    def isAdmin(email):
        admin = (User().where("isAdmin",True))
        if admin[0].email == email:
            return True
        return False


    def login(self, email, password):
        '''
        the variable is 'user' and not 'users' because only one user will always exist for an email
        '''
        user = User().where("email", email)
        if user == []:
            return False
        elif user[0].password == password:
            return True
        else:
            return False

    def my_orders(self, user_id):
        return Order().get_user_orders(user_id)


class MealOption(Model):
    def before_save(self):
        meal_option = MealOption().where("meal_option", self.meal_option)
        if meal_option != []:
            return False
        else:
            return True

    def check_meal_existence(self,meal_option):
        if MealOption().where("meal_option",meal_option) == []:
            return "mealNotRegistered"
        return "mealRegistered"


class Menu(Model):

    def before_save(self):
        menu = Menu().where("date", self.date)
        if menu != []:
            return False
        else:
            return True

    def check_menu_existence(self,date):
        if Menu().where("date",date) == []:
            return "menuNotRegistered"
        return "menuRegistered"


class Order(Model):

    def get_user_orders(self, user_id):
        for order in self.orders:
            if order['customer_id'] == user_id:
                return order

    def get_order(self, order_id):
        if self.orders[order_id] in self.orders:
            return self.orders[order_id]
        else:
            return "Order not found"
