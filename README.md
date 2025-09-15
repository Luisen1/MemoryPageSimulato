# 🧠 Simulador Web de Paginación de Memoria

## 📖 Descripción General

Este proyecto implementa un **simulador completo e interactivo de paginación de memoria** que se ejecuta directamente en el navegador web. Está diseñado como una herramienta educativa para estudiantes de Sistemas Operativos que permite visualizar y comprender los conceptos fundamentales de gestión de memoria mediante paginación.

### 🎯 Objetivos del Proyecto

- **Simular paginación sin memoria virtual:** Implementación pura de paginación básica
- **Visualización interactiva:** Representación gráfica en tiempo real de la memoria física
- **Modelo completo de estados:** Ciclo de vida de procesos con 7 estados diferentes
- **Educación práctica:** Herramienta de aprendizaje visual y experiencial
- **Accesibilidad total:** Sin dependencias complejas, solo navegador web

## 🏗️ Arquitectura del Sistema

### 📁 Estructura del Proyecto

```
MemoryPageSimulato/
├── 📄 README.md              # Este archivo - Documentación completa
├── 🌐 simulador_web.html     # Aplicación web completa (frontend)
├── 🚀 web_launcher.py        # Lanzador automático (backend)
└── 🔒 .gitignore            # Configuración de Git
```

### 🏛️ Arquitectura de Software

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

## 📊 Casos de Uso Educativos

### 🎓 Para Estudiantes

#### Caso 1: Comprensión Básica
**Objetivo:** Entender qué es un marco y una página
```
1. Crear proceso de 4KB (1 página)
2. Observar que ocupa exactamente 1 marco
3. Crear proceso de 8KB (2 páginas)
4. Observar que ocupa exactamente 2 marcos
5. Conclusión: 1 página = 1 marco = 4KB
```

#### Caso 2: Fragmentación vs Paginación
**Objetivo:** Ver por qué la paginación elimina fragmentación externa
```
1. Crear varios procesos pequeños (4KB, 8KB, 4KB)
2. Terminar el proceso del medio
3. Crear proceso grande (12KB)
4. Observar que se ubica en marcos disponibles
5. Conclusión: Sin fragmentación externa, marcos siempre útiles
```

#### Caso 3: Traducción de Direcciones
**Objetivo:** Comprender la conversión lógica → física
```
1. Crear proceso y notar qué marcos ocupa
2. Usar información del marco para entender tabla de páginas
3. Calcular manualmente algunas traducciones
4. Verificar con la herramienta
5. Conclusión: La tabla de páginas es la clave
```

### 👨‍🏫 Para Profesores

#### Demostración en Clase
**Preparación:** Proyectar en pantalla grande
```
1. Mostrar concepto de memoria física dividida
2. Crear proceso en vivo y explicar asignación
3. Usar simulación automática para flujo completo
4. Responder preguntas con ejemplos inmediatos
5. Permitir a estudiantes sugerir experimentos
```

#### Ejercicios Dirigidos
**Actividad grupal:** Resolver problemas específicos
```
1. "¿Cuántos procesos de 12KB caben en memoria?"
2. "¿Qué pasa si creamos 5 procesos de 16KB?"
3. "¿Por qué algunos marcos quedan separados?"
4. Usar simulador para verificar respuestas
5. Discutir implicaciones prácticas
```

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

## 🐛 Solución de Problemas

### ❓ Problemas Comunes

#### El simulador no se abre
**Síntomas:** Error al ejecutar `python web_launcher.py`
```bash
# Verificar Python
python --version  # Debe ser 3.6+

# Verificar archivos
ls -la  # Debe mostrar simulador_web.html

# Método alternativo
# Abrir simulador_web.html manualmente en navegador
```

#### JavaScript deshabilitado
**Síntomas:** Página se carga pero no responde a clics
```
Solución:
1. Configuración del navegador
2. Buscar "JavaScript" o "Scripting"
3. Habilitar para todos los sitios
4. Refrescar página (F5)
```

