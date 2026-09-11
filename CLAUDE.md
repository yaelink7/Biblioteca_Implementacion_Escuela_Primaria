# Sistema de Biblioteca — Escuela Primaria Adalberto Tejeda

Contexto completo del proyecto. Este archivo lo lee Claude Code automáticamente
al abrir el repositorio, así que una sesión nueva en cualquier computadora
arranca sabiendo qué se hizo, por qué, y qué falta.

## Qué es

Proyecto integrador de la asignatura **Programación e Implementación de
Sistemas** (7.º semestre). Consiste en **migrar a Python** un sistema de
biblioteca escolar que ya existía en Java, y entregarlo a una escuela primaria
real de Veracruz que hoy lleva su biblioteca en cuadernos de papel.

No es un ejercicio: hay un cliente real, con una bibliotecaria que va a usar
esto, y datos de menores de edad de por medio.

| | |
|---|---|
| Equipo | 5 integrantes, metodología SCRUM |
| Periodo | 14 de septiembre – 28 de noviembre de 2026, 5 sprints de 2 semanas |
| Repositorio | `yaelink7/Biblioteca_Implementacion_Escuela_Primaria` |
| Tablero | `github.com/users/yaelink7/projects/3` |
| Sistema Java original | `yaelink7/Proyecto-Biblioteca-IngenieriaSoftware` |

### El equipo

| Integrante | GitHub | Rol |
|---|---|---|
| Yael Arenas Guevara | `yaelink7` | Scrum Master · dueña del repositorio |
| Rey David Montes Ciriaco | `DavC010` | Product Owner |
| Yahir Reyes Velasco | `yahirrev` | Desarrollo |
| Pedro Cabrera Barrios Ángel | `Pedro20-amd` | Desarrollo · calidad |
| Roberto Ellyan Vázquez Arriaga | `robertovaz573` | Calidad y pruebas |

---

## Reglas de trabajo

Estas no son preferencias de estilo: son acuerdos con Yael.

1. **No modificar código sin informarlo antes y recibir permiso explícito.**
   Leer, analizar, auditar y proponer no requieren permiso; escribir sí.
2. **Un PR por unidad de propósito.** Nunca acumular varios cambios distintos
   en una rama.
3. **Los PR llevan descripción completa** de todo lo que se agregó: archivos
   nuevos y su propósito, decisiones de diseño con su motivo, defectos
   corregidos con su identificador, cambios de dependencias, datos cargados
   en Supabase, salida real de las pruebas, y lo que queda pendiente.
4. **Abrir un PR solo cuando el anterior ya esté en `main`.** Encadenar PR
   (uno apuntando a la rama de otro) ya falló dos veces en este proyecto:
   al mergearlos seguidos, GitHub no reajusta las bases a tiempo y los
   cambios terminan en la rama intermedia en lugar de `main`.
5. **El código y los comentarios van en español**, sin el sufijo `Biblia`
   que usaban los paquetes del sistema Java (`GUIBiblia`, `DAOBiblia`).

---

## Arquitectura

### Dos clientes, un servicio

```
┌──────────────────────┐   ┌──────────────────────┐
│ Escritorio PySide6   │   │ App móvil (fase 2)   │
│ personal de la       │   │ alumnos              │
│ biblioteca           │   │ aún no existe        │
└──────────┬───────────┘   └──────────┬───────────┘
           │ supabase-py              │ supabase_flutter
           └─────────────┬────────────┘
                         ▼
           ┌─────────────────────────────┐
           │ Supabase · PostgreSQL 17    │
           │ Auth · RLS · API REST       │
           │ Disparadores y funciones    │ ← las reglas viven aquí
           └─────────────────────────────┘
```

### La decisión que ordena todo el proyecto

**Las reglas de negocio viven en Postgres, no en Python.** Esto no es
casualidad ni gusto: es para que la app móvil planeada las herede sin
reimplementarlas, y para que se cumplan aunque alguien llame la API
directamente saltándose el cliente.

