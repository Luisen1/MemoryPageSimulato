import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import time
from ..controllers.simulator import MemorySimulator
from ..utils.constants import ProcessState, NUM_FRAMES, WINDOW_WIDTH, WINDOW_HEIGHT

class SimpleMemorySimulatorGUI:
    """Interfaz gráfica simplificada para el simulador de paginación de memoria."""
    
    def __init__(self, root):
        """Inicializa la interfaz gráfica."""
        self.root = root
        self.simulator = MemorySimulator()
        self.setup_ui()
        self.update_displays()
        
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.root.title("Simulador de Paginación de Memoria")
        self.root.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel de control
        self.setup_control_panel(main_frame)
        
        # Panel de visualización
        self.setup_visualization_panel(main_frame)
        
        # Panel de información
        self.setup_info_panel(main_frame)
    
    def setup_control_panel(self, parent):
        """Configura el panel de controles."""
        control_frame = ttk.LabelFrame(parent, text="Controles", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Crear Proceso", 
                  command=self.create_process_dialog).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(buttons_frame, text="Ejecutar Proceso", 
                  command=self.run_process_dialog).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Terminar Proceso", 
                  command=self.terminate_process_dialog).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Traducir Dirección", 
                  command=self.translate_address_dialog).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Simulación Auto", 
                  command=self.run_auto_simulation).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(buttons_frame, text="Limpiar Todo", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=5)
    
    def setup_visualization_panel(self, parent):
        """Configura el panel de visualización."""
        viz_frame = ttk.LabelFrame(parent, text="Visualización de Memoria", padding=10)
        viz_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Crear notebook para las pestañas
        self.notebook = ttk.Notebook(viz_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de marcos de memoria
        self.setup_memory_frames_tab()
        
        # Pestaña de tablas de páginas
        self.setup_page_tables_tab()
    
    def setup_memory_frames_tab(self):
        """Configura la pestaña de marcos de memoria."""
        frames_frame = ttk.Frame(self.notebook)
        self.notebook.add(frames_frame, text="Marcos de Memoria")
        
        # Frame para los marcos
        self.memory_frame = ttk.Frame(frames_frame)
        self.memory_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Etiqueta de título
        ttk.Label(self.memory_frame, text="Estado de Marcos de Memoria Física", 
                 font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Frame para la grilla de marcos
        self.frames_grid = ttk.Frame(self.memory_frame)
        self.frames_grid.pack()
        
        # Crear labels para cada marco
        self.frame_labels = []
        for i in range(NUM_FRAMES):
            row = i // 4
            col = i % 4
            
            frame_label = ttk.Label(self.frames_grid, text=f"Marco {i}\nLibre", 
                                   relief="solid", borderwidth=1, width=15, 
                                   anchor="center", background="lightgray")
            frame_label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            self.frame_labels.append(frame_label)
    
    def setup_page_tables_tab(self):
        """Configura la pestaña de tablas de páginas."""
        tables_frame = ttk.Frame(self.notebook)
        self.notebook.add(tables_frame, text="Tablas de Páginas")
        
        # Texto para mostrar las tablas de páginas
        self.tables_text = tk.Text(tables_frame, wrap=tk.WORD, font=('Courier', 10))
        scrollbar = ttk.Scrollbar(tables_frame, orient=tk.VERTICAL, command=self.tables_text.yview)
        self.tables_text.configure(yscrollcommand=scrollbar.set)
        
        self.tables_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_info_panel(self, parent):
        """Configura el panel de información."""
        info_frame = ttk.LabelFrame(parent, text="Información del Sistema", padding=10)
        info_frame.pack(fill=tk.X)
        
        # Crear notebook para la información
        info_notebook = ttk.Notebook(info_frame)
        info_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de procesos
        processes_frame = ttk.Frame(info_notebook)
        info_notebook.add(processes_frame, text="Procesos")
        
        self.processes_tree = ttk.Treeview(processes_frame, columns=('PID', 'Estado', 'Tamaño', 'Páginas', 'Marcos'), show='headings', height=6)
        self.processes_tree.heading('PID', text='PID')
        self.processes_tree.heading('Estado', text='Estado')
        self.processes_tree.heading('Tamaño', text='Tamaño (B)')
        self.processes_tree.heading('Páginas', text='Páginas')
        self.processes_tree.heading('Marcos', text='Marcos Asignados')
        
        self.processes_tree.column('PID', width=50)
        self.processes_tree.column('Estado', width=120)
        self.processes_tree.column('Tamaño', width=80)
        self.processes_tree.column('Páginas', width=60)
        self.processes_tree.column('Marcos', width=150)
        
        self.processes_tree.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de estadísticas
        stats_frame = ttk.Frame(info_notebook)
        info_notebook.add(stats_frame, text="Estadísticas")
        
        self.stats_text = tk.Text(stats_frame, height=6, state=tk.DISABLED, font=('Courier', 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
    
    def create_process_dialog(self):
        """Diálogo para crear un nuevo proceso."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nuevo Proceso")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Campos del formulario
        ttk.Label(dialog, text="Nombre del proceso:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Tamaño (bytes):").pack(pady=5)
        size_entry = ttk.Entry(dialog, width=30)
        size_entry.pack(pady=5)
        
        def create_process():
            try:
                name = name_entry.get().strip()
                size = int(size_entry.get())
                
                if not name:
                    messagebox.showerror("Error", "El nombre no puede estar vacío")
                    return
                
                if size <= 0:
                    messagebox.showerror("Error", "El tamaño debe ser mayor a 0")
                    return
                
                process = self.simulator.create_and_allocate_process(name, size)
                if process:
                    messagebox.showinfo("Éxito", f"Proceso '{name}' creado con PID {process.pid}")
                    self.update_displays()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo crear el proceso (memoria insuficiente)")
                
            except ValueError:
                messagebox.showerror("Error", "El tamaño debe ser un número entero")
        
        ttk.Button(dialog, text="Crear", command=create_process).pack(pady=10)
        
        name_entry.focus()
    
    def run_process_dialog(self):
        """Diálogo para ejecutar un proceso."""
        ready_processes = [p for p in self.simulator.memory_manager.get_all_processes() 
                          if p.state == ProcessState.READY]
        
        if not ready_processes:
            messagebox.showinfo("Información", "No hay procesos en estado READY")
            return
        
        # Crear diálogo de selección
        process_names = [f"PID {p.pid}: {p.name}" for p in ready_processes]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Ejecutar Proceso")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Seleccionar proceso:").pack(pady=10)
        
        listbox = tk.Listbox(dialog)
        for name in process_names:
            listbox.insert(tk.END, name)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def execute_selected():
            selection = listbox.curselection()
            if selection:
                selected_process = ready_processes[selection[0]]
                if self.simulator.memory_manager.run_process(selected_process):
                    messagebox.showinfo("Éxito", f"Proceso {selected_process.name} ejecutándose")
                    self.update_displays()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo ejecutar el proceso")
            else:
                messagebox.showwarning("Advertencia", "Seleccione un proceso")
        
        ttk.Button(dialog, text="Ejecutar", command=execute_selected).pack(pady=10)
    
    def terminate_process_dialog(self):
        """Diálogo para terminar un proceso."""
        active_processes = [p for p in self.simulator.memory_manager.get_all_processes() 
                          if p.state != ProcessState.TERMINATED]
        
        if not active_processes:
            messagebox.showinfo("Información", "No hay procesos activos")
            return
        
        # Crear diálogo de selección
        process_names = [f"PID {p.pid}: {p.name} ({p.state})" for p in active_processes]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Terminar Proceso")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Seleccionar proceso:").pack(pady=10)
        
        listbox = tk.Listbox(dialog)
        for name in process_names:
            listbox.insert(tk.END, name)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def terminate_selected():
            selection = listbox.curselection()
            if selection:
                selected_process = active_processes[selection[0]]
                self.simulator.memory_manager.deallocate_memory(selected_process)
                messagebox.showinfo("Éxito", f"Proceso {selected_process.name} terminado")
                self.update_displays()
                dialog.destroy()
            else:
                messagebox.showwarning("Advertencia", "Seleccione un proceso")
        
        ttk.Button(dialog, text="Terminar", command=terminate_selected).pack(pady=10)
    
    def translate_address_dialog(self):
        """Diálogo para traducir direcciones."""
        active_processes = [p for p in self.simulator.memory_manager.get_all_processes() 
                          if p.state != ProcessState.TERMINATED and p.allocated_frames]
        
        if not active_processes:
            messagebox.showinfo("Información", "No hay procesos con memoria asignada")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Traducir Dirección")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Selección de proceso
        ttk.Label(dialog, text="Proceso:").pack(pady=5)
        process_var = tk.StringVar()
        process_combo = ttk.Combobox(dialog, textvariable=process_var, state="readonly")
        process_combo['values'] = [f"PID {p.pid}: {p.name}" for p in active_processes]
        process_combo.pack(pady=5)
        
        # Dirección lógica
        ttk.Label(dialog, text="Dirección lógica:").pack(pady=5)
        address_entry = ttk.Entry(dialog, width=30)
        address_entry.pack(pady=5)
        
        # Resultado
        result_text = tk.Text(dialog, height=10, state=tk.DISABLED, font=('Courier', 9))
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        def translate():
            try:
                if not process_var.get():
                    messagebox.showwarning("Advertencia", "Seleccione un proceso")
                    return
                
                process_index = process_combo.current()
                selected_process = active_processes[process_index]
                logical_addr = int(address_entry.get())
                
                # Realizar traducción
                physical_addr = selected_process.translate_address(logical_addr)
                
                # Mostrar resultado
                result_text.config(state=tk.NORMAL)
                result_text.delete(1.0, tk.END)
                
                if physical_addr is not None:
                    page_num = logical_addr // 4096
                    offset = logical_addr % 4096
                    frame_num = physical_addr // 4096
                    
                    result = f"Traducción exitosa:\n\n"
                    result += f"Proceso: {selected_process.name} (PID {selected_process.pid})\n"
                    result += f"Dirección lógica: {logical_addr}\n"
                    result += f"Página: {page_num}\n"
                    result += f"Offset: {offset}\n"
                    result += f"Marco: {frame_num}\n"
                    result += f"Dirección física: {physical_addr}\n\n"
                    result += f"Tabla de páginas:\n"
                    for page, frame in selected_process.get_page_table().items():
                        result += f"  Página {page} → Marco {frame}\n"
                else:
                    result = f"Error: Dirección lógica {logical_addr} inválida\npara el proceso {selected_process.name}"
                
                result_text.insert(1.0, result)
                result_text.config(state=tk.DISABLED)
                
            except ValueError:
                messagebox.showerror("Error", "La dirección debe ser un número entero")
        
        ttk.Button(dialog, text="Traducir", command=translate).pack(pady=10)
        
        if active_processes:
            process_combo.current(0)
    
    def run_auto_simulation(self):
        """Ejecuta la simulación automática en un hilo separado."""
        def simulation_thread():
            # Crear algunos procesos automáticamente
            processes_data = [
                ("Editor", 8192),
                ("Navegador", 16384),
                ("Reproductor", 12288)
            ]
            
            created_processes = []
            for name, size in processes_data:
                process = self.simulator.create_and_allocate_process(name, size)
                if process:
                    created_processes.append(process)
                    self.root.after(100, self.update_displays)
                    time.sleep(1)
            
            # Simular ejecución
            for process in created_processes:
                if self.simulator.memory_manager.run_process(process):
                    self.root.after(100, self.update_displays)
                    time.sleep(1)
                    
                    # Terminar proceso
                    self.simulator.memory_manager.deallocate_memory(process)
                    self.root.after(100, self.update_displays)
                    time.sleep(1)
        
        threading.Thread(target=simulation_thread, daemon=True).start()
        messagebox.showinfo("Información", "Simulación automática iniciada")
    
    def clear_all(self):
        """Limpia todos los procesos y reinicia el simulador."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea limpiar todo?"):
            self.simulator = MemorySimulator()
            self.update_displays()
            messagebox.showinfo("Información", "Sistema reiniciado")
    
    def update_displays(self):
        """Actualiza todas las visualizaciones."""
        self.update_memory_visualization()
        self.update_page_tables_visualization()
        self.update_processes_info()
        self.update_statistics()
    
    def update_memory_visualization(self):
        """Actualiza la visualización de marcos de memoria."""
        frames = self.simulator.memory_manager.frames
        
        for i, frame_label in enumerate(self.frame_labels):
            if frames[i] is None:
                frame_label.config(text=f"Marco {i}\nLibre", background="lightgray")
            else:
                process = frames[i]
                # Colores según el estado del proceso
                color_map = {
                    ProcessState.NEW: "#FFE6E6",
                    ProcessState.READY: "#E6F3FF", 
                    ProcessState.RUNNING: "#E6FFE6",
                    ProcessState.BLOCKED: "#FFFFE6",
                    ProcessState.READY_SUSPENDED: "#F0E6FF",
                    ProcessState.BLOCKED_SUSPENDED: "#FFE6F0",
                    ProcessState.TERMINATED: "#E6E6E6"
                }
                color = color_map.get(process.state, "white")
                frame_label.config(text=f"Marco {i}\n{process.name}\nPID {process.pid}", 
                                 background=color)
    
    def update_page_tables_visualization(self):
        """Actualiza la visualización de tablas de páginas."""
        self.tables_text.config(state=tk.NORMAL)
        self.tables_text.delete(1.0, tk.END)
        
        active_processes = [p for p in self.simulator.memory_manager.get_all_processes()
                           if p.state != ProcessState.TERMINATED and p.allocated_frames]
        
        if not active_processes:
            self.tables_text.insert(1.0, "No hay procesos con memoria asignada")
        else:
            for i, process in enumerate(active_processes):
                if i > 0:
                    self.tables_text.insert(tk.END, "\n" + "="*50 + "\n\n")
                
                self.tables_text.insert(tk.END, f"Proceso: {process.name} (PID {process.pid})\n")
                self.tables_text.insert(tk.END, f"Estado: {process.state}\n")
                self.tables_text.insert(tk.END, f"Tamaño: {process.size} bytes\n")
                self.tables_text.insert(tk.END, f"Páginas necesarias: {process.pages_needed}\n\n")
                
                self.tables_text.insert(tk.END, "Tabla de Páginas:\n")
                self.tables_text.insert(tk.END, "Página → Marco\n")
                self.tables_text.insert(tk.END, "-" * 15 + "\n")
                
                page_table = process.get_page_table()
                for page, frame in sorted(page_table.items()):
                    self.tables_text.insert(tk.END, f"  {page:2d}   →   {frame:2d}\n")
                
                self.tables_text.insert(tk.END, "\n")
        
        self.tables_text.config(state=tk.DISABLED)
    
    def update_processes_info(self):
        """Actualiza la información de procesos."""
        # Limpiar tabla
        for item in self.processes_tree.get_children():
            self.processes_tree.delete(item)
        
        # Añadir procesos
        for process in self.simulator.memory_manager.get_all_processes():
            marcos_str = ', '.join(map(str, process.allocated_frames)) if process.allocated_frames else 'Ninguno'
            
            self.processes_tree.insert('', 'end', values=(
                process.pid,
                process.state,
                process.size,
                process.pages_needed,
                marcos_str
            ))
    
    def update_statistics(self):
        """Actualiza las estadísticas del sistema."""
        stats = self.simulator.memory_manager.get_memory_usage()
        
        stats_text = f"Estadísticas de Memoria:\n\n"
        stats_text += f"Marcos totales: {stats['total_frames']}\n"
        stats_text += f"Marcos utilizados: {stats['used_frames']}\n"
        stats_text += f"Marcos libres: {stats['free_frames']}\n"
        stats_text += f"Porcentaje de uso: {stats['usage_percentage']:.1f}%\n\n"
        
        # Estadísticas de procesos
        processes = self.simulator.memory_manager.get_all_processes()
        active_processes = [p for p in processes if p.state != ProcessState.TERMINATED]
        
        stats_text += f"Procesos:\n"
        stats_text += f"Total: {len(processes)}\n"
        stats_text += f"Activos: {len(active_processes)}\n"
        
        # Contar por estado
        state_counts = {}
        for process in active_processes:
            state_counts[process.state] = state_counts.get(process.state, 0) + 1
        
        if state_counts:
            stats_text += "\nPor estado:\n"
            for state, count in state_counts.items():
                stats_text += f"  {state}: {count}\n"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
