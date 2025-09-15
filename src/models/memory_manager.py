from typing import Dict, List, Optional
from .process import Process
from ..utils.constants import NUM_FRAMES, PAGE_SIZE, ProcessState

class MemoryManager:
    """Administrador de memoria que maneja la paginación y asignación de marcos."""
    
    def __init__(self):
        """Inicializa el administrador de memoria."""
        self.frames = [None] * NUM_FRAMES  # None = marco libre, Process = proceso que lo ocupa
        self.processes = {}  # pid -> Process
        self.next_pid = 1
        
    def create_process(self, name: str, size: int) -> Optional[Process]:
        """
        Crea un nuevo proceso.
        
        Args:
            name: Nombre del proceso
            size: Tamaño del proceso en bytes
            
        Returns:
            El proceso creado o None si no hay suficiente memoria
        """
        # Crear proceso en estado NEW
        process = Process(self.next_pid, name, size)
        self.next_pid += 1
        
        # Verificar si hay suficientes marcos disponibles
        free_frames = self._get_free_frames()
        if len(free_frames) < process.pages_needed:
            print(f"Error: No hay suficiente memoria para el proceso {name}")
            return None
        
        # Registrar el proceso
        self.processes[process.pid] = process
        print(f"Proceso {name} creado con PID {process.pid}")
        
        return process
    
    def allocate_memory(self, process: Process) -> bool:
        """
        Asigna memoria a un proceso (transición NEW → READY).
        
        Args:
            process: Proceso al que asignar memoria
            
        Returns:
            True si la asignación fue exitosa
        """
        if process.state != ProcessState.NEW:
            print(f"Error: El proceso {process.name} no está en estado NEW")
            return False
        
        free_frames = self._get_free_frames()
        if len(free_frames) < process.pages_needed:
            print(f"Error: No hay suficiente memoria para {process.name}")
            return False
        
        # Asignar marcos al proceso
        for i in range(process.pages_needed):
            frame_number = free_frames[i]
            self.frames[frame_number] = process
            process.allocate_frame(frame_number)
        
        # Cambiar estado a READY
        process.change_state(ProcessState.READY)
        print(f"Memoria asignada al proceso {process.name}: {process.allocated_frames}")
        
        return True
    
    def deallocate_memory(self, process: Process) -> None:
        """
        Libera la memoria de un proceso (transición → TERMINATED).
        
        Args:
            process: Proceso a liberar
        """
        freed_frames = process.deallocate_frames()
        
        # Liberar marcos en la memoria física
        for frame_number in freed_frames:
            self.frames[frame_number] = None
        
        # Cambiar estado a TERMINATED
        process.change_state(ProcessState.TERMINATED)
        print(f"Memoria liberada del proceso {process.name}: {freed_frames}")
    
    def run_process(self, process: Process) -> bool:
        """
        Ejecuta un proceso (transición READY → RUNNING).
        
        Args:
            process: Proceso a ejecutar
            
        Returns:
            True si se pudo ejecutar
        """
        if process.state != ProcessState.READY:
            print(f"Error: El proceso {process.name} no está en estado READY")
            return False
        
        # Verificar que no hay otro proceso ejecutándose
        running_processes = [p for p in self.processes.values() if p.state == ProcessState.RUNNING]
        if running_processes:
            print(f"Error: Ya hay un proceso ejecutándose: {running_processes[0].name}")
            return False
        
        process.change_state(ProcessState.RUNNING)
        return True
    
    def block_process(self, process: Process) -> bool:
        """
        Bloquea un proceso (transición RUNNING → BLOCKED).
        
        Args:
            process: Proceso a bloquear
            
        Returns:
            True si se pudo bloquear
        """
        if process.state != ProcessState.RUNNING:
            print(f"Error: El proceso {process.name} no está ejecutándose")
            return False
        
        process.change_state(ProcessState.BLOCKED)
        return True
    
    def ready_process(self, process: Process) -> bool:
        """
        Pone un proceso en estado listo (transiciones RUNNING/BLOCKED → READY).
        
        Args:
            process: Proceso a poner en estado listo
            
        Returns:
            True si se pudo cambiar el estado
        """
        if process.state not in [ProcessState.RUNNING, ProcessState.BLOCKED]:
            print(f"Error: El proceso {process.name} no puede cambiar a READY desde {process.state}")
            return False
        
        process.change_state(ProcessState.READY)
        return True
    
    def suspend_process(self, process: Process) -> bool:
        """
        Suspende un proceso (transiciones READY/BLOCKED → READY_SUSPENDED/BLOCKED_SUSPENDED).
        
        Args:
            process: Proceso a suspender
            
        Returns:
            True si se pudo suspender
        """
        if process.state == ProcessState.READY:
            process.change_state(ProcessState.READY_SUSPENDED)
            return True
        elif process.state == ProcessState.BLOCKED:
            process.change_state(ProcessState.BLOCKED_SUSPENDED)
            return True
        else:
            print(f"Error: El proceso {process.name} no puede ser suspendido desde {process.state}")
            return False
    
    def resume_process(self, process: Process) -> bool:
        """
        Reanuda un proceso suspendido.
        
        Args:
            process: Proceso a reanudar
            
        Returns:
            True si se pudo reanudar
        """
        if process.state == ProcessState.READY_SUSPENDED:
            process.change_state(ProcessState.READY)
            return True
        elif process.state == ProcessState.BLOCKED_SUSPENDED:
            process.change_state(ProcessState.BLOCKED)
            return True
        else:
            print(f"Error: El proceso {process.name} no está suspendido")
            return False
    
    def get_process_by_pid(self, pid: int) -> Optional[Process]:
        """Obtiene un proceso por su PID."""
        return self.processes.get(pid)
    
    def get_all_processes(self) -> List[Process]:
        """Obtiene todos los procesos."""
        return list(self.processes.values())
    
    def get_memory_usage(self) -> dict:
        """
        Obtiene información sobre el uso de memoria.
        
        Returns:
            Diccionario con estadísticas de memoria
        """
        total_frames = NUM_FRAMES
        used_frames = sum(1 for frame in self.frames if frame is not None)
        free_frames = total_frames - used_frames
        
        return {
            'total_frames': total_frames,
            'used_frames': used_frames,
            'free_frames': free_frames,
            'usage_percentage': (used_frames / total_frames) * 100
        }
    
    def _get_free_frames(self) -> List[int]:
        """Obtiene la lista de marcos libres."""
        return [i for i, frame in enumerate(self.frames) if frame is None]
    
    def translate_address(self, pid: int, logical_address: int) -> Optional[int]:
        """
        Traduce una dirección lógica a física para un proceso específico.
        
        Args:
            pid: PID del proceso
            logical_address: Dirección lógica
            
        Returns:
            Dirección física o None si no es válida
        """
        process = self.get_process_by_pid(pid)
        if process:
            return process.translate_address(logical_address)
        return None
