#!/usr/bin/env python3
"""
Simulador de Paginación de Memoria - Versión Consola Simple
"""

import sys
import os

# Agregar el directorio actual al path para las importaciones
sys.path.insert(0, os.path.dirname(__file__))

from src.controllers.simulator import MemorySimulator
from src.utils.constants import ProcessState

def print_separator(text=""):
    """Imprime un separador visual."""
    print("=" * 60)
    if text:
        print(f" {text} ")
        print("=" * 60)
    print()

def print_memory_state(simulator):
    """Imprime el estado actual de la memoria de forma visual."""
    print("Estado de la Memoria Física:")
    print("-" * 40)
    
    frames = simulator.memory_manager.frames
    for i in range(0, len(frames), 4):  # Mostrar en filas de 4
        row = []
        for j in range(4):
            if i + j < len(frames):
                frame = frames[i + j]
                if frame is None:
                    row.append(f"[{i+j:2d}: Libre ]")
                else:
                    row.append(f"[{i+j:2d}: P{frame.pid:2d}  ]")
            else:
                row.append("")
        print(" ".join(row))
    print()

def print_page_tables(simulator):
    """Imprime las tablas de páginas de los procesos activos."""
    active_processes = [p for p in simulator.memory_manager.get_all_processes()
                       if p.state != ProcessState.TERMINATED and p.allocated_frames]
    
    if not active_processes:
        print("No hay procesos con memoria asignada\n")
        return
    
    print("Tablas de Páginas:")
    print("-" * 40)
    
    for process in active_processes:
        print(f"Proceso: {process.name} (PID {process.pid}) - Estado: {process.state}")
        page_table = process.get_page_table()
        if page_table:
            print("  Página → Marco")
            for page, frame in sorted(page_table.items()):
                print(f"    {page:2d}   →   {frame:2d}")
        else:
            print("  Sin páginas asignadas")
        print()

def main():
    """Función principal del simulador en modo consola."""
    print_separator("SIMULADOR DE PAGINACIÓN DE MEMORIA")
    
    # Crear el simulador
    simulator = MemorySimulator()
    
    print("Configuración del sistema:")
    print(f"- Tamaño de página: 4096 bytes")
    print(f"- Memoria física: 64 KB")
    print(f"- Número de marcos: 16")
    print(f"- Estados de proceso: 7 estados\n")
    
    # Crear procesos de ejemplo
    print_separator("CREANDO PROCESOS")
    
    processes_data = [
        ("Editor de Texto", 8192),
        ("Navegador Web", 16384),
        ("Reproductor", 12288),
    ]
    
    created_processes = []
    for name, size in processes_data:
        print(f"Creando proceso '{name}' ({size} bytes)...")
        process = simulator.create_and_allocate_process(name, size)
        if process:
            created_processes.append(process)
            print(f"  ✓ Proceso creado con PID {process.pid}")
            print(f"  ✓ Páginas necesarias: {process.pages_needed}")
            print(f"  ✓ Marcos asignados: {process.allocated_frames}")
        else:
            print(f"  ✗ Error: No se pudo crear el proceso")
        print()
    
    # Mostrar estado inicial
    print_separator("ESTADO INICIAL DE LA MEMORIA")
    print_memory_state(simulator)
    print_page_tables(simulator)
    
    # Simular ejecución de procesos
    print_separator("SIMULANDO EJECUCIÓN DE PROCESOS")
    
    for i, process in enumerate(created_processes):
        print(f"--- Ejecutando proceso {process.name} ---")
        
        # Ejecutar proceso
        if simulator.memory_manager.run_process(process):
            print(f"  ✓ Proceso {process.name} está ejecutándose")
            
            # Simular trabajo
            import time
            time.sleep(0.5)
            
            # Simular diferentes transiciones
            import random
            transition = random.choice(['complete', 'block'])
            
            if transition == 'complete':
                print(f"  ✓ Proceso {process.name} completado")
                simulator.memory_manager.deallocate_memory(process)
            else:
                print(f"  ⏸ Proceso {process.name} bloqueado")
                simulator.memory_manager.block_process(process)
                time.sleep(0.3)
                
                print(f"  ✓ Proceso {process.name} listo nuevamente")
                simulator.memory_manager.ready_process(process)
                
                # Ejecutar de nuevo
                if simulator.memory_manager.run_process(process):
                    print(f"  ✓ Proceso {process.name} ejecutándose nuevamente")
                    time.sleep(0.3)
                    print(f"  ✓ Proceso {process.name} completado")
                    simulator.memory_manager.deallocate_memory(process)
        
        print()
        print_memory_state(simulator)
        print()
    
    # Demostración de traducción de direcciones
    print_separator("DEMOSTRACIÓN DE TRADUCCIÓN DE DIRECCIONES")
    
    # Crear un proceso para demostrar traducción
    demo_process = simulator.create_and_allocate_process("Demo", 8192)
    if demo_process:
        print(f"Proceso demo creado: {demo_process.name} (PID {demo_process.pid})")
        print(f"Marcos asignados: {demo_process.allocated_frames}")
        print()
        
        # Traducir algunas direcciones
        test_addresses = [0, 1024, 4096, 5120, 8000]
        
        for logical_addr in test_addresses:
            physical_addr = demo_process.translate_address(logical_addr)
            
            if physical_addr is not None:
                page_num = logical_addr // 4096
                offset = logical_addr % 4096
                frame_num = physical_addr // 4096
                
                print(f"Dirección lógica {logical_addr:5d}:")
                print(f"  → Página {page_num}, Offset {offset}")
                print(f"  → Marco {frame_num}")
                print(f"  → Dirección física {physical_addr}")
            else:
                print(f"Dirección lógica {logical_addr:5d}: INVÁLIDA")
            print()
        
        # Terminar proceso demo
        simulator.memory_manager.deallocate_memory(demo_process)
    
    # Estado final
    print_separator("ESTADO FINAL DEL SISTEMA")
    memory_stats = simulator.memory_manager.get_memory_usage()
    print(f"Marcos totales: {memory_stats['total_frames']}")
    print(f"Marcos utilizados: {memory_stats['used_frames']}")
    print(f"Marcos libres: {memory_stats['free_frames']}")
    print(f"Porcentaje de uso: {memory_stats['usage_percentage']:.1f}%")
    print()
    
    print_memory_state(simulator)
    
    print_separator("SIMULACIÓN COMPLETADA")
    print("El simulador ha demostrado:")
    print("✓ Creación y asignación de procesos")
    print("✓ Modelo de 7 estados de procesos")
    print("✓ Paginación de memoria")
    print("✓ Tablas de páginas por proceso")
    print("✓ Traducción de direcciones lógicas a físicas")
    print("✓ Gestión del ciclo de vida de procesos")

if __name__ == "__main__":
    main()
