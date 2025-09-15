# Constantes del sistema de paginación

# Configuración de memoria
PAGE_SIZE = 4096  # Tamaño de página en bytes (4KB)
FRAME_SIZE = PAGE_SIZE  # Tamaño de marco igual al de página
PHYSICAL_MEMORY_SIZE = 64 * 1024  # 64KB de memoria física
NUM_FRAMES = PHYSICAL_MEMORY_SIZE // FRAME_SIZE  # 16 marcos

# Estados de proceso (modelo de 7 estados)
class ProcessState:
    NEW = "Nuevo"
    READY = "Listo"
    RUNNING = "Ejecutando"
    BLOCKED = "Bloqueado"
    READY_SUSPENDED = "Listo Suspendido"
    BLOCKED_SUSPENDED = "Bloqueado Suspendido"
    TERMINATED = "Terminado"

# Colores para la visualización
COLORS = {
    ProcessState.NEW: "#FFE6E6",
    ProcessState.READY: "#E6F3FF",
    ProcessState.RUNNING: "#E6FFE6",
    ProcessState.BLOCKED: "#FFFFE6",
    ProcessState.READY_SUSPENDED: "#F0E6FF",
    ProcessState.BLOCKED_SUSPENDED: "#FFE6F0",
    ProcessState.TERMINATED: "#E6E6E6"
}

# Configuración de la interfaz
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GRID_SIZE = 4  # Para mostrar marcos en una grilla 4x4
