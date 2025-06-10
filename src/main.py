# src/main.py
"""
CLI To-Do List: mezcla paradigmas procedural, OO y funcional.
"""
import sys
from datetime import datetime
from functools import reduce
from models import Task, Category
from data_access import load_data, save_data

def show_menu():
    print("""
Administrador de Tareas
1. Crear tarea
2. Editar tarea
3. Eliminar tarea
4. Asignar categoría
5. Listar tareas
6. Filtrar tareas
7. Mostrar métricas
8. Salir
""")

def get_choice(prompt, valid):
    choice = input(prompt).strip()
    while choice not in valid:
        print("Opción inválida.")
        choice = input(prompt).strip()
    return choice

def create_task(tasks):
    title = input("Título: ")
    desc = input("Descripción: ")
    tasks.append(Task(title, desc))
    print("Tarea creada.")

def edit_task(tasks):
    list_tasks(tasks)
    try:
        tid = int(input("ID a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    task = next((t for t in tasks if t.id == tid), None)
    if not task:
        print("No encontrada.")
        return
    title = input(f"Título ({task.title}): ") or task.title
    desc  = input(f"Descripción ({task.description}): ") or task.description
    task.update(title, desc)
    print("Actualizada.")

def delete_task(tasks):
    list_tasks(tasks)
    try:
        tid = int(input("ID a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return
    tasks[:] = [t for t in tasks if t.id != tid]
    print("Eliminada.")

def assign_category(categories, tasks):
    name = input("Nueva categoría: ")
    cat = Category(name)
    categories.append(cat)
    print("Categoría creada.")
    list_tasks(tasks)
    try:
        tid = int(input("ID tarea: "))
    except ValueError:
        print("ID inválido.")
        return
    task = next((t for t in tasks if t.id == tid), None)
    if task:
        task.category = cat
        print("Asignada.")
    else:
        print("Tarea no encontrada.")

def list_tasks(tasks):
    if not tasks:
        print("-- Sin tareas --")
        return
    for t in tasks:
        cat = t.category.name if t.category else 'Sin categoría'
        print(f"[{t.id}] {t.title} ({t.status}) - {cat}")

def filter_tasks(tasks):
    status = get_choice("Estado (pendiente,en progreso,completada): ",
                        ['pendiente','en progreso','completada'])
    sel = list(filter(lambda x: x.status == status, tasks))
    list_tasks(sel)

def show_metrics(tasks):
    total = len(tasks)
    done  = len([t for t in tasks if t.status == 'completada'])
    pct   = (done/total*100) if total else 0
    print(f"% completadas: {pct:.2f}%")
    durations = [
        (datetime.fromisoformat(t.end_date) - datetime.fromisoformat(t.start_date)).total_seconds()/3600
        for t in tasks if t.start_date and t.end_date
    ]
    avg = sum(durations)/len(durations) if durations else 0
    print(f"Duración promedio (h): {avg:.2f}")

def main():
    categories, tasks = load_data()
    while True:
        show_menu()
        choice = get_choice("→ ", [str(i) for i in range(1,9)])
        if choice == '1': create_task(tasks)
        elif choice == '2': edit_task(tasks)
        elif choice == '3': delete_task(tasks)
        elif choice == '4': assign_category(categories, tasks)
        elif choice == '5': list_tasks(tasks)
        elif choice == '6': filter_tasks(tasks)
        elif choice == '7': show_metrics(tasks)
        elif choice == '8':
            save_data(categories, tasks)
            print("Guardado. Adiós.")
            sys.exit()
        save_data(categories, tasks)

if __name__ == '__main__':
    main()
