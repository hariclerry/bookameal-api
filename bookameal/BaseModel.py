from abc import ABC

data = {}

last_insert_ids = {}


class Model(ABC):
    """Initialises the Model and sets the attributes passed thru the attributes dict"""

    def __init__(self, attributes={}):
        self.set_attributes(attributes)

    def set_attributes(self, attributes):
        for key in attributes:
            setattr(self, key, attributes[key])

    """initialises the Model, sets the attributes to be updated and saves it"""

    def update(self, attributes):
        self.set_attributes(attributes)
        data[self.model_name][self.model_index] = self
        return self

    @property
    def model_index(self):
        return data[self.model_name].index(self)

    def delete(self):
        del data[self.model_name][self.model_index]

    def makeId(self):
        last_id = last_insert_ids.get(self.model_name, 0)
        new_id = last_id + 1
        last_insert_ids[self.model_name] = new_id
        return new_id

    def persist(self):
        existing = data.get(self.model_name, [])
        self.before_persist()
        existing.append(self)
        data[self.model_name] = existing

    def save(self, attributes):
        self.__init__(attributes)
        self.id = self.makeId()
        if self.before_save():
            self.persist()
        else:
            return

    def get_attributes(self):
        return self.__dict__

    def get_all(self):
        try:
            return data[self.model_name]
        except Exception as e:
            return []

    def json_all(self):
        return list(map(lambda model: model.get_attributes(), self.get_all()))

    def before_save(self):
        return True

    def before_persist(self):
        pass

    @property
    def model_name(self):
        return self.__class__

    def find(self, id):
        try:
            return next(model for model in self.get_all() if model.id is id)
        except Exception as e:
            return None
        

    def first(self):
        try:
            return self.get_all()[0]
        except Exception as e:
            return None

    def where(self, key, value):
        return list(
            filter(lambda model: getattr(model, key) == value, self.get_all())
        )

    def __repr__(self):
        return "<{} {}>".format(self.__class__, self.id)
