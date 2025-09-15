from typing import Dict, Optional
from ..utils.constants import PAGE_SIZE

class PageTable:
    """Representa una tabla de páginas para un proceso específico."""
    
    def __init__(self, process_pid: int):
        """
        Inicializa la tabla de páginas.
        
        Args:
            process_pid: PID del proceso propietario
        """
        self.process_pid = process_pid
        self.page_to_frame = {}  # página → marco
        self.frame_to_page = {}  # marco → página
    
    def add_mapping(self, page_number: int, frame_number: int) -> None:
        """
        Añade un mapeo página → marco.
        
        Args:
            page_number: Número de página lógica
            frame_number: Número de marco físico
        """
        self.page_to_frame[page_number] = frame_number
        self.frame_to_page[frame_number] = page_number
    
    def remove_mapping(self, page_number: int) -> Optional[int]:
        """
        Elimina un mapeo de página.
        
        Args:
            page_number: Número de página a eliminar
            
        Returns:
            Número de marco liberado o None
        """
        if page_number in self.page_to_frame:
            frame_number = self.page_to_frame[page_number]
            del self.page_to_frame[page_number]
            del self.frame_to_page[frame_number]
            return frame_number
        return None
    
    def get_frame(self, page_number: int) -> Optional[int]:
        """
        Obtiene el marco asociado a una página.
        
        Args:
            page_number: Número de página
            
        Returns:
            Número de marco o None si no existe
        """
        return self.page_to_frame.get(page_number)
    
    def get_page(self, frame_number: int) -> Optional[int]:
        """
        Obtiene la página asociada a un marco.
        
        Args:
            frame_number: Número de marco
            
        Returns:
            Número de página o None si no existe
        """
        return self.frame_to_page.get(frame_number)
    
    def translate_address(self, logical_address: int) -> Optional[int]:
        """
        Traduce una dirección lógica a física.
        
        Args:
            logical_address: Dirección lógica
            
        Returns:
            Dirección física o None si no es válida
        """
        page_number = logical_address // PAGE_SIZE
        offset = logical_address % PAGE_SIZE
        
        frame_number = self.get_frame(page_number)
        if frame_number is not None:
            physical_address = frame_number * PAGE_SIZE + offset
            return physical_address
        
        return None
    
    def get_all_mappings(self) -> Dict[int, int]:
        """
        Obtiene todos los mapeos página → marco.
        
        Returns:
            Diccionario con todos los mapeos
        """
        return self.page_to_frame.copy()
    
    def get_allocated_pages(self) -> list:
        """Obtiene la lista de páginas asignadas."""
        return list(self.page_to_frame.keys())
    
    def get_allocated_frames(self) -> list:
        """Obtiene la lista de marcos asignados."""
        return list(self.frame_to_page.keys())
    
    def clear(self) -> None:
        """Limpia toda la tabla de páginas."""
        self.page_to_frame.clear()
        self.frame_to_page.clear()
    
    def size(self) -> int:
        """Obtiene el número de entradas en la tabla."""
        return len(self.page_to_frame)
    
    def __str__(self) -> str:
        """Representación en cadena de la tabla de páginas."""
        if not self.page_to_frame:
            return f"Tabla de páginas (PID {self.process_pid}): Vacía"
        
        mappings = []
        for page in sorted(self.page_to_frame.keys()):
            frame = self.page_to_frame[page]
            mappings.append(f"Página {page} → Marco {frame}")
        
        return f"Tabla de páginas (PID {self.process_pid}):\n" + "\n".join(mappings)
    
    def __repr__(self) -> str:
        return self.__str__()
