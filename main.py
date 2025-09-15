#!/usr/bin/env python3
"""
Simulador de Paginación de Memoria
Punto de entrada principal de la aplicación
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio actual al path para las importaciones
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.views.gui import MemorySimulatorGUI
    from src.controllers.simulator import MemorySimulator
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que todas las dependencias estén instaladas.")
    print(f"Python path: {sys.path}")
    print(f"Directorio actual: {os.getcwd()}")
    sys.exit(1)

def main():
    """Función principal que inicia la aplicación."""
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Configurar el icono de la ventana (opcional)
        try:
            root.iconbitmap(default='icon.ico')  # Si tienes un icono
        except:
            pass  # Ignorar si no hay icono
        
        # Crear y ejecutar la aplicación
        app = MemorySimulatorGUI(root)
        
        # Mostrar información inicial
        messagebox.showinfo(
            "Simulador de Paginación de Memoria",
            "Bienvenido al Simulador de Paginación de Memoria\n\n"
            "Características:\n"
            "• Simulación de paginación sin memoria virtual\n"
            "• Modelo de 7 estados de procesos\n"
            "• Visualización gráfica en tiempo real\n"
            "• Traducción de direcciones lógicas a físicas\n\n"
            "Use los controles para crear procesos y observar\n"
            "el comportamiento del administrador de memoria."
        )
        
        # Iniciar el bucle principal de la GUI
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error Fatal", f"Se produjo un error inesperado:\n{e}")
        print(f"Error fatal: {e}")
        sys.exit(1)

def run_console_demo():
    """Ejecuta una demostración en consola del simulador."""
    print("=== Simulador de Paginación de Memoria - Modo Consola ===\n")
    
    try:
        simulator = MemorySimulator()
        
        print("Ejecutando simulación automática...\n")
        simulator.run_simulation()
        
        print("\nDemostración de traducción de direcciones:")
        
        # Obtener un proceso activo para demostrar traducción
        active_processes = [p for p in simulator.memory_manager.get_all_processes()
                          if p.allocated_frames]
        
        if active_processes:
            process = active_processes[0]
            simulator.translate_address_demo(process.pid, 1024)
            simulator.translate_address_demo(process.pid, 8192)
        
    except Exception as e:
        print(f"Error en la simulación: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        # Modo consola
        success = run_console_demo()
        sys.exit(0 if success else 1)
    else:
        # Modo GUI (por defecto)
        main()