| Regla | Dónde vive | Requisito |
|---|---|---|
| Un libro por alumno | Índice único parcial en `prestamos` | REQ-PRE-01 |
| Plazo de 7 días | Disparador `calcular_fecha_limite` | REQ-PRE-02 |
| Movimiento de inventario | Disparador `mover_inventario` | REQ-PRE-01 |
| No dar de baja con préstamos activos | Disparador `validar_baja_de_libro` | REQ-LIB-03 |
| Año de publicación no futuro | Disparador `validar_ano_publicacion` | REQ-LIB-01 |
| Fecha de devolución | Disparador `sellar_devolucion` | — |
| Solo admin cambia perfiles de acceso | Disparador `proteger_rol` | — |
| Acceso por perfil | Políticas RLS en las 7 tablas | Factibilidad Legal |

**Corolario importante:** si vas a añadir una regla de negocio, pregúntate
primero si puede vivir en la base. Los repositorios de Python solo invocan y
traducen el error a algo que el bibliotecario entienda.

**Segundo corolario:** las fechas y los plazos **los calcula la base, no
Python**. La base corre en UTC y los equipos en hora de Veracruz (UTC−6):
seis horas de cada día los dos relojes no coinciden. Ya se corrigió un
defecto por esto; no lo reintroduzcas usando `date.today()` para calcular
retrasos o plazos.

### Estructura del código

```
src/biblioteca/
  core/            configuración, conexión y sesión
    config.py        lee el .env
    supabase_cliente.py
    sesion.py        inicio y cierre de sesión, perfil en curso
  modelos/         entidades del dominio, sin acceso a datos
    persona.py       Perfil → Alumno, Empleado
    libro.py         Publicacion → Libro
    prestamo.py      Prestamo, EstadoPrestamo
  repositorios/    una consulta por operación
    libros.py  personas.py  prestamos.py
  servicios/       reglas independientes de la interfaz
    validador_libro.py  validador_persona.py
  ui/              interfaz de escritorio
    disenos/         archivos .ui que se abren en Qt Designer
    generado/        ui_*.py que produce el compilador — NO editar a mano
    *.py             la lógica: aquí se conectan los botones
herramientas/
  compilar_ui.py   convierte los .ui en módulos de Python
database/migraciones/   esquema versionado, ya aplicado en Supabase
tests/                  pruebas con pytest
Documentacion/          entregables de la materia
```

Equivalencias con el sistema Java, por si hay que consultar el original:

| Sistema Java | Aquí |
|---|---|
| Paquete de entidades | `modelos/` |
| Paquete de acceso a datos | `repositorios/` |
| Paquete de ventanas Swing | `ui/` |
| `ConexionBD.java` | `core/supabase_cliente.py` |
| Validaciones dentro de cada formulario | `servicios/` (capa nueva) |

---

## Cómo trabajar en el proyecto

### Preparar el entorno

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Hace falta un archivo `.env` en la raíz, que **no está en el repositorio**:

```
SUPABASE_URL=https://gibenzgxkbmalljqroxe.supabase.co
SUPABASE_KEY=<llave publishable, pedirla al Scrum Master>
```

La llave `sb_publishable_` no es secreta: está diseñada para ir dentro de
aplicaciones que cualquiera puede descompilar, y su seguridad depende de las
políticas RLS. Lo que **nunca** debe salir del panel de Supabase es la llave
`service_role`, que se salta RLS por completo.

### Ejecutar

```bash
.venv/Scripts/python.exe main.py
```

### Pruebas

```bash
.venv/Scripts/python.exe -m pytest tests/ -v
```

28 pruebas, corren **sin base de datos ni credenciales** en menos de un
segundo. Eso es deliberado: la suite del sistema Java tardaba 13.6 s y
exigía MySQL activo, que es justo por lo que su cobertura se quedó corta.

### Editar las pantallas

Los diseños se editan visualmente, no a mano:

```bash
.venv/Lib/site-packages/PySide6/designer.exe        # abrir Qt Designer
.venv/Scripts/python.exe herramientas/compilar_ui.py # recompilar tras editar
```

Se editan los `.ui` de `ui/disenos/`. Los `ui_*.py` de `ui/generado/` los
produce el compilador y **se sobrescriben**: nunca edites ahí.

### Base de datos

