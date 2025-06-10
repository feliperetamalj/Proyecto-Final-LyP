import json
from pathlib import Path
from models import Category, Task

DATA_FILE = Path('data/tasks.json')

def load_data():  #Devuelve (categorías, tareas) desde JSON.
   
    if not DATA_FILE.exists():
        return [], []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cats = [Category.from_dict(c) for c in data.get('categories', [])]
    tasks = [Task.from_dict(t) for t in data.get('tasks', [])]
    return cats, tasks

def save_data(categories, tasks): #Guarda categorías y tareas en .JSON
    DATA_FILE.parent.mkdir(exist_ok=True)
    payload = {
        'categories': [c.to_dict() for c in categories],
        'tasks': [t.to_dict() for t in tasks]
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
