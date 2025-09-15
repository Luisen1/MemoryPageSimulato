from enum import Enum
from typing import Optional
import time
from ..utils.constants import ProcessState

class Process:
    """Representa un proceso en el sistema con su ciclo de vida completo."""
    
    def __init__(self, pid: int, name: str, size: int):
        """
        Inicializa un nuevo proceso.
        
        Args:
            pid: Identificador único del proceso
            name: Nombre del proceso
            size: Tamaño del proceso en bytes
        """
        self.pid = pid
        self.name = name
        self.size = size
        self.state = ProcessState.NEW
        self.pages_needed = self._calculate_pages_needed()
        self.allocated_frames = []  # Lista de marcos asignados
        self.creation_time = time.time()
        self.last_state_change = time.time()
        
    def _calculate_pages_needed(self) -> int:
        """Calcula el número de páginas necesarias para el proceso."""
        from ..utils.constants import PAGE_SIZE
        return (self.size + PAGE_SIZE - 1) // PAGE_SIZE  # Redondeo hacia arriba
    
    def change_state(self, new_state: str) -> None:
        """
        Cambia el estado del proceso.
        
        Args:
            new_state: Nuevo estado del proceso
        """
        old_state = self.state
        self.state = new_state
        self.last_state_change = time.time()
        print(f"Proceso {self.name} (PID: {self.pid}): {old_state} → {new_state}")
    
    def allocate_frame(self, frame_number: int) -> None:
        """
        Asigna un marco de memoria al proceso.
        
        Args:
            frame_number: Número del marco a asignar
        """
        if frame_number not in self.allocated_frames:
            self.allocated_frames.append(frame_number)
    
    def deallocate_frames(self) -> list:
        """
        Libera todos los marcos asignados al proceso.
        
        Returns:
            Lista de marcos liberados
        """
        freed_frames = self.allocated_frames.copy()
        self.allocated_frames.clear()
        return freed_frames
    
    def get_page_table(self) -> dict:
        """
        Obtiene la tabla de páginas del proceso.
        
        Returns:
            Diccionario con el mapeo página → marco
        """
        page_table = {}
        for page_num, frame_num in enumerate(self.allocated_frames):
            page_table[page_num] = frame_num
        return page_table
    
    def translate_address(self, logical_address: int) -> Optional[int]:
        """
        Traduce una dirección lógica a física.
        
        Args:
            logical_address: Dirección lógica a traducir
            
        Returns:
            Dirección física o None si no es válida
        """
        from ..utils.constants import PAGE_SIZE
        
        page_number = logical_address // PAGE_SIZE
        offset = logical_address % PAGE_SIZE
        
        if page_number < len(self.allocated_frames):
            frame_number = self.allocated_frames[page_number]
            physical_address = frame_number * PAGE_SIZE + offset
            return physical_address
        
        return None
    
    def __str__(self) -> str:
        return f"Proceso {self.name} (PID: {self.pid}, Estado: {self.state}, Tamaño: {self.size}B)"
    
    def __repr__(self) -> str:
        return self.__str__()
