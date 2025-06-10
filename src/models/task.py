# src/models/task.py
"""
Modelo de dominio: Task.
Incluye estados, fechas y serialización a/de dict.
"""
from datetime import datetime
from typing import Optional
from .category import Category

class Task:
    _id_counter = 1

    def __init__(self, title: str, description: str = '', category: Optional[Category] = None):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.title = title
        self.description = description
        self.category = category
        self.status = 'pendiente'        # pendiente, en progreso, completada
        self.start_date: Optional[str] = None
        self.end_date: Optional[str] = None

    def mark_in_progress(self):
        self.status = 'en progreso'
        if not self.start_date:
            self.start_date = datetime.now().isoformat()

    def mark_completed(self):
        self.status = 'completada'
        if not self.end_date:
            self.end_date = datetime.now().isoformat()

    def update(self, title: str = None, description: str = None, category: Category = None):
        if title:
            self.title = title
        if description:
            self.description = description
        if category:
            self.category = category

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.to_dict() if self.category else None,
            'status': self.status,
            'start_date': self.start_date,
            'end_date': self.end_date
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(data['title'], data.get('description', ''), None)
        obj.id = data['id']
        obj.status = data.get('status', 'pendiente')
        obj.start_date = data.get('start_date')
        obj.end_date = data.get('end_date')
        cat_data = data.get('category')
        if cat_data:
            obj.category = Category.from_dict(cat_data)
        if data['id'] >= cls._id_counter:
            cls._id_counter = data['id'] + 1
        return obj
