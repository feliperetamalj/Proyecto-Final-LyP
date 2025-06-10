# src/models/category.py
"""
Modelo de dominio: Category.
Identificación automática y serialización a/de dict.
"""
class Category:
    _id_counter = 1

    def __init__(self, name: str):
        self.id = Category._id_counter
        Category._id_counter += 1
        self.name = name

    def to_dict(self):
        return {'id': self.id, 'name': self.name}

    @classmethod
    def from_dict(cls, data):
        cat = cls(data['name'])
        cat.id = data['id']
        if data['id'] >= cls._id_counter:
            cls._id_counter = data['id'] + 1
        return cat
