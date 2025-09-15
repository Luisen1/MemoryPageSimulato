#!/usr/bin/env python3
"""
Lanzador Web del Simulador Interactivo de Memoria
================================================

Abre el simulador web en el navegador predeterminado del sistema.
Esta versión no requiere instalación de dependencias adicionales
más allá de un navegador web moderno.

Uso:
    python web_launcher.py

Características:
- No requiere Tkinter ni matplotlib
- Funciona en cualquier navegador moderno
- Interfaz completamente interactiva
- Mismo contenido educativo que la versión desktop

Autor: Sistema de Simulación de Memoria
Versión: 2.0 Web
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

def get_html_path():
    """Obtiene la ruta al archivo HTML del simulador."""
    script_dir = Path(__file__).parent
    html_file = script_dir / "simulador_web.html"
    
    if not html_file.exists():
        raise FileNotFoundError(f"No se encontró el archivo {html_file}")
    
    return html_file.absolute()

def check_browser():
    """Verifica que haya un navegador disponible."""
    try:
        # Intentar obtener el navegador predeterminado
        browser = webbrowser.get()
        return True
    except webbrowser.Error:
        return False

def show_startup_message():
    """Muestra mensaje de inicio."""
    print("🌐 SIMULADOR WEB DE PAGINACIÓN DE MEMORIA")
    print("=" * 50)
    print()
    print("🚀 Iniciando simulador web...")
    print("📱 Compatible con cualquier navegador moderno")
    print("🎯 No requiere instalación de dependencias")
    print()

def show_instructions():
    """Muestra instrucciones de uso."""
    print("🎮 INSTRUCCIONES DE USO:")
    print("=" * 30)
    print()
    print("1. 🖥️  PESTAÑA SIMULACIÓN:")
    print("   • Haz clic en 'Crear Proceso' para añadir procesos")
    print("   • Usa 'Simulación Automática' para una demo guiada")
    print("   • Los marcos de memoria se colorean según el estado")
    print("   • Haz clic en cualquier marco para ver detalles")
    print()
    print("2. 📚 PESTAÑA APRENDER:")
    print("   • Conceptos fundamentales de paginación")
    print("   • Explicaciones detalladas del sistema")
    print("   • Teoría y ejemplos prácticos")
    print()
    print("3. 📊 PESTAÑA ESTADÍSTICAS:")
    print("   • Métricas en tiempo real del sistema")
    print("   • Análisis de rendimiento")
    print("   • Estadísticas de uso de memoria")
    print()
    print("💡 CONSEJOS:")
    print("   • Experimenta creando procesos de diferentes tamaños")
    print("   • Observa cómo cambian los colores con los estados")
    print("   • Usa la simulación automática para entender el flujo")
    print()

def open_browser(html_path):
    """Abre el navegador con el simulador."""
    try:
        # Convertir a URL de archivo
        file_url = f"file:///{html_path.as_posix()}"
        
        print(f"🌐 Abriendo navegador...")
        print(f"📄 Archivo: {html_path}")
        print(f"🔗 URL: {file_url}")
        print()
        
        # Abrir en el navegador predeterminado
        webbrowser.open(file_url)
        
        print("✅ Simulador web abierto exitosamente!")
        print()
        print("📌 Si el navegador no se abre automáticamente,")
        print(f"   copia esta URL en tu navegador:")
        print(f"   {file_url}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al abrir navegador: {e}")
        print()
        print("🔧 SOLUCIÓN ALTERNATIVA:")
        print(f"   1. Abre tu navegador manualmente")
        print(f"   2. Ve a Archivo → Abrir archivo")
        print(f"   3. Selecciona: {html_path}")
        print()
        return False

def show_system_info():
    """Muestra información del sistema."""
    print("ℹ️  INFORMACIÓN DEL SISTEMA:")
    print("=" * 35)
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"💻 Sistema: {os.name}")
    print(f"📁 Directorio: {Path.cwd()}")
    print()

def wait_for_exit():
    """Espera que el usuario presione Enter para salir."""
    print("🎯 SIMULADOR ACTIVO")
    print("=" * 20)
    print()
    print("El simulador web está ejecutándose en tu navegador.")
    print("Puedes:")
    print("  • Mantener esta ventana abierta")
    print("  • Minimizarla")
    print("  • Cerrarla si ya no la necesitas")
    print()
    print("📝 El simulador seguirá funcionando en el navegador")
    print("   independientemente de esta ventana.")
    print()
    
    try:
        input("💬 Presiona ENTER para cerrar este launcher... ")
    except KeyboardInterrupt:
        print("\n\n👋 Saliendo del launcher...")

def main():
    """Función principal."""
    try:
        # Mostrar información inicial
        show_startup_message()
        
        # Verificar archivo HTML
        print("🔍 Verificando archivos...")
        html_path = get_html_path()
        print(f"✅ Simulador encontrado: {html_path.name}")
        
        # Verificar navegador
        print("🌐 Verificando navegador...")
        if not check_browser():
            print("⚠️  No se detectó navegador predeterminado")
            print("   El archivo se abrirá de forma manual")
        else:
            print("✅ Navegador disponible")
        
        print()
        
        # Mostrar información del sistema
        show_system_info()
        
        # Abrir navegador
        success = open_browser(html_path)
        
        if success:
            # Mostrar instrucciones
            show_instructions()
            
            # Esperar
            wait_for_exit()
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: {e}")
        print()
        print("🔧 SOLUCIÓN:")
        print("   Asegúrate de ejecutar este script desde el")
        print("   directorio que contiene 'simulador_web.html'")
        print()
        
    except KeyboardInterrupt:
        print("\n\n👋 Salida interrumpida por el usuario")
        
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        print()
        print("🆘 Si el problema persiste:")
        print("   1. Verifica que el archivo simulador_web.html exista")
        print("   2. Asegúrate de tener un navegador instalado")
        print("   3. Intenta abrir el archivo HTML manualmente")
        print()

if __name__ == "__main__":
    main()
