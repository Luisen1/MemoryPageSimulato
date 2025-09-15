# 🧠 Simulador Web de Paginación de Memoria

## 📖 Descripción General

Este proyecto implementa un **simulador completo e interactivo de paginación de memoria** que se ejecuta directamente en el navegador web. Está diseñado como una herramienta educativa que permite visualizar y comprender los conceptos fundamentales de gestión de memoria mediante paginación.

### 🎯 Objetivos del Proyecto

- **Simular paginación sin memoria virtual:** Implementación pura de paginación básica
- **Visualización interactiva:** Representación gráfica en tiempo real de la memoria física
- **Modelo completo de estados:** Ciclo de vida de procesos con 7 estados diferentes
- **Educación práctica:** Herramienta de aprendizaje visual y experiencial
- **Accesibilidad total:** Sin dependencias complejas, solo navegador web

## Arquitectura del Sistema

### 📁 Estructura del Proyecto

```
MemoryPageSimulato/
├── 📄 README.md              # Este archivo - Documentación completa
├── 🌐 simulador_web.html     # Aplicación web completa (frontend)
├── 🚀 web_launcher.py        # Lanzador automático (backend)
└── 🔒 .gitignore            # Configuración de Git
```

### Arquitectura de Software

#### Frontend (simulador_web.html)
```
HTML5 + CSS3 + JavaScript Vanilla
├── 🎨 Interfaz de Usuario
│   ├── Diseño responsive con CSS Grid/Flexbox
│   ├── Componentes interactivos (botones, tablas, formularios)
│   └── Animaciones y transiciones CSS
├── 🧠 Lógica de Simulación (JavaScript)
│   ├── Clase MemorySimulator (núcleo del simulador)
│   ├── Gestión de procesos y memoria
│   ├── Algoritmos de asignación
│   └── Cálculo de estadísticas
└── 📊 Visualización en Tiempo Real
    ├── Grilla de memoria 4x4 (16 marcos)
    ├── Tabla de procesos dinámica
    ├── Panel de estadísticas
    └── Sistema de notificaciones
```

#### Backend (web_launcher.py)
```
Python Launcher
├── 🔍 Detección automática de archivos
├── 🌐 Apertura automática del navegador
├── 📋 Instrucciones de uso
└── 🛠️ Manejo de errores y troubleshooting
```

## 🎮 Funcionalidades Principales

### 💾 Simulación de Memoria
- **16 marcos de memoria física** de 4KB cada uno (64KB total)
- **Páginas de 4KB** para mantener compatibilidad estándar
- **Asignación dinámica** de marcos libres a procesos
- **Liberación automática** al terminar procesos
- **Detección de memoria insuficiente** con manejo de errores

### 🔄 Gestión de Procesos
- **Creación interactiva** con validación de tamaño (4-32 KB)
- **Estados múltiples:** NEW, READY, RUNNING, WAITING, TERMINATED
- **Transiciones automáticas** entre estados
- **Ejecución simulada** con timeouts realistas
- **Terminación manual o automática**

### 📊 Estadísticas en Tiempo Real
- **Uso de memoria:** Marcos totales, usados, libres, porcentaje
- **Métricas de procesos:** Total creados, activos, terminados
- **Análisis de eficiencia:** Fragmentación, utilización efectiva
- **Visualización de datos:** Actualizaciones automáticas cada segundo

### 🎨 Interfaz Interactiva
- **Diseño con pestañas:** Simulación, Aprendizaje, Estadísticas
- **Visualización por colores:** Estados diferenciados cromáticamente
- **Simulación automática:** Demostración guiada paso a paso
- **Contenido educativo:** Explicaciones integradas de conceptos

## 🧮 Algoritmos Implementados

### 🔢 Gestión de Memoria