El esquema está en `database/migraciones/`, numerado y ya aplicado en
Supabase. Los archivos son el registro de lo que corrió: **para cambiar algo,
se crea una migración nueva**, nunca se edita una anterior.

---

## Estado al 11 de septiembre de 2026

**La migración del sistema Java está terminada.** Todas las ventanas del
original tienen equivalente, y el sistema nuevo hace bastante más.

### Avance del backlog: 26 de 43 historias (60 %)

| Sprint | Cerradas | Avance |
|---|---|---|
| Sprint 0 · Cimientos | 6/10 | 60 % |
| Sprint 1 · Identidad y personas | 7/11 | 63 % |
| Sprint 2 · Catálogo y búsqueda | 6/8 | 75 % |
| Sprint 3 · Préstamos | 6/7 | 85 % |
| Sprint 4 · Reportes y avisos | 1/7 | 14 % |

Los sprints 2 y 3 estaban planeados para octubre y noviembre: van adelantados
porque situar las reglas en la base permitió construir las pantallas sobre
lógica ya probada.

### Lo que funciona

Cinco pestañas, todas contra la base real: **Catálogo** (alta, modificación,
baja lógica, búsqueda parcial), **Préstamos** (registro en dos búsquedas y un
botón, devolución, filtro de vencidos), **Alumnos** (padrón, alta, historial),
**Deudores** (reporte que abre ya generado) y **Empleados** (plantilla, alta,
permisos por perfil).

### Lo que falta

| Historia | Qué es |
|---|---|
| `NOT-01`, `NOT-02` | Correos automáticos de vencimiento y su bitácora (REQ-PRE-04) |
| `USU-03` | Registro de cuentas con contraseña propia (REQ-USU-01) |
| `LIB-04` | Bitácora de trazabilidad: la tabla existe, ningún disparador escribe en ella |
| `REP-02` | Reporte de libros faltantes — la vista `v_libros_faltantes` ya existe, falta la pantalla |
| `REP-03` | Exportación a CSV — cierra los defectos D-02, D-04 y D-05 del sistema Java |
| `PRE-05` | Marcado diario de vencidos: la función existe pero `pg_cron` no está instalado, así que nadie la llama sola |
| `QA-02`, `QA-03`, `QA-04` | Ampliar pruebas y aceptación con el docente |
| `DOC-01` a `DOC-04` | Factibilidad, aviso de privacidad, diagramas y manuales |

Tres son rápidos porque el trabajo pesado ya está en Postgres: **libros
faltantes** (copiar la pantalla de deudores), **bitácora** (un disparador, sin
tocar Python) y **exportación CSV**.

### Mejoras pendientes de la auditoría interna

Ninguna es urgente; los cuatro **fallos** ya se corrigieron.

- Código muerto: `sesion.py:exigir_personal()` y `libros.py:obtener()` no se usan
- Diez consultas de los repositorios sin `.limit()`
- Un `except: pass` silencioso al cerrar sesión
- Veinte `except Exception` genéricos: un error de programación se muestra
  al bibliotecario como «revisa tu conexión a internet»
- La cobertura se concentra en los validadores; no hay pruebas de
  repositorios, sesión ni interfaz
- Supabase avisa que la protección contra contraseñas filtradas está
  desactivada — es un interruptor en el panel

---

## El sistema Java del que se parte

Fue auditado antes de migrarlo, y esa auditoría detectó **diez defectos
reales**, cuatro de severidad alta. El patrón de fondo: tres validaciones
medían la **longitud del texto** capturado en lugar de su **valor numérico**,
de modo que el sistema aceptaba justo los datos que sus mensajes de error
decían rechazar.

**Siete están corregidos** (D-01, D-03, D-06, D-07, D-08, D-09, D-10).
Los tres pendientes —D-02, D-04, D-05— son del manejo de CSV y se atienden
con la historia `REP-03`, usando el módulo `csv` de la biblioteca estándar
en vez de concatenar comas a mano.

`tests/test_defectos_auditoria.py` cita cada defecto y su caso de prueba
original: son la red que impide que regresen.

### Correcciones al diseño heredado

