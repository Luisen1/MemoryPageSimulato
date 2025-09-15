#!/usr/bin/env python3
"""
Script de pruebas para verificar el funcionamiento del simulador
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Prueba que todos los módulos se puedan importar."""
    print("🧪 Probando importaciones...")
    
    try:
        from src.models.process import Process
        from src.models.memory_manager import MemoryManager
        from src.models.page_table import PageTable
        from src.controllers.simulator import MemorySimulator
        from src.utils.constants import ProcessState, NUM_FRAMES, PAGE_SIZE
        print("✅ Todas las importaciones exitosas")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_basic_functionality():
    """Prueba la funcionalidad básica del simulador."""
    print("\n🧪 Probando funcionalidad básica...")
    
    try:
        from src.controllers.simulator import MemorySimulator
        
        # Crear simulador
        simulator = MemorySimulator()
        print("✅ Simulador creado")
        
        # Crear proceso
        process = simulator.create_and_allocate_process("Prueba", 8192)
        if not process:
            print("❌ Error: No se pudo crear proceso")
            return False
        print(f"✅ Proceso creado: {process.name} (PID {process.pid})")
        
        # Verificar asignación de memoria
        if len(process.allocated_frames) != 2:
            print(f"❌ Error: Marcos asignados incorrectos: {process.allocated_frames}")
            return False
        print(f"✅ Marcos asignados correctamente: {process.allocated_frames}")
        
        # Probar traducción de direcciones
        logical_addr = 1024
        physical_addr = process.translate_address(logical_addr)
        if physical_addr is None:
            print("❌ Error: Traducción de dirección falló")
            return False
        print(f"✅ Traducción exitosa: {logical_addr} → {physical_addr}")
        
        # Probar cambios de estado
        original_state = process.state
        simulator.memory_manager.run_process(process)
        if process.state == original_state:
            print("❌ Error: Estado no cambió")
            return False
        print(f"✅ Cambio de estado: {original_state} → {process.state}")
        
        # Limpiar
        simulator.memory_manager.deallocate_memory(process)
        print("✅ Proceso terminado y memoria liberada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en funcionalidad básica: {e}")
        return False

def test_memory_management():
    """Prueba la gestión de memoria."""
    print("\n🧪 Probando gestión de memoria...")
    
    try:
        from src.controllers.simulator import MemorySimulator
        
        simulator = MemorySimulator()
        
        # Crear múltiples procesos
        processes = []
        for i in range(3):
            process = simulator.create_and_allocate_process(f"Proceso{i+1}", 4096 * (i + 1))
            if process:
                processes.append(process)
        
        if len(processes) != 3:
            print(f"❌ Error: Solo se crearon {len(processes)} de 3 procesos")
            return False
        print(f"✅ Creados {len(processes)} procesos correctamente")
        
        # Verificar uso de memoria
        stats = simulator.memory_manager.get_memory_usage()
        expected_frames = 1 + 2 + 3  # Procesos de 1, 2 y 3 páginas
        if stats['used_frames'] != expected_frames:
            print(f"❌ Error: Marcos usados incorrectos: {stats['used_frames']} != {expected_frames}")
            return False
        print(f"✅ Uso de memoria correcto: {stats['used_frames']} marcos")
        
        # Terminar procesos
        for process in processes:
            simulator.memory_manager.deallocate_memory(process)
        
        # Verificar liberación
        stats = simulator.memory_manager.get_memory_usage()
        if stats['used_frames'] != 0:
            print(f"❌ Error: Memoria no liberada completamente: {stats['used_frames']}")
            return False
        print("✅ Memoria liberada completamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en gestión de memoria: {e}")
        return False

def test_gui_imports():
    """Prueba que las GUIs se puedan importar."""
    print("\n🧪 Probando importaciones de GUI...")
    
    try:
        import tkinter as tk
        print("✅ Tkinter disponible")
        
        from src.views.simple_gui import SimpleMemorySimulatorGUI
        print("✅ GUI simplificada importable")
        
        try:
            import matplotlib.pyplot as plt
            from src.views.gui import MemorySimulatorGUI
            print("✅ GUI completa con matplotlib importable")
        except ImportError:
            print("⚠️  Matplotlib no disponible - GUI completa no disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en importaciones GUI: {e}")
        return False

def main():
    """Función principal de pruebas."""
    print("=" * 60)
    print("  PRUEBAS DEL SIMULADOR DE PAGINACIÓN DE MEMORIA")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_memory_management,
        test_gui_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("❌ Prueba falló")
    
    print("\n" + "=" * 60)
    print(f"  RESULTADOS: {passed}/{total} PRUEBAS PASARON")
    print("=" * 60)
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El simulador está listo para usar.")
        print("\n📋 FORMAS DE EJECUTAR:")
        print("   • Consola: python demo_console.py")
        print("   • GUI Simple: python gui_simple.py")
        print("   • GUI Completa: python main.py")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revise los errores anteriores.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
