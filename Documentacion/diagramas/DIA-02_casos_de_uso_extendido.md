# DIA-02 · Casos de uso extendido

> Issue [#60](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/60) · 8 puntos · Rey David Montes Ciriaco

La narrativa de los cuatro casos de uso principales. **Los caminos de excepción no
son hipotéticos**: cada rechazo que aparece aquí existe hoy en la base de datos, y
la columna «quién lo aplica» dice qué disparador o restricción lo levanta.

---

## CU-01 · Registrar préstamo

| | |
|---|---|
| **Actor principal** | Bibliotecario |
| **Requisitos** | `REQ-PRE-01`, `REQ-PRE-02` |
| **Precondiciones** | Sesión iniciada con perfil de personal. El alumno existe en el padrón. El libro existe y está activo |
| **Postcondiciones** | Una fila nueva en `prestamos` con su fecha límite calculada, y una unidad menos en `libros.existencias` |
| **Meta de operación** | Menos de 30 segundos (`RNF-USA-01`) |

### Flujo normal

1. El bibliotecario abre el diálogo *Nuevo préstamo*.
2. Escribe parte del nombre, el código o el salón del alumno. El sistema busca por
   coincidencia parcial y muestra los resultados sin que haya que elegir el criterio.
3. Selecciona al alumno.
4. Escribe parte del título o del autor del libro. El sistema busca y muestra.
5. Selecciona el libro. El resumen muestra quién se lleva qué y para cuándo.
6. Pulsa *Registrar préstamo*.
7. El sistema guarda el préstamo, calcula el plazo, descuenta el ejemplar y cierra
   el diálogo. La lista de préstamos se actualiza.

### Flujos alternativos

**A1 · El alumno buscado no está en el padrón.** El bibliotecario cancela, va a la
pestaña *Alumnos*, lo da de alta y vuelve. No hay alta de alumno desde el diálogo
de préstamo, a propósito: mantiene el flujo en dos búsquedas y un botón.

**A2 · Búsqueda sin resultados.** La lista queda vacía y el botón de confirmar
permanece deshabilitado.

### Caminos de excepción

| Excepción | Qué ve el bibliotecario | Quién lo aplica |
|---|---|---|
| El alumno ya tiene un préstamo activo | «Este alumno ya tiene un préstamo activo. Solo se permite un libro por alumno» | Índice único parcial `prestamo_unico_activo_por_usuario` |
| No quedan ejemplares | «No hay ejemplares disponibles de "*título*"» | Disparador `mover_inventario` |
| El libro está dado de baja | «El libro "*título*" está dado de baja del acervo» | Disparador `mover_inventario` |
| El libro o el alumno ya no existe | El registro al que se hace referencia no existe | Llave foránea |
| Sin permiso para registrar préstamos | El perfil no tiene permiso | Políticas RLS |
| Sin conexión | No hay conexión con el servidor | Cliente |

**Detalle que importa para el diagrama de secuencia:** el rechazo por «ya tiene un
préstamo» ocurre **después** de que el disparador calcula la fecha límite, porque
`calcular_fecha_limite` es `before insert` y el índice único se evalúa al
materializar la fila. La fecha se calcula y se descarta.

---

## CU-02 · Registrar devolución

| | |
|---|---|
| **Actor principal** | Bibliotecario |
| **Requisito** | `REQ-PRE-05` |
| **Precondiciones** | Existe un préstamo en estado `activo` o `vencido` |
| **Postcondiciones** | El préstamo queda en `devuelto` con su fecha de devolución sellada por la base, y el ejemplar vuelve al inventario |

### Flujo normal

1. El bibliotecario abre la pestaña *Préstamos*.
2. Selecciona el préstamo de la lista.
3. Pulsa *Registrar devolución* y confirma.
4. El sistema marca el préstamo como devuelto. **Python envía únicamente el estado**;
   la fecha la pone la base y el ejemplar lo reintegra un disparador.

### Flujos alternativos

**A1 · Devolución de un préstamo vencido.** Idéntica. El sistema no cobra ni
bloquea: el retraso queda registrado en el historial y el alumno queda libre para
llevarse otro libro.

### Caminos de excepción

| Excepción | Qué ve el bibliotecario | Quién lo aplica |
|---|---|---|
| El préstamo ya no existe | «No se encontró ese préstamo» | Repositorio |
| Sin permiso | El perfil no tiene permiso | Políticas RLS |
| Sin conexión | No hay conexión con el servidor | Cliente |

**Por qué la fecha no la pone el cliente:** la base corre en UTC y los equipos en
hora de Veracruz. Si el cliente enviara la fecha, seis horas de cada día el
historial quedaría sellado con un día distinto del real. El disparador
`sellar_devolucion` la pone, y además la **borra** si alguien reabre el préstamo:
no puede haber una devolución sin fecha ni una fecha sin devolución.

---

## CU-03 · Dar de alta un libro

| | |
|---|---|
| **Actor principal** | Bibliotecario |
| **Requisito** | `REQ-LIB-01` |
| **Precondiciones** | Sesión iniciada con perfil de personal |
| **Postcondiciones** | Una fila nueva en `libros`, visible en el catálogo |

### Flujo normal

1. El bibliotecario abre *Catálogo* y pulsa *Nuevo libro*.
2. Captura título, autor, tipo, editorial, existencias, año y páginas.
3. Pulsa *Guardar*.
4. El sistema valida, guarda y refresca el catálogo.

### Flujos alternativos

**A1 · Modificar un libro existente.** El mismo formulario, precargado. El
identificador no se captura ni se puede cambiar: lo genera la base.

### Caminos de excepción

| Excepción | Qué ve el bibliotecario | Quién lo aplica |
|---|---|---|
| Falta el título o el autor | «El título es obligatorio» / «El autor es obligatorio» | Validador de Python y restricción `check` |
| Año de publicación futuro | «El año de publicación no puede ser futuro» | Disparador `validar_ano_publicacion` |
| Año anterior a 1400 | El año no es razonable | Disparador `validar_ano_publicacion` |
| Cero páginas o páginas negativas | El número de páginas debe ser positivo | Restricción `check` |
| Alta sin ejemplares | Un libro nuevo debe traer al menos un ejemplar | Validador de Python |
| Existencias negativas | No pueden quedar en negativo | Restricción `check` |

**Nota:** la regla «un libro nuevo debe traer al menos un ejemplar» vive **solo en
Python**. La base acepta cero, y a propósito: un libro ya registrado puede quedar
en cero cuando todos sus ejemplares están prestados.

---

## CU-04 · Consultar el reporte de deudores

| | |
|---|---|
| **Actor principal** | Bibliotecario |
| **Requisito** | `REQ-REP-01` |
| **Precondiciones** | Sesión iniciada con perfil de personal |
| **Postcondiciones** | Ninguna. Es una consulta: no modifica nada |

### Flujo normal

1. El bibliotecario abre la pestaña *Deudores*.
2. **El reporte ya está generado.** No hay que pulsar nada ni elegir fechas.
3. Cada renglón muestra el alumno, su salón, el libro adeudado, los días de retraso
   y el contacto para avisar.
4. Opcionalmente filtra por salón.

### Flujos alternativos

**A1 · Nadie debe nada.** La tabla aparece vacía con un mensaje.

### Caminos de excepción

| Excepción | Qué ve el bibliotecario | Quién lo aplica |
|---|---|---|
| Sin permiso | No devuelve filas | Políticas RLS |
| Sin conexión | No hay conexión con el servidor | Cliente |

**Por qué el reporte abre ya hecho:** era el segundo de los cuatro problemas que
la escuela reportó — «sacar la lista de deudores exige revisar el cuaderno entero a
mano». La vista `v_deudores` calcula el retraso en cada consulta y no depende de
que alguien haya marcado los préstamos como vencidos.

---

## Dos casos de uso que el sistema aplica y conviene documentar

### CU-05 · Cambiar el perfil de acceso de una persona

Reservado al administrador. El disparador `proteger_rol` lo rechaza en dos
situaciones, **en este orden**:

1. **Si intenta cambiar su propio perfil**, aunque sea administrador. Nadie se
   modifica a sí mismo.
2. **Si quien lo intenta no es administrador.**

### CU-06 · Dar de baja un libro

Es **baja lógica**: el libro conserva su historial de préstamos y queda marcado
como inactivo con su motivo y su fecha. El sistema Java borraba físicamente, lo que
destruía el historial que exige `REQ-PRE-03`.

| Excepción | Quién lo aplica |
|---|---|
| El libro tiene préstamos sin devolver | Disparador `validar_baja_de_libro` |
| No se indicó el motivo de la baja | Restricción `baja_con_motivo` |

---

## Caminos de excepción comunes a todos los casos

| Excepción | Quién lo aplica |
|---|---|
| Sesión no iniciada o vencida | Las 16 políticas RLS: sin sesión no devuelven ninguna fila |
| La fila no pertenece al perfil | Políticas RLS |
| Código de persona repetido | Restricción `unique` sobre `perfiles.codigo` |
| Grado fuera del rango 1 a 6 | Restricción `check` |
| Nombre o apellido vacío | Restricción `check` |
