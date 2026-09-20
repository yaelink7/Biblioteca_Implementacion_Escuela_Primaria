# Sistema de Biblioteca — Escuela Primaria Adalberto Tejeda

Contexto completo del proyecto. Claude Code lee este archivo automáticamente al
abrir el repositorio: una sesión nueva en cualquier computadora debe poder
continuar el trabajo solo con esto y acceso al repositorio, sin preguntar nada.

**Última actualización:** 20 de septiembre de 2026 — Avance 1.3, mensajes de
error por causa real, insumos de los diagramas (sección 10) y el tablero
sincronizado con los hitos.

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

Los 51 issues del backlog están asignados nominalmente a estas cuentas.

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
6. **Este archivo se actualiza con cada cambio del proyecto**, en la misma
   entrega. Si queda desfasado deja de servir para lo que existe: que una
   sesión nueva continúe el trabajo sin preguntar nada.
7. **No agregar requerimientos por cuenta propia.** Si algo parece faltar como
   requisito funcional o no funcional, **proponerlo y esperar respuesta**. Un
   requisito lo define el cliente y lo aprueba el Product Owner; deducirlo del
   código va al revés y ya causó un problema (ver abajo).

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
- **El tablero no se llena solo.** Crear un issue con `--milestone` lo mete en
  el hito, **no en el tablero de Projects**: son dos cosas distintas. Las
  diecisiete historias creadas después de armar el tablero (#59 a #67 y #72 a
  #79) se quedaron fuera, de modo que el Sprint 1 mostraba cinco tarjetas
  cuando el hito ya tenía veintidós. Al crear un issue hay que agregarlo con
  `gh project item-add 3 --owner yaelink7 --url <url>` y fijarle Status,
  Puntos, Responsable, Inicio y Fin.
- **Puntos duplicados en un issue paraguas.** `DOC-03` (#28) agrupa los ocho
  diagramas y además llevaba 5 puntos propios, que se sumaban a los 46 de sus
  hijas. Quedó en 0: un paraguas no estima trabajo, lo agrupa.
- **Requerimientos inventados.** En el Avance 1.2 se declararon 25 requisitos
  deducidos de leer el código: 9 funcionales y los 16 no funcionales completos.
  Ninguno pasó por el Product Owner. Varios describían cosas que no existen
  —exportación a CSV, bitácora, manuales, aviso de privacidad— y uno,
  `RNF-LEG-03`, comprometía al equipo a definir un periodo de borrado de datos
  de menores. El equipo corrigió los funcionales (PR #71) y los no funcionales
  siguen en revisión. De ahí la regla 7.

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
    errores.py             explicar(), mensaje(), causa(): por qué falló de verdad
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
tests/                     48 pruebas con pytest
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
.venv/Scripts/python.exe -m pytest tests/ -v            # 48 pruebas, <1 s
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
| #57 | Archivo de contexto completo del proyecto — este documento |
| #58 | Avance 1.2: sistemas bibliotecarios revisados y requisitos completos |
| #68 | Cronograma rehecho: la migración pasa a trabajo preliminar |
| #69 | Archivo de contexto al día tras el Avance 1.2 y el cronograma |
| #70 | Avance 1.3 — **cerrado sin mergear**, se rehará sobre el 1.2 corregido |
| #71 | Corrección de los requerimientos funcionales del 1.2, por el equipo |

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
- ~~Veinte `except Exception` genéricos~~ — **corregido**. Las nueve pantallas
  usan `core/errores.py`, que distingue la falta de red, la sesión vencida, el
  permiso faltante, la regla de la base y el defecto de programación. Cada
  mensaje dice la causa, qué hacer y el detalle técnico. Es lo que exige
  `RNF-USA-03`, que antes el código contradecía. Los repositorios conservan sus
  propios `_mensaje_claro()`, que ya traducían bien
- Sin pruebas de repositorios, sesión ni interfaz
- Supabase avisa que la protección contra contraseñas filtradas está
  desactivada — es un interruptor en el panel

---

# 7. LO SIGUIENTE QUE SE DEBE HACER

El sistema funciona; lo que estaba desalineado eran los entregables. De las
tres tareas que esta sección listaba, **dos ya se cerraron**: el cronograma
se rehízo (7.1) y los requerimientos se completaron en el Avance 1.2 (7.2).
Lo que queda abierto son **los ocho diagramas** (7.3) —el contenido del
Sprint 1— más dos correcciones menores al Avance 1.2.

## 7.1 Cronograma — rehecho el 18 de septiembre

El cronograma anterior no reflejaba la realidad: daba la migración como
trabajo de los sprints 2 y 3, cuando ya estaba terminada antes de que el
Sprint 1 empezara. Se rehízo con esta estructura:

| Periodo | Fechas | Contenido |
|---|---|---|
| **Trabajo preliminar** | hasta el 13 sep | Migración completa a Python — **concluido** |
| **Sprint 1** | 14 – 27 sep | Los ocho diagramas y la documentación pendiente |
| **Sprint 2** | 28 sep – 11 oct | **Por definir** tras los acuerdos de la reunión |
| **Sprint 3** | 12 – 25 oct | **Por definir** |
| **Sprint 4** | 26 oct – 8 nov | **Por definir** |
| **Cierre** | 9 – 28 nov | Aceptación con el docente, correcciones, manuales, entrega |

**Los sprints 2, 3 y 4 están deliberadamente sin contenido definido.** La
reunión con la escuela ya se realizó, pero sus acuerdos aún no se documentan
(issue #67). Definir el contenido antes de conocerlos sería planear sobre
supuestos, y de ellos depende si las reglas implementadas —un libro por
alumno, siete días de plazo— siguen siendo válidas.

Los hitos de GitHub llevan esos nombres literalmente: «Sprint 2 — Por definir
tras la reunión». Al documentarse los acuerdos hay que renombrarlos con su
contenido real y repartir ahí el trabajo pendiente listado en la sección 8.

### Sprint 1: los ocho diagramas

Cada entregable gráfico es un issue propio, para poder repartirlos:

Los ocho quedaron a cargo de **Rey David y Pedro**, 23 puntos cada uno. Pedro
toma los que salen del esquema de la base, que es el módulo en el que ya
trabajó; Rey David, los de proceso, flujos e interfaces.

| Issue | Entregable | Puntos | Responsable |
|---|---|---|---|
| #59 | DIA-01 Diagrama de casos de uso | 5 | Pedro Cabrera |
| #60 | DIA-02 Casos de uso extendido | 8 | Rey David Montes |
| #61 | DIA-03 Diagrama de proceso | 5 | Rey David Montes |
| #62 | DIA-04 Diagrama de flujo de datos | 5 | Rey David Montes |
| #63 | DIA-05 Modelado de base de datos | 5 | Pedro Cabrera |
| #64 | DIA-06 Modelo E-R y relacional | 8 | Pedro Cabrera |
| #65 | DIA-07 Documentación de la base de datos | 5 | Pedro Cabrera |
| #66 | DIA-08 Diagramas de interfaces | 5 | Rey David Montes |

**Los insumos de los ocho están en la sección 10 de este archivo**, sacados del
código y del esquema reales. No hay que inventar nada: hay que representarlo.

El issue #28 quedó como paraguas de los ocho. Su alcance original mencionaba
tres diagramas: el profesor pide ocho.

El Sprint 1 lleva además la documentación que quedó pendiente: `DOC-01`,
`DOC-02`, `QA-01` y el registro de los acuerdos de la reunión. `INF-02`
—configurar VS Code para todo el equipo— **ya se cerró**: los cinco integrantes
ejecutan el proyecto desde VS Code.

### Sprint 1: lo que pidió la escuela

Por decisión de la Scrum Master, los acuerdos de la reunión entran también al
Sprint 1. Son ocho historias más, 39 puntos:

| Issue | Historia | Puntos | Responsable |
|---|---|---|---|
| #72 | `LIB-06` Géneros según las colecciones de la SEP | 5 | Pedro Cabrera |
| #73 | `LIB-07` Asignatura o área del libro | 3 | Pedro Cabrera |
| #74 | `USU-07` CURP del alumno | 5 | Yahir Reyes |
| #75 | `USU-08` Teléfono y dirección del tutor; quitar el correo | 5 | Yahir Reyes |
| #76 | `USU-09` Maestro de grupo del alumno | 3 | Yael Arenas |
| #77 | `PRE-08` Adeudo por libro no devuelto | 8 | Rey David Montes |
| #78 | `REP-04` Vistas de estadísticas del padrón | 5 | Roberto Vázquez |
| #79 | `REP-05` Pantalla de estadísticas del padrón | 5 | Roberto Vázquez |

**El Sprint 1 queda con 22 historias y 95 puntos, y cierra el 27 de
septiembre.** El promedio de los sprints anteriores era 36. Está sobrecargado
y conviene saberlo.

**Orden importante:** siete de estas ocho historias cambian el esquema de la
base. Los diagramas `DIA-05`, `DIA-06` y `DIA-07` documentan ese mismo
esquema. **Hacer los diagramas antes que las migraciones significa dibujar una
base que está por cambiar.** Conviene aplicar primero la migración 10 y
después documentarla.

## 7.2 Requerimientos — corregidos por el equipo en el PR #71

El Avance 1.2 quedó con **19 requerimientos funcionales**, no 21. Roberto
Vázquez revisó los que se habían agregado sin aprobación y corrigió:

| Requisito | Qué pasó |
|---|---|
| `REQ-USU-03` (el usuario actualiza sus propios datos) | Eliminado, sustituido por `REQ-EMP-03`: es **el empleado** quien actualiza los datos del alumno |
| `REQ-USU-04` (ficha de alumno sin cuenta, con contacto del tutor) | Eliminado |
| `REQ-USU-05` (historial de préstamos) | Renumerado a `REQ-USU-03` |
| `REQ-PRE-04` (notificaciones por correo) | Eliminado — la escuela confirmó que el correo no funciona |
| `REQ-EMP-03` | Nuevo |

El cambio de fondo es correcto: en una primaria el niño no administra su
cuenta, la maestra administra sus datos.

**Dos cabos sueltos que dejó la corrección:**

1. `REQ-PRE-04` ya no está en el capítulo 3, pero **sigue citado** en la matriz
   de trazabilidad (3.3) y en el capítulo 6. Los issues `NOT-01` y `NOT-02`
   (#39 y #40, 11 puntos) implementan un requisito que ya no existe.
2. La numeración quedó con hueco: `REQ-PRE-01, 02, 03, 05`.

**Los no funcionales ya se revisaron.** De los 16, la Scrum Master aprobó
retirar dos, y quedan **14** en el Avance 1.3:

| Retirado | Por qué |
|---|---|
| `RNF-LEG-03` | Comprometía al equipo a definir un periodo de borrado de datos de menores que nadie acordó con la dirección |
| `RNF-REN-01` | El límite de dos segundos no salía de ninguna medición ni de la escuela |

`RNF-USA-03` —los mensajes de error deben decir la causa y qué hacer— **se
conservó, y se corrigió el código para cumplirlo**. Ver la auditoría interna en
la sección 6.

De los que quedan, nueve describen el sistema tal como es y cinco respaldan
historias del backlog que ya estaban aprobadas: `RNF-LEG-02` ← #20,
`RNF-USA-02` ← #42 y `RNF-DIS-01` ← #38.

`RNF-USA-01` —el préstamo en menos de 30 segundos— se conserva, pero conviene
saber que **no viene del Avance 1 original**: aparece por primera vez en el
1.1. Moldeó el diseño real, así que vale la pena confirmarlo con la escuela en
vez de borrarlo.

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

**28 de 60 historias cerradas** al 20 de septiembre de 2026, y 113 de los 261
puntos estimados. El total subió de 43 a 60 en tres pasos: los ocho diagramas se
abrieron como historias propias, la reunión dejó un issue de seguimiento, y
los acuerdos de la escuela agregaron ocho historias más.

| Hito | Cerradas | Abiertas | Puntos |
|---|---|---|---|
| Trabajo preliminar — Migración a Python | 27 | 0 | 111 de 111 |
| Sprint 1 — Diagramas, diseño y acuerdos | 1 | 21 | 2 de 95 |
| Sprint 2 — Por definir | 0 | 4 | 0 de 20 |
| Sprint 3 — Por definir | 0 | 5 | 0 de 27 |
| Sprint 4 — Por definir | 0 | 0 | — |
| Cierre — Entrega final | 0 | 2 | 0 de 8 |

**El tablero (`github.com/users/yaelink7/projects/3`) ya coincide con los
hitos:** 60 tarjetas, 261 puntos. Si alguna vez no coinciden, lo más probable
es que falte agregar issues al tablero, no que falten en el hito.

Todo lo terminado quedó agrupado en el hito de trabajo preliminar: es la
migración completa del sistema Java, concluida antes de que el Sprint 1
empezara.

## Las 32 historias abiertas

| Issue | Historia | Qué falta |
|---|---|---|
| #9 | `DOC-01` | Actualizar la Factibilidad Técnica (resuelto en el Avance 1.1 y 1.2, falta cerrar el issue) |
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
| #59 a #66 | `DIA-01` a `DIA-08` | Los ocho entregables gráficos (Sprint 1) |
| #67 | Reunión | Documentar los acuerdos de la escuela y ajustar los sprints |
| #72 a #79 | `LIB-06`, `LIB-07`, `USU-07` a `USU-09`, `PRE-08`, `REP-04`, `REP-05` | Lo que pidió la escuela (Sprint 1) |

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
- `Documentacion/Avance_Biblioteca_1.1.docx` — actualiza el anterior. Llena las
  secciones de metodología y herramientas que el Avance 1 dejó con las
  preguntas del profesor sin responder, reescribe la Factibilidad Técnica —la
  premisa de conectividad cambió al verificarla en sitio— y agrega tres
  capítulos: migración del sistema Java, arquitectura y estado de avance
- `Documentacion/Avance_Biblioteca_1.2.docx` — clona el 1.1 y agrega la
  revisión de sistemas bibliotecarios existentes (Koha, SIABUC, SLiMS,
  OpenBiblio) que justifica construir en vez de adoptar, el alcance y las
  exclusiones del sistema, y el capítulo 3 completo. **Corregido por el equipo
  en el PR #71**: quedó con 19 requerimientos funcionales
- `Documentacion/Avance_Biblioteca_1.3.docx` — **la versión vigente**. Clona el
  1.2 corregido y agrega: el cronograma real en el capítulo 2, la sección 1.4.1
  con lo que la escuela pidió en la reunión, el retiro de dos requerimientos no
  funcionales, el estado de avance rehecho y las correcciones de redacción que
  arrastraban las versiones anteriores. **19 requerimientos funcionales y 14 no
  funcionales**
- `Documentacion/Factibilidad.docx`, `Investigación_Equipo_Biblioteca.docx`,
  `Metodologías_Equipo_Biblioteca.docx` — insumos del Avance 1
- El **Reporte Técnico de Calidad** del sistema Java (de otra asignatura) vive
  en `NetBeansProjects/BibliotecaIngeSoftware/Documentacion/` y es la fuente
  de los diez defectos

## La reunión con la escuela

**Ya se realizó** el 14 de septiembre. El issue #44 está cerrado; el #67 sigue
abierto para el registro formal.

### Lo que la escuela pidió

**El acervo se clasifica por las colecciones de Libros del Rincón**, no por un
género libre como hoy:

| Colección | Grados |
|---|---|
| Al sol solito | 1.º, los más pequeños |
| Pasos de luna | 1.º y 2.º |
| Astrolabio | 3.º y 4.º |
| Espejo de urania | 5.º y 6.º |
| Cometas convidados | puede que no haya ninguno en la biblioteca |

Que cada colección tenga grados asociados abre algo que hoy no se puede:
sugerir al bibliotecario los libros que corresponden al grado del niño que
tiene enfrente.

**Del alumno:** agregar CURP, agregar teléfono y dirección **del tutor**, y
**quitar el correo** —la escuela confirmó que no funciona ni con el tutor—.
El correo se quita solo a los alumnos: los empleados lo conservan porque
Supabase Auth inicia sesión con correo y sin él no hay acceso.

**Del perfil del niño:** el maestro de grupo actual, y el adeudo si debe un
libro que no entregó. El botón de editar que pidieron **ya existe**: la
pantalla de Alumnos tiene `botonEditar` y ya permite cambiar grado y grupo sin
recapturar al niño cada ciclo.

**Cuatro secciones de estadísticas**, en formato de tabla de posiciones: quién
se ha llevado más libros, quién ha tardado más veces en devolver, quién debe
más y quién cumple mejor. Salen de datos que `prestamos` ya guarda.

### Dos consecuencias que hay que atender

**El adeudo es dinero.** Confirmado con la Scrum Master: es el costo del libro
no devuelto. Eso invalida una exclusión que el Avance 1.2 declara —«Cobro de
multas por retraso: la escuela no cobra multas a los alumnos»— y hay que
quitarla del siguiente avance. **Falta preguntar a la escuela desde cuándo un
libro no devuelto se vuelve deuda**: un niño con tres días de retraso no debe
el costo del libro; uno que lo perdió en marzo sí.

**El CURP sube la sensibilidad del padrón.** Es un identificador nacional
único de un menor. Refuerza lo que ya estaba acordado: no cargar datos reales
hasta que el aviso de privacidad esté firmado (`DOC-02`, #20).

### Lo que sigue sin confirmarse

De los cuatro puntos que la reunión debía resolver, dos siguen abiertos: si el
límite de un libro por alumno corresponde a su práctica real, y si el plazo de
siete días es el que aplican hoy. Ambos están implementados como reglas en la
base. **Conviene saberlo antes de darlos por definitivos**, porque cambiarlos
después cuesta más.

---

# 10. Insumos para los ocho diagramas

Todo lo que sigue está sacado del esquema y del código que corren hoy, no de
la documentación. **Los diagramas no hay que inventarlos: hay que
representarlos.** Si algo aquí no coincide con el sistema, gana el sistema y
este archivo está mal.

**Antes de dibujar, léase esto:** siete de las ocho historias de la reunión
(#72 a #79) modifican el esquema. `DIA-05`, `DIA-06` y `DIA-07` documentan ese
mismo esquema. Conviene aplicar primero la migración 10 y dibujar después, o
habrá que rehacer los tres.

## 10.1 Actores y casos de uso · `DIA-01` (#59)

Tres actores. El alumno **no necesita cuenta** para recibir un préstamo: la
bibliotecaria lo registra. El perfil de alumno existe para la fase 2 móvil.

| Actor | Alcance |
|---|---|
| **Bibliotecario** | Todo lo operativo: catálogo, préstamos, padrón, reportes y plantilla |
| **Administrador** | Lo del bibliotecario, más cambiar el perfil de acceso de otras personas |
| **Alumno** | Solo lo suyo: su ficha y sus propios préstamos |

Casos de uso, cada uno con el requisito que lo respalda:

| Caso de uso | Requisito | Actor |
|---|---|---|
| Iniciar sesión | `REQ-USU-02` | los tres |
| Buscar en el catálogo | `REQ-BUS-01`, `REQ-BUS-02` | los tres |
| Registrar libro | `REQ-LIB-01` | bibliotecario, administrador |
| Modificar libro | `REQ-LIB-02` | bibliotecario, administrador |
| Dar de baja libro | `REQ-LIB-03` | bibliotecario, administrador |
| Consultar bitácora del catálogo | `REQ-LIB-04` | bibliotecario, administrador |
| Registrar préstamo | `REQ-PRE-01`, `REQ-PRE-02` | bibliotecario, administrador |
| Registrar devolución | `REQ-PRE-05` | bibliotecario, administrador |
| Consultar préstamos e historial | `REQ-PRE-03`, `REQ-USU-03` | bibliotecario, administrador; el alumno solo los suyos |
| Generar reporte de deudores | `REQ-REP-01` | bibliotecario, administrador |
| Consultar libros dados de baja | `REQ-REP-02` | bibliotecario, administrador |
| Exportar respaldo | `REQ-REP-03` | bibliotecario, administrador |
| Registrar empleado | `REQ-EMP-01` | bibliotecario, administrador |
| Consultar plantilla | `REQ-EMP-02` | bibliotecario, administrador |
| Actualizar datos de un alumno | `REQ-EMP-03` | bibliotecario, administrador |
| Registrar cuenta de acceso | `REQ-USU-01` | administrador |
| Cambiar el perfil de acceso de alguien | — (disparador `proteger_rol`) | solo administrador |

Tres relaciones que conviene dibujar: *Registrar préstamo* **incluye** *Buscar
en el catálogo* y *Buscar alumno*; *Registrar devolución* **extiende**
*Consultar préstamos*; y todos los casos **incluyen** *Iniciar sesión*, porque
sin sesión las políticas RLS no devuelven ni una fila.

## 10.2 Caminos de excepción · `DIA-02` (#60)

Los rechazos **no son hipotéticos**: cada uno existe hoy en la base y tiene su
mensaje. Esta es la lista completa, con quién lo aplica.

| Caso de uso | Excepción | Quién la aplica |
|---|---|---|
| Registrar préstamo | El alumno ya tiene un préstamo activo | Índice único parcial `prestamo_unico_activo` sobre `prestamos` |
| Registrar préstamo | No quedan ejemplares | Disparador `mover_inventario` |
| Registrar préstamo | El libro o el alumno no existe | Llave foránea |
| Dar de baja libro | Tiene préstamos activos | Disparador `validar_baja_de_libro` |
| Dar de baja libro | No se indicó motivo | Restricción `baja_con_motivo` |
| Registrar libro | Año de publicación futuro | Disparador `validar_ano_publicacion` |
| Registrar libro | Páginas o existencias no positivas | Restricciones `check` |
| Registrar persona | Código repetido | Restricción `unique` sobre `perfiles.codigo` |
| Cambiar perfil de acceso | No eres administrador | Disparador `proteger_rol` |
| Cambiar perfil de acceso | Es tu propio perfil | Disparador `proteger_rol` |
| Cualquiera | Tu perfil no alcanza esa fila | Las 16 políticas RLS |
| Cualquiera | Sesión vencida o sin conexión | `core/errores.py` lo distingue y lo explica |

Precondición común a todos: sesión iniciada. Postcondición del préstamo: una
fila en `prestamos` con su `fecha_limite` ya calculada y una unidad menos en
`libros.existencias` — las dos las escribe la base, no Python.

## 10.3 Proceso de préstamo y devolución · `DIA-03` (#61)

El flujo tal como ocurre. Lo que está en **negrita** lo hace Postgres solo:

**Préstamo**

1. El bibliotecario escribe parte del nombre, código o salón del alumno.
2. Escribe parte del título o autor del libro.
3. Pulsa *Registrar préstamo*. Python envía un `insert` con dos datos:
   `libro_id` y `usuario_id`.
4. **El índice único rechaza si el alumno ya tiene uno activo.**
5. **`calcular_fecha_limite` pone `fecha_limite` = hoy + 7 días.**
6. **`mover_inventario` descuenta una unidad; si no hay, rechaza.**
7. La pantalla recarga desde `v_prestamos`.

**Devolución**

1. El bibliotecario elige el préstamo y pulsa *Registrar devolución*.
2. Python envía `estado = 'devuelto'`. Nada más.
3. **`sellar_devolucion` pone `fecha_devolucion` con la fecha de la base.**
4. **`mover_inventario` reintegra la unidad.**

**Vencimiento:** un préstamo pasa a `vencido` cuando `fecha_limite < hoy`. La
función `marcar_prestamos_vencidos()` existe pero **nadie la llama todavía**
(`PRE-05`, #33); mientras tanto `v_prestamos` calcula `dias_restantes` en cada
consulta, así que el reporte de deudores sale correcto igual.

**Por qué importa que los pasos en negrita estén en la base:** el diagrama
debe mostrarlos dentro del almacén de datos y no dentro de la aplicación. Esa
es la decisión que ordena el proyecto y la razón de que la app móvil no tenga
que reimplementar nada.

## 10.4 Flujo de datos · `DIA-04` (#62)

**Entidades externas:** bibliotecario, administrador, alumno. (Los correos
automáticos ya no son entidad externa: el requisito se retiró.)

**Almacenes** — las 7 tablas: `perfiles`, `usuarios`, `empleados`, `libros`,
`prestamos`, `bitacora_libros`, `notificaciones`.

**Procesos de nivel 1**, con lo que leen y escriben:

| Proceso | Lee | Escribe |
|---|---|---|
| 1. Controlar acceso | `perfiles`, `auth.users` | — |
| 2. Gestionar catálogo | `libros` | `libros`, `bitacora_libros` |
| 3. Buscar y filtrar | `v_catalogo` | — |
| 4. Gestionar padrón | `perfiles`, `usuarios` | `perfiles`, `usuarios` |
| 5. Gestionar plantilla | `perfiles`, `empleados` | `perfiles`, `empleados` |
| 6. Operar préstamos | `v_prestamos`, `v_catalogo` | `prestamos`, `libros` |
| 7. Generar reportes | `v_deudores`, `v_libros_faltantes` | — |

`bitacora_libros` y `notificaciones` aparecen como almacenes **sin flujo de
escritura**: las tablas existen y nada escribe en ellas (`LIB-04` #24,
`NOT-01` #39). Dibujarlas así es correcto y además deja ver el hueco.

## 10.5 y 10.6 Modelo de datos · `DIA-05` (#63) y `DIA-06` (#64)

Las 7 tablas con sus columnas reales. **PK** llave primaria, **FK** foránea.

**`perfiles`** — lo común a toda persona
```
id              uuid      PK, default gen_random_uuid()
auth_id         uuid      FK → auth.users(id) ON DELETE SET NULL, unique, NULL
rol             enum      rol_usuario, not null, default 'alumno'
codigo          text      not null, unique
nombre          text      not null, no vacío
apellido        text      not null, no vacío
calle           text      · colonia text · numero integer
codigo_postal   text      texto: conserva ceros a la izquierda
telefono        text      texto: no es un valor aritmético
correo          text      NULL, check de formato
activo          boolean   not null, default true
creado_en       timestamptz · actualizado_en timestamptz
```
`auth_id` admite NULL a propósito: **un alumno tiene ficha sin tener cuenta.**

**`usuarios`** — lo propio del alumno · **`empleados`** — lo propio del empleado
```
usuarios:   perfil_id uuid PK, FK → perfiles(id) ON DELETE CASCADE
            grado smallint check (1..6) · grupo text check (≤ 4 caracteres)

empleados:  perfil_id uuid PK, FK → perfiles(id) ON DELETE CASCADE
            tipo_empleado text not null · fecha_ingreso date not null
```
Ambas comparten la PK con `perfiles`: es **herencia por tabla**, relación 1:1.
Una persona es alumno o empleado, nunca las dos.

**`libros`**
```
id              bigint    PK, generated always as identity
titulo          text      not null, no vacío
autor           text      not null, no vacío
tipo_libro      text      · editorial text
existencias     integer   not null, default 0, check (>= 0)
ano_publicacion smallint  · num_paginas integer check (> 0)
activo          boolean   not null, default true     ← baja lógica
motivo_baja     text      · dado_baja_en timestamptz
constraint baja_con_motivo: si no está activo, exige motivo y fecha
```
**No hay columna `disponible`**: se deduce de las existencias en `v_catalogo`.
El sistema Java la almacenaba y podía contradecir al inventario (defecto D-09).

**`prestamos`**
```
id              bigint    PK
libro_id        bigint    FK → libros(id)    ON DELETE RESTRICT
usuario_id      uuid      FK → perfiles(id)  ON DELETE RESTRICT
registrado_por  uuid      FK → perfiles(id)  ON DELETE SET NULL, NULL
fecha_prestamo  date      not null, default current_date
fecha_limite    date      not null            ← la pone el disparador
fecha_devolucion date     NULL                ← la pone el disparador
estado          enum      estado_prestamo, default 'activo'
constraint devolucion_coherente
índice único parcial sobre (usuario_id) where estado in ('activo','vencido')
```
**`RESTRICT` y no `CASCADE`** es deliberado: `REQ-PRE-03` exige conservar el
historial. Borrar en cascada lo destruiría, que es lo que hacía el Java.
Ese índice único parcial **es** la regla de un libro por alumno.

**`bitacora_libros`** · **`notificaciones`** — existen, nadie escribe en ellas
```
bitacora_libros: id PK · libro_id FK→libros CASCADE · perfil_id FK→perfiles SET NULL
                 accion text check ('alta','modificacion','baja')
                 datos_antes jsonb · datos_despues jsonb · ocurrido_en

notificaciones:  id PK · perfil_id FK→perfiles CASCADE
                 prestamo_id FK→prestamos SET NULL
                 tipo   check ('vencimiento_proximo','prestamo_vencido','libro_disponible')
                 destinatario text not null
                 estado check ('pendiente','enviada','fallida'), default 'pendiente'
                 detalle text · enviada_en · creada_en
```
`notificaciones` quedó sin requisito que la respalde: `REQ-PRE-04` se retiró
porque la escuela confirmó que no se comunica por correo con las familias.

**Cardinalidades para el E-R**

| Relación | Cardinalidad | Regla |
|---|---|---|
| `perfiles` – `usuarios` | 1 : 0..1 | Un perfil es alumno, o no |
| `perfiles` – `empleados` | 1 : 0..1 | Un perfil es empleado, o no |
| `perfiles` – `prestamos` (`usuario_id`) | 1 : 0..N | Pero **solo uno activo a la vez** |
| `perfiles` – `prestamos` (`registrado_por`) | 1 : 0..N | Quién lo capturó |
| `libros` – `prestamos` | 1 : 0..N | Historial completo del ejemplar |
| `libros` – `bitacora_libros` | 1 : 0..N | |
| `perfiles` – `notificaciones` | 1 : 0..N | |

Dos tipos enumerados: `rol_usuario` (alumno, bibliotecario, administrador) y
`estado_prestamo` (activo, vencido, devuelto).

**Aviso para el E-R:** los UML del repositorio Java **ya no corresponden**.
Cambió el esquema, apareció la capa de servicios y las reglas se movieron a la
base. Partir de ellos produce un diagrama equivocado.

## 10.7 Documentación de la base · `DIA-07` (#65)

**4 vistas**, todas con `security_invoker = on` para que respeten RLS:

| Vista | Qué responde | Quién la usa |
|---|---|---|
| `v_catalogo` | El acervo con la disponibilidad deducida de las existencias | Catálogo, Nuevo préstamo |
| `v_prestamos` | Préstamos con `dias_restantes` calculado **por la base** | Préstamos |
| `v_deudores` | Quién debe, desde cuándo y cómo localizar al tutor | Deudores |
| `v_libros_faltantes` | Libros dados de baja, con motivo y fecha | **Nadie todavía** (`REP-02`) |

**8 disparadores**, en orden de aparición:

| Disparador | Sobre | Cuándo | Qué hace |
|---|---|---|---|
| `perfiles_actualizacion` | `perfiles` | before update | Sella `actualizado_en` |
| `perfiles_protege_rol` | `perfiles` | before update **of rol** | Impide cambiar perfiles de acceso sin ser admin, y cambiar el propio |
| `libros_valida_ano` | `libros` | before insert or update **of ano_publicacion** | Rechaza año futuro |
| `libros_actualizacion` | `libros` | before update | Sella `actualizado_en` |
| `libros_valida_baja` | `libros` | before update **of activo** | Impide dar de baja con préstamos activos |
| `prestamos_fecha_limite` | `prestamos` | before insert | Calcula `fecha_limite` = hoy + 7 |
| `prestamos_inventario` | `prestamos` | after insert or update **of estado** | Descuenta y reintegra existencias |
| `prestamos_sella_devolucion` | `prestamos` | before update **of estado** | Pone `fecha_devolucion` con la fecha de la base |

Las cláusulas `of <columna>` importan para el diagrama: el disparador **no se
dispara en cualquier actualización**, solo cuando cambia esa columna.

**15 funciones:** `es_personal`, `es_administrador`, `mi_perfil`, `mi_rol`
(apoyan a las políticas); `registrar_alumno`, `registrar_empleado`,
`actualizar_alumno` (altas y cambios atómicos, para que no queden perfiles a
medias); las ocho de los disparadores; y `marcar_prestamos_vencidos`, que
existe pero nadie llama.

**16 políticas RLS** sobre las 7 tablas:

| Tabla | Políticas |
|---|---|
| `perfiles` | `perfiles_lectura`, `perfiles_alta`, `perfiles_edicion`, `perfiles_baja` |
| `usuarios` | `usuarios_lectura`, `usuarios_escritura` |
| `empleados` | `empleados_lectura`, `empleados_escritura` |
| `libros` | `libros_lectura`, `libros_escritura` |
| `prestamos` | `prestamos_lectura`, `prestamos_escritura` |
| `bitacora_libros` | `bitacora_lectura`, `bitacora_alta` |
| `notificaciones` | `notificaciones_lectura`, `notificaciones_escritura` |

El patrón: el personal alcanza todo; el alumno, solo las filas que le
pertenecen. Se verificó con una cuenta real de perfil alumno.

## 10.8 Interfaces · `DIA-08` (#66)

**11 archivos `.ui`** en `src/biblioteca/ui/disenos/`, editables en Qt Designer.
Los `ui_*.py` de `ui/generado/` los produce el compilador y se sobrescriben.

**Navegación:**

```
login.ui  ─────────────────────► ventana principal (5 pestañas)
                                  │
  ┌───────────────┬───────────────┼───────────────┬───────────────┐
Catálogo       Préstamos       Alumnos        Deudores       Empleados
  │               │               │                              │
formulario_    nuevo_         formulario_                  formulario_
libro.ui       prestamo.ui    alumno.ui                    empleado.ui
(alta y            │          historial_
 edición)          │          alumno.ui
                   └── dos búsquedas y un botón
```

Los cinco diálogos son modales; las cinco pestañas conviven en una ventana.

| Pantalla | Controles principales | Origen de los datos |
|---|---|---|
| Login | correo, contraseña, entrar | Supabase Auth |
| Catálogo | búsqueda, casilla *ver bajas*, tabla ordenable, nuevo/editar/baja | `v_catalogo` |
| Préstamos | tabla, filtro de vencidos, nuevo préstamo, devolución | `v_prestamos` |
| Alumnos | búsqueda, tabla, nuevo/editar/historial | `perfiles` + `usuarios` |
| Deudores | tabla ya generada al abrir | `v_deudores` |
| Empleados | tabla, registrar, modificar | `perfiles` + `empleados` |
| Nuevo préstamo | dos listas de búsqueda, resumen, confirmar | `v_catalogo`, `perfiles` |

**Detalles que conviene reflejar** porque nacieron de defectos corregidos: el
diálogo de préstamo **no es un formulario** sino dos búsquedas y un botón, por
`RNF-USA-01`; la búsqueda del alumno acepta indistintamente nombre, código o
salón, sin elegir criterio antes; y la paleta se fuerza en claro porque el
modo oscuro de Windows dejaba ilegibles los encabezados de las tablas.

**Cuando se apliquen las historias de la reunión** cambian tres pantallas: el
formulario de libro gana colección y asignatura, el de alumno gana CURP,
maestro y datos del tutor y pierde el correo, y aparece una pantalla nueva de
estadísticas. Conviene dibujarlas después de #72–#79, no antes.