#### Algoritmo de Asignación de Marcos
```javascript
function allocateMemory(process) {
    // 1. Calcular páginas necesarias
    const pagesNeeded = Math.ceil(process.size / PAGE_SIZE);
    
    // 2. Encontrar marcos libres
    const availableFrames = this.getAvailableFrames();
    
    // 3. Verificar disponibilidad
    if (availableFrames.length < pagesNeeded) {
        throw new Error('Memoria insuficiente');
    }
    
    // 4. Asignar marcos consecutivos disponibles
    const framesToAllocate = availableFrames.slice(0, pagesNeeded);
    
    // 5. Actualizar tabla de páginas
    for (let i = 0; i < pagesNeeded; i++) {
        process.pageTable.set(i, framesToAllocate[i]);
        this.frames[framesToAllocate[i]] = process;
    }
}
```

#### Algoritmo de Traducción de Direcciones
```javascript
function translateAddress(logicalAddress, process) {
    // 1. Calcular número de página
    const pageNumber = Math.floor(logicalAddress / PAGE_SIZE);
    
    // 2. Calcular offset dentro de la página
    const offset = logicalAddress % PAGE_SIZE;
    
    // 3. Buscar marco físico en tabla de páginas
    const frameNumber = process.pageTable.get(pageNumber);
    
    // 4. Calcular dirección física
    const physicalAddress = (frameNumber * PAGE_SIZE) + offset;
    
    return {
        logicalAddress,
        pageNumber,
        offset,
        frameNumber,
        physicalAddress
    };
}
```

### 🔄 Gestión de Estados de Procesos

#### Máquina de Estados Implementada
```
NEW ────────────────┐
  │                 │
  └──→ READY ───────┼──→ RUNNING ───┐
         ↑          │       │       │
         │          │       ↓       │
         └──────────┼─── WAITING    │
                    │               │
                    │               ↓
                    └────────── TERMINATED
```

#### Algoritmo de Transición de Estados
```javascript
function transitionTo(process, newState) {
    const currentState = process.state;
    
    // Validar transiciones permitidas
    const validTransitions = {
        'NEW': ['READY'],
        'READY': ['RUNNING', 'TERMINATED'],
        'RUNNING': ['READY', 'WAITING', 'TERMINATED'],
        'WAITING': ['READY', 'TERMINATED'],
        'TERMINATED': [] // Estado final
    };
    
    if (!validTransitions[currentState].includes(newState)) {
        throw new Error(`Transición inválida: ${currentState} → ${newState}`);
    }
    
    // Ejecutar transición
    process.state = newState;
    
    // Acciones especiales por estado
    if (newState === 'TERMINATED') {
        this.deallocateMemory(process);
    }
}
```

## 🔧 Implementación Técnica Detallada

### 📱 Frontend: HTML + CSS + JavaScript

#### Estructura HTML5
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <!-- Meta tags para responsive design -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- CSS embebido para portabilidad -->
    <style>/* Estilos responsive y profesionales */</style>
</head>
<body>
    <!-- Contenedor principal -->
    <div class="container">
        <!-- Header con título e información -->
        <div class="header">...</div>
        
        <!-- Sistema de pestañas -->
        <div class="tabs">...</div>
        
        <!-- Contenido dinámico por pestaña -->
        <div class="tab-content">...</div>
    </div>
    
    <!-- JavaScript embebido para funcionalidad completa -->
    <script>/* Lógica completa del simulador */</script>
</body>
</html>
```

#### CSS3 Responsive Design
```css
/* Sistema de Grid para memoria */
.memory-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    max-width: 500px;
    margin: 20px auto;
}

