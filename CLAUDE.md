# Sistema de Biblioteca — Escuela Primaria Adalberto Tejeda

Contexto completo del proyecto. Claude Code lee este archivo automáticamente al
abrir el repositorio: una sesión nueva en cualquier computadora debe poder
continuar el trabajo solo con esto y acceso al repositorio, sin preguntar nada.

**Última actualización:** 8 de noviembre de 2026 — la capa de datos de
colección, asignatura, CURP y maestros de grupo, en el #92 (sección 14), sobre
la migración 11, que corre en Supabase desde el 3 de noviembre, y las cuatro
decisiones de Yael del mismo día sobre lo que la regla 7 había dejado
pendiente (7.0, punto 3). **Lo que sigue está en 7.0.** El mismo día entraron a `main` el Avance 3 (sección 11),
las propuestas de diseño del 27 de octubre (12), el diseño «Lápiz» (13) y el
ejecutable de Windows (sección 5).

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
4. **Cuidar de qué `main` sale cada rama y a cuál vuelve.** Son dos
   comprobaciones, una antes de empujar y otra antes de mergear:

   ```bash
   git log --oneline origin/main..HEAD          # antes de empujar
   git diff --stat origin/main origin/<rama>    # antes de mergear
   ```

   La primera avisa si el PR de esa rama ya se mergeó: entonces hay que abrir
   una rama nueva desde `main`, no seguir empujando ahí. La segunda avisa si
   la rama quedó vieja: **si aparecen líneas en rojo de archivos que esa rama
   nunca tocó, mergearla revertiría el trabajo de otro PR.** Se corrige con
   `git merge origin/main` en la rama, antes de mergear.

   Abrir un PR solo cuando el anterior ya esté en `main` evita la mitad del
   problema; la otra mitad la evitan esas dos órdenes.
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
- **Ramas desalineadas con `main`.** Ha pasado **cinco veces**, en dos
  variantes.

  *Empujar a una rama ya mergeada* — cuatro veces: tras el #55 (rescate #56),
  tras el #68, tras el #80 y tras el #82 (rescate #83). Se entrega, la Scrum
  Master mergea, y se sigue empujando a esa rama porque el PR «sigue abierto»
  en la sesión. La última vez dejó la migración 10 aplicada en Supabase pero
  sin registrar en `main`, con la aplicación llamando todavía a la función
  vieja.

  *Mergear una rama vieja* — una vez, detectada antes de que ocurriera: la
  rama del Avance 2 salió del merge del #82 y el #83 se mergeó después, así
  que su diff contra `main` **borraba** la migración 10 y `actualizar_empleado`.
  Se corrigió con `git merge origin/main` en la rama.

  Las dos comprobaciones de la regla 4 detectan cada variante.
- **Verificar nombres de archivo con acentos.** `git ls-tree` escapa `ó` como
  `\303\263`; comparar esa cadena contra el sistema de archivos da falsos
  «archivo faltante». Usar `git ls-tree -z` o `core.quotepath false`.
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
| Colección de Libros del Rincón y asignatura válidas | Restricciones `libros_coleccion_valida` y `libros_asignatura_valida` | `LIB-06`, `LIB-07` |
| CURP con el formato oficial y sin repetirse | Restricciones `usuarios_curp_formato` y `usuarios_curp_key` | `USU-07` |
| Acceso por perfil | 18 políticas RLS sobre las 8 tablas | Factibilidad Legal |

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
    consultas.py           patron_de_busqueda(): escapa el texto para PostgREST
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
    recursos/              letras (Manrope, IBM Plex Mono · OFL) e iconos (Lucide · ISC)
    apariencia.py          carga las letras; icono() tiñe un SVG del color pedido
    estilo.py              paleta mostaza, hoja de estilo, aplicar_apariencia(), rotular()
    componentes.py         BotonRiel (menú de iconos), DelegadoFilaElegida, poner_icono()
    formato.py             fecha_corta(), inicial() de la portada de un libro
    login.py               REQ-USU-02 — la ficha de biblioteca sobre el grafito
    ventana_principal.py   columna de iconos con las cinco secciones
    catalogo.py            + formulario_libro.py
    prestamos.py           + nuevo_prestamo.py
    alumnos.py             + formulario_alumno.py + historial_alumno.py
    deudores.py
    empleados.py           + formulario_empleado.py
herramientas/
  compilar_ui.py           convierte los .ui en módulos de Python
  capturar_pantallas.py    fotografía las pantallas contra la base real (sección 11)
  empaquetar.py            arma el .exe de Windows con PyInstaller (sección 5)
database/migraciones/      11 migraciones, ya aplicadas en Supabase
tests/                     819 pruebas con pytest, en los cuatro grupos que
  conftest.py              tenía la suite JUnit del sistema Java
  caja_negra/              las reglas, sin leer la implementación
  caja_blanca/             las ramas del código, con dobles del cliente
  interfaz/                las nueve pantallas, Qt en modo offscreen
  integracion/             el flujo completo, de la pantalla a la consulta
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

## 8 tablas

| Tabla | Qué guarda |
|---|---|
| `perfiles` | Datos comunes de toda persona. `auth_id` opcional: un alumno puede tener ficha sin cuenta |
| `usuarios` | Lo propio del alumno: grado, grupo y CURP (opcional; si se escribe, con el formato oficial y sin repetirse) |
| `empleados` | Lo propio del empleado: tipo y fecha de ingreso |
| `libros` | Catálogo, con baja lógica (`activo`, `motivo_baja`, `dado_baja_en`), colección de Libros del Rincón y asignatura |
| `prestamos` | Con `ON DELETE RESTRICT`, no CASCADE (REQ-PRE-03) |
| `bitacora_libros` | Trazabilidad — **la tabla existe pero nada escribe en ella** (`LIB-04`) |
| `notificaciones` | Avisos por correo — **vacía**, falta `NOT-01` |
| `maestros_de_grupo` | El maestro de cada salón (grado y grupo), que heredan sus alumnos — **vacía**, falta su pantalla (sección 14) |

## 4 vistas

| Vista | Para qué |
|---|---|
| `v_catalogo` | Catálogo con disponibilidad deducida de las existencias; desde la migración 11, también colección y asignatura |
| `v_prestamos` | Préstamos con `dias_restantes` calculado por la base |
| `v_deudores` | Reporte de deudores, con contacto del tutor |
| `v_libros_faltantes` | Libros dados de baja — **existe pero no hay pantalla** (`REP-02`) |

Todas con `security_invoker = on`, para que respeten las políticas RLS.

## 18 funciones

`es_personal`, `es_administrador`, `mi_perfil`, `mi_rol` (apoyo a las políticas);
`registrar_alumno`, `registrar_empleado`, `actualizar_alumno` (altas atómicas);
`calcular_fecha_limite`, `mover_inventario`, `validar_baja_de_libro`,
`validar_ano_publicacion`, `sellar_devolucion`, `proteger_rol`,
`marcar_actualizacion`, `descontar_ejemplar` (disparadores);
`marcar_prestamos_vencidos` (**existe pero nadie la llama sola**, ver
`PRE-05`); `actualizar_empleado` (cambio atómico del personal); y `hoy()`,
**que devuelve la fecha en el huso de Veracruz**. La base corre en UTC: todo
cálculo de fechas pasa por `hoy()`, nunca por `current_date`.

Desde la migración 11, `registrar_alumno` y `actualizar_alumno` reciben la
CURP en un último parámetro, `p_curp`, con valor por omisión: una llamada que
no la manda sigue funcionando igual.

## 9 disparadores · 18 políticas RLS

