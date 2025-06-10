# src/gui.py
"""
Interfaz gráfica para el To-Do List usando Tkinter.
Incluye creación, edición, eliminación y marcado de tareas.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox
from models.category import Category
from models.task import Task
from data_access import load_data, save_data

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Administrador de Tareas")
        self.geometry("600x400")

        # Carga datos
        self.categories, self.tasks = load_data()

        # Lista de tareas
        self.task_listbox = tk.Listbox(self, height=15, width=50)
        self.task_listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_listbox.bind("<Double-Button-1>", lambda e: self.edit_task())

        # Panel de botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(padx=10, pady=10, side=tk.RIGHT, fill=tk.Y)

        tk.Button(btn_frame, text="➕ Agregar",   command=self.add_task,      width=15).pack(pady=5)
        tk.Button(btn_frame, text="✏️ Editar",   command=self.edit_task,     width=15).pack(pady=5)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=self.delete_task,   width=15).pack(pady=5)
        tk.Button(btn_frame, text="✅ Completar",command=self.complete_task, width=15).pack(pady=5)
        tk.Button(btn_frame, text="🔄 Refrescar", command=self.refresh_list,  width=15).pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        """Recarga la lista de tareas en el listbox."""
        self.task_listbox.delete(0, tk.END)
        for t in self.tasks:
            status = "✓" if t.status == "completada" else "•"
            cat    = f"[{t.category.name}]" if t.category else ""
            self.task_listbox.insert(tk.END, f"{status} ({t.id}) {t.title} {cat}")

    def add_task(self):
        """Diálogo para crear una nueva tarea."""
        title = simpledialog.askstring("Nueva tarea", "Título:")
        if not title:
            return
        desc = simpledialog.askstring("Descripción", "Descripción:")
        # Opcional: asignar categoría al crear
        cat_name = simpledialog.askstring("Categoría (opcional)", "Nombre de categoría:")
        category = None
        if cat_name:
            category = Category(cat_name)
            self.categories.append(category)

        new = Task(title, desc or '', category)
        self.tasks.append(new)
        self._save_and_refresh()

    def edit_task(self):
        """Editar título y descripción de la tarea seleccionada."""
        sel = self.task_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        task = self.tasks[idx]
        title = simpledialog.askstring("Editar título", "Título:", initialvalue=task.title)
        desc  = simpledialog.askstring("Editar descripción", "Descripción:", initialvalue=task.description)
        if title:
            task.update(title, desc or task.description)
            self._save_and_refresh()

    def delete_task(self):
        """Eliminar la tarea seleccionada."""
        sel = self.task_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"):
            del self.tasks[idx]
            self._save_and_refresh()

    def complete_task(self):
        """Marcar la tarea seleccionada como completada."""
        sel = self.task_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        task = self.tasks[idx]
        task.mark_completed()
        self._save_and_refresh()

    def _save_and_refresh(self):
        """Helper: guardar datos y refrescar UI."""
        save_data(self.categories, self.tasks)
        self.refresh_list()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