/* Estados de marco con colores semánticos */
.memory-frame.free { background: #e9ecef; }     /* Gris - Libre */
.memory-frame.new { background: #ffeaa7; }      /* Amarillo - Nuevo */
.memory-frame.ready { background: #74b9ff; }    /* Azul - Listo */
.memory-frame.running { background: #00b894; }  /* Verde - Ejecutando */
.memory-frame.waiting { background: #fdcb6e; }  /* Naranja - Esperando */
.memory-frame.terminated { background: #fd79a8; } /* Rosa - Terminado */

/* Diseño responsive para móviles */
@media (max-width: 768px) {
    .memory-grid {
        grid-template-columns: repeat(2, 1fr);
        max-width: 300px;
    }
}
```

#### JavaScript ES6+ Simulador
```javascript
class MemorySimulator {
    constructor() {
        this.frames = new Array(16).fill(null);  // 16 marcos físicos
        this.processes = new Map();              // Mapa de procesos activos
        this.nextPid = 1;                       // Contador de PIDs
        this.isSimulating = false;              // Estado de simulación
    }
    
    // Método principal para crear procesos
    createProcess(size, name = null) {
        // Validación de entrada
        if (size < 4 || size > 32) {
            throw new Error('Tamaño inválido');
        }
        
        // Cálculo de páginas necesarias
        const pagesNeeded = Math.ceil(size / 4);
        
        // Verificación de memoria disponible
        if (this.getAvailableFrames().length < pagesNeeded) {
            throw new Error('Memoria insuficiente');
        }
        
        // Creación del proceso
        const process = {
            pid: this.nextPid++,
            name: name || `Proceso ${this.nextPid - 1}`,
            size: size,
            pages: pagesNeeded,
            state: 'NEW',
            frames: [],
            pageTable: new Map()
        };
        
        // Registro y asignación
        this.processes.set(process.pid, process);
        this.allocateMemory(process);
        this.transitionTo(process, 'READY');
        
        return process;
    }
}
```

### 🚀 Backend: Python Launcher

#### Arquitectura del Lanzador
```python
#!/usr/bin/env python3
"""
Lanzador Web del Simulador
- Detección automática de archivos
- Apertura del navegador
- Manejo de errores
- Instrucciones de uso
"""

import os, webbrowser, sys
from pathlib import Path

def main():
    try:
        # 1. Verificar archivos necesarios
        html_path = get_html_path()
        
        # 2. Detectar navegador disponible
        check_browser()
        
        # 3. Abrir automáticamente
        open_browser(html_path)
        
        # 4. Mostrar instrucciones
        show_instructions()
        
    except Exception as e:
        handle_error(e)
```

## 🎓 Conceptos Educativos Implementados

### 🧠 Paginación de Memoria

#### ¿Qué es la Paginación?
La paginación es una técnica de gestión de memoria que:

1. **Divide la memoria física** en bloques de tamaño fijo llamados "marcos"
2. **Divide la memoria lógica** en bloques del mismo tamaño llamados "páginas"
3. **Permite asignación no contigua** - las páginas pueden estar en marcos dispersos
4. **Elimina fragmentación externa** - todos los bloques son del mismo tamaño
5. **Simplifica la gestión** - operaciones uniformes para todos los tamaños

#### Implementación en el Simulador
```
Memoria Física: 64KB divididos en 16 marcos de 4KB
┌─────┬─────┬─────┬─────┐
│ M0  │ M1  │ M2  │ M3  │  Fila 0: Marcos 0-3
├─────┼─────┼─────┼─────┤
│ M4  │ M5  │ M6  │ M7  │  Fila 1: Marcos 4-7
├─────┼─────┼─────┼─────┤
│ M8  │ M9  │ M10 │ M11 │  Fila 2: Marcos 8-11
├─────┼─────┼─────┼─────┤
│ M12 │ M13 │ M14 │ M15 │  Fila 3: Marcos 12-15
└─────┴─────┴─────┴─────┘

Proceso de 12KB = 3 páginas → Necesita 3 marcos
Puede asignarse a marcos no consecutivos: M1, M5, M14
```

### 🔄 Estados de Proceso

#### Modelo de 7 Estados Implementado
```
1. NEW (Nuevo)
   - Proceso creado pero sin memoria asignada
   - Color: Amarillo claro
   - Duración: Instantánea (transición automática)

2. READY (Listo)
   - Proceso con memoria asignada, esperando CPU
   - Color: Azul
   - Puede ejecutarse inmediatamente

3. RUNNING (Ejecutando)
   - Proceso actualmente usando CPU
   - Color: Verde
   - Estado activo de procesamiento

4. WAITING (Esperando)
   - Proceso bloqueado esperando E/S
   - Color: Naranja
   - Implementado para completitud teórica

5. TERMINATED (Terminado)
   - Proceso finalizado, memoria liberada
   - Color: Rosa
   - Estado final - memoria se libera automáticamente
```

### 📊 Traducción de Direcciones

#### Fórmula Implementada
```
Dirección Lógica → Dirección Física

1. Página = Dirección_Lógica ÷ Tamaño_Página
2. Offset = Dirección_Lógica % Tamaño_Página
3. Marco = Tabla_Páginas[Página]
4. Dirección_Física = (Marco × Tamaño_Página) + Offset
```

#### Ejemplo Práctico
```
Proceso con tabla de páginas:
Página 0 → Marco 5
Página 1 → Marco 12

Traducir dirección lógica 6144:
1. Página = 6144 ÷ 4096 = 1
2. Offset = 6144 % 4096 = 2048
3. Marco = Tabla[1] = 12
4. Dirección_Física = (12 × 4096) + 2048 = 51200
```

## 🎮 Manual de Usuario Completo

### 🚀 Instalación y Ejecución

#### Método 1: Ejecución Automática (Recomendado)
```bash
# 1. Abrir terminal en el directorio del proyecto
cd MemoryPageSimulato

# 2. Ejecutar lanzador automático
python web_launcher.py

# 3. El navegador se abre automáticamente
# ¡Listo para usar!
```

#### Método 2: Apertura Manual
```bash
# Si hay problemas con el lanzador:
# 1. Abrir cualquier navegador web
# 2. Ir a Archivo → Abrir archivo
# 3. Seleccionar simulador_web.html
# 4. ¡Funciona igual!
```

### 🎯 Uso Paso a Paso

#### Primer Uso: Familiarización
1. **Explora la pestaña "Aprender"**
   - Lee los conceptos fundamentales
   - Entiende qué es la paginación
   - Familiarízate con los estados de proceso

2. **Ve a "Simulación"**
   - Observa la grilla de 16 marcos de memoria
   - Todos están en gris (libres) inicialmente
   - Lee la leyenda de colores

3. **Crea tu primer proceso**
   - Clic en "➕ Crear Proceso"
   - Ingresa 8 (KB) como tamaño
   - Observa cómo se asignan 2 marcos automáticamente

#### Experimentación Básica
4. **Observa los cambios visuales**
   - Los marcos cambian de gris a azul (READY)
   - La tabla de procesos se actualiza
   - Las estadísticas cambian en tiempo real

5. **Ejecuta el proceso**
   - Clic en "▶️" en la tabla de procesos
   - El color cambia a verde (RUNNING)
   - Después de 2 segundos cambia a rosa (TERMINATED)
   - Los marcos se liberan (vuelven a gris)

#### Experimentación Avanzada
6. **Crea múltiples procesos**
   - Crea procesos de diferentes tamaños: 4KB, 12KB, 16KB
   - Observa cómo se distribuyen en la memoria
   - Nota que pueden ubicarse en marcos no consecutivos

7. **Prueba la simulación automática**
   - Clic en "🎯 Simulación Automática"
   - Observa la secuencia completa automatizada
   - Ve cómo se crean, ejecutan y terminan procesos

8. **Analiza las estadísticas**
   - Ve a la pestaña "📊 Estadísticas"
   - Observa métricas como uso de memoria, eficiencia
   - Comprende el análisis de rendimiento

### 🔧 Funcionalidades Avanzadas

#### Interacción con Marcos de Memoria
- **Clic en cualquier marco** → Muestra información detallada
- **Marcos libres** → Información de disponibilidad
- **Marcos ocupados** → Proceso propietario, página lógica, tamaño

#### Control de Procesos Individual
- **Botón ▶️** → Ejecutar proceso específico
- **Botón ❌** → Terminar proceso manualmente
- **Selección de fila** → Ver detalles del proceso

#### Simulación Automática Controlada
- **Inicio/Pausa** → Control total de la demostración
- **Velocidad variable** → Observa a tu ritmo
- **Secuencias predefinidas** → Casos de uso educativos

## 🔍 Análisis de Rendimiento

### 📈 Métricas Implementadas

#### Métricas Básicas de Memoria
```javascript
// Cálculo en tiempo real
const memoryUsage = {
    total: 16,                              // Marcos totales
    used: framesWithProcesses.length,       // Marcos ocupados
    free: 16 - used,                        // Marcos libres
    percentage: Math.round((used/16) * 100) // Porcentaje uso
};
```

#### Métricas de Procesos
```javascript
const processMetrics = {
    totalCreated: this.processes.size,           // Total histórico
    active: activeProcesses.length,              // Procesos vivos
    terminated: total - active,                  // Procesos finalizados
    averageSize: calculateAverageSize(active)    // Tamaño promedio
};
```

#### Análisis de Eficiencia
```javascript
const efficiency = {
    memoryUtilization: (used / total) * 100,     // % memoria usada
    averageProcessSize: totalSize / processCount, // Tamaño medio
    fragmentation: calculateFragmentation(),       // Fragmentación
    systemLoad: active / maxConcurrent           // Carga del sistema
};
```

### 🎯 Interpretación de Resultados

#### Utilización de Memoria Óptima
- **0-25%:** Sistema infrautilizado, puede aceptar más procesos
- **26-75%:** Rango óptimo de operación
- **76-90%:** Alta utilización, monitorear de cerca
- **91-100%:** Sistema saturado, posibles rechazos

#### Fragmentación (en contexto de paginación)
- **Fragmentación externa:** ❌ Eliminada por diseño de paginación
- **Fragmentación interna:** ✅ Presente, calculada automáticamente
- **Fórmula:** `(Memoria_Asignada - Memoria_Usada) / Memoria_Asignada`

## 🛠️ Personalización y Extensión

### 🔧 Parámetros Configurables

#### Constantes del Sistema (en JavaScript)
```javascript
// Configuración de memoria
const TOTAL_FRAMES = 16;        // Número de marcos físicos
const PAGE_SIZE = 4;            // Tamaño de página en KB
const TOTAL_MEMORY = 64;        // Memoria total en KB

// Límites de procesos
const MIN_PROCESS_SIZE = 4;     // Tamaño mínimo de proceso
const MAX_PROCESS_SIZE = 32;    // Tamaño máximo de proceso
const MAX_CONCURRENT = 8;       // Procesos simultáneos máximos

// Tiempos de simulación
const EXECUTION_TIME = 2000;    // Tiempo de ejecución en ms
const ANIMATION_SPEED = 1000;   // Velocidad de animación
```

#### Colores de Estado (en CSS)
```css
/* Personalización de colores */
:root {
    --color-free: #e9ecef;      /* Marcos libres */
    --color-new: #ffeaa7;       /* Procesos nuevos */
    --color-ready: #74b9ff;     /* Procesos listos */
    --color-running: #00b894;   /* Procesos ejecutando */
    --color-waiting: #fdcb6e;   /* Procesos esperando */
    --color-terminated: #fd79a8; /* Procesos terminados */
}
```

### 🚀 Extensiones Posibles

#### Algoritmos de Reemplazo
```javascript
// Extensión futura: Implementar LRU
class LRUPageReplacement {
    constructor() {
        this.accessHistory = new Map();
    }
    
    selectVictimPage(process) {
        // Lógica LRU aquí
        return oldestPage;
    }
}
```

#### Memoria Virtual
```javascript
// Extensión futura: Swap space
class VirtualMemoryManager extends MemorySimulator {
    constructor() {
        super();
        this.swapSpace = new Array(32).fill(null); // Área de intercambio
    }
    
    swapOut(process) {
        // Mover proceso a disco
    }
    
    swapIn(process) {
        // Traer proceso de disco
    }
}
```

#### Múltiples Algoritmos
```javascript
// Extensión futura: Comparación de algoritmos
const algorithms = {
    'FIFO': new FIFOAlgorithm(),
    'LRU': new LRUAlgorithm(),
    'Optimal': new OptimalAlgorithm()
};
```

## 📚 Referencias y Recursos 

### 📖 Libros Recomendados
- **"Operating System Concepts"** - Silberschatz, Galvin, Gagne
- **"Modern Operating Systems"** - Andrew S. Tanenbaum
- **"Operating Systems: Three Easy Pieces"** - Remzi Arpaci-Dusseau

### 🌐 Recursos Online
- **GeeksforGeeks:** Paging in Operating System
- **Tutorialspoint:** Operating System - Memory Management
- **Khan Academy:** Intro to Operating Systems