RLS activa en las 8 tablas. Un alumno autenticado solo alcanza su propio
perfil y sus propios préstamos; lo verificamos con una cuenta real.
`maestros_de_grupo` sigue el patrón del padrón: el personal lee y escribe, y
un alumno no ve ninguna fila.

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
10_correcciones_de_la_auditoria          reloj, escalada, inventario, puesto
11_datos_que_pidio_la_escuela            colección, asignatura, CURP, maestros de grupo
```

**Para cambiar el esquema se crea una migración nueva**, nunca se edita una
anterior: los archivos son el registro de lo que ya corrió en Supabase. En el
registro de Supabase la 10 quedó sin su número, como
`correcciones_de_la_auditoria`; las demás llevan el mismo nombre que su
archivo.

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

**Si la carpeta del proyecto cambia de nombre o de lugar, hay que repetirlo.**
La instalación editable guarda la ruta de `src/` en un archivo `.pth` del
`.venv`. Con la ruta vieja, `python main.py` da `ModuleNotFoundError` aunque
las pruebas pasen —`pyproject.toml` les agrega `src` por su cuenta— y aunque
F5 funcione, porque `launch.json` pone `PYTHONPATH`. Pasó el 8 de noviembre:
la carpeta se había renombrado de `7mo semetre` a `7mo_semetre`.

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
.venv/Scripts/python.exe -m pytest tests/ -v            # 819 pruebas, ~7 s
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
| `bibliotecaria@demo.com` | `12345` | administrador |
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

Al 8 de noviembre la base tiene 10 libros activos y 2 dados de baja, los
mismos 6 alumnos y 2 empleados, y 8 préstamos: 4 devueltos y 4 abiertos,
todos ya pasados de su fecha límite. Dos de esos cuatro siguen marcados
`activo` porque nadie llama a `marcar_prestamos_vencidos` (`PRE-05`, #33);
`v_prestamos` y el reporte de deudores los cuentan bien porque calculan los
días en cada consulta. Ningún alumno tiene CURP ni maestro de grupo, y ningún
libro tiene colección.

## Abrir la aplicación sin VS Code

```bash
.venv/Scripts/python.exe herramientas/empaquetar.py
```

Arma `Biblioteca Escolar.exe` con PyInstaller, lo deja en
`%LOCALAPPDATA%\Programs\Biblioteca Escolar\` y pone un acceso directo
«Biblioteca Escolar» en el escritorio. Lleva dentro Python, Qt, las letras y
los iconos, así que la computadora no necesita tener Python. Pesa unos 145 MB
y tarda unos tres minutos en armarse.

- **Es una foto del código.** Después de cada cambio, o al cambiar de rama,
  hay que volver a correr el guion con la aplicación cerrada; si no, el
  acceso directo abre la versión anterior.
- **El `.env` viaja junto al `.exe`.** `core/config.py` lo busca tres
  carpetas arriba de sí mismo, y dentro del ejecutable esa carpeta es la del
  `.exe`: no hubo que tocar el código. Su llave publishable no es secreta.
- **Para la computadora de la biblioteca**, `--destino E:/` y
  `--sin-acceso-directo` dejan la carpeta en una memoria USB. Se copia
  completa y allá se crea el acceso directo.
- **El ejecutable no está firmado.** Si Windows o el antivirus lo detienen la
  primera vez, es por eso; no hay certificado de firma en el proyecto.

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
| #80 | Acuerdos de la reunión con la escuela, y las ocho historias que dejó |
| #81 | Los ocho diagramas del Sprint 1, en `Documentacion/diagramas/` |
| #82 | Los diez defectos de la auditoría profunda + migración 10 |
| #83 | PR de rescate: integró a `main` la migración 10 y `actualizar_empleado` |
| #84 | Avance 2 con los ocho criterios de la rúbrica; regla 4 ampliada |
| #85 | Suite de pruebas rehecha sobre la del sistema Java (ver 6.4) |
| #86 | Historial de PR al día, que se había quedado en el #71 |
| #87 | Avance 3: seguridad, implementación y evaluación (ver 11) |
| #88 | Diseño «Lápiz», mostaza: base, inicio de sesión y Catálogo (ver 13) |
| #89 | Ejecutable de Windows, para abrir la biblioteca sin VS Code (ver 5) |
| #90 | Propuestas de diseño del 27 de octubre y prototipos navegables (ver 12) |
| #91 | Migración 11 registrada en el repositorio; este archivo al día (ver 14 y 7.0) |
| — | `diseno/pantallas-restantes`: pantallas restantes del diseño «Lápiz» y el logo; PR pendiente de que entre el #92 (ver 13) |
| — | `docs/manual-de-usuario`: manual de usuario en Word (`DOC-04`, #42) |
| #92 | Capa de datos de los campos de la escuela, el traductor al día con las migraciones 10 y 11, y las decisiones de Yael del 8 de noviembre (ver 14 y 7.0) |

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

## Auditoría profunda — 21 de septiembre

Diez auditorías en paralelo sobre código, esquema, pruebas, documentos y
backlog. Unos 240 hallazgos en bruto, ~130 reales.

### Corregido en el código

| Defecto | Qué pasaba |
|---|---|
| Los patrones de error no coincidían con la base | Tres de las reglas más usadas buscaban textos que los disparadores **nunca emiten**, así que «no quedan ejemplares» llegaba como volcado de Postgres |
| Cuatro traductores de errores | Cada repositorio tenía su lista y se contradecían: el mismo `duplicate key` significaba tres cosas distintas. Ahora todos delegan en `core/errores.py` |
| `"401"` como señal de sesión vencida | Cualquier error con esos dígitos —un `id` 1401— mandaba a reiniciar sesión |
| Las tres pantallas de captura | No pasaban por el traductor: un corte de red se leía «la base rechazó la operación» |
| El login culpaba a la contraseña | Sin internet decía «correo o contraseña incorrectos», y la bibliotecaria la cambiaba |
| La coma rompía la búsqueda | «García, Ana» partía el filtro de PostgREST. Ahora se escapa en `core/consultas.py` |
| `date.today()` en el préstamo | Anunciaba una fecha de vencimiento que la base no iba a guardar. Ahora muestra el plazo, no una fecha |
| `filas.data[0]` sin guarda | Un `UPDATE` que no afectaba filas reventaba con `IndexError` que ninguna pantalla atrapa |
| La búsqueda por salón | No filtraba por `activo` ni por rol: «4B» mostraba alumnos dados de baja que su nombre no mostraba |
| El perfil de acceso al dar de alta | El combo solo se bloqueaba al modificar, de modo que cualquiera podía registrar a un administrador |

Las pruebas pasaron de 48 a 96. Las nuevas cubren **cada mensaje que la base
levanta**, copiado literalmente de los `raise exception` de las migraciones:
si un disparador cambia su texto y nadie actualiza el traductor, la prueba
falla. Antes `coverage` reportaba 100 % con siete de las ocho reglas sin
interrogar. *(Esas 96 son las de la auditoría; después se rehizo la suite
entera sobre la del sistema Java y quedaron 684 — ver 6.4.)*

### Corregido en la base — migración 10, aplicada el 22 de septiembre

`database/migraciones/10_correcciones_de_la_auditoria.sql`. Los cuatro
defectos que no se podían arreglar desde Python, verificados contra la base
real después de aplicarla:

1. **Escalada de privilegios.** `proteger_rol` es `before update of rol`: no
   corre en el INSERT, `perfiles_alta` solo exige `es_personal()` y
   `registrar_empleado` acepta `p_rol => 'administrador'`. Además `auth_id`
   no está protegido, así que se puede repuntar el del administrador. Se cerró
   la puerta de la interfaz; **la de la API sigue abierta**.
2. **Cambiar el puesto de un empleado no guarda nada.** `tipo_empleado` vive
   en la tabla `empleados` y `actualizar()` solo escribe `perfiles`. Falta una
   función `actualizar_empleado` como la que ya existe para alumnos.
3. **El inventario puede descuadrarse.** `mover_inventario` no cubre el
   `DELETE` de un préstamo, ni reabrir uno devuelto, ni cambiar `libro_id`.
4. **El reloj sigue en UTC.** Seis sitios usan `current_date`: en Veracruz un
   libro se marca vencido desde las 18:00 del día que aún no vence.

**Comprobado en la base, no solo escrito:**

| Prueba | Resultado |
|---|---|
| Bibliotecario da de alta un perfil administrador | rechazado |
| Bibliotecario repunta el `auth_id` del administrador | rechazado |
| `registrar_empleado(..., 'administrador')` desde bibliotecario | rechazado |
| Bibliotecario registra a un bibliotecario (REQ-EMP-01) | permitido |
| Administrador cambia el perfil de acceso de otro | permitido |
| Administrador cambia **el suyo** | rechazado |
| Cambiar el puesto de un empleado | **se guarda** |
| Prestar → devolver → reabrir → borrar | 3 → 2 → 3 → 2 → 3 |
| `insert` con `fecha_limite = 2099-01-01` | la base guardó 2026-09-29 |

La última fila importa: `calcular_fecha_limite` dejó de respetar la fecha que
envíe el cliente, así que **REQ-PRE-02 pasó de valor por omisión a regla**.

Las pruebas corrieron dentro de transacciones que abortan solas: los datos
quedaron intactos —7 préstamos, 21 ejemplares, 8 perfiles, 1 administrador—.

**Aviso del revisor de Supabase que NO hay que "corregir":** marca
`es_personal`, `es_administrador`, `mi_perfil` y `mi_rol` como funciones
`security definer` invocables por `authenticated`. Es intencional y necesario:
las políticas RLS las evalúan como el invocador, así que revocarles
`execute` rompería el control de acceso entero. Solo devuelven información que
el propio usuario ya tiene sobre sí mismo.

### Mejoras pendientes, ninguna urgente

- Código muerto: `sesion.py:exigir_personal()`, `sesion.py:hay_sesion()`,
  `libros.py:obtener()` y los dos `datos_propios()` de `modelos/persona.py`
- Diez consultas de los repositorios sin `.limit()`
- Un `except Exception: pass` silencioso al cerrar sesión — **ya probado**:
  existe para que la aplicación pueda cerrarse sin internet
- ~~`core/config.py` lee el entorno al importarse~~ — sigue leyéndolo, pero ya
  no impide probar: `tests/conftest.py` pone valores de prueba antes de que
  nada importe el paquete
- ~~Sin pruebas de repositorios, sesión ni interfaz~~ — las tres capas están
  al 100 %, ver la sección 6.4
- Supabase avisa que la protección contra contraseñas filtradas está
  desactivada — es un interruptor en el panel
- Hay un libro de prueba en el catálogo real: `"El principito"` duplicado,
  autor `"nl"`

## 6.4 La suite de pruebas — rehecha sobre la del sistema Java

El sistema Java tenía **70 pruebas JUnit en 16 archivos**, repartidas en
cuatro paquetes, y un informe de métricas con JaCoCo. Se rehicieron los
cuatro grupos, no solo caja blanca y negra: `QA-02` (#19) queda cerrado.

| Paquete Java | Qué probaba | Archivos · pruebas | Equivalente aquí | Pruebas |
|---|---|---|---|---|
| `ClasesBiblia` | Entidades del dominio | 4 · 13 | `tests/caja_negra/` | 162 |
| `DAOBiblia` | Persistencia en CSV | 2 · 5 | `tests/caja_blanca/` | 176 |
| `GUIBiblia` | Las ventanas Swing | 10 · 47 | `tests/interfaz/` | 226 |
| `ConsolaBiblia` | Alta de libro completa | 1 · 9 | `tests/integracion/` | 24 |
| | | | los cinco archivos que ya existían | 96 |
| **16 · 70** | | | **684** | |

**La diferencia está en el indicador de ramas, no en el de líneas.** El
informe del Java reportaba **74 % de instrucciones y 24 % de ramas**, y su
propia conclusión era que «las pruebas recorren el código, pero no lo
interrogan». Midiendo lo mismo con `coverage`, que es el JaCoCo de Python:

| | Sistema Java | Aquí |
|---|---|---|
| Instrucciones · sentencias | 74 % | **100 %** (1 617, ninguna sin recorrer) |
| Ramas | 24 % | **99 %** (357 de 360) |
| Capa gráfica, ramas | 14 % | 100 % en las nueve pantallas |

```bash
.venv/Scripts/python.exe -m pytest tests/ --cov=biblioteca --cov-branch
```

Las tres ramas parciales que quedan son salidas de bucle sin interés y una
condición de `ui/estilo.py`. Los `ui_*.py` de `ui/generado/` se cuentan
aparte: son código de máquina que se sobrescribe, y mezclarlos infla la cifra
igual que `GUIBiblia` inflaba la del original.

### Qué cambió respecto del original, y por qué

- **Los casos TC-19 a TC-30 ya se pueden ejecutar.** La matriz del Java los
  dejaba sin automatizar porque la lógica vivía dentro de `guardarenlista`,
  un método privado de `GUILibro` atado a Swing, y cada `JOptionPane` dejaba
  la suite esperando un clic. Al extraer las reglas a `servicios/` dejaron de
  necesitar una ventana.
- **`AltaLibroConsola` ya no hace falta.** Era un desvío: una interfaz de
  texto escrita para poder probar lo que el formulario no dejaba. Se probaba
  el desvío, no el camino del usuario. `tests/integracion/` recorre el
  formulario real.
- **Tres pruebas cambiaron de signo.** Las que documentaban D-01, D-06 y D-09
  celebraban que el sistema aceptara datos que sus mensajes decían rechazar.
  Ahora comprueban el rechazo.
- **Los tres casos de CSV siguen sin cerrarse.** `tests/caja_negra/
  test_alta_de_libro.py` trae la prueba de TC-06 marcada como fallo esperado:
  el día que se implemente `REP-03` (#38) deja de fallar y avisa sola.

### Cosas que las pruebas nuevas encontraron

- **`repositorios/prestamos.py:189`** — `registrar()` hace `filas.data[0]` sin
  la guarda que sí tienen `libros.dar_de_alta` y `libros.modificar`. Con una
  respuesta vacía levanta `IndexError`, que no es `ErrorDePrestamo` y
  **ninguna pantalla atrapa**. La prueba fija el comportamiento de hoy: el día
  que se agregue la guarda, falla y hay que cambiarla.
- **`core/sesion.py:12-14`** — el mismo `import` repetido tres veces.
- **`ui/formulario_empleado.py:52-56`** — el comentario dice «falta la
  migración 10». Ya está aplicada.
- **`repositorios/personas.py:_aplanar()`** consume el diccionario que recibe
  (`fila.pop`). En la aplicación da igual, porque cada fila llega recién
  deserializada; queda anotado porque no se ve al leer la llamada.

### Dos trampas del andamiaje, por si alguien agrega pruebas

1. **Un widget sin nombre al que apuntar se destruye solo.** `Pantalla().ui.x`
   deja la pantalla como temporal: Python la recoge y Qt destruye el objeto
   C++ antes de la aserción. Hay que guardarla en una variable.
2. **`monkeypatch.setattr(QMessageBox, "warning", ...)` no prende**, porque es
   un tipo de Shiboken: el cuadro se abre de verdad y la suite se cuelga
   esperando un clic — el mismo problema que el Java no supo resolver. Se
   sustituye el nombre que importa cada módulo de `ui/`.

`tests/conftest.py` tiene además una red de seguridad de ámbito de sesión que
impide salir a internet: `cerrar_sesion()` construía un cliente real y la
suite se colgaba **después de la última prueba**, sin mensaje.

---

# 7. LO SIGUIENTE QUE SE DEBE HACER

## 7.0 Al 8 de noviembre

**El calendario manda.** El Sprint 4 terminó el 8 de noviembre y el 9 empieza
el cierre, hasta el 28: aceptación con el docente, correcciones, manuales y
entrega. Los hitos de GitHub todavía se llaman «Por definir tras la reunión».

En este orden:

1. **La capa de datos de lo que pidió la escuela** (#72 a #76): **lista en
   el #92**, rama `datos/campos-de-la-escuela`, esperando revisión. Modelos,
   repositorios, validadores y traductor ya conocen colección, asignatura,
   CURP y maestros de grupo; la suite queda en 819. Detalle en la sección 14.
2. **Las pantallas que faltan del diseño «Lápiz»**: **hechas** en la rama
   `diseno/pantallas-restantes` (sección 13), con el logo de la escuela y las
   cuatro funciones aprobadas. Su PR se abre cuando el #92 esté en `main`.
   **Las pruebas de interfaz no se pusieron al día**, por decisión de Yael del
   9 de noviembre: unas 34 describen las pantallas viejas y fallan, y
   `tests/interfaz/test_acciones.py` se queda colgado porque «Registrar
   devolución» abre ahora un diálogo propio y no el `QMessageBox` que la
   prueba sustituye. Está pendiente.
   El **manual de usuario** (`DOC-04`, #42) está en
   `Documentacion/Manual_de_usuario.docx`, rama `docs/manual-de-usuario`.
3. **Lo que quedó decidido el 8 de noviembre.** Este punto juntaba las
   preguntas que la regla 7 había dejado pendientes, y Yael las contestó:
   - **Entran a la aplicación las cuatro funciones de las maquetas** que
     estaban fuera: «por vencer» —tres días o menos— con su conteo y su
     filtro en Préstamos; el contador de deudores junto al icono de Deudores;
     y en el panel del préstamo, el teléfono del tutor y quién lo registró.
     Van con el punto 2 y no piden migración.
   - **Se quedan las reglas del prototipo** que la migración 11 ya aplica:
     CURP opcional, con el formato oficial y sin repetirse; teléfono del
     tutor obligatorio; colección y asignatura opcionales.
   - **Un libro no devuelto se vuelve adeudo cuando la bibliotecaria lo marca
     como perdido**; nada automático. Es `PRE-08` (#77) y no se implementa
     ahora.
   - **Siguen el límite de un libro por alumno y el plazo de siete días**
     (sección 9).
4. **El cierre**: la sesión de aceptación con el docente (`QA-04`, #41), los
   manuales (`DOC-04`, #42) y el aviso de privacidad (`DOC-02`, #20). **Sin
   aviso firmado no se cargan datos reales**, y antes de cargarlos hay que
   cambiar las contraseñas de las cuentas de demostración.
5. **Issues terminados que siguen abiertos**: `DOC-01` (#9), `QA-02` (#19) y
   los diagramas (`DOC-03` #28, y #59 a #66, a los que les faltan capturas de
   algunos criterios). `DIA-05`, `DIA-06` y `DIA-07` además dibujan la base de
   antes de la migración 11. Los acuerdos del #67 se documentaron en el #80;
   falta ajustar los hitos.

Después de cada cambio de código hay que volver a armar el ejecutable
(sección 5): el acceso directo abre la versión con que se armó.

**Lo que sigue en 7.1 a 7.3 es el plan de septiembre**, que se conserva como
historia. El sistema funciona; lo que estaba desalineado eran los entregables. De las
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

**Los ocho ya están hechos**, en `Documentacion/diagramas/`. Cada uno trae el
diagrama y su explicación, verificados contra las migraciones y los `.ui`, no
contra la documentación. Los de Mermaid se ven dibujados en GitHub sin instalar
nada; el de casos de uso es un SVG hecho a mano.

Lo que falta de esos issues son las **capturas de pantalla** que piden algunos
criterios de aceptación, y exportar las imágenes para pegarlas en el Avance 2.

El issue #28 quedó como paraguas de los ocho. Su alcance original mencionaba
tres diagramas: el profesor pide ocho.

El Sprint 1 lleva además la documentación que quedó pendiente: `INF-02`,
`DOC-01`, `DOC-02`, `QA-01` y el registro de los acuerdos de la reunión.

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

**28 de 60 historias cerradas** al 8 de noviembre de 2026, sobre 261 puntos
estimados. Desde el 20 de septiembre solo se cerró `INF-02` (#3), aunque
varias de las abiertas ya están hechas (7.0, punto 5). El total subió de 43 a
60 en tres pasos: los ocho diagramas se abrieron como historias propias, la
reunión dejó un issue de seguimiento, y los acuerdos de la escuela agregaron
ocho historias más.

| Hito | Cerradas | Abiertas |
|---|---|---|
| Trabajo preliminar — Migración a Python | 27 | 0 |
| Sprint 1 — Diagramas y diseño | 1 | 21 |
| Sprint 2 — Por definir | 0 | 4 |
| Sprint 3 — Por definir | 0 | 5 |
| Sprint 4 — Por definir | 0 | 0 |
| Cierre — Entrega final | 0 | 2 |

Todo lo terminado quedó agrupado en el hito de trabajo preliminar: es la
migración completa del sistema Java, concluida antes de que el Sprint 1
empezara.

## Las 32 historias abiertas

| Issue | Historia | Qué falta |
|---|---|---|
| #9 | `DOC-01` | Actualizar la Factibilidad Técnica (resuelto en el Avance 1.1 y 1.2, falta cerrar el issue) |
| #10 | `QA-01` | Acordar la Definición de Terminado del equipo |
| #13 | `USU-03` | Registro de cuentas con contraseña propia |
| #19 | `QA-02` | ~~Traducir la suite JUnit a pytest~~ — **hecho**, falta cerrar el issue (ver 6.4) |
| #20 | `DOC-02` | Aviso de privacidad para tutores |
| #24 | `LIB-04` | Bitácora de trazabilidad: falta el disparador |
| #28 | `DOC-03` | Paraguas de los ocho diagramas, ya hechos |
| #33 | `PRE-05` | Marcado diario de vencidos: falta programar la tarea |
| #37 | `REP-02` | Pantalla de libros faltantes |
| #38 | `REP-03` | Exportación a CSV (cierra D-02, D-04, D-05) |
| #39 | `NOT-01` | Correos automáticos |
| #40 | `NOT-02` | Bitácora de notificaciones |
| #41 | `QA-04` | Pruebas de aceptación con el docente |
| #42 | `DOC-04` | Manuales de una página por rol |
| #43 | `QA-03` | Casos de prueba por módulo |
| #59 a #66 | `DIA-01` a `DIA-08` | Hechos en `Documentacion/diagramas/`; faltan capturas de algunos criterios, y `DIA-05` a `DIA-07` son de antes de la migración 11 |
| #67 | Reunión | Los acuerdos se documentaron en el #80; falta ajustar los hitos |
| #72 a #76 | `LIB-06`, `LIB-07`, `USU-07` a `USU-09` | La base ya los tiene (migración 11, sección 14); faltan la capa de datos y las pantallas |
| #77 a #79 | `PRE-08`, `REP-04`, `REP-05` | Sin empezar. `PRE-08` ya tiene su regla —un libro es adeudo cuando la bibliotecaria lo marca como perdido, nada automático; Yael, 8 de noviembre— y no se implementa ahora |

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
- `Documentacion/Avance_Biblioteca_1.3.docx` — cierra la serie del Avance 1.
  Clona el 1.2 corregido y agrega: el cronograma real en el capítulo 2, la
  sección 1.4.1 con lo que la escuela pidió en la reunión, el retiro de dos
  requerimientos no funcionales, el estado de avance rehecho y las
  correcciones de redacción que arrastraban las versiones anteriores.
  **19 requerimientos funcionales y 14 no funcionales**
- `Documentacion/Avance_Biblioteca_1.4.docx` — versión del equipo sobre el 1.3,
  con los casos de uso extendidos `CU-01` a `CU-06` y el diagrama de casos de
  uso incrustado. Es el insumo del que salió el Avance 2
- `Documentacion/Avance_Biblioteca_2.docx` — contiene **únicamente los ocho
  criterios de la rúbrica**, uno por capítulo: requisitos, casos de uso, casos
  de uso extendidos, proceso, modelado de datos, base de datos, interfaces y
  trazabilidad. La planeación, el análisis y el estado de avance se quedaron
  en la serie del Avance 1. Trece figuras, sin pies
- `Documentacion/Avance_Biblioteca_3.docx` — **la entrega vigente**. Mismo
  criterio: solo lo que pide la rúbrica —**Seguridad, Implementación,
  Evaluación**— más el capítulo de interfaces que pidió el equipo,
  desglosado pantalla por pantalla con captura, descripción y
  funcionalidades. Cuatro capítulos, 14 tablas, 12 capturas, ~5 300 palabras.
  Las cifras no están escritas a mano: salen de correr el sistema y las
  pruebas contra la base real el 19 de octubre. La portada, con los nombres
  del equipo, la puso David Montes. Ver la sección 11
- `Documentacion/Factibilidad.docx`, `Investigación_Equipo_Biblioteca.docx`,
  `Metodologías_Equipo_Biblioteca.docx` — insumos del Avance 1
- `Documentacion/diagramas/` — los entregables gráficos. Un archivo por
  diagrama, con su explicación; los de Mermaid se ven dibujados en GitHub.
  Además:
  - `DIA-01_casos_de_uso.svg` y `DIA-03_diagrama_de_proceso.svg`, dibujados a
    mano para poder exportarlos a cualquier resolución
  - `biblioteca_relacional.png` — **cuidado con el nombre: es el modelo
    entidad-relación**, no el relacional. Lo hizo el equipo y el nombre
    despista; ya provocó un error en una versión del Avance 2
  - `DIA-06b_modelo_relacional.svg` — el relacional de verdad, sin
    `notificaciones` por decisión de la Scrum Master
  - `esquema_supabase.svg` y su `.png` — el esquema tal como lo muestra el
    panel del gestor. **El SVG que exporta Supabase usa `foreignObject` con
    HTML dentro**, así que ningún renderizador de SVG corriente lo dibuja: hay
    que convertirlo con un navegador en modo headless
  - `capturas/` — ocho capturas de la aplicación en ejecución contra la base
    real, generadas con un guion que inicia sesión y fotografía cada pantalla
- `Documentacion/disenos/Propuestas_de_diseno.html` — las cuatro propuestas
  de diseño visual, en un solo archivo que abre sin internet. Ver la sección 12
- `Documentacion/disenos/Propuestas_azul_y_mostaza.html` — la misma
  presentación solo con las propuestas C y D
- `Documentacion/disenos/Prototipo_azul.html` y `Prototipo_mostaza.html` — la
  aplicación simulada en el navegador, con cada botón funcionando. Ver la
  sección 12
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
quitarla del siguiente avance. **Desde cuándo un libro no devuelto se vuelve
deuda lo decidió Yael el 8 de noviembre:** cuando la bibliotecaria lo marca
como perdido, nunca de forma automática. Un niño con tres días de retraso no
debe el costo del libro; uno que lo perdió en marzo sí, y quien distingue un
caso del otro es la bibliotecaria. Es `PRE-08` (#77), que no se implementa
todavía.

**El CURP sube la sensibilidad del padrón.** Es un identificador nacional
único de un menor. Refuerza lo que ya estaba acordado: no cargar datos reales
hasta que el aviso de privacidad esté firmado (`DOC-02`, #20).

### El límite y el plazo, decididos el 8 de noviembre

De los cuatro puntos que la reunión debía resolver, dos se quedaron abiertos
hasta el 8 de noviembre: si el límite de un libro por alumno corresponde a su
práctica real, y si el plazo de siete días es el que aplican hoy. **Yael
decidió que los dos siguen.** Las reglas de la base que los aplican —el índice
único parcial de `prestamos` y `calcular_fecha_limite`— no cambian.

---

# 10. Insumos para los ocho diagramas

> **Esta sección quedó superada por `Documentacion/diagramas/`.** Al construir
> los diagramas se verificó cada dato contra las migraciones y el código, y
> aparecieron errores en lo que sigue. Los confirmados: `v_catalogo` **no la
> consulta nadie** —el catálogo lee la tabla `libros`—; el índice se llama
> `prestamo_unico_activo_por_usuario`; en 10.3 los pasos 4 y 5 están invertidos
> y `calcular_fecha_limite` suma sobre `fecha_prestamo`, no sobre hoy, y solo si
> la fecha viene nula; faltan `creado_en` y `actualizado_en` en `libros` y
> `prestamos`, y dos llaves foráneas en las cardinalidades; y son siete las
> funciones de disparador, no ocho, porque `marcar_actualizacion` sirve a dos.
> **Ante la duda, gana la carpeta de diagramas.**

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
**Es el modelo de antes de la migración 11**: faltan `libros.coleccion`,
`libros.asignatura`, `usuarios.curp` y la tabla `maestros_de_grupo`
(sección 14).

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

**Cifras de antes de la migración 11.** Leídas en la base el 8 de noviembre
son 8 tablas, 4 vistas, 9 disparadores, 18 funciones y 18 políticas RLS
(sección 4).

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

---

# 11. Avance 3 — seguridad, implementación y evaluación

Entregado el **19 de octubre de 2026**. Como el Avance 2, lleva solo lo que
pide la rúbrica. La instrucción del profesor son tres palabras —**Seguridad,
Implementación, Evaluación**— y el equipo pidió además una sección de
interfaces desglosada pantalla por pantalla.

**Hay dos versiones en la historia del repositorio, y vale la de David.** El
mismo día, David Montes subió el documento a `main` directamente (`a21f50a`)
con una portada nueva: los nombres del equipo, la materia y la escuela. Fuera
de la portada el texto es idéntico al de este PR y lleva las mismas 12
capturas, así que al integrar el #87 se conservó su versión.

Hay una guía en `Downloads/Guía para el Avance 3.md` que propone siete
secciones. **No se siguió**, por decisión de la Scrum Master: es una
sugerencia de una IA, no la rúbrica, y agregaba introducción, conclusiones y
anexos que el profesor no pidió y que repetirían el Avance 1.

## Las capturas

`Documentacion/avance3/capturas/` — doce PNG tomados el 19 de octubre con el
sistema corriendo **contra la base real**, no maquetas. Se regeneran con:

```bash
.venv/Scripts/python.exe herramientas/capturar_pantallas.py Documentacion/avance3/capturas
```

**Esas doce son las del documento entregado, con la interfaz de pestañas.**
Desde el #88 el guion aplica el diseño «Lápiz» con `aplicar_apariencia()`,
como `main.py`: correrlo sobre esa carpeta reemplazaría la evidencia del
Avance 3 por pantallas que el documento no describe. Para capturas nuevas,
dale otra carpeta.

**Dos trampas del guion, que costaron dos intentos cada una:**

1. **No usar `QT_QPA_PLATFORM=offscreen`.** Esa plataforma no trae
   tipografías y todo el texto sale como cajas vacías. Con la plataforma
   nativa las ventanas parpadean un instante, que es el precio de que se lea.
2. **Deseleccionar los campos después de `show()`, no antes.** El foco se
   reparte al mostrar la ventana, y es el foco el que selecciona el texto:
   si no, el primer campo de cada formulario sale resaltado en magenta.

## Lo que el Avance 3 verificó contra la base real

El Avance 2 declaró, para cada requisito de seguridad, **cómo** se
comprobaría. El Avance 3 ejecutó esas comprobaciones:

| Prueba | Resultado |
|---|---|
| Consulta sin sesión, con la llave publishable | Las 7 tablas devuelven **0 filas** |
| La misma consulta con los tres perfiles | Alumno: 1 perfil, 2 préstamos, 0 empleados. Personal: todo |
| Seis intentos de escalada de privilegios | **Seis rechazos**, padrón intacto |
| Inspección del repositorio | Ninguna credencial en el código |

Los seis intentos de escalada fueron: el alumno cambiando su propio rol,
leyendo la plantilla y leyendo préstamos ajenos; el bibliotecario dando de
alta un perfil administrador, llamando `registrar_empleado` con rol
administrador, y cambiando su propio rol.

## Un defecto que destapó esa verificación

**`core/errores.py` no traduce un mensaje de la migración 10.** La base
responde `"Solo un administrador puede registrar a otro administrador."`, y
el traductor solo reconoce la variante `"solo un administrador puede
cambiar"`. El bibliotecario lee «La operación no se pudo completar» y no sabe
qué hizo mal.

