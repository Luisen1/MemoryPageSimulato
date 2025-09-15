import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
import threading
import time
from ..controllers.simulator import MemorySimulator
from ..utils.constants import ProcessState, COLORS, WINDOW_WIDTH, WINDOW_HEIGHT, NUM_FRAMES, GRID_SIZE

class MemorySimulatorGUI:
    """Interfaz gráfica para el simulador de paginación de memoria."""
    
    def __init__(self, root):
        """Inicializa la interfaz gráfica."""
        self.root = root
        self.simulator = MemorySimulator()
        self.setup_ui()
        self.update_displays()
        
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.root.title("Simulador de Paginación de Memoria")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
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
        
        ttk.Button(buttons_frame, text="Bloquear Proceso", 
                  command=self.block_process_dialog).pack(side=tk.LEFT, padx=5)
        
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
        
        # Crear figura de matplotlib
        self.memory_fig, self.memory_ax = plt.subplots(figsize=(8, 6))
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, frames_frame)
        self.memory_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_page_tables_tab(self):
        """Configura la pestaña de tablas de páginas."""
        tables_frame = ttk.Frame(self.notebook)
        self.notebook.add(tables_frame, text="Tablas de Páginas")
        
        # Crear figura de matplotlib
        self.tables_fig, self.tables_ax = plt.subplots(figsize=(8, 6))
        self.tables_canvas = FigureCanvasTkAgg(self.tables_fig, tables_frame)
        self.tables_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
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
        
        self.stats_text = tk.Text(stats_frame, height=6, state=tk.DISABLED)
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
    
    def block_process_dialog(self):
        """Diálogo para bloquear un proceso."""
        running_processes = [p for p in self.simulator.memory_manager.get_all_processes() 
                           if p.state == ProcessState.RUNNING]
        
        if not running_processes:
            messagebox.showinfo("Información", "No hay procesos ejecutándose")
            return
        
        # Como solo puede haber un proceso ejecutándose, lo bloqueamos directamente
        process = running_processes[0]
        if self.simulator.memory_manager.block_process(process):
            messagebox.showinfo("Éxito", f"Proceso {process.name} bloqueado")
            self.update_displays()
        else:
            messagebox.showerror("Error", "No se pudo bloquear el proceso")
    
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
        dialog.geometry("400x250")
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
        result_text = tk.Text(dialog, height=8, state=tk.DISABLED)
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
                    result += f"Tabla de páginas:\n{selected_process.get_page_table()}"
                else:
                    result = f"Error: Dirección lógica {logical_addr} inválida para el proceso {selected_process.name}"
                
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
            self.simulator.run_simulation()
            self.root.after(100, self.update_displays)
        
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
        self.memory_ax.clear()
        
        data = self.simulator.get_memory_visualization_data()
        frames = data['frames']
        
        # Crear grilla de marcos
        rows = cols = GRID_SIZE
        
        for i, frame_data in enumerate(frames):
            row = i // cols
            col = i % cols
            
            # Determinar color
            if frame_data['status'] == 'free':
                color = 'lightgray'
                text = f"Marco {i}\nLibre"
            else:
                process = frame_data['process']
                color = COLORS.get(process.state, 'white')
                text = f"Marco {i}\n{process.name}\nPID {process.pid}"
            
            # Dibujar rectángulo
            rect = patches.Rectangle((col, rows-row-1), 1, 1, 
                                   linewidth=1, edgecolor='black', facecolor=color)
            self.memory_ax.add_patch(rect)
            
            # Añadir texto
            self.memory_ax.text(col+0.5, rows-row-0.5, text, 
                              ha='center', va='center', fontsize=8, wrap=True)
        
        self.memory_ax.set_xlim(0, cols)
        self.memory_ax.set_ylim(0, rows)
        self.memory_ax.set_aspect('equal')
        self.memory_ax.set_title('Estado de Marcos de Memoria Física')
        self.memory_ax.set_xticks([])
        self.memory_ax.set_yticks([])
        
        self.memory_canvas.draw()
    
    def update_page_tables_visualization(self):
        """Actualiza la visualización de tablas de páginas."""
        self.tables_ax.clear()
        
        data = self.simulator.get_memory_visualization_data()
        processes = data['processes']
        
        if not processes:
            self.tables_ax.text(0.5, 0.5, 'No hay procesos activos', 
                              ha='center', va='center', transform=self.tables_ax.transAxes)
            self.tables_canvas.draw()
            return
        
        # Mostrar tabla de páginas del primer proceso activo
        process_data = processes[0]
        process = process_data['process']
        page_table = process_data['page_table']
        
        if not page_table:
            self.tables_ax.text(0.5, 0.5, f'Proceso {process.name} sin páginas asignadas', 
                              ha='center', va='center', transform=self.tables_ax.transAxes)
            self.tables_canvas.draw()
            return
        
        # Crear tabla visual
        pages = list(page_table.keys())
        frames = list(page_table.values())
        
        table_data = []
        for page, frame in zip(pages, frames):
            table_data.append([f"Página {page}", f"Marco {frame}"])
        
        # Dibujar tabla
        table = self.tables_ax.table(cellText=table_data,
                                   colLabels=['Página Lógica', 'Marco Físico'],
                                   cellLoc='center',
                                   loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Colorear según el estado del proceso
        color = COLORS.get(process.state, 'white')
        for i in range(len(table_data)):
            table[(i+1, 0)].set_facecolor(color)
            table[(i+1, 1)].set_facecolor(color)
        
        self.tables_ax.set_title(f'Tabla de Páginas - {process.name} (PID {process.pid})')
        self.tables_ax.axis('off')
        
        self.tables_canvas.draw()
    
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
        
        for state, count in state_counts.items():
            stats_text += f"  {state}: {count}\n"
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state=tk.DISABLED)
