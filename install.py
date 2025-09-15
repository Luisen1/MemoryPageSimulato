#!/usr/bin/env python3
"""
Instalador automático para el Simulador de Paginación de Memoria
"""

import os
import sys
import subprocess
import venv

def print_banner():
    """Imprime el banner de instalación."""
    print("=" * 60)
    print("  INSTALADOR - SIMULADOR DE PAGINACIÓN DE MEMORIA")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica que la versión de Python sea compatible."""
    print("Verificando versión de Python...")
    
    if sys.version_info < (3, 7):
        print("❌ Error: Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version} - Compatible")
    return True

def create_virtual_environment():
    """Crea un entorno virtual."""
    print("\nCreando entorno virtual...")
    
    venv_path = os.path.join(os.getcwd(), "venv")
    
    if os.path.exists(venv_path):
        print("⚠️  El entorno virtual ya existe, se reutilizará")
        return venv_path
    
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Entorno virtual creado exitosamente")
        return venv_path
    except Exception as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return None

def get_venv_python(venv_path):
    """Obtiene la ruta del ejecutable de Python del entorno virtual."""
    if os.name == 'nt':  # Windows
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Unix/Linux/Mac
        return os.path.join(venv_path, "bin", "python")

def install_dependencies(python_path):
    """Instala las dependencias necesarias."""
    print("\nInstalando dependencias...")
    
    dependencies = ["matplotlib"]
    
    for dep in dependencies:
        print(f"Instalando {dep}...")
        try:
            result = subprocess.run([python_path, "-m", "pip", "install", dep], 
                                  check=True, capture_output=True, text=True)
            print(f"✅ {dep} instalado exitosamente")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {dep}: {e}")
            print(f"   Salida: {e.stdout}")
            print(f"   Error: {e.stderr}")
            return False
    
    return True

def test_installation(python_path):
    """Prueba la instalación ejecutando una demo rápida."""
    print("\nProbando instalación...")
    
    test_script = '''
import sys
sys.path.insert(0, ".")

try:
    from src.controllers.simulator import MemorySimulator
    from src.utils.constants import ProcessState
    
    # Crear simulador
    simulator = MemorySimulator()
    
    # Crear un proceso de prueba
    process = simulator.create_and_allocate_process("Test", 4096)
    
    if process:
        print("✅ Simulador funcionando correctamente")
        print(f"   Proceso creado: {process.name} (PID {process.pid})")
        print(f"   Marcos asignados: {process.allocated_frames}")
        
        # Limpiar
        simulator.memory_manager.deallocate_memory(process)
        print("✅ Limpieza completada")
    else:
        print("❌ Error creando proceso de prueba")
        
except Exception as e:
    print(f"❌ Error en la prueba: {e}")
    '''
    
    try:
        result = subprocess.run([python_path, "-c", test_script], 
                              check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la prueba: {e}")
        print(f"   Salida: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def create_run_scripts(python_path):
    """Crea scripts de ejecución para facilitar el uso."""
    print("\nCreando scripts de ejecución...")
    
    # Script para Windows
    if os.name == 'nt':
        # Script para consola
        console_script = f'''@echo off
echo Ejecutando Simulador en modo consola...
"{python_path}" demo_console.py
pause
'''
        with open("run_console.bat", "w") as f:
            f.write(console_script)
        
        # Script para GUI simple
        gui_script = f'''@echo off
echo Ejecutando Simulador con interfaz gráfica...
"{python_path}" gui_simple.py
'''
        with open("run_gui.bat", "w") as f:
            f.write(gui_script)
        
        print("✅ Scripts creados: run_console.bat, run_gui.bat")
    
    # Script para Unix/Linux/Mac
    else:
        # Script para consola
        console_script = f'''#!/bin/bash
echo "Ejecutando Simulador en modo consola..."
"{python_path}" demo_console.py
'''
        with open("run_console.sh", "w") as f:
            f.write(console_script)
        os.chmod("run_console.sh", 0o755)
        
        # Script para GUI
        gui_script = f'''#!/bin/bash
echo "Ejecutando Simulador con interfaz gráfica..."
"{python_path}" gui_simple.py
'''
        with open("run_gui.sh", "w") as f:
            f.write(gui_script)
        os.chmod("run_gui.sh", 0o755)
        
        print("✅ Scripts creados: run_console.sh, run_gui.sh")

def print_usage_instructions(python_path):
    """Imprime las instrucciones de uso."""
    print("\n" + "=" * 60)
    print("  INSTALACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    
    print("\n📋 FORMAS DE EJECUTAR EL SIMULADOR:")
    print("\n1. 🖥️  Modo Consola (Demostración automática):")
    if os.name == 'nt':
        print("   - Hacer doble clic en: run_console.bat")
        print("   - O ejecutar: python demo_console.py")
    else:
        print("   - Ejecutar: ./run_console.sh")
        print("   - O ejecutar: python demo_console.py")
    
    print("\n2. 🖼️  Modo GUI Simplificado (Interfaz gráfica):")
    if os.name == 'nt':
        print("   - Hacer doble clic en: run_gui.bat")
        print("   - O ejecutar: python gui_simple.py")
    else:
        print("   - Ejecutar: ./run_gui.sh")
        print("   - O ejecutar: python gui_simple.py")
    
    print("\n3. 🎨 Modo GUI Completo (Con matplotlib):")
    print("   - Ejecutar: python main.py")
    
    print("\n📚 CARACTERÍSTICAS PRINCIPALES:")
    print("   ✅ Simulación de paginación sin memoria virtual")
    print("   ✅ Modelo completo de 7 estados de procesos")
    print("   ✅ Asignación dinámica de marcos de memoria")
    print("   ✅ Tablas de páginas individuales por proceso")
    print("   ✅ Traducción de direcciones lógicas a físicas")
    print("   ✅ Visualización gráfica del estado del sistema")
    
    print("\n🔧 CONFIGURACIÓN DEL SISTEMA:")
    print("   • Tamaño de página: 4096 bytes (4 KB)")
    print("   • Memoria física total: 64 KB")
    print("   • Número de marcos: 16")
    print("   • Capacidad: 3+ procesos simultáneos")
    
    print("\n📖 Para más información, consulte README.md")
    print("=" * 60)

def main():
    """Función principal del instalador."""
    print_banner()
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Crear entorno virtual
    venv_path = create_virtual_environment()
    if not venv_path:
        return False
    
    # Obtener ruta del Python del entorno virtual
    python_path = get_venv_python(venv_path)
    
    # Verificar que el Python del entorno virtual existe
    if not os.path.exists(python_path):
        print(f"❌ Error: No se encontró Python en {python_path}")
        return False
    
    # Instalar dependencias
    if not install_dependencies(python_path):
        return False
    
    # Probar instalación
    if not test_installation(python_path):
        return False
    
    # Crear scripts de ejecución
    create_run_scripts(python_path)
    
    # Mostrar instrucciones
    print_usage_instructions(python_path)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ La instalación falló. Consulte los errores anteriores.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Instalación cancelada por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante la instalación: {e}")
        sys.exit(1)
