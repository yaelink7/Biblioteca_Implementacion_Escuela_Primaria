# DIA-07 · Documentación de la base de datos

> Issue [#65](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/65) · 5 puntos · Pedro Cabrera Barrios Ángel

Qué hay en la base, para qué sirve cada cosa y qué regla implementa. Proyecto
Supabase `gibenzgxkbmalljqroxe`, región `us-east-2`, PostgreSQL 17.6.

**Inventario:** 7 tablas · 4 vistas · 15 funciones · 8 disparadores · 16 políticas
de seguridad · 2 tipos enumerados.

---

## 1 · Las siete tablas

| Tabla | Para qué existe |
|---|---|
| `perfiles` | Los datos comunes de toda persona del sistema, sea alumno o empleado |
| `usuarios` | Lo que solo tiene un alumno: su grado y su grupo |
| `empleados` | Lo que solo tiene un empleado: su puesto y su fecha de ingreso |
| `libros` | El acervo, con baja lógica para no perder el historial |
| `prestamos` | Cada préstamo y su ciclo completo hasta la devolución |
| `bitacora_libros` | Trazabilidad de los cambios del catálogo. **Existe y nadie escribe en ella** |
| `notificaciones` | Avisos a las familias. **Vacía**, y su requisito se retiró |

### Columnas cuyo propósito no es evidente

| Tabla · columna | Por qué está así |
|---|---|
| `perfiles.auth_id` | Enlaza con la cuenta de Supabase Auth. **Admite nulo a propósito**: un alumno de primaria tiene ficha sin tener cuenta ni correo |
| `perfiles.codigo` | El identificador escolar con el que la bibliotecaria busca a la persona. Único |
| `perfiles.codigo_postal` | **Texto y no número.** Un CP como `04600` perdería el cero a la izquierda |
| `perfiles.telefono` | **Texto y no número.** No es un valor aritmético; puede traer espacios o guiones |
| `perfiles.activo` | Baja lógica de personas |
| `libros.existencias` | Ejemplares disponibles **ahora**, no los que se compraron. Un disparador lo mueve |
| `libros.activo` + `motivo_baja` + `dado_baja_en` | Baja lógica. El sistema Java borraba físicamente y destruía el historial |
| `prestamos.registrado_por` | Qué empleado capturó la operación. Distinto de `usuario_id`, que es quien se lleva el libro |
| `prestamos.fecha_limite` | **La escribe el disparador, no el cliente** |
| `prestamos.fecha_devolucion` | Ídem. Nula mientras el libro no regrese |
| `bitacora_libros.datos_antes` / `datos_despues` | `jsonb` con la fila completa antes y después del cambio |

### Lo que no hay, y por qué

**No existe una columna `disponible` en `libros`.** El sistema Java la almacenaba, y
podía contradecir al inventario: era el defecto D-09 de la auditoría de calidad. Hoy
se deduce de las existencias en la vista `v_catalogo`.

---

## 2 · Las cuatro vistas

Las cuatro se crean con `security_invoker = on`, de modo que **respetan las
políticas de acceso de quien consulta**, no las de quien las creó. Sin eso, una
vista sería una puerta trasera a los datos.

| Vista | Qué responde | Quién la consulta hoy |
|---|---|---|
| `v_catalogo` | El acervo **activo**, con la disponibilidad deducida de las existencias | **Nadie.** El catálogo lee la tabla directamente, porque necesita poder mostrar las bajas |
| `v_prestamos` | Los préstamos con `dias_restantes` calculado **por la base** en cada consulta | Pantalla de Préstamos |
| `v_deudores` | Quién no ha devuelto, desde cuándo, y el contacto para avisar | Pantalla de Deudores |
| `v_libros_faltantes` | Los libros dados de baja, con su motivo y su fecha | **Nadie todavía** (`REP-02`, issue #37) |

**Por qué `dias_restantes` se calcula en la vista y no en Python:** la base corre en
UTC y los equipos de la escuela en hora de Veracruz. Cuando el cálculo estaba
repartido, la pantalla de Préstamos decía «vencido hace 11 días» y el reporte de
Deudores decía 12, para el mismo préstamo. Un solo reloj lo resolvió.

**Por qué `v_deudores` no filtra por `estado`:** filtra por `fecha_limite < hoy`.
Así el reporte funciona aunque nadie marque los préstamos como vencidos, que es
justo lo que ocurre hoy.

---

## 3 · Las quince funciones

### Apoyo a las políticas de seguridad (4)

| Función | Qué devuelve |
|---|---|
| `mi_perfil()` | El `id` del perfil de quien consulta |
| `mi_rol()` | Su rol |
| `es_personal()` | Cierto si es bibliotecario o administrador |
| `es_administrador()` | Cierto solo si es administrador |

Las cuatro son `security definer` con `set search_path = ''`, porque tienen que leer
`perfiles` sin quedar atrapadas en la propia política que ayudan a evaluar.

### Altas y cambios atómicos (3)

| Función | Qué hace |
|---|---|
| `registrar_alumno(...)` | Inserta en `perfiles` **y** en `usuarios`, o en ninguna |
| `registrar_empleado(...)` | Inserta en `perfiles` **y** en `empleados`, o en ninguna |
| `actualizar_alumno(...)` | Actualiza las dos tablas en una sola transacción |

**Por qué existen.** Los datos de una persona viven en dos tablas. Cuando Python las
escribía con dos llamadas separadas, una podía fallar y dejar un perfil huérfano: un
nombre en el padrón sin ficha de alumno. Pasó dos veces en el proyecto —en el alta y
en la modificación— y estas funciones lo cerraron.

### Funciones de disparador (7)

| Función | Qué impone |
|---|---|
| `calcular_fecha_limite()` | El plazo de siete días, si el cliente no envió uno |
| `mover_inventario()` | Descuenta al prestar, reintegra al devolver, y rechaza si no hay ejemplares o el libro está de baja |
| `validar_baja_de_libro()` | Impide dar de baja un libro con préstamos sin devolver |
| `validar_ano_publicacion()` | Rechaza años futuros y anteriores a 1400 |
| `sellar_devolucion()` | Pone la fecha de devolución con el reloj de la base, y la borra si el préstamo se reabre |
| `proteger_rol()` | Impide cambiar perfiles de acceso sin ser administrador, y cambiar el propio |
| `marcar_actualizacion()` | Sella `actualizado_en`. **Sirve a dos disparadores**: `perfiles` y `libros` |

Son siete funciones para ocho disparadores, porque `marcar_actualizacion` se usa dos
veces. Ese detalle es el que suele hacer que el conteo no cuadre.

### Tarea programada (1)

| Función | Situación |
|---|---|
| `marcar_prestamos_vencidos()` | Existe, **nadie la llama**. `pg_cron` no está instalado (`PRE-05`, issue #33) |

---

## 4 · Los ocho disparadores

| Disparador | Tabla | Momento | Qué hace |
|---|---|---|---|
| `perfiles_actualizacion` | `perfiles` | `before update` | Sella `actualizado_en` |
| `perfiles_protege_rol` | `perfiles` | `before update of rol` | Protege el perfil de acceso |
| `libros_valida_ano` | `libros` | `before insert or update of ano_publicacion` | Valida el año |
| `libros_actualizacion` | `libros` | `before update` | Sella `actualizado_en` |
| `libros_valida_baja` | `libros` | `before update of activo` | Impide la baja con préstamos vivos |
| `prestamos_fecha_limite` | `prestamos` | `before insert` | Calcula el plazo |
| `prestamos_inventario` | `prestamos` | `after insert or update of estado` | Mueve el inventario |
| `prestamos_sella_devolucion` | `prestamos` | `before update of estado` | Sella la fecha de devolución |

**Las cláusulas `of <columna>` importan.** Un disparador con `of estado` **no corre
en cualquier actualización**, solo cuando esa columna cambia. Es la diferencia entre
un diagrama correcto y uno que promete comprobaciones que no ocurren.

---

## 5 · Las dieciséis políticas de acceso

RLS está activa en las siete tablas. Todas las políticas son `to authenticated`: sin
sesión iniciada, **ninguna consulta devuelve una sola fila**.

| Tabla | Política | Operación | Quién pasa |
|---|---|---|---|
| `perfiles` | `perfiles_lectura` | `select` | El personal, o el titular de su propia ficha |
| `perfiles` | `perfiles_alta` | `insert` | El personal |
| `perfiles` | `perfiles_edicion` | `update` | El personal, o el titular de su propia ficha |
| `perfiles` | `perfiles_baja` | `delete` | **Solo el administrador** |
| `usuarios` | `usuarios_lectura` | `select` | El personal, o el alumno sobre su propia fila |
| `usuarios` | `usuarios_escritura` | `all` | El personal |
| `empleados` | `empleados_lectura` | `select` | El personal |
| `empleados` | `empleados_escritura` | `all` | El personal |
| `libros` | `libros_lectura` | `select` | **Cualquiera con sesión** |
| `libros` | `libros_escritura` | `all` | El personal |
| `prestamos` | `prestamos_lectura` | `select` | El personal, o el alumno sobre los suyos |
| `prestamos` | `prestamos_escritura` | `all` | El personal |
| `bitacora_libros` | `bitacora_lectura` | `select` | El personal |
| `bitacora_libros` | `bitacora_alta` | `insert` | El personal |
| `notificaciones` | `notificaciones_lectura` | `select` | El personal, o el destinatario |
| `notificaciones` | `notificaciones_escritura` | `all` | El personal |

### Tres observaciones sobre este cuadro

**El catálogo es de lectura abierta.** `libros_lectura` usa `using (true)`: cualquier
persona con sesión lee **toda** la tabla, incluidos los libros dados de baja con su
motivo. Es coherente con que el acervo sea público para la comunidad escolar, y es
la razón por la que la vista `v_catalogo` filtra lo que la tabla no filtra.

**`empleados_escritura` cambió en la migración 09.** Antes exigía
`es_administrador()`; hoy exige `es_personal()`, porque la escuela confirmó que el
bibliotecario necesita poder registrar personal sin depender de un administrador.

**El alumno puede escribir su propia ficha.** `perfiles_edicion` incluye
`auth_id = auth.uid()` en la rama de `update`, no solo en la de lectura. Está
reportado como algo a acotar cuando exista el registro de cuentas (`USU-03`).

---

## 6 · Los dos tipos enumerados

```sql
create type public.rol_usuario     as enum ('administrador', 'bibliotecario', 'alumno');
create type public.estado_prestamo as enum ('activo', 'devuelto', 'vencido');
```

El orden de declaración define cómo se comparan y cómo ordena un `ORDER BY`.

**`'vencido'` casi nunca se escribe**, porque la función que lo asignaría no se
ejecuta. Los préstamos vencidos siguen almacenados como `'activo'` y las vistas los
detectan por fecha. Conviene saberlo antes de escribir una consulta que filtre por
`estado`: daría cero donde el reporte de deudores da filas.

---

## 7 · Las nueve migraciones

| Archivo | Qué introdujo |
|---|---|
| `01_tipos_y_personas` | Los dos enumerados, `perfiles`, `usuarios`, `empleados` |
| `02_catalogo_y_bitacora` | `libros`, `bitacora_libros`, validación del año |
| `03_prestamos_y_reglas` | `prestamos`, el límite por alumno, el plazo, el inventario |
| `04_reportes_y_seguridad` | Las cuatro vistas y las dieciséis políticas |
| `05_restringir_funciones` | Revoca la ejecución pública de funciones internas |
| `06_altas_de_personas_transaccionales` | `registrar_alumno`, `registrar_empleado` |
| `07_actualizar_alumno_y_vista_prestamos` | `actualizar_alumno`, `v_prestamos` |
| `08_fecha_de_devolucion_desde_la_base` | `sellar_devolucion` |
| `09_permisos_de_bibliotecario_y_proteccion_de_rol` | `proteger_rol` y el permiso del bibliotecario |

**Para cambiar el esquema se crea una migración nueva, nunca se edita una anterior.**
Los archivos son el registro de lo que ya corrió en Supabase: editarlos haría que el
repositorio dejara de describir la base real.

---

> **Aviso de vigencia.** La migración 10 traerá los cambios de la reunión: colección
> restringida, asignatura, CURP, maestro de grupo, datos del tutor, costo de
> reposición y cuatro vistas de estadísticas. Este documento habrá que ampliarlo.
