import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
from models.category import Category
from models.task import Task
from data_access import load_data, save_data

# Apariencia y tema
ctk.set_appearance_mode("system")      # Opciones: "light", "dark", "system"
ctk.set_default_color_theme("blue")    # Temas: "blue", "dark-blue", "green"

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🏷️ To-Do List Moderno")
        self.geometry("900x650")

        # Configuración de grid: sidebar + panel + footer
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Cargo datos
        self.categories, self.tasks = load_data()

        # ─── SIDEBAR ────────────────────────────────────────────
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        ctk.CTkLabel(sidebar, text="Categorías",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))

        # ComboBox para filtrar por categoría
        self.category_var = tk.StringVar(value="Todas")
        cat_names = ["Todas"] + [c.name for c in self.categories]
        self.cat_combobox = ctk.CTkComboBox(
            sidebar,
            values=cat_names,
            variable=self.category_var,
            command=self.on_category_change
        )
        self.cat_combobox.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(sidebar, text="Mis Tareas",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        self.task_list_frame = ctk.CTkScrollableFrame(sidebar)
        self.task_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ─── PANEL PRINCIPAL ────────────────────────────────────
        panel = ctk.CTkFrame(self)
        panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkButton(panel, text="➕ Agregar Tarea", command=self.add_task).pack(pady=5)
        ctk.CTkButton(panel, text="🔄 Refrescar",     command=self.refresh_list).pack(pady=5)

        # ─── FOOTER ─────────────────────────────────────────────
        footer = ctk.CTkLabel(
            self,
            text=f"Fecha actual: {datetime.now().strftime('%Y-%m-%d')}",
            font=ctk.CTkFont(size=12)
        )
        footer.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0,10))

        # Primera carga de la lista
        self.refresh_list()

    def on_category_change(self, _):
        """Se dispara al cambiar la categoría seleccionada."""
        self.refresh_list()

    def refresh_list(self):
        """Refresca la lista de tareas, aplicando filtro de categoría."""
        sel_cat = self.category_var.get()
        # Limpio el frame
        for w in self.task_list_frame.winfo_children():
            w.destroy()

        # Aplico filtro
        tareas = self.tasks
        if sel_cat != "Todas":
            tareas = [t for t in tareas if t.category and t.category.name == sel_cat]

        # Repinto cada tarea
        for task in tareas:
            frame = ctk.CTkFrame(self.task_list_frame, corner_radius=6)
            frame.pack(fill="x", padx=5, pady=5)

            var = tk.BooleanVar(value=(task.status == "completada"))
            text = task.title
            if task.start_date:
                text += f"  📅 {task.start_date.split('T')[0]}"

            cb = ctk.CTkCheckBox(
                frame,
                text=text,
                variable=var,
                command=lambda t=task, v=var: self.toggle_task(t, v)
            )
            cb.pack(side="left", padx=5, pady=5)

            ctk.CTkButton(
                frame,
                text="✏️",
                width=30,
                command=lambda t=task: self.edit_task(t)
            ).pack(side="right", padx=2, pady=5)

            ctk.CTkButton(
                frame,
                text="🗑️",
                width=30,
                command=lambda t=task: self.delete_task(t)
            ).pack(side="right", padx=2, pady=5)

        # Guardar cambios
        save_data(self.categories, self.tasks)

    def add_task(self):
        """Diálogo para crear una nueva tarea con fecha y categoría."""
        title = simpledialog.askstring("Nueva tarea", "Título:", parent=self)
        if not title:
            return
        desc = simpledialog.askstring("Descripción", "Descripción:", parent=self)
        date_str = simpledialog.askstring(
            "Fecha (YYYY-MM-DD)",
            "Fecha de la tarea:",
            parent=self,
            initialvalue=datetime.now().strftime('%Y-%m-%d')
        )

        # Selección o creación de categoría
        category = None
        if self.categories:
            opts = [c.name for c in self.categories] + ["Nueva..."]
            sel = simpledialog.askstring("Categoría", f"Elige: {', '.join(opts)}", parent=self)
            if sel == "Nueva...":
                nombre = simpledialog.askstring("Nueva categoría", "Nombre:", parent=self)
                if nombre:
                    category = Category(nombre)
                    self.categories.append(category)
            else:
                for c in self.categories:
                    if c.name == sel:
                        category = c
                        break
        else:
            nombre = simpledialog.askstring("Categoría", "Nombre de categoría:", parent=self)
            if nombre:
                category = Category(nombre)
                self.categories.append(category)

        # Crear y asignar fecha
        new_task = Task(title, desc or "", category)
        try:
            new_task.start_date = datetime.strptime(date_str, '%Y-%m-%d').isoformat()
        except:
            new_task.start_date = datetime.now().isoformat()

        self.tasks.append(new_task)
        # Actualizar opciones de filtro
        self.cat_combobox.configure(values=["Todas"] + [c.name for c in self.categories])
        self.refresh_list()

    def edit_task(self, task):
        """Editar tarea y su fecha."""
        title = simpledialog.askstring("Editar tarea", "Título:", initialvalue=task.title, parent=self)
        if not title:
            return
        desc = simpledialog.askstring("Descripción", "Descripción:", initialvalue=task.description, parent=self)
        task.update(title, desc or task.description, task.category)

        current = task.start_date.split('T')[0] if task.start_date else datetime.now().strftime('%Y-%m-%d')
        date_str = simpledialog.askstring("Fecha (YYYY-MM-DD)", "Fecha de la tarea:",
                                          initialvalue=current, parent=self)
        try:
            task.start_date = datetime.strptime(date_str, '%Y-%m-%d').isoformat()
        except:
            pass

        self.refresh_list()

    def delete_task(self, task):
        """Eliminar tarea con confirmación."""
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?", parent=self):
            self.tasks.remove(task)
            self.refresh_list()

    def toggle_task(self, task, var):
        """Marcar/Desmarcar tarea completada."""
        if var.get():
            task.mark_completed()
        else:
            task.status = "pendiente"
            task.end_date = None
        self.refresh_list()

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