#### Visualización incorrecta
**Síntomas:** Diseño desorganizado, elementos superpuestos
```
Causas posibles:
- Navegador muy antiguo → Actualizar navegador
- Ventana muy pequeña → Redimensionar ventana
- Zoom incorrecto → Resetear zoom (Ctrl+0)
```

#### Performance lenta
**Síntomas:** Respuesta lenta a acciones del usuario
```
Optimizaciones:
- Cerrar otras pestañas del navegador
- Reducir velocidad de simulación automática
- Usar navegadores más eficientes (Chrome, Firefox)
```

### 🔧 Debugging y Desarrollo

#### Consola de Desarrollador
```javascript
// Abrir con F12 en la mayoría de navegadores
// Comandos útiles para debugging:

// Ver estado actual del simulador
console.log(simulator);

// Ver memoria actual
console.log(simulator.frames);

// Ver procesos activos
console.log(simulator.getActiveProcesses());

// Crear proceso desde consola
simulator.createProcess(12, "Debug Process");
```

#### Modificaciones en Vivo
```javascript
// Cambiar parámetros durante ejecución
simulator.isSimulating = false;  // Detener simulación
EXECUTION_TIME = 5000;          // Cambiar tiempo de ejecución
updateMemoryDisplay();          // Refrescar visualización
```

## 📚 Referencias y Recursos Adicionales

### 📖 Libros Recomendados
- **"Operating System Concepts"** - Silberschatz, Galvin, Gagne
- **"Modern Operating Systems"** - Andrew S. Tanenbaum
- **"Operating Systems: Three Easy Pieces"** - Remzi Arpaci-Dusseau

### 🌐 Recursos Online
- **GeeksforGeeks:** Paging in Operating System
- **Tutorialspoint:** Operating System - Memory Management
- **Khan Academy:** Intro to Operating Systems

### 🎓 Conceptos Relacionados para Estudio Adicional
- **Segmentación de memoria** - Alternativa a paginación
- **Memoria virtual** - Extensión con almacenamiento secundario
- **Translation Lookaside Buffer (TLB)** - Cache de tabla de páginas
- **Working Set** - Conjunto de páginas activamente usadas
- **Thrashing** - Problema de exceso de paginación

## 🎯 Conclusiones y Valor Educativo

### 🏆 Logros del Proyecto

Este simulador cumple exitosamente con todos los objetivos educativos planteados:

1. **✅ Visualización clara:** La representación gráfica hace tangibles conceptos abstractos
2. **✅ Interactividad total:** El usuario experimenta directamente con los algoritmos
3. **✅ Accesibilidad máxima:** Solo requiere navegador web, sin instalaciones complejas
4. **✅ Pedagogía efectiva:** Combina teoría, práctica y experimentación
5. **✅ Escalabilidad:** Fácilmente extensible para conceptos más avanzados

### 🎓 Valor para el Aprendizaje

#### Para Estudiantes
- **Comprensión visual:** Ve exactamente cómo funciona la paginación
- **Experimentación segura:** Prueba diferentes escenarios sin consecuencias
- **Aprendizaje activo:** Manipula directamente los conceptos teóricos
- **Preparación práctica:** Ejercita habilidades para exámenes y proyectos

#### Para Educadores
- **Herramienta versátil:** Adaptable a diferentes niveles y enfoques
- **Demostración efectiva:** Muestra conceptos complejos de forma simple
- **Evaluación práctica:** Permite ejercicios específicos y medibles
- **Engagement estudiantil:** Mantiene atención e interés

### 🚀 Impacto en la Comprensión

Este simulador transforma el aprendizaje de gestión de memoria de:

**Antes:** "La paginación divide la memoria en bloques..." (abstracto, difícil)
**Después:** "Veo cómo este proceso de 12KB se divide en 3 páginas que van a los marcos 2, 7 y 11" (concreto, claro)

**Antes:** "La tabla de páginas mapea direcciones..." (teórico, memorización)
**Después:** "Si accedo a la dirección 8192, voy a la página 2, que está en el marco 11, entonces la dirección física es 45056" (práctico, comprensión)

