from .BaseModel import Model


class User(Model):

    def before_save(self):
        self.isAdmin = False
        del self.password_conf

    def login(self, email, password):
        user = (User().where("email", email)
                and User().where("password", password))
        if (user != []):
            return True
        else:
            return False

    def my_orders(self, user_id):
        return Order().get_user_orders(user_id)


class MealOption(Model):
    pass


class Menu(Model):
    def get_a_days_menu(self, day):
        i = 0
        while (i < len(self.menus)):
            if self.menus[i]['date'] == day:
                return self.menus[i]
            i = i + 1


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
