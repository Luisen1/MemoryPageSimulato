import random
import time
from typing import List, Optional
from ..models.memory_manager import MemoryManager
from ..models.process import Process
from ..utils.constants import ProcessState

class MemorySimulator:
    """Controlador principal que maneja la simulación del sistema de memoria."""
    
    def __init__(self):
        """Inicializa el simulador."""
        self.memory_manager = MemoryManager()
        self.simulation_running = False
        self.auto_simulation = False
    
    def create_and_allocate_process(self, name: str, size: int) -> Optional[Process]:
        """
        Crea un proceso y le asigna memoria automáticamente.
        
        Args:
            name: Nombre del proceso
            size: Tamaño del proceso en bytes
            
        Returns:
            El proceso creado o None si falló
        """
        # Crear proceso
        process = self.memory_manager.create_process(name, size)
        if not process:
            return None
        
        # Asignar memoria automáticamente
        if self.memory_manager.allocate_memory(process):
            return process
        else:
            # Si no se pudo asignar memoria, remover el proceso
            del self.memory_manager.processes[process.pid]
            return None
    
    def simulate_process_lifecycle(self, process: Process) -> None:
        """
        Simula el ciclo de vida completo de un proceso.
        
        Args:
            process: Proceso a simular
        """
        if not process:
            return
        
        # El proceso ya está en READY después de allocate_memory
        
        # Simular ejecución
        if self.memory_manager.run_process(process):
            time.sleep(0.5)  # Simular tiempo de ejecución
            
            # Simular diferentes transiciones aleatoriamente
            transition = random.choice(['complete', 'block', 'preempt'])
            
            if transition == 'complete':
                # Proceso completa su ejecución
                self.memory_manager.deallocate_memory(process)
            
            elif transition == 'block':
                # Proceso se bloquea
                self.memory_manager.block_process(process)
                time.sleep(0.3)  # Tiempo bloqueado
                
                # Puede ser suspendido mientras está bloqueado
                if random.choice([True, False]):
                    self.memory_manager.suspend_process(process)
                    time.sleep(0.2)
                    self.memory_manager.resume_process(process)
                
                # Vuelve a estado listo
                self.memory_manager.ready_process(process)
                
                # Intentar ejecutar de nuevo
                if self.memory_manager.run_process(process):
                    time.sleep(0.3)
                    self.memory_manager.deallocate_memory(process)
            
            elif transition == 'preempt':
                # Proceso es interrumpido (preempted)
                self.memory_manager.ready_process(process)
                
                # Puede ser suspendido
                if random.choice([True, False]):
                    self.memory_manager.suspend_process(process)
                    time.sleep(0.2)
                    self.memory_manager.resume_process(process)
                
                # Ejecutar de nuevo
                if self.memory_manager.run_process(process):
                    time.sleep(0.3)
                    self.memory_manager.deallocate_memory(process)
    
    def create_sample_processes(self) -> List[Process]:
        """
        Crea procesos de ejemplo para la simulación.
        
        Returns:
            Lista de procesos creados
        """
        sample_processes = [
            ("Editor de Texto", 8192),    # 2 páginas
            ("Navegador Web", 16384),     # 4 páginas  
            ("Reproductor", 12288),       # 3 páginas
            ("Calculadora", 4096),        # 1 página
            ("Terminal", 6144)            # 2 páginas (redondeado)
        ]
        
        created_processes = []
        
        for name, size in sample_processes:
            process = self.create_and_allocate_process(name, size)
            if process:
                created_processes.append(process)
            else:
                print(f"No se pudo crear el proceso {name}")
        
        return created_processes
    
    def run_simulation(self) -> None:
        """Ejecuta una simulación automática."""
        print("=== Iniciando Simulación de Paginación de Memoria ===\n")
        
        # Crear procesos de ejemplo
        processes = self.create_sample_processes()
        
        if not processes:
            print("No se pudieron crear procesos para la simulación")
            return
        
        print(f"\nProcesos creados: {len(processes)}")
        self.print_memory_status()
        
        # Simular ciclo de vida para cada proceso
        for i, process in enumerate(processes):
            print(f"\n--- Simulando proceso {i+1}: {process.name} ---")
            self.simulate_process_lifecycle(process)
            self.print_memory_status()
            time.sleep(0.5)
        
        print("\n=== Simulación Completada ===")
    
    def print_memory_status(self) -> None:
        """Imprime el estado actual de la memoria."""
        print("\n--- Estado de la Memoria ---")
        
        # Estadísticas generales
        memory_usage = self.memory_manager.get_memory_usage()
        print(f"Marcos totales: {memory_usage['total_frames']}")
        print(f"Marcos usados: {memory_usage['used_frames']}")
        print(f"Marcos libres: {memory_usage['free_frames']}")
        print(f"Uso de memoria: {memory_usage['usage_percentage']:.1f}%")
        
        # Procesos activos
        active_processes = [p for p in self.memory_manager.get_all_processes() 
                          if p.state != ProcessState.TERMINATED]
        
        if active_processes:
            print("\nProcesos activos:")
            for process in active_processes:
                print(f"  {process}")
                if process.allocated_frames:
                    print(f"    Marcos asignados: {process.allocated_frames}")
                    page_table = process.get_page_table()
                    print(f"    Tabla de páginas: {page_table}")
        else:
            print("\nNo hay procesos activos")
        
        print("-" * 30)
    
    def get_memory_visualization_data(self) -> dict:
        """
        Obtiene datos para la visualización gráfica.
        
        Returns:
            Diccionario con datos de visualización
        """
        # Estado de los marcos
        frame_data = []
        for i, frame in enumerate(self.memory_manager.frames):
            if frame is None:
                frame_data.append({
                    'frame_number': i,
                    'process': None,
                    'status': 'free'
                })
            else:
                frame_data.append({
                    'frame_number': i,
                    'process': frame,
                    'status': 'occupied'
                })
        
        # Información de procesos
        processes_data = []
        for process in self.memory_manager.get_all_processes():
            if process.state != ProcessState.TERMINATED:
                processes_data.append({
                    'process': process,
                    'page_table': process.get_page_table(),
                    'allocated_frames': process.allocated_frames
                })
        
        # Estadísticas de memoria
        memory_stats = self.memory_manager.get_memory_usage()
        
        return {
            'frames': frame_data,
            'processes': processes_data,
            'memory_stats': memory_stats
        }
    
    def translate_address_demo(self, pid: int, logical_address: int) -> None:
        """
        Demuestra la traducción de direcciones lógicas a físicas.
        
        Args:
            pid: PID del proceso
            logical_address: Dirección lógica a traducir
        """
        physical_address = self.memory_manager.translate_address(pid, logical_address)
        
        if physical_address is not None:
            page_number = logical_address // 4096  # PAGE_SIZE
            offset = logical_address % 4096
            frame_number = physical_address // 4096
            
            print(f"\n--- Traducción de Dirección ---")
            print(f"Proceso PID: {pid}")
            print(f"Dirección lógica: {logical_address}")
            print(f"Página: {page_number}, Offset: {offset}")
            print(f"Marco: {frame_number}")
            print(f"Dirección física: {physical_address}")
        else:
            print(f"Error: No se pudo traducir la dirección {logical_address} para el proceso {pid}")
    
    def cleanup_terminated_processes(self) -> None:
        """Limpia los procesos terminados del sistema."""
        terminated_pids = [
            pid for pid, process in self.memory_manager.processes.items()
            if process.state == ProcessState.TERMINATED
        ]
        
        for pid in terminated_pids:
            del self.memory_manager.processes[pid]
        
        if terminated_pids:
            print(f"Procesos terminados removidos: {terminated_pids}")
