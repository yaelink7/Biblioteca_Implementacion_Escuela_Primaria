# Sistema de Biblioteca — Escuela Primaria Adalberto Tejeda

Contexto completo del proyecto. Claude Code lee este archivo automáticamente al
abrir el repositorio: una sesión nueva en cualquier computadora debe poder
continuar el trabajo solo con esto y acceso al repositorio, sin preguntar nada.

**Última actualización:** 18 de septiembre de 2026.

---

# 1. Qué es el proyecto

Proyecto integrador de **Programación e Implementación de Sistemas** (7.º
semestre, Universidad Veracruzana). Consiste en **migrar a Python** un sistema
de biblioteca escolar que ya existía en Java, y entregarlo a una escuela
primaria real de Veracruz que hoy lleva su biblioteca en cuadernos de papel.

No es un ejercicio de clase: hay un cliente real, una bibliotecaria que va a
usar esto todos los días, y datos personales de menores de edad de por medio.

| | |
|---|---|
| Equipo | 5 integrantes, metodología SCRUM |
| Periodo | 14 de septiembre – 28 de noviembre de 2026 |
| Repositorio | `yaelink7/Biblioteca_Implementacion_Escuela_Primaria` |
| Tablero | `github.com/users/yaelink7/projects/3` |
| Sistema Java original | `yaelink7/Proyecto-Biblioteca-IngenieriaSoftware` |
| Proyecto Supabase | `gibenzgxkbmalljqroxe` · región `us-east-2` · PostgreSQL 17.6 |

## El equipo

| Integrante | GitHub | Rol |
|---|---|---|
| Yael Arenas Guevara | `yaelink7` | Scrum Master · dueña del repositorio |
| Rey David Montes Ciriaco | `DavC010` | Product Owner |
| Yahir Reyes Velasco | `yahirrev` | Desarrollo |
| Pedro Cabrera Barrios Ángel | `Pedro20-amd` | Desarrollo · calidad |
| Roberto Ellyan Vázquez Arriaga | `robertovaz573` | Calidad y pruebas |

Los 43 issues del backlog están asignados nominalmente a estas cuentas.

## Contexto del cliente

La escuela lleva la biblioteca **en cuadernos**. De la entrevista salieron
cuatro problemas, y conviene tenerlos presentes al decidir cualquier cosa:

1. No se sabe rápido quién tiene cada ejemplar ni cuáles están vencidos.
2. Sacar la lista de deudores exige revisar el cuaderno entero a mano.
3. Los libros se pierden sin registro, así que el inventario real se desfasa.
4. Los niños no pueden saber qué hay sin preguntarle a un adulto.

La biblioteca la atiende **un docente comisionado**, sin formación en sistemas
y con su propio grupo a cargo. De ahí la meta operativa del Avance 1: registrar
un préstamo debe tomar **menos de 30 segundos**, buscando al alumno por nombre
o grupo, sin llenar más de tres campos. Por eso el diálogo de préstamo son dos
búsquedas y un botón, y no un formulario.

Se procesan **datos de menores de edad**, así que aplica la Ley General de
Protección de Datos Personales en Posesión de Sujetos Obligados. Falta el
aviso de privacidad (`DOC-02`): **no cargar datos reales de alumnos hasta que
esté firmado.**

---

# 2. Reglas de trabajo

No son preferencias de estilo: son acuerdos con Yael. Respétalas.

1. **No modificar código sin informarlo antes y recibir permiso explícito.**
   Leer, analizar, auditar y proponer no requieren permiso; escribir sí.
   Ante la duda, preguntar.
2. **Un PR por unidad de propósito.** Nunca acumular varios cambios distintos
   en una rama.
3. **Los PR llevan descripción completa** de todo lo que se agregó: archivos
   nuevos y su propósito, decisiones de diseño con su motivo, defectos
   corregidos con su identificador, cambios de dependencias, datos cargados en
   Supabase, salida real de las pruebas, y lo que queda pendiente.
4. **Abrir un PR solo cuando el anterior ya esté en `main`,** y no volver a
   empujar a una rama cuyo PR ya se mergeó.
5. **El código y los comentarios van en español**, sin el sufijo `Biblia` que
   usaban los paquetes del sistema Java (`GUIBiblia`, `DAOBiblia`).

## Errores ya cometidos, para no repetirlos

