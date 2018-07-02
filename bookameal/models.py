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

    def check_meal_ids(self,ids):
        for id in ids:
            found = MealOption().where("id",id)
            if found == []:
                return "unfoundId"
        return "foundIds"

    def get_meals_by_ids(self,ids):
        meals = []
        i=0
        try:
            for i in ids:
                meal = MealOption().where("id",i)
                meals.append({
                    "id":meal[0].id,
                    "meal_option":meal[0].meal_option,
                    "meal_option_price":meal[0].meal_option_price
                    })
            return meals
        except Exception as e:
            return meals


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

    def check_for_meal_in_menu(self,meal,date):
        """The meal here comes as an integer, ie, as the meal id"""
        meal = Menu().where("id",meal) and Menu().where("date",date)
        if meal == []:
            return "menuHasNoMeal"
        return "menuHasMeal"


    def json_all(self):
        menus = list(map(lambda model: model.get_attributes(), self.get_all()))
        menu_with_extracted_meals = []

        for menu in menus:
            menu['menu'] = MealOption().get_meals_by_ids(menu['menu'])
            menu_with_extracted_meals.append(menu)
        return menu_with_extracted_meals




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



    def json_all(self):
        orders = list(map(lambda model: model.get_attributes(), self.get_all()))
        order_with_extracted_meals = []

        for order in orders:
            try:
                meal_option = MealOption().where("id",order['meal_option'])[0].meal_option
            except Exception as e:
                meal_option = "Meal not available"
            order_with_extracted_meals.append({
                    "customer_id":order['customer_id'],
                    "date":order['date'],
                    "meal_option":meal_option
                })
        return order_with_extracted_meals