### 🔮 Proyección Futura

Este proyecto establece las bases para simuladores más avanzados que podrían incluir:

- **Múltiples algoritmos** de reemplazo de páginas
- **Memoria virtual completa** con swap space
- **Concurrencia real** entre procesos
- **Análisis de rendimiento** más sofisticado
- **Casos de estudio** de sistemas reales

---

## 🏃‍♂️ ¡Empezar Ahora!

```bash
# Un solo comando para comenzar:
python web_launcher.py

# ¡Y ya estás explorando la paginación de memoria!
```

**¿Listo para dominar la gestión de memoria? ¡El simulador te está esperando!** 🚀
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

### 2. 🎯 GUI Simplificada (`gui_simple.py`)
- Interfaz gráfica básica con Tkinter
- Creación manual de procesos
- Visualización simple de memoria
- Ideal para entornos con recursos limitados

### 3. 🌟 GUI Completa (`main.py`)
- Interfaz avanzada con matplotlib
- Gráficos profesionales de memoria
- Visualización de tabla de páginas
- Estadísticas detalladas del sistema

### 4. 🆕 **GUI Interactiva Educativa** (`gui_interactivo.py`)
- **Nueva versión mejorada y educativa**
- **Interfaz con múltiples pestañas**
- **Simulación automática guiada**
- **Contenido educativo integrado**
- **Estadísticas avanzadas con gráficos**
- **Modo interactivo para aprendizaje**

### 5. 🎓 **Demo Interactiva** (`demo_interactivo.py`)
- **Demostración guiada paso a paso**
- **Tres modos: Básico, Avanzado y Libre**
- **Tutorial integrado con explicaciones**
- **Perfecto para estudiantes**

**Ejemplo de salida en consola:**
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

### 4. 🆕 **GUI Interactiva Educativa** (`gui_interactivo.py`)
**¡Nueva versión mejorada para aprendizaje!**

**Características principales:**
- **🎮 Interfaz con pestañas múltiples:** Simulación, Aprendizaje, Estadísticas
- **🎯 Simulación automática:** Demostración guiada paso a paso
- **📚 Contenido educativo integrado:** Explicaciones de conceptos clave
- **📊 Estadísticas avanzadas:** Gráficos en tiempo real con matplotlib
- **⚡ Control de velocidad:** Ajuste de velocidad de simulación
- **🎨 Visualización mejorada:** Memoria en grid 4x4 con efectos visuales
- **📋 Gestión interactiva:** Menús contextuales para procesos
- **❓ Sistema de ayuda:** Tutoriales y documentación integrada

**Pestañas disponibles:**
- **🖥️ Simulación:** Panel principal con controles y visualización
- **🎓 Aprender:** Contenido educativo sobre paginación de memoria
- **📈 Estadísticas:** Gráficos avanzados de rendimiento del sistema

### 6. � **Versión Web** (`web_launcher.py` + `simulador_web.html`)
**¡Nueva versión que no requiere dependencias!**

**Características principales:**
- **🌐 Solo requiere navegador web** - No necesita Tkinter ni matplotlib
- **� Compatible con cualquier dispositivo** - PC, tablet, móvil
- **🎮 Interfaz completamente funcional** con todas las características
- **🚀 Cero configuración** - Solo ejecutar y usar
- **🎨 Diseño responsive** - Se adapta al tamaño de pantalla
- **📊 JavaScript nativo** - Sin dependencias externas

**Ventajas únicas:**
- **Soluciona problemas de dependencias** - Ideal si Tkinter no funciona
- **Multiplataforma real** - Funciona en Windows, Mac, Linux
- **Instalación cero** - Solo necesita Python básico y navegador
- **Compartible** - El archivo HTML se puede enviar a otros
- **Offline** - No requiere conexión a internet

**Uso:**
```bash
python web_launcher.py
# Se abre automáticamente en el navegador
# ¡Listo para usar inmediatamente!
```

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
