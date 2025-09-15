#!/usr/bin/env python3
"""
Simulador de Paginación de Memoria - Interfaz Gráfica Simplificada
Punto de entrada para la versión GUI sin matplotlib
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Agregar el directorio actual al path para las importaciones
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.views.simple_gui import SimpleMemorySimulatorGUI
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrese de que todas las dependencias estén instaladas.")
    sys.exit(1)

def main():
    """Función principal que inicia la aplicación."""
    try:
        # Crear ventana principal
        root = tk.Tk()
        
        # Crear y ejecutar la aplicación
        app = SimpleMemorySimulatorGUI(root)
        
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

if __name__ == "__main__":
    main()
