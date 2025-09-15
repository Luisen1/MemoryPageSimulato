# Instalador del Simulador de Paginación de Memoria

Este script automatiza la configuración e instalación del simulador.

## Instrucciones de Instalación

### Opción 1: Instalación Automática (Recomendada)

1. Abra PowerShell como administrador
2. Navegue al directorio del proyecto:
   ```powershell
   cd "c:\Users\luise\OneDrive\Documentos\8vo semestre\SistemasOperativos\EntregableTaller\memory_page_simulator"
   ```

3. Ejecute el instalador:
   ```powershell
   python install.py
   ```

### Opción 2: Instalación Manual

1. **Crear entorno virtual:**
   ```powershell
   python -m venv venv
   ```

2. **Activar entorno virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias:**
   ```powershell
   pip install matplotlib
   ```

4. **Ejecutar el programa:**
   ```powershell
   # Versión consola
   python demo_console.py
   
   # Versión GUI simplificada
   python gui_simple.py
   
   # Versión GUI completa (requiere matplotlib)
   python main.py
   ```

## Uso del Programa

### Modo Consola
```powershell
python demo_console.py
```
- Ejecuta una demostración completa automática
- Muestra todos los conceptos del simulador
- No requiere interfaz gráfica

### Modo GUI Simplificado
```powershell
python gui_simple.py
```
- Interfaz gráfica usando solo Tkinter
- Visualización de marcos de memoria
- Control manual de procesos
- No requiere matplotlib

### Modo GUI Completo
```powershell
python main.py
```
- Interfaz gráfica con matplotlib
- Gráficos avanzados
- Visualizaciones detalladas
- Requiere matplotlib instalado

## Características del Simulador

- ✅ **Paginación sin memoria virtual**
- ✅ **Modelo de 7 estados de procesos**
- ✅ **Asignación dinámica de marcos**
- ✅ **Tablas de páginas por proceso**
- ✅ **Traducción direcciones lógicas → físicas**
- ✅ **Visualización gráfica en tiempo real**
- ✅ **Simulación de ciclo de vida completo**

## Configuración del Sistema

- **Tamaño de página:** 4096 bytes (4 KB)
- **Memoria física:** 64 KB
- **Número de marcos:** 16
- **Estados soportados:** Nuevo, Listo, Ejecutando, Bloqueado, Listo Suspendido, Bloqueado Suspendido, Terminado

## Solución de Problemas

### Error: "No module named 'matplotlib'"
Solución:
```powershell
pip install matplotlib
```

### Error: "tkinter not found"
Tkinter viene preinstalado con Python. Reinstale Python si es necesario.

### La GUI no se abre
1. Verifique que esté en el directorio correcto
2. Use la versión simplificada: `python gui_simple.py`
3. Pruebe la versión consola: `python demo_console.py`

## Estructura de Archivos

```
memory_page_simulator/
├── src/
│   ├── models/           # Modelos de datos
│   ├── controllers/      # Lógica del simulador
│   ├── views/           # Interfaces gráficas
│   └── utils/           # Utilidades y constantes
├── main.py              # GUI completa con matplotlib
├── gui_simple.py        # GUI simplificada solo Tkinter
├── demo_console.py      # Demostración en consola
├── install.py           # Instalador automático
└── README.md            # Documentación
```
