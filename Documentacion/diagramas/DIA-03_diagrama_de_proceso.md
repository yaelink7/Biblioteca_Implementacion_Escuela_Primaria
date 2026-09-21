# DIA-03 · Diagrama de proceso

> Issue [#61](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/61) · 5 puntos · Rey David Montes Ciriaco

El proceso de préstamo y devolución **tal como lo ejecuta el sistema**, no como se
planeó. Lo que aparece en el carril de PostgreSQL lo hace la base por su cuenta: el
cliente no lo pide ni puede saltárselo.

## Préstamo

```mermaid
flowchart TD
    subgraph BIB["👤 Bibliotecario"]
        A1["Abre Nuevo préstamo"]
        A2["Escribe nombre,<br/>código o salón"]
        A3["Selecciona alumno"]
        A4["Escribe título o autor"]
        A5["Selecciona libro"]
        A6["Pulsa Registrar préstamo"]
    end

    subgraph APP["💻 Aplicación de escritorio"]
        B1["Busca por coincidencia parcial<br/>en perfiles + usuarios"]
        B2["Busca por coincidencia parcial<br/>en libros"]
        B3["Envía INSERT:<br/>libro_id, usuario_id,<br/>registrado_por"]
        B9["Recarga desde v_prestamos"]
        BE["Traduce el error<br/>y lo explica"]
    end

    subgraph PG["🗄️ PostgreSQL — aquí viven las reglas"]
        C1["calcular_fecha_limite<br/><i>before insert</i>"]
        C2{"¿fecha_limite<br/>viene nula?"}
        C3["fecha_limite =<br/>fecha_prestamo + 7 días"]
        C4{"¿el alumno ya tiene<br/>un préstamo abierto?"}
        C5["mover_inventario<br/><i>after insert</i>"]
        C6{"¿el libro<br/>está activo?"}
        C7{"¿existencias ≥ 1?"}
        C8["existencias = existencias − 1"]
    end

    A1 --> A2 --> B1 --> A3 --> A4 --> B2 --> A5 --> A6 --> B3
    B3 --> C1 --> C2
    C2 -- sí --> C3 --> C4
    C2 -- "no: la respeta" --> C4
    C4 -- sí --> E1["❌ Ya tiene un préstamo activo"]
    C4 -- no --> C5 --> C6
    C6 -- no --> E2["❌ El libro está dado de baja"]
    C6 -- sí --> C7
    C7 -- no --> E3["❌ No hay ejemplares disponibles"]
    C7 -- sí --> C8 --> B9
    E1 --> BE
    E2 --> BE
    E3 --> BE

    style C1 fill:#EEF2F8,stroke:#2D4B73
    style C5 fill:#EEF2F8,stroke:#2D4B73
    style C3 fill:#EEF2F8,stroke:#2D4B73
    style C8 fill:#EEF2F8,stroke:#2D4B73
    style E1 fill:#FDECEC,stroke:#C0392B
    style E2 fill:#FDECEC,stroke:#C0392B
    style E3 fill:#FDECEC,stroke:#C0392B
```

### Tres detalles que el diagrama tiene que mostrar bien

**El orden real.** `calcular_fecha_limite` es `before insert`, así que corre
**antes** de que la fila se materialice y, por tanto, **antes** de que el índice
único evalúe si el alumno ya tiene un préstamo. La fecha se calcula incluso en los
préstamos que van a ser rechazados.

**El plazo se cuenta desde `fecha_prestamo`, no desde hoy.** Y solo se calcula **si
viene nula**: si el cliente envía una fecha límite, el disparador la respeta. Por
eso el diagrama lleva ese nodo de decisión y no una asignación directa.

**El límite es de un préstamo abierto, no de un libro.** El índice único parcial
cubre los estados `activo` y `vencido`. Un alumno con un ejemplar en casa no puede
llevarse otro título, aunque el primero ya esté vencido.

## Devolución

```mermaid
flowchart TD
    subgraph BIB["👤 Bibliotecario"]
        D1["Abre la pestaña Préstamos"]
        D2["Selecciona el préstamo"]
        D3["Pulsa Registrar devolución"]
    end

    subgraph APP["💻 Aplicación de escritorio"]
        E0["Envía UPDATE:<br/>estado = 'devuelto'<br/><b>y nada más</b>"]
        E9["Recarga desde v_prestamos"]
    end

    subgraph PG["🗄️ PostgreSQL"]
        F1["sellar_devolucion<br/><i>before update of estado</i>"]
        F2["fecha_devolucion =<br/>current_date"]
        F3["mover_inventario<br/><i>after update of estado</i>"]
        F4["existencias = existencias + 1"]
    end

    D1 --> D2 --> D3 --> E0 --> F1 --> F2 --> F3 --> F4 --> E9

    style F1 fill:#EEF2F8,stroke:#2D4B73
    style F2 fill:#EEF2F8,stroke:#2D4B73
    style F3 fill:#EEF2F8,stroke:#2D4B73
    style F4 fill:#EEF2F8,stroke:#2D4B73
```

`sellar_devolucion` hace además lo contrario cuando hace falta: si alguien reabre un
préstamo devuelto, **borra** la fecha. No puede existir una devolución sin fecha ni
una fecha sin devolución.

## Vencimiento

```mermaid
flowchart LR
    G1["Préstamo registrado<br/>estado = 'activo'"]
    G2{"¿fecha_limite<br/>&lt; hoy?"}
    G3["v_prestamos calcula<br/>dias_restantes en cada consulta"]
    G4["Aparece como vencido<br/>en Préstamos y en Deudores"]
    G5["marcar_prestamos_vencidos()<br/><i>existe, nadie la llama</i>"]
    G6["estado = 'vencido'<br/>en la tabla"]

    G1 --> G2
    G2 -- sí --> G3 --> G4
    G2 -.-> G5 -.-> G6

    style G5 fill:#FDF3E7,stroke:#A8621B,stroke-dasharray: 5 4
    style G6 fill:#FDF3E7,stroke:#A8621B,stroke-dasharray: 5 4
```

**El camino punteado no ocurre todavía.** La función existe pero nadie la programa
(`PRE-05`, issue #33; `pg_cron` no está instalado). En la práctica no se nota
porque las vistas calculan el retraso en cada consulta, así que el reporte de
deudores sale correcto igual. La consecuencia real es que **la columna `estado` no
sirve para saber si un préstamo está vencido**: hay préstamos realmente vencidos
almacenados como `'activo'`.

## Por qué las reglas están en la base y no en la aplicación

Es la decisión que ordena el proyecto. La llave de Supabase que viaja dentro de la
aplicación es pública por diseño: cualquiera puede extraerla y llamar la API
directamente. Una regla que viviera solo en el cliente no sería una regla, sería una
sugerencia.

Además, la aplicación móvil para alumnos de la fase 2 heredará estas reglas sin
tener que reimplementarlas. Por eso el diagrama debe mostrar los rechazos **dentro
del carril de PostgreSQL** y no dentro del de la aplicación.