- **PR encadenados.** Se abrieron PR apuntando a la rama de otro PR en vez de
  a `main`. Al mergearlos seguidos, GitHub no reajusta las bases a tiempo y los
  cambios terminan en la rama intermedia. Pasó **dos veces** (#47/#48 y #53) y
  hubo que abrir PR de rescate (#49 y #54).
- **Empujar a una rama ya mergeada.** Los commits posteriores al merge del #55
  se quedaron fuera de `main` y hubo que abrir el #56.
- **Verificar nombres de archivo con acentos.** `git ls-tree` escapa `ó` como
  `\303\263`; comparar esa cadena contra el sistema de archivos da falsos
  «archivo faltante». Usar `git ls-tree -z` o `core.quotepath false`.

---

# 3. Arquitectura

## Dos clientes, un servicio

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

## La decisión que ordena todo el proyecto

**Las reglas de negocio viven en Postgres, no en Python.** No es gusto: es
para que la app móvil planeada las herede sin reimplementarlas, y para que se
cumplan aunque alguien llame la API directamente saltándose el cliente. La
llave publishable de Supabase es pública por diseño, así que cualquier regla
que viva solo en el cliente **no es una regla, es una sugerencia**.

| Regla | Dónde vive | Requisito |
|---|---|---|
| Un libro por alumno | Índice único parcial en `prestamos` | REQ-PRE-01 |
| Plazo de 7 días | Disparador `calcular_fecha_limite` | REQ-PRE-02 |
| Movimiento de inventario | Disparador `mover_inventario` | REQ-PRE-01 |
| No dar de baja con préstamos activos | Disparador `validar_baja_de_libro` | REQ-LIB-03 |
| Año de publicación no futuro | Disparador `validar_ano_publicacion` | REQ-LIB-01 |
| Fecha de devolución | Disparador `sellar_devolucion` | — |
| Solo admin cambia perfiles de acceso | Disparador `proteger_rol` | — |
| Altas y cambios atómicos de personas | Funciones `registrar_*`, `actualizar_alumno` | — |
| Acceso por perfil | 16 políticas RLS sobre las 7 tablas | Factibilidad Legal |

**Corolario 1.** Antes de escribir una regla de negocio, pregúntate si puede
vivir en la base. Los repositorios de Python solo invocan y traducen el error
a algo que el bibliotecario entienda.

**Corolario 2.** Las fechas y plazos **los calcula la base, no Python**. La
base corre en UTC y los equipos en hora de Veracruz (UTC−6): seis horas de
cada día los dos relojes no coinciden. Ya se corrigió un defecto por esto
(PR #55); **no lo reintroduzcas usando `date.today()`** para calcular retrasos,
plazos o fechas de devolución. `tests/test_plazos.py` falla si alguien lo hace.

**Corolario 3.** Los datos de una persona viven en dos tablas (`perfiles` más
`usuarios` o `empleados`). Nunca las escribas con dos llamadas separadas desde
Python: si la segunda falla, queda un registro a medias. Ya pasó dos veces —en
el alta (PR #53) y en la modificación (PR #55)— y por eso existen las funciones
`registrar_alumno`, `registrar_empleado` y `actualizar_alumno`.

## Estructura del código

```
src/biblioteca/
  core/
    config.py              lee el .env; define DIAS_DE_PRESTAMO y LIBROS_POR_USUARIO
    supabase_cliente.py    cliente único, cacheado con lru_cache
    sesion.py              iniciar_sesion, cerrar_sesion, sesion_actual, exigir_personal
  modelos/                 entidades del dominio, sin acceso a datos
    persona.py             Rol (enum), Perfil → Alumno, Empleado
    libro.py               Publicacion → Libro
    prestamo.py            EstadoPrestamo (enum), Prestamo
  repositorios/            una consulta por operación
    libros.py              listar, buscar, obtener, dar_de_alta, modificar, dar_de_baja
    personas.py            listar/buscar alumnos y empleados, altas y modificaciones
    prestamos.py           registrar, devolver, activos, historial_de, deudores
  servicios/               reglas independientes de la interfaz
    validador_libro.py     Resultado, validar(libro, es_alta)
    validador_persona.py   validar_perfil, validar_alumno, validar_empleado
  ui/
    disenos/               11 archivos .ui que se abren en Qt Designer
    generado/              ui_*.py que produce el compilador — NO editar a mano
    estilo.py              paleta y hoja de estilo compartida
    login.py               REQ-USU-02
    ventana_principal.py   las cinco pestañas
    catalogo.py            + formulario_libro.py
    prestamos.py           + nuevo_prestamo.py
    alumnos.py             + formulario_alumno.py + historial_alumno.py
    deudores.py
    empleados.py           + formulario_empleado.py
herramientas/
  compilar_ui.py           convierte los .ui en módulos de Python
database/migraciones/      9 migraciones, ya aplicadas en Supabase
tests/                     28 pruebas con pytest
Documentacion/             entregables de la materia
.vscode/                   launch.json, settings.json, extensions.json
```

Equivalencias con el sistema Java, por si hay que consultar el original:

| Sistema Java | Aquí |
|---|---|
| Paquete de entidades | `modelos/` |
| Paquete de acceso a datos | `repositorios/` |
| Paquete de ventanas Swing | `ui/` |
| `ConexionBD.java` | `core/supabase_cliente.py` |
| `VentanaMani.java` | `ui/ventana_principal.py` |
| Validaciones dentro de cada formulario | `servicios/` (capa nueva) |

---

# 4. Base de datos

## 7 tablas

| Tabla | Qué guarda |
|---|---|
| `perfiles` | Datos comunes de toda persona. `auth_id` opcional: un alumno puede tener ficha sin cuenta |
| `usuarios` | Lo propio del alumno: grado y grupo |
| `empleados` | Lo propio del empleado: tipo y fecha de ingreso |
| `libros` | Catálogo, con baja lógica (`activo`, `motivo_baja`, `dado_baja_en`) |
| `prestamos` | Con `ON DELETE RESTRICT`, no CASCADE (REQ-PRE-03) |
| `bitacora_libros` | Trazabilidad — **la tabla existe pero nada escribe en ella** (`LIB-04`) |
| `notificaciones` | Avisos por correo — **vacía**, falta `NOT-01` |

## 4 vistas

| Vista | Para qué |
|---|---|
| `v_catalogo` | Catálogo con disponibilidad deducida de las existencias |
| `v_prestamos` | Préstamos con `dias_restantes` calculado por la base |
| `v_deudores` | Reporte de deudores, con contacto del tutor |
| `v_libros_faltantes` | Libros dados de baja — **existe pero no hay pantalla** (`REP-02`) |

Todas con `security_invoker = on`, para que respeten las políticas RLS.

## 15 funciones

`es_personal`, `es_administrador`, `mi_perfil`, `mi_rol` (apoyo a las políticas);
`registrar_alumno`, `registrar_empleado`, `actualizar_alumno` (altas atómicas);
`calcular_fecha_limite`, `mover_inventario`, `validar_baja_de_libro`,
`validar_ano_publicacion`, `sellar_devolucion`, `proteger_rol`,
`marcar_actualizacion` (disparadores); `marcar_prestamos_vencidos`
(**existe pero nadie la llama sola**, ver `PRE-05`).

## 8 disparadores · 16 políticas RLS

RLS activa en las 7 tablas. Un alumno autenticado solo alcanza su propio
perfil y sus propios préstamos; lo verificamos con una cuenta real.

## Migraciones

```
01_tipos_y_personas                      roles, perfiles, usuarios, empleados
02_catalogo_y_bitacora                   libros, bitácora, validación de año
03_prestamos_y_reglas                    préstamos, límite, plazo, inventario
04_reportes_y_seguridad                  vistas y políticas RLS
05_restringir_funciones                  revoca ejecución pública
06_altas_de_personas_transaccionales     corrige perfiles huérfanos
07_actualizar_alumno_y_vista_prestamos   modificación atómica y v_prestamos
08_fecha_de_devolucion_desde_la_base     disparador sellar_devolucion
09_permisos_de_bibliotecario_y_proteccion_de_rol
```

**Para cambiar el esquema se crea una migración nueva**, nunca se edita una
anterior: los archivos son el registro de lo que ya corrió en Supabase.

---

# 5. Cómo trabajar

## Preparar el entorno

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pip install -e .
```

El último paso es necesario: hace que `import biblioteca` funcione. **No viene
de `requirements.txt`**, así que quien lo omita tendrá `ModuleNotFoundError`.

Hace falta un `.env` en la raíz, que **no está en el repositorio**:

```
SUPABASE_URL=https://gibenzgxkbmalljqroxe.supabase.co
SUPABASE_KEY=<llave publishable, pedirla al Scrum Master>
```

La llave `sb_publishable_` **no es secreta**: está diseñada para ir dentro de
aplicaciones que cualquiera puede descompilar, y su seguridad depende de las
políticas RLS. Lo que nunca debe salir del panel de Supabase es la llave
`service_role`, que se salta RLS por completo.

## Ejecutar, probar, diseñar

```bash
.venv/Scripts/python.exe main.py                        # ejecutar
.venv/Scripts/python.exe -m pytest tests/ -v            # 28 pruebas, <1 s
.venv/Lib/site-packages/PySide6/designer.exe            # editar pantallas
.venv/Scripts/python.exe herramientas/compilar_ui.py    # recompilar los .ui
```

En VS Code: **F5** ofrece las tres configuraciones (aplicación, pruebas,
compilar diseños). El icono del matraz muestra las pruebas en árbol.

Los `.ui` de `ui/disenos/` se editan en Qt Designer; los `ui_*.py` de
`ui/generado/` los produce el compilador y **se sobrescriben**.

## Cuentas de demostración

| Correo | Contraseña | Perfil |
|---|---|---|
| `bibliotecaria@demo.com` | `123456` | administrador |
| `auxiliar@demo.com` | `Auxiliar2026!` | bibliotecario |
| `alumno.prueba@demo.com` | `AlumnoPrueba2026!` | alumno |

Sirven para enseñar que cada perfil ve solo lo suyo. **Cambiarlas antes de
cargar el padrón real**: el `REQ-USU-01` exige criterios mínimos de seguridad
y seis dígitos no los cumplen con datos de menores de por medio.

| Acción | Bibliotecario | Administrador | Alumno |
|---|---|---|---|
| Catálogo, préstamos, alumnos, reportes | sí | sí | solo lo suyo |
| Registrar y modificar personal | sí | sí | no |
| Cambiar el perfil de acceso de alguien | no | sí | no |
| Cambiar el **propio** perfil de acceso | no | no | no |

## Datos cargados

10 libros apropiados para una primaria, 6 alumnos, 2 empleados y 4 préstamos
—dos vencidos a propósito, para que el reporte de deudores tenga qué mostrar.
Sustituyen a los del volcado Java, que no eran presentables ante una escuela.

---

# 6. Qué se ha hecho

## Historial de PR

| PR | Qué entregó |
|---|---|
| #1 | Estructura del proyecto y esquema completo en Supabase |
| #45 | Modelos, repositorios y sesión migrados del Java |
| #46 | Corrección de 7 defectos de la auditoría; cambio de PyQt6 a PySide6 |
| #47 | Renombrado de referencias heredadas y documentación de la estructura |
| #48 | Pantalla de catálogo, login y formulario de libro |
| #49 | PR de rescate: integró #47 y #48 a `main` |
| #50 | Pantalla de préstamos y devoluciones |
| #51 | Reporte de deudores |
| #52 | Padrón de alumnos con alta, modificación e historial |
| #53 | Plantilla de empleados y altas transaccionales |
| #54 | PR de rescate: integró #53 a `main` |
| #55 | Tres defectos de la auditoría interna + protección de roles |
| #56 | Contexto del proyecto y configuración de VS Code |

## La migración del Java está terminada

Las cinco pestañas funcionan contra la base real: **Catálogo** (alta,
modificación, baja lógica, búsqueda parcial), **Préstamos** (registro en dos
búsquedas y un botón, devolución, filtro de vencidos), **Alumnos** (padrón,
alta, historial), **Deudores** (reporte que abre ya generado) y **Empleados**
(plantilla, alta, permisos por perfil).

El sistema nuevo hace además lo que el Java nunca tuvo: inicio de sesión con
perfiles, búsqueda por coincidencia parcial, control automático de plazos y
reporte de deudores en un clic.

## Los 10 defectos del sistema Java

Fue auditado antes de migrarlo. El patrón de fondo: tres validaciones medían
la **longitud del texto** capturado en lugar de su **valor numérico**, de modo
que el sistema aceptaba justo los datos que sus mensajes de error decían
rechazar.

**Corregidos (7):** D-01 (disponibilidad ignoraba el parámetro), D-03 (dos
getters del mismo atributo), D-06 (aceptaba cero y negativos), D-07 (cero
páginas), D-08 (año futuro), D-09 (nacía disponible sin existencias), D-10
(código muerto, no migrado).

**Pendientes (3):** D-02, D-04, D-05, los tres del manejo de CSV. Se atienden
con `REP-03`, usando el módulo `csv` de la biblioteca estándar en vez de
concatenar comas a mano. `tests/test_defectos_auditoria.py` cita cada defecto
y su caso de prueba original.

### Correcciones al diseño heredado

| Sistema Java | Ahora | Motivo |
|---|---|---|
| `ON DELETE CASCADE` en préstamos | `RESTRICT` | Borraba el historial que exige REQ-PRE-03 |
| Teléfono y CP numéricos | Texto | Un CP como `04600` perdía el cero |
| Columna `Disponible` almacenada | Se deduce de las existencias | Podía contradecir al inventario |
| Borrado físico de libros | Baja lógica con motivo | REQ-LIB-03 |
| Credenciales en `ConexionBD.java` | `.env` fuera del repositorio | Estaban en un repo público |

## Auditoría interna del código Python

Se auditaron las 3 301 líneas propias. **Los cuatro fallos ya están
corregidos** (PR #55):

1. El cambio de perfil de acceso se descartaba en silencio — y esa línea era
   lo único que impedía una escalada de privilegios.
2. La modificación de un alumno podía quedar a medias.
3. Los días de retraso se calculaban con dos relojes distintos.
4. La fecha de devolución la ponía el cliente.

**Mejoras pendientes, ninguna urgente:**

- Código muerto: `sesion.py:exigir_personal()` y `libros.py:obtener()`
- Diez consultas de los repositorios sin `.limit()`
- Un `except: pass` silencioso al cerrar sesión
- Veinte `except Exception` genéricos: un error de programación se muestra al
  bibliotecario como «revisa tu conexión a internet»
- Sin pruebas de repositorios, sesión ni interfaz
- Supabase avisa que la protección contra contraseñas filtradas está
  desactivada — es un interruptor en el panel

---

# 7. LO SIGUIENTE QUE SE DEBE HACER

Tres tareas, en este orden. Las tres son de documentación y planeación, no de
código: el sistema funciona, lo que está desalineado son los entregables.

## 7.1 Rehacer el cronograma — está mal hecho

**Decisión de Yael: el cronograma actual está mal y hay que rehacerlo.**

Problemas concretos que lo sostienen:

- **No refleja la realidad.** Los sprints 2 y 3 estaban planeados para octubre
  y noviembre, y hoy están al 75 % y 85 %. El trabajo se adelantó porque situar
  las reglas en la base permitió construir las pantallas sobre lógica ya
  probada, pero el cronograma sigue diciendo lo contrario.
- **Sprint 1 desbalanceado:** 53 puntos contra un promedio de 36. Es el único
  fuera de rango y nadie lo ha ajustado.
- **El Sprint 0 arrancó tarde en el papel.** Figura del 14 al 27 de septiembre,
  pero buena parte de su contenido ya estaba hecho antes de esa fecha.
- **El cronograma del Avance 1 original** (el de actividades por semana de
  agosto a noviembre) nunca se alineó con los sprints: son dos planes
  distintos conviviendo en el mismo documento.
- **El Sprint 4 concentra 6 de las 17 historias abiertas** y casi todo lo que
  el sistema Java no tenía. Es el de mayor riesgo y está planeado al final.

Al rehacerlo conviene: partir del avance real (26 de 43 historias), redistribuir
lo que queda, equilibrar los puntos por sprint, y fijar fechas que el equipo
pueda sostener con su dedicación real (la Factibilidad de Calendario habla de
ritmo escolar, no de tiempo completo).

## 7.2 Completar los requerimientos del Avance 1.1

El Avance 1 declara **12 requerimientos funcionales** (REQ-USU-01 a 03,
REQ-EMP-01, REQ-LIB-01 a 03, REQ-BUS-01, REQ-PRE-01 a 04) y **ningún
requerimiento no funcional**. La norma ISO/IEC/IEEE 29148 que el propio
documento cita exige ambos.

### Funcionales que faltan declarar

Todos están implementados o planeados, pero no figuran como requisito:

| Propuesto | Qué cubre | Estado |
|---|---|---|
| REQ-REP-01 | Reporte de alumnos deudores con un clic | implementado |
| REQ-REP-02 | Registro de libros faltantes o dados de baja | vista lista, falta pantalla |
| REQ-REP-03 | Exportación a CSV como respaldo | pendiente |
| REQ-USU-04 | Alta de alumno sin cuenta de acceso, con datos del tutor | implementado |
| REQ-USU-05 | Consulta del historial de préstamos de un alumno | implementado |
| REQ-EMP-02 | Consulta de la plantilla de personal | implementado |
| REQ-BUS-02 | Filtrado y ordenamiento de resultados | implementado |
| REQ-PRE-05 | Registro de devolución con reintegro al inventario | implementado |
| REQ-LIB-04 | Bitácora de trazabilidad consultable | tabla lista, falta el disparador |

### No funcionales que faltan por completo

| Propuesto | Enunciado |
|---|---|
| RNF-USA-01 | Registrar un préstamo debe tomar menos de 30 segundos, buscando al alumno por nombre o grupo, sin llenar más de tres campos |
| RNF-USA-02 | La interfaz debe ser operable por personal sin formación en sistemas, con un manual de una página por rol |
| RNF-SEG-01 | Ninguna operación debe ser posible sin sesión iniciada |
| RNF-SEG-02 | El control de acceso debe aplicarse en la base de datos, no solo en la interfaz |
| RNF-SEG-03 | Las credenciales no deben residir en el código fuente |
| RNF-SEG-04 | Un usuario no puede modificar su propio perfil de acceso |
| RNF-LEG-01 | Los datos completos del alumno solo son visibles al personal; el alumno ve únicamente los suyos |
| RNF-LEG-02 | Debe existir aviso de privacidad firmado antes de registrar datos reales de menores |
| RNF-LEG-03 | Debe definirse un periodo de conservación y borrado al concluir el ciclo escolar |
| RNF-DIS-01 | El sistema depende de conexión a internet; debe existir respaldo exportable como contingencia |
| RNF-REN-01 | Las consultas de catálogo y préstamos deben responder en menos de dos segundos con el acervo completo |
| RNF-MAN-01 | Las reglas de negocio deben residir en un solo lugar, verificable por pruebas automatizadas |
| RNF-MAN-02 | El código y la documentación se mantienen en español |
| RNF-POR-01 | El sistema debe ejecutarse en Windows 10 o superior sin instalación de servidor local |

Conviene además añadir al Avance 1.1 una **matriz de trazabilidad** que cruce
cada requisito con la historia del backlog que lo implementa y la prueba que
lo verifica. Es lo que la norma citada espera y hoy no existe.

## 7.3 Diagramas que pide el profesor

Lista tomada del pizarrón de clase (fotografía del 18 de septiembre de 2026).
Son **ocho entregables**, y ninguno está hecho todavía:

| # | Entregable | Insumo que ya existe |
|---|---|---|
| 1 | **Casos de uso** | Los 12 requisitos del capítulo 3 y los 3 perfiles de la sección 1.5 |
| 2 | **Casos de uso extendido** | La descripción narrativa de cada REQ, con sus caminos de excepción |
| 3 | **Diagrama de proceso** | El flujo de préstamo y devolución tal como lo aplican los disparadores |
| 4 | **Diagrama de flujo de datos** | Las cinco pantallas y las siete tablas ya delimitan los flujos |
| 5 | **Modelado de base de datos** | Las 9 migraciones de `database/migraciones/` |
| 6 | **Modelo E-R y modelo relacional** | Derivables de las 7 tablas con sus llaves foráneas |
| 7 | **Base de datos** | Ya implementada y funcionando en Supabase |
| 8 | **Interfaces** | Los 11 archivos `.ui` de `ui/disenos/`, ya construidos |

En el pizarrón los puntos 5 y 6 aparecen agrupados por una llave: el **E-R** y
el **relacional** son las dos partes del modelado de base de datos.

**La mayoría son derivables del trabajo ya hecho**, no hay que inventarlos:
el esquema existe y funciona, las pantallas están construidas, y los flujos
están implementados como disparadores. Lo que falta es representarlos.

Un punto de atención para el **diagrama de clases** y el **E-R**: deben
reflejar la arquitectura actual, no la del sistema Java. Los UML del proyecto
original (`UML/` en el repositorio Java) ya no corresponden — cambió el
esquema, apareció la capa de servicios y las reglas se movieron a la base.

Esto corresponde a la historia `DOC-03` (issue #28, asignada a Pedro Cabrera
Barrios Ángel), cuyo alcance conviene ampliar: hoy el issue solo menciona tres
diagramas y el profesor pide ocho entregables.

---

# 8. Estado del backlog

**26 de 43 historias cerradas (60 %)** al 18 de septiembre de 2026.

| Sprint | Cerradas | Abiertas |
|---|---|---|
| Sprint 0 · Cimientos | 6 | 4 |
| Sprint 1 · Identidad y personas | 7 | 4 |
| Sprint 2 · Catálogo y búsqueda | 6 | 2 |
| Sprint 3 · Préstamos | 6 | 1 |
| Sprint 4 · Reportes y avisos | 1 | 6 |

## Las 17 historias abiertas

| Issue | Historia | Qué falta |
|---|---|---|
| #3 | `INF-02` | Confirmar que los cinco integrantes ejecutan el proyecto |
| #9 | `DOC-01` | Actualizar la Factibilidad Técnica (hecho en el Avance 1.1, falta cerrarlo) |
| #10 | `QA-01` | Acordar la Definición de Terminado del equipo |
| #13 | `USU-03` | Registro de cuentas con contraseña propia |
| #19 | `QA-02` | Traducir la suite JUnit a pytest |
| #20 | `DOC-02` | Aviso de privacidad para tutores |
| #24 | `LIB-04` | Bitácora de trazabilidad: falta el disparador |
| #28 | `DOC-03` | Diagramas del sistema |
| #33 | `PRE-05` | Marcado diario de vencidos: falta programar la tarea |
| #37 | `REP-02` | Pantalla de libros faltantes |
| #38 | `REP-03` | Exportación a CSV (cierra D-02, D-04, D-05) |
| #39 | `NOT-01` | Correos automáticos |
| #40 | `NOT-02` | Bitácora de notificaciones |
| #41 | `QA-04` | Pruebas de aceptación con el docente |
| #42 | `DOC-04` | Manuales de una página por rol |
| #43 | `QA-03` | Casos de prueba por módulo |
| #44 | Reunión | Primer acercamiento con la escuela |

## Lo más rápido de cerrar

Tres son casi gratis porque el trabajo pesado ya está en Postgres:

1. **`REP-02` libros faltantes** — la vista `v_libros_faltantes` existe; es
   copiar la estructura de `ui/deudores.py`. Una hora.
2. **`LIB-04` bitácora** — un disparador sobre `libros` que escriba en
   `bitacora_libros`. Sin tocar Python.
3. **`PRE-05` vencidos** — la función `marcar_prestamos_vencidos()` existe;
   falta programarla. `pg_cron` no está instalado en el proyecto.

---

# 9. Documentos de la materia

- `Documentacion/Avance_Biblioteca_1.docx` — entrega original, 19 páginas
- **Avance 1.1** — actualiza el anterior. Llena las secciones de metodología y
  herramientas que el Avance 1 dejó con las preguntas del profesor sin
  responder, reescribe la Factibilidad Técnica (la premisa de conectividad
  cambió al verificarla en sitio) y agrega tres capítulos: migración del
  sistema Java, arquitectura y estado de avance. **Le faltan los
  requerimientos de la sección 7.2 y los diagramas de la 7.3.**
- `Documentacion/Factibilidad.docx`, `Investigación_Equipo_Biblioteca.docx`,
  `Metodologías_Equipo_Biblioteca.docx` — insumos del Avance 1
- El **Reporte Técnico de Calidad** del sistema Java (de otra asignatura) vive
  en `NetBeansProjects/BibliotecaIngeSoftware/Documentacion/` y es la fuente
  de los diez defectos

## La reunión con la escuela

Está registrada como issue #44 y sigue **abierta**. Ahí se confirman cuatro
cosas que condicionan el código:

1. Si el límite de un libro por alumno corresponde a su práctica real.
2. Si el plazo de siete días es el que aplican hoy.
3. Qué datos del alumno autoriza la dirección, y quién firma el aviso de
   privacidad.
4. En qué equipo de cómputo quedará instalado el sistema.

Las dos primeras están implementadas como reglas dentro de la base. **Si la
escuela usa otras, conviene saberlo antes de darlas por definitivas**, porque
cambiarlas después cuesta más.