No es un fallo de seguridad —el rechazo ocurre igual— pero incumple
`RNF-USA-03`. Se corrige agregando una entrada a `REGLAS_DE_LA_BASE`.
**Corregido en el #92**, junto con otros tres mensajes de la misma migración
que tampoco estaban (sección 14).

Es exactamente el mismo patrón que la auditoría de septiembre ya había
encontrado: se agrega un mensaje en una migración y nadie lo da de alta en el
traductor. `tests/test_mensajes_de_la_base.py` existía para atraparlo, pero
solo cubría los mensajes que alguien recordó copiar. Desde el #92 también lee
los `raise exception` de las migraciones mismas.

## Cambios de estado de los requisitos

| Requisito | Antes | Ahora | Por qué |
|---|---|---|---|
| `RNF-MAN-01` | Parcial | **Cumplido** | Le faltaban las pruebas automatizadas; la suite las aporta |
| `RNF-USA-03` | Cumplido | **Parcial** | El mensaje sin traducir de arriba |

Los funcionales no cambiaron: **14 cumplidos, 4 parciales, 3 pendientes**, de
19. Lo que cambió es que ahora cada uno dice con qué se verificó.

## Lo que el Avance 3 dice que NO se ha evaluado

La sesión de aceptación con el docente (`QA-04`, #41) **sigue abierta**, y el
documento lo declara sin rodeos en vez de inventarla. Deja el guion de lo que
hay que medir: cronometrar el préstamo contra `RNF-USA-01`, confirmar el
límite de un libro y el plazo de siete días, ver si los mensajes de error se
entienden, y verificar el vocabulario —el sistema dice «tipo o género» donde
la escuela dice «colección»—.

---

# 12. Propuestas de diseño visual — 27 de octubre

`Documentacion/disenos/Propuestas_de_diseno.html` reúne cuatro direcciones
visuales para la aplicación de escritorio, con los mismos datos de ejemplo.
A y B se muestran en Préstamos e Inicio de sesión, como imágenes fijas; C y
D, en las cinco pestañas más el inicio de sesión, y se navegan como prototipo:
con un selector o desde el menú de la propia maqueta («Cerrar sesión» lleva
al inicio y «Entrar» regresa a Préstamos). Abre sin internet: las
tipografías van incluidas.

**El 3 de noviembre Yael eligió la D, «Lápiz»**, mostaza sobre grafito, con
los ajustes de su prototipo navegable (abajo). La aplicación empezó a usarla
en el #88. El resto de esta sección se escribió el 27 de octubre, antes de
elegir, y se conserva como registro de las cuatro opciones.

`Propuestas_azul_y_mostaza.html`, en la misma carpeta, deja solo C y D y
agrega una tabla que las compara punto por punto. Sus secciones salen de la
misma fuente que el archivo de las cuatro, así que no se contradicen.

| Propuesta | Color principal | Navegación | Tipografía | Esfuerzo estimado |
|---|---|---|---|---|
| A · Clásica | Rojo oscuro `#7F1D2D` | Barra lateral | Source Serif 4 + Source Sans 3 | 5–6 días |
| B · Pizarrón | Verde oscuro `#1F4D3A` | Pestañas, como hoy | Lexend + Atkinson Hyperlegible | 3–4 días |
| C · Luminosa | Azul claro `#7CC6EE` | Barra lateral flotante | Plus Jakarta Sans | 10–12 días |
| D · Lápiz | Mostaza `#E0A526` y grafito | Columna de iconos | Manrope + IBM Plex Mono | 7–8 días |

Las cifras de C y D son las más firmes porque tienen las cinco pestañas
diseñadas. C convierte en tarjetas Préstamos, Catálogo y Deudores; D usa en
todas una tabla con panel de detalle a la derecha.

Las cuatro se implementan con PySide6 y QSS, sin paquetes de Python nuevos:
tipografías con licencia OFL cargadas con `QFontDatabase.addApplicationFont`,
iconos SVG de Lucide (licencia ISC) y la paleta reescrita en `ui/estilo.py`.
El cambio se queda en `ui/`. QML, Flet o pywebview darían mejor acabado, pero
cuestan de 3 a 6 semanas y obligan a rehacer las pruebas de interfaz: no caben
este semestre.

**Al implementar la que se elija:**

- **Tres piezas de las maquetas son funciones nuevas** y pasan por el Product
  Owner (regla 7): el criterio «por vencer» con su conteo y su filtro —el
  umbral de tres días lo propusieron las maquetas, no la escuela—, el contador
  de deudores junto al menú, y el panel de detalle de D con el teléfono del
  tutor (depende de `USU-08`, #75) y quién registró el préstamo. *Yael las
  aprobó el 8 de noviembre (7.0, punto 3).*
- **Lo demás ya existe**: el buscador de Préstamos es `campoFiltro` y el
  resumen es `etiquetaResumen`. La paginación de las maquetas solo está para
  que quepan en la imagen.
- **Pruebas que cambian según la propuesta**: `TestVentanaPrincipal`, en
  `tests/integracion/`, cuenta las pestañas (A, C y D); una prueba marca
  `casillaSoloVencidos` (B, C y D); las de devolución seleccionan una fila y
  pulsan `botonDevolver`, y A, B y C ponen Devolver en cada fila; C cambia
  por tarjetas `tablaPrestamos`, `tablaLibros` y `tablaDeudores`.
- **Color**: en A, el rojo de la marca y el de «vencido» son de la misma
  familia; el azul claro y el mostaza no aguantan texto blanco.

Las maquetas editables viven en un lienzo de diseño privado en claude.ai, en la
cuenta de Yael. El HTML es una exportación de ese lienzo.

## Prototipos navegables — azul y mostaza

`Documentacion/disenos/Prototipo_azul.html` y `Prototipo_mostaza.html` simulan
la aplicación completa en el navegador, sin internet ni base de datos. Se
inicia sesión, se presta, se devuelve, se registran y modifican libros,
alumnos y empleados, se da de baja, se consulta el historial y el reporte de
deudores. Cada regla de la base responde con el mismo mensaje que la app
(`core/errores.py`) y las validaciones son las de `servicios/`. Los datos son
de ejemplo, viven en memoria y **se reinician al recargar**; las fechas se
calculan a partir del día en que se abre, así que siempre hay dos vencidos.

Los dos comparten el mismo núcleo de reglas y el mismo controlador; solo
cambia cómo se dibuja cada pantalla. Cada HTML lleva su código legible dentro.

**Decisiones de Yael para los prototipos (27 de octubre):**

- Los formularios llevan lo que pidió la escuela (#72 a #76): colección de
  Libros del Rincón con sus grados, asignatura de la lista tradicional
  (Español, Matemáticas, Ciencias Naturales, Historia, Geografía, Formación
  Cívica y Ética, Artes e Inglés), CURP, y teléfono y dirección del tutor,
  sin correo del alumno.
- El maestro de grupo se asigna **por salón** y lo heredan sus alumnos; se
  edita desde «Maestros de grupo», en Alumnos.
- El inicio de sesión tiene botones para entrar como administrador o como
  bibliotecario con un clic. **Es solo para el prototipo**: no pasa a la app.

**Supuestos del prototipo, que Yael confirmó el 8 de noviembre:** la CURP es
opcional, pero si se escribe se valida el formato y no puede repetirse; el
teléfono del tutor es obligatorio porque queda como único contacto; la
colección y la asignatura son opcionales. El 3 de noviembre Yael pidió
aplicarlos en la base tal cual (migración 11, sección 14), y el 8 decidió que
se quedan. El criterio «por vencer» de tres días, que aquí era una propuesta
de las maquetas, quedó aprobado ese mismo día para la aplicación (7.0).

---

# 13. El diseño «Lápiz» en la aplicación — 3 de noviembre

Yael eligió la propuesta D, mostaza sobre grafito, y pidió llevarla a la
aplicación. Las cuatro propuestas y los dos prototipos navegables viven en
`Documentacion/disenos/` (sección 12, #90). La referencia para implementar es
`Prototipo_mostaza.html`; cuando el prototipo y esta aplicación no coincidan,
gana el prototipo.

## Qué cubre la primera entrega

La base que usan todas las pantallas, más la primera pantalla completa:

- **Letras e iconos dentro del paquete** (`ui/recursos/`): Manrope variable,
  con sus pesos de 400 a 800; IBM Plex Mono en tres pesos, y los 31 iconos de
  Lucide del prototipo, cada uno con su licencia. No hace falta internet ni
  ningún paquete de Python nuevo: PySide6 ya trae QtSvg.
- **Paleta y hoja de estilo** en `ui/estilo.py`. El estilo base es Fusion y la
  paleta se fija completa, para que el tema oscuro de Windows no cambie nada.
- **Columna de iconos** en lugar de pestañas. Arriba de cada pantalla va una
  línea con la escuela, la fecha y quién entró, que sustituye a la barra de
  estado. Abajo de la columna, el avatar y **cerrar sesión**, que regresa a
  la ficha de entrada sin cerrar el programa.
- **Inicio de sesión**: la ficha de biblioteca sobre el grafito punteado.
- **Catálogo**, completo: título, resumen, búsqueda y «Registrar libro»
  arriba; la tabla en su tarjeta, y a la derecha la ficha del libro elegido,
  con Modificar y Dar de baja.
- **Formulario de libro** en dos columnas, con un recuadro rojo arriba que
  dice qué revisar.

## Lo que sigue

**Entregado el 9 de noviembre** (rama `diseno/pantallas-restantes`):
Préstamos con sus vistas Todos, Por vencer y Vencidos y su panel; Alumnos con
su panel y el diálogo «Maestros de grupo»; Deudores como hoja de reporte;
Empleados con su aviso de permisos y su panel; los diálogos de préstamo,
devolución, historial, alumno, empleado y libro. El Catálogo cambió «Tipo» y
«Año» por colección y asignatura. Las capturas se compararon contra el
prototipo y una revisión de cuatro agentes encontró 16 defectos; se
corrigieron los que afectan el uso (la selección que saltaba de renglón al
filtrar, las pantallas que no se refrescaban entre sí, el alto del historial).

- **El logo es provisional** (lo entregó Yael el 8 de noviembre):
  `ui/recursos/logo/escuela.jpg`. La columna de iconos usa el árbol recortado
  (`RECORTE_ARBOL` en `apariencia.py`) y la ficha de entrada, el logo entero.
- **«Por vencer»** son tres días o menos, con `dias_restantes` de la base
  (`DIAS_POR_VENCER` en `modelos/prestamo.py`).
- **El número junto a Deudores** son las filas de `v_deudores`; Préstamos
  avisa a Deudores, Alumnos y Catálogo cuando presta o recibe un libro.
- **El panel del préstamo** lee código, teléfono del tutor, autor y quién lo
  registró con `repositorios.prestamos.detalles()`, una sola consulta.
- **Quién registró** lo escribe el cliente (`registrado_por`): la base no lo
  sella. Hacerlo en la base sería una migración nueva; no se propuso aplicar.
- **El formulario de libro ya no pide «tipo o género»**, pero conserva el que
  tenga un libro al modificarlo; el de alumno tampoco borra un correo viejo.
- Los `.ui` se escribieron con un generador y se abren normal en Designer.

**Quedaban fuera hasta que se aprobaran** (regla 7) el criterio «por vencer»
de tres días con su conteo, el contador de deudores junto al menú y, en el
panel del préstamo, el teléfono del tutor (depende de `USU-08`, #75) y quién
registró el préstamo. Yael las aprobó el 8 de noviembre, y van con las
pantallas que faltan (7.0, puntos 2 y 3).

**Los campos que pidió la escuela** (#72 a #76) ya están en la base desde la
migración 11 (sección 14), pero todavía no en la aplicación: el Catálogo
sigue mostrando «Tipo o género» hasta que lleguen su capa de datos y sus
pantallas (7.0). Las entradas rápidas del prototipo, para entrar con un
clic como administrador o como bibliotecario, no pasan a la aplicación; así
se decidió desde el 27 de octubre.

## Decisiones y trampas, para quien siga con otra pantalla

1. **La hoja de estilo de Qt no sabe de mayúsculas ni de espacio entre
   letras.** `rotular()` se los pone a la fuente del control. El texto queda
   como se escribió, así que las pruebas lo siguen leyendo igual.
2. **Los encabezados de tabla son la excepción.** Al dibujar cada sección, Qt
   ignora la fuente del encabezado entero; `rotular_encabezados()` se la pone
   a cada columna. Si la hoja fija la letra en `QHeaderView::section`, las
   mayúsculas se pierden también.
3. **La hoja de estilo no sabe teñir un SVG.** Las flechas y la palomita que
   cita con `url()` las escribe `ruta_para_hoja()`, ya coloreadas, en la
   carpeta temporal del sistema.
4. **Qt deja 4 px entre icono y texto en un botón; el prototipo, 8.**
   `poner_icono()` agrega la diferencia.
5. **Los selectores van por propiedad** (`[rol="titulo"]`,
   `[secundario="true"]`, `[peligro="true"]`) y no por tipo dentro de un
   contenedor: un `QFrame QLabel` le ganaría a cualquier etiqueta con rol
   propio, y ese choque solo se ve al abrir la pantalla.
6. **El rojo quedó para lo urgente.** Un libro agotado va en rojo, con su
   punto; uno dado de baja apaga su fila en gris. La prueba que pedía rojo
   para los dos se cambió a esta regla.
7. **Para fotografiar ventanas sin que parpadeen** sirve
   `WA_DontShowOnScreen` antes de `show()`: Qt las arma como si estuvieran
   en pantalla, con las letras reales, y no aparecen. La plataforma
   `offscreen` no sirve para eso porque dibuja el texto como cajas vacías.

## Pruebas

`tests/interfaz/test_diseno.py` suma 35 pruebas: las letras e iconos del
paquete, la hoja de estilo, el menú de iconos, la línea superior, cerrar
sesión, la ficha del Catálogo, el recuadro de error y la ficha de entrada. La
suite queda en 719: pasan 718, y la de TC-06 falla como se espera. Todas las
sentencias de `biblioteca` se recorren, y fuera del código generado las
únicas ramas parciales son las dos de siempre, en `formulario_empleado.py`.

---

# 14. Los campos que pidió la escuela — migración 11, 3 de noviembre

`database/migraciones/11_datos_que_pidio_la_escuela.sql`. Yael aprobó
aplicarla con las reglas del prototipo mostaza (sección 12), y se aplicó en
Supabase el **3 de noviembre de 2026** (versión `20261103235304`). Su archivo
entró al repositorio el 8 de noviembre, en el #91. Durante esos cinco días la
base corrió una migración que `main` no tenía, el mismo riesgo que «Errores
ya cometidos» cuenta con la 10.

## Qué agrega

| Historia | En la base | Regla |
|---|---|---|
| `LIB-06` (#72) | `libros.coleccion` | Una de las cinco colecciones de Libros del Rincón, o vacía (`libros_coleccion_valida`) |
| `LIB-07` (#73) | `libros.asignatura` | Una de las ocho asignaturas, o vacía (`libros_asignatura_valida`) |
| `USU-07` (#74) | `usuarios.curp` | Opcional; si se escribe, con el formato oficial (`usuarios_curp_formato`) y sin repetirse (`usuarios_curp_key`) |
| `USU-09` (#76) | Tabla `maestros_de_grupo` | Un maestro por salón —grado y grupo—, que heredan sus alumnos |
| `USU-08` (#75) | Nada nuevo | El teléfono y la dirección del tutor ya caben en `perfiles`. Que el teléfono sea obligatorio y el correo desaparezca lo aplican el validador y el formulario |

Las colecciones son *Al sol solito*, *Pasos de luna*, *Astrolabio*, *Espejo de
Urania* y *Cometas convidados*; las asignaturas, Español, Matemáticas,
Ciencias Naturales, Historia, Geografía, Formación Cívica y Ética, Artes e
Inglés. Las listas de `modelos/libro.py` tienen que ser las mismas.

Además:

- `v_catalogo` agrega `coleccion` y `asignatura` al final, para no mover las
  columnas que ya tenía.
- `registrar_alumno` y `actualizar_alumno` se recrearon con `p_curp` al final
  y con valor por omisión, así que la aplicación de `main`, que no lo manda,
  sigue funcionando. Conservan los permisos de las migraciones 06 y 07.
- `maestros_de_grupo` tiene RLS con dos políticas, `maestros_lectura` y
  `maestros_escritura`: el personal lee y escribe, y un alumno no ve nada. Su
  disparador `maestros_actualizacion` sella `actualizado_en`. Al empezar cada
  ciclo escolar se corrige ahí, sin tocar la ficha de ningún alumno.

## Cómo se verificó

Primero, un ensayo dentro de una transacción que se deshace sola, con 18
comprobaciones. Después de aplicarla, las mismas sobre la base ya migrada,
también deshechas:

- colección y asignatura válidas pasan; las inventadas se rechazan;
- una CURP válida pasa, una repetida o mal escrita se rechaza y una vacía
  pasa; la llamada sin `p_curp` funciona, y `actualizar_alumno` la guarda;
- el personal da de alta y cambia maestros; un alumno ve 0 filas y no puede
  escribir; sin sesión se ven 0 filas; el grado 7 se rechaza;
- los permisos de las dos funciones quedaron como estaban.

El 8 de noviembre se volvió a leer el esquema: 8 tablas con RLS, 4 vistas, 18
políticas, 9 disparadores y 18 funciones.

## La capa de datos — #92

Lo que la aplicación necesita para leer, escribir y explicar los campos
nuevos, sin tocar pantallas:

- **Modelos.** `Libro` lleva `coleccion` y `asignatura`; `COLECCIONES` dice
  los grados de cada colección y `ASIGNATURAS` es la lista de la escuela.
  `Alumno` lleva `curp`, que va a `usuarios` con el grado y el grupo.
- **Repositorios.**
  - La búsqueda del catálogo también encuentra por colección y asignatura:
    «astro» trae la colección Astrolabio.
  - La búsqueda de alumnos también encuentra por CURP. La CURP vive en
    `usuarios` y PostgREST no la mezcla en el mismo `.or_()` con las columnas
    de `perfiles`, así que va en una segunda consulta; quien ya apareció por
    su nombre no se repite, y un alumno dado de baja no aparece.
  - El alta y la modificación del alumno mandan `p_curp`.
  - `listar_maestros()` y `guardar_maestros()` leen y escriben
    `maestros_de_grupo`: un nombre vacío quita al maestro del salón.
- **Validadores.** El teléfono del tutor es obligatorio y el correo ya no
  cuenta como contacto; la CURP, si se escribe, va con el formato oficial;
  colección y asignatura, si se escriben, tienen que estar en sus listas.
- **Traductor de errores.** Reconoce las siete restricciones de la migración
  11 —«Ya hay un alumno registrado con esa CURP», por ejemplo—, y los cuatro
  mensajes de la migración 10 que no tenía.

**Tres pruebas comparan el código con la migración**, para que no se
desfasen en silencio: las listas de colecciones y asignaturas contra las
restricciones, la expresión de la CURP contra `usuarios_curp_formato`, y cada
`raise exception` de `database/migraciones/` contra el traductor. Esta última
es la que encontró los tres mensajes de la 10 que faltaban.

La suite pasó de 719 a 819: pasan 818 y TC-06 falla como se espera. Todas las
sentencias se recorren; las únicas ramas parciales fuera del código generado
siguen siendo las dos de `formulario_empleado.py`.

## Lo que falta

- **Las pantallas** todavía no muestran nada de esto (7.0, punto 2).
- **Los diagramas `DIA-05`, `DIA-06` y `DIA-07`** dibujan la base de antes,
  sin colección, asignatura, CURP ni `maestros_de_grupo`. Es lo que 7.1
  advertía: dibujar antes de migrar obliga a redibujar.
- ~~Las reglas siguen siendo supuestos del prototipo~~ — Yael las confirmó el
  8 de noviembre: CURP opcional, teléfono del tutor obligatorio, colección y
  asignatura opcionales (sección 12 y 7.0).
