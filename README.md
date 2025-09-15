# Simulador de Paginación de Memoria

Este proyecto implementa un simulador completo del comportamiento básico del administrador de memoria de un sistema operativo utilizando el esquema de paginación sin memoria virtual.

## 🎯 Objetivos Cumplidos

### ✅ Funcionalidades Principales

- **Asignación de memoria mediante paginación:**
  - División del espacio lógico en páginas de 4096 bytes
  - Asignación de marcos físicos disponibles para cada página
  - Implementación de tabla de páginas por proceso

- **Visualización gráfica completa:**
  - Tabla de páginas por proceso con mapeo página → marco
  - Estado actual de la memoria física (marcos ocupados/libres)
  - Mapeo visual entre direcciones lógicas y físicas

- **Modelo de ciclo de vida de procesos:**
  - Implementación completa del modelo de 7 estados
  - Transiciones automáticas entre estados
  - Efectos visuales de cambios de estado en la memoria

### ✅ Exclusiones Respetadas

- ❌ Sin memoria virtual (como se solicitó)
- ❌ Sin algoritmos de reemplazo de páginas
- ✅ Memoria finita pero suficiente para 3+ procesos simultáneos

## 🏗️ Arquitectura del Proyecto

El proyecto sigue buenas prácticas de desarrollo con arquitectura MVC:

```
memory_page_simulator/
├── src/
│   ├── models/              # Modelos de datos
│   │   ├── process.py       # Modelo del proceso y estados
│   │   ├── memory_manager.py # Administrador de memoria
│   │   └── page_table.py    # Tabla de páginas
│   ├── controllers/         # Lógica de negocio
│   │   └── simulator.py     # Controlador principal
│   ├── views/              # Interfaces de usuario
│   │   ├── gui.py          # GUI completa con matplotlib
│   │   └── simple_gui.py   # GUI simplificada con Tkinter
│   └── utils/              # Utilidades
│       └── constants.py    # Constantes del sistema
├── main.py                 # GUI completa
├── gui_simple.py          # GUI simplificada  
├── demo_console.py        # Demostración en consola
├── install.py             # Instalador automático
└── README.md              # Esta documentación
```

## 🔧 Configuración del Sistema

- **Tamaño de página:** 4096 bytes (4 KB)
- **Memoria física:** 64 KB total
- **Número de marcos:** 16 marcos disponibles
- **Estados de proceso:** 7 estados (Nuevo, Listo, Ejecutando, Bloqueado, Listo Suspendido, Bloqueado Suspendido, Terminado)

## 🚀 Instalación y Ejecución

### Opción 1: Instalación Automática (Recomendada)

```bash
# Clonar o descargar el proyecto
cd memory_page_simulator

# Ejecutar instalador automático
python install.py
```

### Opción 2: Instalación Manual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\Activate.ps1

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install matplotlib

# Ejecutar el programa
python demo_console.py    # Modo consola
python gui_simple.py      # GUI simplificada
python main.py            # GUI completa
```

## 🎮 Modos de Uso

### 1. 🖥️ Modo Consola (`demo_console.py`)
- Demostración automática completa
- Visualización textual de marcos de memoria
- Tablas de páginas impresas en formato texto
- Simulación de ciclo de vida completo
- Traducción de direcciones ejemplo

**Ejemplo de salida:**
```
Estado de la Memoria Física:
----------------------------------------
[ 0: P 1  ] [ 1: P 1  ] [ 2: P 2  ] [ 3: P 2  ]
[ 4: Libre] [ 5: Libre] [ 6: P 3  ] [ 7: P 3  ]

Tablas de Páginas:
----------------------------------------
Proceso: Editor de Texto (PID 1) - Estado: Ejecutando
  Página → Marco
     0   →    0
     1   →    1