| Sistema Java | Ahora | Motivo |
|---|---|---|
| `ON DELETE CASCADE` en préstamos | `RESTRICT` | Borraba el historial que exige REQ-PRE-03 |
| Teléfono y CP numéricos | Texto | Un CP como `04600` perdía el cero |
| Columna `Disponible` almacenada | Se deduce de las existencias | Podía contradecir al inventario |
| Borrado físico de libros | Baja lógica con motivo | REQ-LIB-03 |
| Credenciales en `ConexionBD.java` | `.env` fuera del repositorio | Estaban en un repo público |

---

## Cuentas de demostración

Las tres sirven para enseñar que cada perfil ve solo lo suyo, que es la forma
más clara de explicar el control de acceso sin hablar de tecnología.

| Correo | Contraseña | Perfil |
|---|---|---|
| `bibliotecaria@demo.com` | `123456` | administrador |
| `auxiliar@demo.com` | `Auxiliar2026!` | bibliotecario |
| `alumno.prueba@demo.com` | `AlumnoPrueba2026!` | alumno |

Son cuentas de prueba en el proyecto propio, no de personas reales. La
primera usa una contraseña corta a propósito, para teclearla rápido durante
la demostración.

**Antes de cargar datos reales de alumnos hay que cambiar las tres.** El
REQ-USU-01 exige «criterios mínimos de seguridad», y una contraseña de seis
dígitos no los cumple: es aceptable mientras la base solo tiene datos de
ejemplo, no cuando contenga el padrón de una escuela. Conviene además activar
en el panel de Supabase la protección contra contraseñas filtradas, que hoy
está desactivada.

Permisos vigentes:

| Acción | Bibliotecario | Administrador | Alumno |
|---|---|---|---|
| Catálogo, préstamos, alumnos, reportes | sí | sí | solo lectura de lo suyo |
| Registrar y modificar personal | sí | sí | no |
| Cambiar el perfil de acceso de alguien | no | sí | no |
| Cambiar el **propio** perfil de acceso | no | no | no |

### Datos cargados

10 libros apropiados para una primaria, 6 alumnos, 2 empleados y 4 préstamos
—dos de ellos vencidos a propósito, para que el reporte de deudores tenga qué
mostrar. Sustituyen a los datos del volcado Java, que no eran presentables
ante una escuela.

---

## Contexto del cliente

La escuela lleva la biblioteca **en cuadernos**. De la entrevista salieron
cuatro problemas, y conviene tenerlos presentes al decidir cualquier cosa:

1. No se sabe rápido quién tiene cada ejemplar ni cuáles están vencidos.
2. Sacar la lista de deudores exige revisar el cuaderno entero a mano.
3. Los libros se pierden sin registro, así que el inventario real se desfasa.
4. Los niños no pueden saber qué hay sin preguntarle a un adulto.

La biblioteca la atiende **un docente comisionado**, sin formación en
sistemas y con su propio grupo a cargo. De ahí la meta operativa del Avance 1:
registrar un préstamo debe tomar **menos de 30 segundos**, buscando al alumno
por nombre o grupo, sin llenar más de tres campos. Por eso el diálogo de
préstamo son dos búsquedas y un botón, y no un formulario.

Se procesan **datos de menores de edad**, así que aplica la Ley General de
Protección de Datos Personales. Falta el aviso de privacidad (`DOC-02`):
**no cargar datos reales de alumnos hasta que esté firmado.**

---

## Documentos de la materia

- `Documentacion/Avance_Biblioteca_1.docx` — entrega original
- **Avance 1.1** — actualiza el anterior: llena las secciones de metodología
  y herramientas que quedaron sin responder, reescribe la Factibilidad
  Técnica (la premisa de conectividad cambió al verificarla en sitio) y
  agrega tres capítulos: migración del sistema Java, arquitectura y estado
  de avance.

La reunión de presentación con la escuela es el **lunes 14 de septiembre**
(issue #44). Ahí se confirman cuatro cosas que condicionan el código: si el
límite de un libro y el plazo de siete días corresponden a su práctica real,
qué datos de alumno autoriza la dirección, y en qué equipo se instalará.

Las dos primeras están implementadas como reglas dentro de la base: si la
escuela usa otras, conviene saberlo antes de que el Sprint 3 las dé por
definitivas.