```

### 2. 🖼️ GUI Simplificada (`gui_simple.py`)
- Interfaz gráfica usando solo Tkinter
- Visualización de marcos en grilla 4x4 con colores
- Control manual de procesos
- Traducción interactiva de direcciones
- No requiere matplotlib

**Características de la GUI:**
- Grilla visual de 16 marcos de memoria
- Colores por estado de proceso
- Pestañas para marcos y tablas de páginas
- Controles para crear/ejecutar/terminar procesos

### 3. 🎨 GUI Completa (`main.py`)
- Interfaz gráfica avanzada con matplotlib
- Gráficos detallados y visualizaciones
- Representaciones gráficas profesionales
- Requiere matplotlib instalado

## 🧠 Conceptos Implementados

### Estados de Proceso (Modelo de 7 Estados)
1. **Nuevo:** Proceso creado pero sin memoria asignada
2. **Listo:** Proceso con memoria asignada, esperando CPU
3. **Ejecutando:** Proceso actualmente usando CPU
4. **Bloqueado:** Proceso esperando E/S u otro evento
5. **Listo Suspendido:** Proceso listo pero suspendido a disco
6. **Bloqueado Suspendido:** Proceso bloqueado y suspendido
7. **Terminado:** Proceso finalizado, memoria liberada

### Paginación de Memoria
- **Páginas lógicas:** Divisiones del espacio de direcciones del proceso
- **Marcos físicos:** Divisiones de la memoria física real
- **Tabla de páginas:** Mapeo directo página → marco por proceso
- **Traducción de direcciones:** Conversión automática lógica → física

### Gestión de Memoria
- Asignación dinámica de marcos libres
- Liberación automática al terminar procesos
- Verificación de memoria disponible antes de crear procesos
- Estadísticas en tiempo real de uso de memoria

## 🔍 Funcionalidades Destacadas

### Traducción de Direcciones
```python
# Ejemplo: Proceso con páginas en marcos 0 y 1
dirección_lógica = 5120  # Dirección a traducir
página = 5120 // 4096 = 1
offset = 5120 % 4096 = 1024
marco = tabla_páginas[página] = 1
dirección_física = 1 * 4096 + 1024 = 5120
```

### Visualización Gráfica
- Marcos de memoria con código de colores
- Estado de procesos en tiempo real
- Tablas de páginas interactivas
- Estadísticas del sistema actualizadas

### Simulación Automática
- Creación automática de procesos ejemplo
- Simulación de diferentes transiciones de estado
- Demostración de bloqueo y reanudación
- Limpieza automática de procesos terminados

## 🧪 Casos de Prueba

El simulador incluye casos de prueba automáticos que demuestran:

1. **Creación de procesos** con diferentes tamaños
2. **Asignación de memoria** respetando límites físicos
3. **Transiciones de estado** según el modelo de 7 estados
4. **Traducción de direcciones** lógicas a físicas
5. **Liberación de memoria** al terminar procesos
6. **Gestión de memoria** con múltiples procesos simultáneos

## 📊 Representación Gráfica

### Tablas de Páginas Completas
El simulador muestra al menos una tabla de páginas completa que incluye:
- Mapeo página → marco para cada proceso
- Estado actual del proceso
- Tamaño y número de páginas necesarias
- Marcos físicos asignados

### Estado de Marcos de Memoria Física
Visualización en tiempo real que muestra:
- 16 marcos organizados en grilla 4x4
- Estado libre/ocupado de cada marco
- Proceso propietario de cada marco ocupado
- Código de colores según estado del proceso

## 🔬 Tecnologías Utilizadas

- **Python 3.7+:** Lenguaje principal
- **Tkinter:** Interfaz gráfica nativa
- **Matplotlib:** Gráficos avanzados (opcional)
- **Threading:** Simulaciones en segundo plano
- **Arquitectura MVC:** Separación de responsabilidades

## 📝 Cumplimiento de Requerimientos

| Requerimiento | Estado | Implementación |
|---------------|--------|----------------|
| Paginación sin memoria virtual | ✅ | Mapeo directo página→marco |
| Tabla de páginas por proceso | ✅ | Clase PageTable individual |
| Visualización gráfica | ✅ | GUI con Tkinter/Matplotlib |
| Modelo 7 estados | ✅ | Transiciones completas |
| Traducción direcciones | ✅ | Lógica→física automática |
| 3+ procesos simultáneos | ✅ | Hasta 16 marcos disponibles |
| Representación gráfica tablas | ✅ | Pestañas dedicadas |
| Estado marcos memoria | ✅ | Grilla visual actualizada |

## 👨‍💻 Autor

Este proyecto fue desarrollado como entregable del taller de Sistemas Operativos, demostrando la implementación práctica de conceptos de gestión de memoria mediante paginación.
